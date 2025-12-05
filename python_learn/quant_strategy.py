#!/usr/bin/env python3
"""
基于“高点创新高持有，跌破前低清仓，并忽略被包住K线”的简易量化策略。

默认标的：中国平安（601318.SH），可通过 --csv 指定本地数据。
依赖：pandas，可选依赖 akshare 或 yfinance（任一存在即可自动取数，支持自定义 ticker）。
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path
from typing import List, Optional, Sequence, Tuple

import pandas as pd


def _to_float(value) -> float:
    if isinstance(value, pd.Series):
        return float(value.iloc[0])
    return float(value)


def _akshare_symbol_from_ticker(ticker: str) -> Optional[str]:
    code = ticker.upper()
    for suffix in (".SS", ".SH", ".SZ", ".SZSE", ".SSE"):
        if code.endswith(suffix):
            code = code.split(".")[0]
            break
    if code.isdigit() and len(code) == 6:
        return code
    return None


def _load_from_csv(csv_path: Path) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    date_col = next((col for col in df.columns if col.lower().startswith("date")), None)
    if not date_col:
        raise ValueError("CSV 中需要包含日期列，例如 date 或 Date")
    df[date_col] = pd.to_datetime(df[date_col])
    rename_map = {
        date_col: "date",
    }
    for col in df.columns:
        lower = col.lower()
        if lower.startswith("open"):
            rename_map[col] = "open"
        elif lower.startswith("high"):
            rename_map[col] = "high"
        elif lower.startswith("low"):
            rename_map[col] = "low"
        elif lower.startswith("close"):
            rename_map[col] = "close"
        elif lower.startswith("volume"):
            rename_map[col] = "volume"
    df = df.rename(columns=rename_map)
    required = {"date", "open", "high", "low", "close"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"CSV 缺少必要列: {missing}")
    return df[list(required | {"volume"}) if "volume" in df.columns else list(required)]


def _try_load_from_akshare(
    symbol: Optional[str], start: str, end: Optional[str]
) -> Optional[pd.DataFrame]:
    if not symbol:
        return None
    try:
        import akshare as ak  # type: ignore
    except ModuleNotFoundError:
        return None
    start_fmt = start.replace("-", "")
    end_fmt = end.replace("-", "") if end else None
    try:
        raw = ak.stock_zh_a_hist(
            symbol=symbol,
            period="daily",
            start_date=start_fmt,
            end_date=end_fmt,
            adjust="qfq",
        )
    except Exception:
        return None
    if raw.empty:
        return None
    raw = raw.rename(
        columns={
            "日期": "date",
            "开盘": "open",
            "最高": "high",
            "最低": "low",
            "收盘": "close",
            "成交量": "volume",
        }
    )
    raw["date"] = pd.to_datetime(raw["date"])
    return raw[["date", "open", "high", "low", "close", "volume"]]


def _try_load_from_yfinance(ticker: str, start: str, end: Optional[str]) -> Optional[pd.DataFrame]:
    try:
        import yfinance as yf  # type: ignore
    except ModuleNotFoundError:
        return None
    try:
        data = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=True)
    except Exception:
        return None
    if data.empty:
        return None
    data = data.reset_index()
    data = data.rename(
        columns={
            "Date": "date",
            "Open": "open",
            "High": "high",
            "Low": "low",
            "Close": "close",
            "Volume": "volume",
        }
    )
    return data[["date", "open", "high", "low", "close", "volume"]]


def load_market_data(
    csv: Optional[Path], ticker: str, start: str, end: Optional[str]
) -> pd.DataFrame:
    if csv:
        return _load_from_csv(csv)

    ak_symbol = _akshare_symbol_from_ticker(ticker)
    loader_calls = []
    if ak_symbol:
        loader_calls.append(lambda: _try_load_from_akshare(ak_symbol, start, end))
    loader_calls.append(lambda: _try_load_from_yfinance(ticker, start, end))

    for call in loader_calls:
        data = call()
        if data is not None:
            return data
    raise RuntimeError(
        f"无法自动获取 {ticker} 的数据，请通过 --csv 提供包含 date/open/high/low/close 的文件。"
    )


def filter_bars(df: pd.DataFrame) -> Tuple[pd.DataFrame, List[int]]:
    """根据包含关系忽略被包住的K线，返回标记后的DataFrame以及有效索引列表。"""
    work = df.sort_values("date").reset_index(drop=True).copy()
    work = work.loc[:, ~work.columns.duplicated()].copy()
    ignored_flags = [False] * len(work)
    considered: List[int] = []
    for idx, row in work.iterrows():
        if not considered:
            considered.append(idx)
            continue
        row_high = _to_float(row["high"])
        row_low = _to_float(row["low"])
        while considered:
            prev_idx = considered[-1]
            prev = work.loc[prev_idx]
            prev_high = _to_float(prev["high"])
            prev_low = _to_float(prev["low"])
            if row_high <= prev_high and row_low >= prev_low:
                ignored_flags[idx] = True
                break
            if row_high >= prev_high and row_low <= prev_low:
                ignored_flags[prev_idx] = True
                considered.pop()
                continue
            break
        if not ignored_flags[idx]:
            considered.append(idx)
    work["ignored"] = ignored_flags
    return work, considered


@dataclass
class TradeRecord:
    date: pd.Timestamp
    action: str
    price: float
    ref_high: float
    ref_low: float
    position: int
    cash: float
    shares: float
    equity: float


def run_strategy(df: pd.DataFrame, initial_capital: float) -> Tuple[pd.DataFrame, pd.DataFrame]:
    prepared, valid_indices = filter_bars(df)
    if len(valid_indices) < 2:
        raise RuntimeError("有效K线少于2根，无法运行策略。")
    cash = initial_capital
    shares = 0.0
    position = 0
    records: List[TradeRecord] = []
    last_idx = valid_indices[0]
    for idx in valid_indices[1:]:
        row = prepared.loc[idx]
        ref = prepared.loc[last_idx]
        row_high = _to_float(row["high"])
        row_low = _to_float(row["low"])
        ref_high = _to_float(ref["high"])
        ref_low = _to_float(ref["low"])
        action = "wait"
        price = _to_float(row["close"])
        if row_low < ref_low and position == 1:
            cash = shares * price
            shares = 0.0
            position = 0
            action = "sell"
        elif row_high > ref_high:
            if position == 0:
                shares = cash / price
                cash = 0.0
                position = 1
                action = "buy"
            else:
                action = "hold"
        equity = cash + shares * price
        records.append(
            TradeRecord(
                date=row["date"],
                action=action,
                price=price,
                ref_high=ref_high,
                ref_low=ref_low,
                position=position,
                cash=round(cash, 2),
                shares=round(shares, 4),
                equity=round(equity, 2),
            )
        )
        last_idx = idx
    trades_df = pd.DataFrame(records)
    return prepared, trades_df


def summarize(trades: pd.DataFrame, initial_capital: float) -> str:
    if trades.empty:
        return "无交易产生。"
    total_return = trades.iloc[-1]["equity"] / initial_capital - 1
    buys = (trades["action"] == "buy").sum()
    sells = (trades["action"] == "sell").sum()
    return (
        f"策略共发出 {buys} 次买入、{sells} 次卖出指令，"
        f"期末权益 {trades.iloc[-1]['equity']:.2f}，总收益率 {total_return:.2%}。"
    )


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="中国平安包含关系趋势策略示例")
    parser.add_argument("--csv", type=Path, help="本地CSV数据路径（列需包含 date/open/high/low/close）")
    parser.add_argument("--start", default="2018-01-01", help="回测开始日期，默认2018-01-01")
    parser.add_argument("--end", default=None, help="回测结束日期，默认为今日")
    parser.add_argument("--capital", type=float, default=1_000_000, help="初始资金，默认100万")
    parser.add_argument(
        "--ticker",
        default="601318.SS",
        help="标的代码（yfinance 格式，如 601318.SS 或 9880.HK），默认中国平安A股",
    )
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> None:
    args = parse_args(argv)
    market = load_market_data(args.csv, args.ticker, args.start, args.end)
    prepared, trades = run_strategy(market, args.capital)

    print("=== 策略过滤后的K线统计 ===")
    ignored_ratio = prepared["ignored"].mean()
    print(
        f"总K线 {len(prepared)}，被忽略 {prepared['ignored'].sum()} 根，占比 {ignored_ratio:.2%}。\n"
    )

    print("=== 交易记录（仅展示有动作的K线） ===")
    actionable = trades[trades["action"].isin({"buy", "sell"})]
    if actionable.empty:
        print("无买卖信号，策略 全程空仓。")
    else:
        print(actionable.to_string(index=False))

    print("\n=== 策略表现 ===")
    print(summarize(trades, args.capital))


if __name__ == "__main__":
    main()
