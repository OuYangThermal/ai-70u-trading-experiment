"""Metrics: strategy vs buy&hold benchmark, no cherry-picking."""
import numpy as np


def max_drawdown(equity_values):
    peak = -np.inf
    mdd = 0.0
    for v in equity_values:
        peak = max(peak, v)
        dd = (v - peak) / peak if peak else 0.0
        mdd = min(mdd, dd)
    return mdd


def summarize(trades, equity_curve, starting_capital, df):
    """trades: list of dicts (trades.csv columns). equity_curve: [(ts, value)]."""
    eq = [e[1] for e in equity_curve]
    current = eq[-1] if eq else starting_capital
    total_return = (current - starting_capital) / starting_capital

    # buy & hold benchmark: all-in at first close
    first_close = float(df["close"].iloc[0])
    last_close = float(df["close"].iloc[-1])
    bh_value = starting_capital / first_close * last_close
    bh_return = (bh_value - starting_capital) / starting_capital

    sells = [t for t in trades if t["side"] == "SELL"]
    wins = [t for t in sells if t["realized_PnL"] > 0]
    losses = [t for t in sells if t["realized_PnL"] <= 0]
    gross_win = sum(t["realized_PnL"] for t in wins)
    gross_loss = abs(sum(t["realized_PnL"] for t in losses))
    fees = sum(t["fee"] for t in trades)

    # position snapshot from last trade state
    buys_qty = sum(t["quantity"] for t in trades if t["side"] == "BUY")
    sells_qty = sum(t["quantity"] for t in trades if t["side"] == "SELL")
    position_qty = buys_qty - sells_qty
    position_value = position_qty * last_close
    cash = current - position_value
    # unrealized: current position value minus what we spent on the open lot
    unrealized = 0.0
    if position_qty > 0:
        last_buy = [t for t in trades if t["side"] == "BUY"][-1]
        spent = last_buy["balance_before"] - last_buy["balance_after"]
        unrealized = round(position_value - spent, 2)

    n_days = max(1, (equity_curve[-1][0] - equity_curve[0][0]).total_seconds() / 86400) if equity_curve else 1

    return {
        "starting_capital": round(starting_capital, 2),
        "current_equity": round(current, 2),
        "cash": round(cash, 2),
        "position_qty": round(position_qty, 8),
        "position_value": round(position_value, 2),
        "total_return_pct": round(total_return * 100, 2),
        "avg_daily_return_pct": round(total_return / n_days * 100, 3),
        "realized_pnl": round(sum(t["realized_PnL"] for t in sells), 2),
        "unrealized_pnl": round(unrealized, 2),
        "num_trades": len(trades),
        "num_round_trips": len(sells),
        "win_rate_pct": round(len(wins) / len(sells) * 100, 1) if sells else 0.0,
        "avg_win": round(gross_win / len(wins), 2) if wins else 0.0,
        "avg_loss": round(-gross_loss / len(losses), 2) if losses else 0.0,
        "profit_factor": round(gross_win / gross_loss, 2) if gross_loss > 0 else float("inf"),
        "max_drawdown_pct": round(max_drawdown(eq) * 100, 2),
        "fees_paid": round(fees, 2),
        "benchmark_bh_value": round(bh_value, 2),
        "benchmark_bh_return_pct": round(bh_return * 100, 2),
        "excess_return_vs_bh_pct": round((total_return - bh_return) * 100, 2),
    }
