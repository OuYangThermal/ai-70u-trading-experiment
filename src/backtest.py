"""Backtest engine: honest simulation, no lookahead, costs included."""
import argparse
import pandas as pd

from .data import fetch_history_binance
from .strategy import STRATEGIES, DEFAULT_PARAMS


def run_backtest(df, target, symbol, strategy_name, fee_rate, slippage_rate,
                 starting_capital, max_position_pct, min_trade_usdt):
    cash = starting_capital
    qty = 0.0
    cost_basis = 0.0  # total USDT spent (incl. buy fee) on current position
    trades = []
    equity_curve = []
    realized_total = 0.0

    closes = df["close"]
    for i in range(len(df)):
        price = float(closes.iloc[i])
        ts = pd.to_datetime(int(df["ts"].iloc[i]), unit="ms", utc=True)
        tgt = int(target.iloc[i])
        holding = qty > 0
        eq_before = cash + qty * price

        if tgt == 1 and not holding:
            spend = min(cash, eq_before * max_position_pct)
            if spend >= min_trade_usdt:
                exec_price = price * (1 + slippage_rate)
                fee = spend * fee_rate
                buy_qty = (spend - fee) / exec_price
                slippage_cost = buy_qty * (exec_price - price)
                cash -= spend
                qty += buy_qty
                cost_basis = spend
                eq_after = cash + qty * price
                trades.append({
                    "timestamp": ts.isoformat(), "symbol": symbol, "side": "BUY",
                    "price": round(exec_price, 2), "quantity": round(buy_qty, 8),
                    "fee": round(fee, 4), "slippage": round(slippage_cost, 4),
                    "reason": "signal", "strategy": strategy_name,
                    "balance_before": round(eq_before, 2), "balance_after": round(eq_after, 2),
                    "realized_PnL": 0.0,
                    "unrealized_PnL": round(qty * price - cost_basis, 2),
                })
        elif tgt == 0 and holding:
            exec_price = price * (1 - slippage_rate)
            gross = qty * exec_price
            fee = gross * fee_rate
            net = gross - fee
            slippage_cost = qty * (price - exec_price)
            realized = net - cost_basis
            realized_total += realized
            cash += net
            eq_after = cash  # qty -> 0
            trades.append({
                "timestamp": ts.isoformat(), "symbol": symbol, "side": "SELL",
                "price": round(exec_price, 2), "quantity": round(qty, 8),
                "fee": round(fee, 4), "slippage": round(slippage_cost, 4),
                "reason": "signal", "strategy": strategy_name,
                "balance_before": round(eq_before, 2), "balance_after": round(eq_after, 2),
                "realized_PnL": round(realized, 2),
                "unrealized_PnL": 0.0,
            })
            qty, cost_basis = 0.0, 0.0

        equity_curve.append((ts, cash + qty * price))

    return trades, equity_curve, realized_total


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--strategy", default="ma_trend", choices=list(STRATEGIES))
    ap.add_argument("--days", type=int, default=730)
    ap.add_argument("--symbol", default="BTCUSDT")
    args = ap.parse_args()

    from .metrics import summarize
    import yaml

    cfg = yaml.safe_load(open("config.yaml"))
    df = fetch_history_binance(args.symbol, "1h", args.days)
    print(f"[backtest] {args.symbol}: {len(df)} closed 1h candles, "
          f"{df['ts'].iloc[0]} -> {df['ts'].iloc[-1]}")

    target = STRATEGIES[args.strategy](df, **DEFAULT_PARAMS[args.strategy])
    trades, equity, _ = run_backtest(
        df, target, args.symbol, args.strategy,
        cfg["costs"]["fee_rate"], cfg["costs"]["slippage_rate"],
        cfg["experiment"]["starting_capital_usdt"],
        cfg["risk"]["max_position_pct"], cfg["risk"]["min_trade_usdt"],
    )
    m = summarize(trades, equity, cfg["experiment"]["starting_capital_usdt"], df)
    print(f"[backtest] strategy={args.strategy}")
    for k, v in m.items():
        print(f"  {k}: {v}")


if __name__ == "__main__":
    main()
