"""Market data: public read-only APIs, no keys, no account.

Primary : Binance public market data  (https://data-api.binance.vision)
Fallback: Kraken public OHLC          (https://api.kraken.com)
"""
import time
import requests
import pandas as pd

BINANCE_VISION = "https://data-api.binance.vision"
KRAKEN = "https://api.kraken.com"
INTERVAL_MS = {"1h": 3_600_000, "4h": 14_400_000, "1d": 86_400_000}


def _binance_klines(symbol, interval, start_ms=None, end_ms=None, limit=1000, timeout=20):
    url = f"{BINANCE_VISION}/api/v3/klines"
    params = {"symbol": symbol, "interval": interval, "limit": limit}
    if start_ms:
        params["startTime"] = int(start_ms)
    if end_ms:
        params["endTime"] = int(end_ms)
    r = requests.get(url, params=params, timeout=timeout)
    r.raise_for_status()
    data = r.json()
    if not data:
        return pd.DataFrame(columns=["ts", "open", "high", "low", "close", "volume"])
    df = pd.DataFrame(
        data,
        columns=["ts", "open", "high", "low", "close", "volume", "close_ts",
                 "qav", "trades", "taker_base", "taker_quote", "ignore"],
    )
    for c in ["open", "high", "low", "close", "volume"]:
        df[c] = df[c].astype(float)
    df["ts"] = df["ts"].astype("int64")
    return df[["ts", "open", "high", "low", "close", "volume"]]


def _drop_forming_candle(df, interval):
    """Remove the currently-forming candle: only CLOSED candles allowed (no lookahead)."""
    if df.empty:
        return df
    step = INTERVAL_MS[interval]
    now_ms = int(time.time() * 1000)
    last_closed_open = (now_ms // step) * step
    return df[df["ts"] < last_closed_open].reset_index(drop=True)


def fetch_history_binance(symbol="BTCUSDT", interval="1h", days=730):
    """Fetch up to `days` of closed 1h candles from Binance Vision (paginated)."""
    step = INTERVAL_MS[interval]
    need = int(days * 24 * 3600_000 / step) + 10
    end_ms = int(time.time() * 1000)
    parts, fetched = [], 0
    while fetched < need:
        df = _binance_klines(symbol, interval, end_ms=end_ms, limit=1000)
        if df.empty:
            break
        parts.append(df)
        fetched += len(df)
        end_ms = int(df["ts"].iloc[0]) - 1
        if len(df) < 1000:
            break
        time.sleep(0.15)
    if not parts:
        raise RuntimeError("Binance Vision returned no data")
    full = (
        pd.concat(parts)
        .drop_duplicates("ts")
        .sort_values("ts")
        .reset_index(drop=True)
    )
    return _drop_forming_candle(full, interval)


def fetch_recent_binance(symbol="BTCUSDT", interval="1h", limit=300):
    """Fetch the most recent `limit` closed candles (for paper-live steps)."""
    df = _binance_klines(symbol, interval, limit=limit)
    return _drop_forming_candle(df, interval)


KRAKEN_PAIR = {"BTCUSDT": "XBTUSDT", "ETHUSDT": "ETHUSDT"}


def fetch_recent_kraken(symbol="BTCUSDT", interval="1h", limit=300):
    """Fallback: Kraken public OHLC (max 720 candles per call)."""
    pair = KRAKEN_PAIR[symbol]
    iv = {"1h": 60, "4h": 240, "1d": 1440}[interval]
    r = requests.get(
        f"{KRAKEN}/0/public/OHLC",
        params={"pair": pair, "interval": iv},
        timeout=20,
    )
    r.raise_for_status()
    payload = r.json()
    if payload.get("error"):
        raise RuntimeError(f"Kraken error: {payload['error']}")
    key = next(k for k in payload["result"] if k != "last")
    rows = payload["result"][key][-limit:]
    df = pd.DataFrame(rows, columns=["ts", "open", "high", "low", "close", "vwap", "volume", "count"])
    df["ts"] = (df["ts"].astype(float) * 1000).astype("int64")
    for c in ["open", "high", "low", "close", "volume"]:
        df[c] = df[c].astype(float)
    return _drop_forming_candle(df[["ts", "open", "high", "low", "close", "volume"]], interval)


def fetch_recent(symbol="BTCUSDT", interval="1h", limit=300):
    """Recent closed candles, primary -> fallback."""
    try:
        df = fetch_recent_binance(symbol, interval, limit)
        if len(df) >= 60:
            return df
    except Exception as e:
        print(f"[data] binance vision failed ({e}), trying kraken…")
    return fetch_recent_kraken(symbol, interval, limit)
