"""Dashboard generator: reads data/*.csv + state.json -> dashboard.html (repo root).

Shows: all required KPIs + Buy&Hold benchmark comparison. No hype language.
"""
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def _read_trades():
    p = DATA / "trades.csv"
    if not p.exists():
        return []
    return list(csv.DictReader(open(p)))


def _read_daily():
    p = DATA / "daily_equity.csv"
    if not p.exists():
        return []
    return list(csv.DictReader(open(p)))


def _svg_chart(daily):
    W, H, PAD = 900, 300, 40
    if len(daily) < 1:
        return "<p>暂无权益数据</p>"
    eq = [float(r["equity"]) for r in daily]
    bh = [float(r["benchmark_value"]) for r in daily]
    labels = [r["date"] for r in daily]
    lo = min(min(eq), min(bh))
    hi = max(max(eq), max(bh))
    span = (hi - lo) or 1
    lo -= span * 0.05
    hi += span * 0.05

    def xy(i, v):
        x = PAD + i * (W - 2 * PAD) / max(len(daily) - 1, 1)
        y = H - PAD - (v - lo) / (hi - lo) * (H - 2 * PAD)
        return f"{x:.1f},{y:.1f}"

    eq_pts = " ".join(xy(i, v) for i, v in enumerate(eq))
    bh_pts = " ".join(xy(i, v) for i, v in enumerate(bh))
    mid = labels[len(labels) // 2] if len(labels) > 2 else ""
    return f"""
<svg viewBox="0 0 {W} {H}" style="width:100%;height:auto;background:#0f1420;border-radius:8px">
  <polyline points="{bh_pts}" fill="none" stroke="#8a93a6" stroke-width="2" stroke-dasharray="6,4"/>
  <polyline points="{eq_pts}" fill="none" stroke="#4da3ff" stroke-width="2.5"/>
  <text x="{PAD}" y="{H-12}" fill="#8a93a6" font-size="12">{labels[0]}</text>
  <text x="{W/2-30}" y="{H-12}" fill="#8a93a6" font-size="12">{mid}</text>
  <text x="{W-PAD-60}" y="{H-12}" fill="#8a93a6" font-size="12">{labels[-1]}</text>
  <text x="{PAD}" y="22" fill="#4da3ff" font-size="13">━ AI Strategy</text>
  <text x="{PAD+130}" y="22" fill="#8a93a6" font-size="13">┄ Buy &amp; Hold BTC</text>
  <text x="{W-PAD-120}" y="22" fill="#8a93a6" font-size="12">max {hi:.2f} / min {lo:.2f}</text>
</svg>"""


def generate():
    cfg = yaml.safe_load(open(ROOT / "config.yaml"))
    start_cap = cfg["experiment"]["starting_capital_usdt"]
    trades = _read_trades()
    daily = _read_daily()
    state_p = DATA / "state.json"
    state = json.loads(state_p.read_text()) if state_p.exists() else None

    now = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    if not daily or not state:
        html = f"""<html><head><meta charset="utf-8"><title>AI 70U Trading Experiment</title></head>
<body style="font-family:sans-serif;background:#0b0e14;color:#e6e9f0;padding:40px">
<h1>AI 70U Trading Experiment</h1><p>实验尚未开始。Paper Live 启动后这里会显示实时 Dashboard。</p>
<p>Last update: {now}</p></body></html>"""
        (ROOT / "dashboard.html").write_text(html)
        return

    last = daily[-1]
    equity = float(last["equity"])
    bh_value = float(last["benchmark_value"])
    btc_price = float(last["btc_price"])
    cash = state["cash"]
    qty = state["qty"]
    pos_value = qty * btc_price
    total_ret = (equity - start_cap) / start_cap * 100
    bh_ret = (bh_value - start_cap) / start_cap * 100
    excess = total_ret - bh_ret
    n_days = max(1, len(daily))

    sells = [t for t in trades if t["side"] == "SELL"]
    wins = [t for t in sells if float(t["realized_PnL"]) > 0]
    losses = [t for t in sells if float(t["realized_PnL"]) <= 0]
    gross_win = sum(float(t["realized_PnL"]) for t in wins)
    gross_loss = abs(sum(float(t["realized_PnL"]) for t in losses))
    fees = sum(float(t["fee"]) for t in trades)
    realized = sum(float(t["realized_PnL"]) for t in sells)
    spent = (state.get("cost_basis") or 0)
    unrealized = pos_value - spent if qty > 0 else 0.0

    eq_series = [float(r["equity"]) for r in daily]
    peak, mdd = -1e18, 0.0
    for v in eq_series:
        peak = max(peak, v)
        mdd = min(mdd, (v - peak) / peak if peak else 0)

    def card(label, value, sub=""):
        color = "#e6e9f0"
        return (f'<div style="background:#151b29;border-radius:8px;padding:14px 16px">'
                f'<div style="color:#8a93a6;font-size:12px">{label}</div>'
                f'<div style="font-size:22px;font-weight:700;color:{color}">{value}</div>'
                f'<div style="color:#8a93a6;font-size:11px">{sub}</div></div>')

    verdict = ("AI 策略当前跑赢 Buy&Hold" if excess > 0
               else "AI 策略当前未跑赢 Buy&Hold" if excess < 0 else "持平")
    verdict_color = "#3ddc84" if excess > 0 else "#ff6b6b" if excess < 0 else "#8a93a6"

    rows = ""
    for t in trades[-20:][::-1]:
        pnl = float(t["realized_PnL"])
        pnl_s = f"{pnl:+.2f}" if t["side"] == "SELL" else "—"
        rows += (f"<tr><td>{t['timestamp'][:16]}</td><td>{t['side']}</td>"
                 f"<td>{t['price']}</td><td>{t['quantity']}</td><td>{t['fee']}</td>"
                 f"<td>{t['strategy']}</td><td>{pnl_s}</td>"
                 f"<td>{t['balance_after']}</td></tr>")

    html = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>AI 70U Trading Experiment — Dashboard</title></head>
<body style="font-family:-apple-system,sans-serif;background:#0b0e14;color:#e6e9f0;margin:0;padding:24px;max-width:1100px">
<h1 style="margin:0 0 4px">AI 70U Trading Experiment</h1>
<p style="color:#8a93a6;margin:0 0 20px">Phase 1 · SPOT PAPER ONLY · 70 USDT · BTC/USDT 1h · Strategy v1: {cfg["strategy"]["v1"].get("name") or "—"}
· 开始 {state.get("start_date")} · 更新 {now}</p>

<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(160px,1fr));gap:10px;margin-bottom:20px">
{card("Starting Capital", f"{start_cap:.2f} USDT")}
{card("Current Equity", f"{equity:.2f} USDT", f"{total_ret:+.2f}%")}
{card("Cash", f"{cash:.2f} USDT")}
{card("Position", f"{qty:.6f} BTC", f"≈ {pos_value:.2f} USDT @ {btc_price:,.0f}")}
{card("Total Return", f"{total_ret:+.2f}%")}
{card("Avg Daily Return", f"{total_ret/n_days:+.3f}%")}
{card("Realized P&L", f"{realized:+.2f} USDT")}
{card("Unrealized P&L", f"{unrealized:+.2f} USDT")}
{card("Number of Trades", f"{len(trades)}", f"{len(sells)} round trips")}
{card("Win Rate", f"{(len(wins)/len(sells)*100 if sells else 0):.1f}%")}
{card("Average Win", f"{(gross_win/len(wins) if wins else 0):+.2f}")}
{card("Average Loss", f"{(-gross_loss/len(losses) if losses else 0):+.2f}")}
{card("Profit Factor", f"{(gross_win/gross_loss if gross_loss>0 else float('inf')):.2f}")}
{card("Maximum Drawdown", f"{mdd*100:.2f}%")}
{card("Fees Paid", f"{fees:.2f} USDT")}
</div>

<h2>Benchmark: Buy &amp; Hold</h2>
<div style="display:grid;grid-template-columns:repeat(auto-fill,minmax(200px,1fr));gap:10px;margin-bottom:20px">
{card("BH Value (70U all-in day 1)", f"{bh_value:.2f} USDT", f"{bh_ret:+.2f}%")}
{card("Excess Return (AI − BH)", f"{excess:+.2f}%", verdict)}
</div>
<p style="color:{verdict_color};font-weight:700">{verdict}。{'其中 ' + f'{excess:.2f}% 为策略超额收益' if excess>0 else '策略尚未证明有 alpha。'}</p>

<h2>Equity Curve</h2>
{_svg_chart(daily)}

<h2 style="margin-top:24px">Recent Trades (latest 20)</h2>
<table style="width:100%;border-collapse:collapse;font-size:13px">
<tr style="color:#8a93a6;text-align:left"><th>时间</th><th>方向</th><th>价格</th><th>数量</th><th>手续费</th><th>策略</th><th>已实现PnL</th><th>余额</th></tr>
{rows}
</table>
<p style="color:#8a93a6;font-size:12px;margin-top:20px">手续费 0.1%/边 · 滑点 0.05%/边已计入每一笔。日志只追加不修改。No hype: 数字就是数字。</p>
</body></html>"""
    (ROOT / "dashboard.html").write_text(html)
    print("[dashboard] dashboard.html updated")


if __name__ == "__main__":
    generate()
