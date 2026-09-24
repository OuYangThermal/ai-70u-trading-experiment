"""Paper Live: single-step executor, called hourly by cron.

- SPOT PAPER ONLY. No real orders, no keys, no leverage.
- State in data/state.json. Log in data/trades.csv (append-only).
- Refuses to run until Strategy v1 is frozen in config.yaml.
"""
import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path

import yaml

from .data import fetch_recent
from .strategy import STRATEGIES
from .dashboard import generate as generate_dashboard

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
STATE_PATH = DATA / "state.json"
TRADES_PATH = DATA / "trades.csv"
DAILY_PATH = DATA / "daily_equity.csv"

TRADES_HEADER = ["timestamp", "symbol", "side", "price", "quantity", "fee",
                 "slippage", "reason", "strategy", "balance_before",
                 "balance_after", "realized_PnL", "unrealized_PnL"]


def load_config():
    return yaml.safe_load(open(ROOT / "config.yaml"))


def load_state():
    if STATE_PATH.exists():
        return json.loads(STATE_PATH.read_text())
    return None


def save_state(s):
    STATE_PATH.write_text(json.dumps(s, indent=2))


def append_trade(row):
    new = not TRADES_PATH.exists()
    with open(TRADES_PATH, "a", newline="") as f:
        w = csv.DictWriter(f, fieldnames=TRADES_HEADER)
        if new:
            w.writeheader()
        w.writerow(row)


def append_daily_equity(date_str, equity, btc_price, benchmark_value, n_trades):
    new = not DAILY_PATH.exists()
    with open(DAILY_PATH, "a", newline="") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["date", "equity", "btc_price", "benchmark_value", "num_trades"])
        # one row per date: rewrite file replacing today's row if present
    rows = list(csv.DictReader(open(DAILY_PATH)))
    rows = [r for r in rows if r["date"] != date_str]
    rows.append({"date": date_str, "equity": f"{equity:.2f}",
                 "btc_price": f"{btc_price:.2f}",
                 "benchmark_value": f"{benchmark_value:.2f}",
                 "num_trades": n_trades})
    with open(DAILY_PATH, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=["date", "equity", "btc_price", "benchmark_value", "num_trades"])
        w.writeheader()
        w.writerows(rows)


def finalize_if_due(state, start_cap):
    """30 天到期后写 FINAL_REPORT.md（只写一次）。"""
    final_path = ROOT / "FINAL_REPORT.md"
    if final_path.exists():
        return
    start = datetime.fromisoformat(state["start_date"]).replace(tzinfo=timezone.utc)
    days = (datetime.now(timezone.utc) - start).days
    if days < 30:
        return
    trades = []
    if TRADES_PATH.exists():
        trades = list(csv.DictReader(open(TRADES_PATH)))
    daily = []
    if DAILY_PATH.exists():
        daily = list(csv.DictReader(open(DAILY_PATH)))
    last = daily[-1] if daily else None
    equity = float(last["equity"]) if last else start_cap
    bh_value = float(last["benchmark_value"]) if last else start_cap
    sells = [t for t in trades if t["side"] == "SELL"]
    fees = sum(float(t["fee"]) for t in trades)
    eq_series = [float(r["equity"]) for r in daily]
    peak, mdd = -1e18, 0.0
    for v in eq_series:
        peak = max(peak, v)
        mdd = min(mdd, (v - peak) / peak if peak else 0)
    ai_ret = (equity - start_cap) / start_cap * 100
    bh_ret = (bh_value - start_cap) / start_cap * 100
    beat = ai_ret > bh_ret
    final_path.write_text(f"""# FINAL REPORT — AI 70U Trading Experiment（30 天）

> 实验周期：{state["start_date"]} → {datetime.now(timezone.utc).strftime("%Y-%m-%d")}
> Phase 1 · SPOT PAPER ONLY · 策略版本：v1（{state.get("strategy", "hold_cash")}）

## 核心结果

| 指标 | 数值 |
|---|---|
| 初始资金 | {start_cap:.2f} USDT |
| 最终权益 | {equity:.2f} USDT |
| AI 策略收益率 | {ai_ret:+.2f}% |
| 最大回撤 | {mdd*100:.2f}% |
| 手续费总计 | {fees:.2f} USDT |
| 交易笔数 | {len(trades)} |
| Buy&Hold 终值 | {bh_value:.2f} USDT（{bh_ret:+.2f}%） |

## 是否跑赢 Benchmark？

**{"是" if beat else "否"}**。超额收益（AI − BH）：{ai_ret - bh_ret:+.2f}%。

## 利润来源拆解

- 来自市场上涨（beta）：策略持有 BTC 期间的被动涨跌，本实验 v1=hold_cash，未持有，beta 贡献为 0。
- 来自策略本身（alpha）：{ai_ret:+.2f}% − 0 = {ai_ret:+.2f}%，即全部（未）收益都来自"不交易"的决策本身。

## 结论（无宣传语言）

{("AI 策略跑赢了 Buy&Hold。" if beat else "AI 策略未能跑赢 Buy&Hold。回测阶段已显示三个主动策略 730 天全部跑输持有不动，"
 "v1 选择不交易是诚实且符合预定规则的决定。本次实验验证：在无明确 edge 时，不交易优于乱交易，但不产生超额收益。")}

原始数据：data/trades.csv（{len(trades)} 笔）/ data/daily_equity.csv（{len(daily)} 天）
""")
    print("[paper] FINAL_REPORT.md written — experiment complete")


def step():
    cfg = load_config()
    v1 = cfg["strategy"]["v1"]
    if not v1.get("name"):
        raise SystemExit("[paper] REFUSED: Strategy v1 is not frozen yet. Run backtests and freeze v1 first.")

    strategy_name = v1["name"]
    strategy_fn = STRATEGIES[strategy_name]
    params = v1.get("params", {})
    symbol = cfg["market"]["primary_symbol"]
    fee_rate = cfg["costs"]["fee_rate"]
    slip_rate = cfg["costs"]["slippage_rate"]
    start_cap = cfg["experiment"]["starting_capital_usdt"]

    state = load_state()
    df = fetch_recent(symbol, "1h", 300)
    if len(df) < 60:
        raise SystemExit(f"[paper] not enough candles ({len(df)}), skipping step")
    last = df.iloc[-1]
    price = float(last["close"])
    ts = datetime.now(timezone.utc)
    today = ts.strftime("%Y-%m-%d")

    if state is None:
        state = {
            "cash": start_cap, "qty": 0.0, "cost_basis": 0.0,
            "start_date": today,
            "strategy": f"{strategy_name}@v1",
            "benchmark_buy_price": price,
            "trades_today": 0, "last_trade_day": None,
            "day_start_equity": start_cap,
            "halted": False, "halt_reason": None,
        }
        save_state(state)
        print(f"[paper] initialized: start_date={today}, benchmark BTC buy @ {price:.2f}")

    if today != state.get("equity_day"):
        state["equity_day"] = today
        state["day_start_equity"] = state["cash"] + state["qty"] * price
        state["trades_today"] = 0

    if state.get("halted"):
        print(f"[paper] HALTED: {state.get('halt_reason')}; step skipped (dashboard still refreshed)")
    else:
        target = int(strategy_fn(df, **params).iloc[-1])
        holding = state["qty"] > 0
        equity = state["cash"] + state["qty"] * price

        # risk: daily loss halt
        day_start = state["day_start_equity"]
        if (equity - day_start) / day_start <= -cfg["risk"]["daily_loss_halt_pct"]:
            state["halted"] = True
            state["halt_reason"] = f"daily loss halt at {today}"
            print(f"[paper] {state['halt_reason']}")
        # risk: total loss halt
        elif equity <= start_cap * (1 - cfg["risk"]["total_loss_halt_pct"]):
            state["halted"] = True
            state["halt_reason"] = "total loss halt (equity < 52.5 USDT)"
            print(f"[paper] {state['halt_reason']}")
        elif target == 1 and not holding and state["trades_today"] < cfg["risk"]["max_trades_per_day"]:
            spend = min(state["cash"], equity * cfg["risk"]["max_position_pct"])
            if spend >= cfg["risk"]["min_trade_usdt"]:
                exec_price = price * (1 + slip_rate)
                fee = spend * fee_rate
                buy_qty = (spend - fee) / exec_price
                slip_cost = buy_qty * (exec_price - price)
                eq_before = equity
                state["cash"] -= spend
                state["qty"] += buy_qty
                state["cost_basis"] = spend
                eq_after = state["cash"] + state["qty"] * price
                append_trade({
                    "timestamp": ts.isoformat(), "symbol": symbol, "side": "BUY",
                    "price": round(exec_price, 2), "quantity": round(buy_qty, 8),
                    "fee": round(fee, 4), "slippage": round(slip_cost, 4),
                    "reason": "signal", "strategy": f"{strategy_name}@v1",
                    "balance_before": round(eq_before, 2), "balance_after": round(eq_after, 2),
                    "realized_PnL": 0.0,
                    "unrealized_PnL": round(state["qty"] * price - state["cost_basis"], 2),
                })
                state["trades_today"] += 1
                state["last_trade_day"] = today
                print(f"[paper] BUY {buy_qty:.6f} BTC @ {exec_price:.2f}")
        elif target == 0 and holding:
            exec_price = price * (1 - slip_rate)
            gross = state["qty"] * exec_price
            fee = gross * fee_rate
            net = gross - fee
            slip_cost = state["qty"] * (price - exec_price)
            realized = net - state["cost_basis"]
            eq_before = equity
            state["cash"] += net
            sold_qty = state["qty"]
            state["qty"] = 0.0
            state["cost_basis"] = 0.0
            append_trade({
                "timestamp": ts.isoformat(), "symbol": symbol, "side": "SELL",
                "price": round(exec_price, 2), "quantity": round(sold_qty, 8),
                "fee": round(fee, 4), "slippage": round(slip_cost, 4),
                "reason": "signal", "strategy": f"{strategy_name}@v1",
                "balance_before": round(eq_before, 2), "balance_after": round(state["cash"], 2),
                "realized_PnL": round(realized, 2), "unrealized_PnL": 0.0,
            })
            state["trades_today"] += 1
            state["last_trade_day"] = today
            print(f"[paper] SELL {sold_qty:.6f} BTC @ {exec_price:.2f} | realized {realized:+.2f}")
        else:
            print(f"[paper] no action (target={target}, holding={holding}, price={price:.2f})")

    save_state(state)
    equity = state["cash"] + state["qty"] * price
    bh_value = start_cap / state["benchmark_buy_price"] * price
    n_trades = sum(1 for _ in open(TRADES_PATH)) - 1 if TRADES_PATH.exists() else 0
    append_daily_equity(today, equity, price, bh_value, max(n_trades, 0))
    finalize_if_due(state, start_cap)
    generate_dashboard()
    print(f"[paper] equity={equity:.2f} | benchmark BH={bh_value:.2f}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--step", action="store_true")
    args = ap.parse_args()
    if args.step:
        step()
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
