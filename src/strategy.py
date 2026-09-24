"""Strategies: simple, explainable, no LLM guessing.

Each strategy is a function(df, **params) -> pandas Series of target position
(1 = hold BTC, 0 = hold cash), computed ONLY from closed candles.
Execution happens at that candle's close -> no lookahead.
"""
import pandas as pd
import numpy as np


# ---------- indicators ----------
def sma(s, n):
    return s.rolling(n).mean()


def rsi(close, n=14):
    d = close.diff()
    gain = d.clip(lower=0)
    loss = -d.clip(upper=0)
    ag = gain.ewm(alpha=1 / n, adjust=False).mean()
    al = loss.ewm(alpha=1 / n, adjust=False).mean()
    rs = ag / al.replace(0, np.nan)
    out = 100 - 100 / (1 + rs)
    return out.fillna(50)


def atr(df, n=14):
    pc = df["close"].shift(1)
    tr = pd.concat(
        [df["high"] - df["low"], (df["high"] - pc).abs(), (df["low"] - pc).abs()],
        axis=1,
    ).max(axis=1)
    return tr.ewm(alpha=1 / n, adjust=False).mean()


# ---------- strategies ----------
def ma_trend(df, fast=20, slow=50, atr_n=14, vol_filter=0.03):
    """MA cross trend following + volatility filter."""
    ma_f = sma(df["close"], fast)
    ma_s = sma(df["close"], slow)
    vol = atr(df, atr_n) / df["close"]
    cross_up = (ma_f > ma_s) & (ma_f.shift(1) <= ma_s.shift(1))
    cross_dn = (ma_f < ma_s) & (ma_f.shift(1) >= ma_s.shift(1))
    pos, out = 0, []
    for i in range(len(df)):
        if cross_dn.iloc[i]:
            pos = 0
        elif cross_up.iloc[i] and vol.iloc[i] < vol_filter:
            pos = 1
        out.append(pos)
    return pd.Series(out, index=df.index)


def rsi_reversion(df, n=14, oversold=30, exit_level=60):
    """Buy oversold, exit back to neutral."""
    r = rsi(df["close"], n)
    pos, out = 0, []
    for i in range(len(df)):
        v = r.iloc[i]
        if pos == 0 and v < oversold:
            pos = 1
        elif pos == 1 and v > exit_level:
            pos = 0
        out.append(pos)
    return pd.Series(out, index=df.index)


def donchian_breakout(df, entry_n=20, exit_n=10):
    """Buy N-bar high breakout, exit M-bar low breakdown (prior bars only)."""
    hi = df["high"].rolling(entry_n).max().shift(1)
    lo = df["low"].rolling(exit_n).min().shift(1)
    pos, out = 0, []
    for i in range(len(df)):
        c = df["close"].iloc[i]
        if pos == 0 and c > hi.iloc[i]:
            pos = 1
        elif pos == 1 and c < lo.iloc[i]:
            pos = 0
        out.append(pos)
    return pd.Series(out, index=df.index)


def hold_cash(df):
    """Baseline: never trade. Used if no candidate beats buy&hold."""
    return pd.Series(0, index=df.index)


STRATEGIES = {
    "ma_trend": ma_trend,
    "rsi_reversion": rsi_reversion,
    "donchian_breakout": donchian_breakout,
    "hold_cash": hold_cash,
}

DEFAULT_PARAMS = {
    "ma_trend": {"fast": 20, "slow": 50, "atr_n": 14, "vol_filter": 0.03},
    "rsi_reversion": {"n": 14, "oversold": 30, "exit_level": 60},
    "donchian_breakout": {"entry_n": 20, "exit_n": 10},
    "hold_cash": {},
}
