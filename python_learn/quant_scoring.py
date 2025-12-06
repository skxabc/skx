#!/usr/bin/env python3
"""
量化评分系统：

给定一组 ticker，自动从 yfinance 拉取历史行情，计算趋势、波动、流动性等指标，
对每只股票打分并排序，辅助“先筛选后执行”。

示例：
    python3 python_learn/quant_scoring.py --tickers 9880.HK 2018.HK 0165.HK \\
        --start 2023-01-01 --lookback 252
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from typing import Dict, Iterable, List, Optional, Sequence, Tuple

import numpy as np
import pandas as pd


try:
    import yfinance as yf
except ModuleNotFoundError as exc:  # pragma: no cover - handled at runtime
    raise SystemExit("请先安装 yfinance：pip install yfinance") from exc


def _atr(df: pd.DataFrame, window: int = 14) -> pd.Series:
    high_low = df["High"] - df["Low"]
    high_close = (df["High"] - df["Close"].shift()).abs()
    low_close = (df["Low"] - df["Close"].shift()).abs()
    tr = pd.concat([high_low, high_close, low_close], axis=1).max(axis=1)
    return tr.rolling(window=window).mean()


@dataclass
class Metrics:
    ticker: str
    last_price: float
    ret_6m: float
    ret_3m: float
    price_vs_ma50: float
    price_vs_ma150: float
    atr_pct: float
    dollar_vol: float


def compute_metrics(ticker: str, start: str, end: Optional[str], lookback: int) -> Optional[Metrics]:
    data = yf.download(
        ticker,
        start=start,
        end=end,
        auto_adjust=False,
        progress=False,
    )
    if data.empty:
        return None
    close = data["Close"]
    high = data["High"]
    low = data["Low"]
    volume = data["Volume"]
    if isinstance(close, pd.DataFrame):
        close = close.iloc[:, 0]
        high = high.iloc[:, 0]
        low = low.iloc[:, 0]
        volume = volume.iloc[:, 0]
        data = pd.DataFrame({"High": high, "Low": low, "Close": close, "Volume": volume})
    if len(close) < lookback:
        return None
    ret_6m = close.pct_change(126).iloc[-1]
    ret_3m = close.pct_change(63).iloc[-1]
    ma50 = close.rolling(50).mean().iloc[-1]
    ma150 = close.rolling(150).mean().iloc[-1]
    if pd.isna(ma50) or pd.isna(ma150):
        return None
    last_price = close.iloc[-1]
    atr_val = _atr(data, window=14).iloc[-1]
    atr_pct = atr_val / last_price if last_price else 0.0
    dollar_vol = (data["Volume"] * close).rolling(20).mean().iloc[-1]
    return Metrics(
        ticker=ticker,
        last_price=float(last_price),
        ret_6m=float(ret_6m),
        ret_3m=float(ret_3m),
        price_vs_ma50=float(last_price / ma50 - 1),
        price_vs_ma150=float(last_price / ma150 - 1),
        atr_pct=float(atr_pct),
        dollar_vol=float(dollar_vol),
    )


def _min_max(values: Iterable[float]) -> Tuple[float, float]:
    arr = np.array(list(values), dtype=float)
    return float(arr.min()), float(arr.max())


def normalize(series: pd.Series, reverse: bool = False) -> pd.Series:
    lo, hi = series.min(), series.max()
    if np.isclose(lo, hi):
        return pd.Series(50.0, index=series.index)
    scaled = (series - lo) / (hi - lo) * 100
    return 100 - scaled if reverse else scaled


def build_scoreboard(metrics: List[Metrics]) -> pd.DataFrame:
    df = pd.DataFrame([m.__dict__ for m in metrics]).set_index("ticker")
    # 趋势：6M/3M收益 + 相对MA
    df["trend_raw"] = (
        df["ret_6m"] * 0.4
        + df["ret_3m"] * 0.3
        + df["price_vs_ma50"] * 0.2
        + df["price_vs_ma150"] * 0.1
    )
    df["trend_score"] = normalize(df["trend_raw"].fillna(0))
    # 波动：ATR/Price 越适中越好，设定目标 5%-15%，偏离越大扣分
    target_low, target_high = 0.05, 0.15
    atr_penalty = (
        df["atr_pct"]
        .apply(lambda x: 0 if target_low <= x <= target_high else min(abs(x - target_low), abs(x - target_high)))
        .fillna(0)
    )
    df["volatility_score"] = normalize(-atr_penalty)
    # 流动性：美元成交额越高越好
    df["liquidity_score"] = normalize(df["dollar_vol"].fillna(0))
    # 综合得分
    df["total_score"] = (
        df["trend_score"] * 0.5 + df["volatility_score"] * 0.2 + df["liquidity_score"] * 0.3
    )
    df = df.sort_values("total_score", ascending=False)
    return df


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="量化评分系统")
    parser.add_argument("--tickers", nargs="+", required=True, help="待评估的 ticker 列表（yfinance 代码）")
    parser.add_argument("--start", default="2023-01-01", help="下载行情的起始日期，默认 2023-01-01")
    parser.add_argument("--end", default=None, help="下载行情的结束日期，默认今日")
    parser.add_argument("--lookback", type=int, default=252, help="所需最短数据长度，默认 252 个交易日")
    parser.add_argument("--top", type=int, default=10, help="打印前 N 名，默认 10")
    parser.add_argument("--csv", type=str, help="若提供，将把评分结果输出到该 CSV 路径")
    return parser.parse_args(argv)


def main(argv: Optional[Sequence[str]] = None) -> None:
    args = parse_args(argv)
    metrics_list: List[Metrics] = []
    failed: List[str] = []
    for ticker in args.tickers:
        metrics = compute_metrics(ticker, args.start, args.end, args.lookback)
        if metrics is None:
            failed.append(ticker)
        else:
            metrics_list.append(metrics)
    if not metrics_list:
        raise SystemExit("没有成功获取任何 ticker 的指标，请检查代码或日期范围。")
    board = build_scoreboard(metrics_list)
    top_n = board.head(args.top)
    print("=== 综合评分排名 ===")
    print(
        top_n[
            [
                "total_score",
                "trend_score",
                "volatility_score",
                "liquidity_score",
                "ret_6m",
                "ret_3m",
                "atr_pct",
                "dollar_vol",
            ]
        ].round(3)
    )
    if args.csv:
        board.to_csv(args.csv)
        print(f"\n已保存完整评分到 {args.csv}")
    if failed:
        print("\n以下 ticker 下载失败或数据不足，已跳过：", ", ".join(failed))


if __name__ == "__main__":
    main()
