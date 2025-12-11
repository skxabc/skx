"""
基于缠论的买卖点策略（JQData）

策略规则：
- 一买：下跌趋势最后一个中枢后的背驰点（MACD底背离）
- 二买：一买后的回调不破一买低点
- 三买：突破中枢后的回调不破中枢上沿
- 一卖：上涨趋势最后一个中枢后的背驰点（MACD顶背离）
- 二卖：一卖后的反弹不破一卖高点
- 三卖：跌破中枢后的反弹不破中枢下沿

使用方法：
python3 chan_strategy.py --symbol 000001.XSHE --enable-buy1 --enable-buy2 --enable-buy3
"""
import os
import argparse
from datetime import date
from typing import Optional, List, Tuple, Dict, Any
import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta
from jqdatasdk import auth, logout, get_price


def parse_date(value: str) -> date:
    """解析 YYYY-MM-DD 格式日期"""
    try:
        return date.fromisoformat(value)
    except Exception as exc:
        raise argparse.ArgumentTypeError("日期格式需为 YYYY-MM-DD") from exc


def identify_bi(df: pd.DataFrame, lookback: int = 5) -> pd.DataFrame:
    """
    识别笔（简化版）：连续上涨或下跌的K线组合
    """
    df = df.copy()
    highs = df["high"].values
    lows = df["low"].values
    closes = df["close"].values
    
    # 简化笔识别：找局部高点和低点
    bi_highs = []
    bi_lows = []
    
    for i in range(lookback, len(df) - lookback):
        # 局部高点：前后lookback天内最高
        if highs[i] == max(highs[i-lookback:i+lookback+1]):
            bi_highs.append(i)
        # 局部低点：前后lookback天内最低
        if lows[i] == min(lows[i-lookback:i+lookback+1]):
            bi_lows.append(i)
    
    df["bi_high"] = False
    df["bi_low"] = False
    df.loc[df.index[bi_highs], "bi_high"] = True
    df.loc[df.index[bi_lows], "bi_low"] = True
    
    return df


def identify_zhongshu(df: pd.DataFrame, min_bars: int = 9) -> pd.DataFrame:
    """
    识别中枢：至少min_bars根K线的盘整区间
    """
    df = df.copy()
    df["zhongshu_high"] = np.nan
    df["zhongshu_low"] = np.nan
    df["in_zhongshu"] = False
    
    # 简化中枢识别：使用滚动窗口找盘整区间
    window = min_bars
    for i in range(window, len(df)):
        window_high = df["high"].iloc[i-window:i].max()
        window_low = df["low"].iloc[i-window:i].min()
        window_range = window_high - window_low
        
        # 如果波动范围较小，认为是中枢
        if window_range < df["close"].iloc[i] * 0.1:  # 波动小于10%
            df.loc[df.index[i], "zhongshu_high"] = window_high
            df.loc[df.index[i], "zhongshu_low"] = window_low
            df.loc[df.index[i], "in_zhongshu"] = True
    
    return df


def identify_macd_divergence(df: pd.DataFrame, lookback: int = 20) -> pd.DataFrame:
    """
    识别MACD背驰（简化版）
    """
    df = df.copy()
    
    # 计算MACD
    exp1 = df["close"].ewm(span=12, adjust=False).mean()
    exp2 = df["close"].ewm(span=26, adjust=False).mean()
    df["macd"] = exp1 - exp2
    df["macd_signal"] = df["macd"].ewm(span=9, adjust=False).mean()
    df["macd_hist"] = df["macd"] - df["macd_signal"]
    
    # 简化背驰识别：价格创新低但MACD不创新低（底背离），或价格创新高但MACD不创新高（顶背离）
    df["bottom_divergence"] = False
    df["top_divergence"] = False
    
    for i in range(lookback, len(df)):
        # 底背离：价格创新低，MACD不创新低
        recent_low_idx = df["low"].iloc[i-lookback:i].idxmin()
        recent_low = df["low"].iloc[i-lookback:i].min()
        current_low = df["low"].iloc[i]
        
        if current_low < recent_low:
            recent_macd = df["macd_hist"].loc[recent_low_idx]
            current_macd = df["macd_hist"].iloc[i]
            if current_macd > recent_macd:  # MACD不创新低
                df.loc[df.index[i], "bottom_divergence"] = True
        
        # 顶背离：价格创新高，MACD不创新高
        recent_high_idx = df["high"].iloc[i-lookback:i].idxmax()
        recent_high = df["high"].iloc[i-lookback:i].max()
        current_high = df["high"].iloc[i]
        
        if current_high > recent_high:
            recent_macd = df["macd_hist"].loc[recent_high_idx]
            current_macd = df["macd_hist"].iloc[i]
            if current_macd < recent_macd:  # MACD不创新高
                df.loc[df.index[i], "top_divergence"] = True
    
    return df


def identify_buy_points(
    df: pd.DataFrame,
    enable_buy1: bool = True,
    enable_buy2: bool = True,
    enable_buy3: bool = True,
) -> pd.DataFrame:
    """
    识别买点
    """
    df = df.copy()
    df["buy1"] = False
    df["buy2"] = False
    df["buy3"] = False
    
    # 一买：底背离 + 在下跌趋势中
    if enable_buy1:
        df["buy1"] = df["bottom_divergence"] & (df["close"] < df["close"].shift(20))
    
    # 二买：一买后的回调不破一买低点
    if enable_buy2:
        buy1_indices = df[df["buy1"]].index
        for buy1_idx in buy1_indices:
            buy1_low = df.loc[buy1_idx, "low"]
            # 找一买后20天内的最低点，如果不破一买低点，认为是二买
            after_buy1 = df.loc[buy1_idx:].iloc[:20]
            if len(after_buy1) > 5:
                min_after = after_buy1["low"].min()
                if min_after >= buy1_low * 0.98:  # 允许2%误差
                    min_idx = after_buy1["low"].idxmin()
                    if min_idx != buy1_idx:
                        df.loc[min_idx, "buy2"] = True
    
    # 三买：突破中枢后的回调不破中枢上沿
    if enable_buy3:
        for i in range(20, len(df)):
            # 检查是否刚突破中枢
            if i > 0 and df.loc[df.index[i-1], "in_zhongshu"]:
                zhongshu_high = df.loc[df.index[i-1], "zhongshu_high"]
                if pd.notna(zhongshu_high) and df["close"].iloc[i] > zhongshu_high:
                    # 突破后回调不破中枢上沿
                    for j in range(i, min(i+10, len(df))):
                        if df["low"].iloc[j] >= zhongshu_high * 0.99:
                            df.loc[df.index[j], "buy3"] = True
                            break
    
    return df


def identify_sell_points(
    df: pd.DataFrame,
    enable_sell1: bool = True,
    enable_sell2: bool = True,
    enable_sell3: bool = True,
) -> pd.DataFrame:
    """
    识别卖点
    """
    df = df.copy()
    df["sell1"] = False
    df["sell2"] = False
    df["sell3"] = False
    
    # 一卖：顶背离 + 在上涨趋势中
    if enable_sell1:
        df["sell1"] = df["top_divergence"] & (df["close"] > df["close"].shift(20))
    
    # 二卖：一卖后的反弹不破一卖高点
    if enable_sell2:
        sell1_indices = df[df["sell1"]].index
        for sell1_idx in sell1_indices:
            sell1_high = df.loc[sell1_idx, "high"]
            # 找一卖后20天内的最高点，如果不破一卖高点，认为是二卖
            after_sell1 = df.loc[sell1_idx:].iloc[:20]
            if len(after_sell1) > 5:
                max_after = after_sell1["high"].max()
                if max_after <= sell1_high * 1.02:  # 允许2%误差
                    max_idx = after_sell1["high"].idxmax()
                    if max_idx != sell1_idx:
                        df.loc[max_idx, "sell2"] = True
    
    # 三卖：跌破中枢后的反弹不破中枢下沿
    if enable_sell3:
        for i in range(20, len(df)):
            # 检查是否刚跌破中枢
            if i > 0 and df.loc[df.index[i-1], "in_zhongshu"]:
                zhongshu_low = df.loc[df.index[i-1], "zhongshu_low"]
                if pd.notna(zhongshu_low) and df["close"].iloc[i] < zhongshu_low:
                    # 跌破后反弹不破中枢下沿
                    for j in range(i, min(i+10, len(df))):
                        if df["high"].iloc[j] <= zhongshu_low * 1.01:
                            df.loc[df.index[j], "sell3"] = True
                            break
    
    return df


def run_backtest(
    symbol: str = "000001.XSHE",
    username: str = "",
    password: str = "",
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    enable_buy1: bool = True,
    enable_buy2: bool = True,
    enable_buy3: bool = True,
    enable_sell1: bool = True,
    enable_sell2: bool = True,
    enable_sell3: bool = True,
    fee_rate: float = 0.0005,
    slippage_bp: float = 1.0,
) -> None:
    """运行缠论策略回测"""
    today = date.today()
    raw_start = start_date or (today - relativedelta(months=15))
    raw_end = end_date or (today - relativedelta(months=3))
    permission_start = date(2024, 9, 1)
    permission_end = date(2025, 9, 8)
    start_date = max(raw_start, permission_start)
    end_date = min(raw_end, permission_end)
    
    if start_date >= end_date:
        print(f"可用区间为空，请检查权限或手动调整时间。当前计算区间: {start_date} ~ {end_date}")
        return
    
    if not username or not password:
        print("错误：需要提供JQData账号和密码")
        return
    
    auth(username, password)
    try:
        fq_mode = None if symbol.endswith("XHKG") else "pre"
        df = get_price(
            symbol,
            start_date=start_date,
            end_date=end_date,
            frequency="daily",
            fields=["open", "close", "high", "low", "volume"],
            skip_paused=not symbol.endswith("XHKG"),
            fq=fq_mode,
        )
        
        if df.empty:
            print("未取到数据，请检查代码或权限。")
            return
        
        # 识别缠论结构
        print("正在识别缠论结构...")
        df = identify_bi(df)
        df = identify_zhongshu(df)
        df = identify_macd_divergence(df)
        df = identify_buy_points(df, enable_buy1, enable_buy2, enable_buy3)
        df = identify_sell_points(df, enable_sell1, enable_sell2, enable_sell3)
        
        # 计算20日均线（用于止损）
        df["ma20"] = df["close"].rolling(20).mean()
        
        # 回测逻辑
        cash = 1.0
        shares = 0.0
        trades = []
        buy_price = None
        buy_idx = None  # 记录买入时的索引，用于判断是否买入当天
        
        for i in range(len(df)):
            # 检查买点
            if shares == 0:
                if (df["buy1"].iloc[i] or df["buy2"].iloc[i] or df["buy3"].iloc[i]):
                    buy_type = "BUY1" if df["buy1"].iloc[i] else ("BUY2" if df["buy2"].iloc[i] else "BUY3")
                    cost = df["close"].iloc[i] * (fee_rate + slippage_bp / 10000)
                    shares = cash / (df["close"].iloc[i] + cost)
                    cash = 0.0
                    buy_price = df["close"].iloc[i]
                    buy_idx = i  # 记录买入索引
                    trades.append((df.index[i], buy_type, buy_price))
            
            # 检查卖点
            if shares > 0:
                # 优先检查20日均线止损（买入当天不检查，从下一个交易日开始）
                stop_loss = False
                if i > buy_idx and pd.notna(df["ma20"].iloc[i]) and df["close"].iloc[i] < df["ma20"].iloc[i]:
                    stop_loss = True
                    sell_type = "STOP_LOSS"
                    sell_price = df["close"].iloc[i]
                    cost = sell_price * (fee_rate + slippage_bp / 10000)
                    cash = shares * (sell_price - cost)
                    trades.append((df.index[i], sell_type, sell_price))
                    shares = 0.0
                    buy_price = None
                    buy_idx = None
                # 如果没有止损，检查卖点信号
                elif (df["sell1"].iloc[i] or df["sell2"].iloc[i] or df["sell3"].iloc[i]):
                    sell_type = "SELL1" if df["sell1"].iloc[i] else ("SELL2" if df["sell2"].iloc[i] else "SELL3")
                    sell_price = df["close"].iloc[i]
                    cost = sell_price * (fee_rate + slippage_bp / 10000)
                    cash = shares * (sell_price - cost)
                    trades.append((df.index[i], sell_type, sell_price))
                    shares = 0.0
                    buy_price = None
                    buy_idx = None
        
        final_value = cash + shares * df["close"].iloc[-1]
        
        # 统计绩效
        trade_pairs = []
        buy_price = None
        for ts, side, px in trades:
            if side.startswith("BUY"):
                buy_price = px
            elif (side.startswith("SELL") or side == "STOP_LOSS") and buy_price is not None:
                pnl = px - buy_price
                ret = pnl / buy_price
                trade_pairs.append({"buy": buy_price, "sell": px, "pnl": pnl, "ret": ret, "buy_type": side, "sell_type": side})
                buy_price = None
        
        win_trades = [t for t in trade_pairs if t["pnl"] > 0]
        loss_trades = [t for t in trade_pairs if t["pnl"] < 0]
        success_rate = len(win_trades) / len(trade_pairs) * 100 if trade_pairs else 0.0
        avg_win = sum(t["pnl"] for t in win_trades) / len(win_trades) if win_trades else 0.0
        avg_loss = sum(t["pnl"] for t in loss_trades) / len(loss_trades) if loss_trades else 0.0
        win_loss_ratio = (avg_win / abs(avg_loss)) if avg_loss != 0 else float("inf") if avg_win > 0 else 0.0
        total_ret = final_value - 1.0
        
        # 输出结果
        print(f"\n回测标的: {symbol}")
        print(f"区间: {start_date} ~ {end_date}")
        print(f"启用的买点: {'一买' if enable_buy1 else ''} {'二买' if enable_buy2 else ''} {'三买' if enable_buy3 else ''}")
        print(f"启用的卖点: {'一卖' if enable_sell1 else ''} {'二卖' if enable_sell2 else ''} {'三卖' if enable_sell3 else ''}")
        print(f"止损策略: 跌破20日均线强制止损")
        print(f"交易次数(指令): {len(trades)}, 成交轮数(买卖对): {len(trade_pairs)}")
        print("\n交易记录:")
        for t in trades:
            print(f"{t[0].date()} {t[1]} @ {t[2]:.2f}")
        print("\n--- 绩效汇总 ---")
        print(f"期末资产: {final_value:.4f} (总收益 {total_ret*100:.2f}%)")
        print(f"胜率: {success_rate:.2f}%  | 盈亏比: {win_loss_ratio:.2f}")
        print(f"平均盈利(每笔): {avg_win:.4f}  | 平均亏损(每笔): {avg_loss:.4f}")
        if trade_pairs:
            print(f"样本笔数: 胜 {len(win_trades)} / 负 {len(loss_trades)} / 总 {len(trade_pairs)}")
        if shares > 0:
            print("注意：仍有持仓未平仓。")
    
    finally:
        logout()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="缠论买卖点策略回测（JQData）",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--symbol", default=os.getenv("JQ_SYMBOL", "000001.XSHE"), help="标的代码")
    parser.add_argument("--username", default=os.getenv("JQ_USERNAME", ""), help="JQData 账号")
    parser.add_argument("--password", default=os.getenv("JQ_PASSWORD", ""), help="JQData 密码")
    parser.add_argument("--start-date", type=parse_date, default=None, help="回测开始日期，格式 YYYY-MM-DD")
    parser.add_argument("--end-date", type=parse_date, default=None, help="回测结束日期，格式 YYYY-MM-DD")
    parser.add_argument("--enable-buy1", action="store_true", help="启用一买（默认启用）")
    parser.add_argument("--disable-buy1", action="store_true", help="禁用一买")
    parser.add_argument("--enable-buy2", action="store_true", help="启用二买（默认启用）")
    parser.add_argument("--disable-buy2", action="store_true", help="禁用二买")
    parser.add_argument("--enable-buy3", action="store_true", help="启用三买（默认启用）")
    parser.add_argument("--disable-buy3", action="store_true", help="禁用三买")
    parser.add_argument("--enable-sell1", action="store_true", help="启用一卖（默认启用）")
    parser.add_argument("--disable-sell1", action="store_true", help="禁用一卖")
    parser.add_argument("--enable-sell2", action="store_true", help="启用二卖（默认启用）")
    parser.add_argument("--disable-sell2", action="store_true", help="禁用二卖")
    parser.add_argument("--enable-sell3", action="store_true", help="启用三卖（默认启用）")
    parser.add_argument("--disable-sell3", action="store_true", help="禁用三卖")
    parser.add_argument("--fee-rate", type=float, default=0.0005, help="单边手续费率")
    parser.add_argument("--slippage-bp", type=float, default=1.0, help="滑点（基点）")
    
    args = parser.parse_args()
    
    # 默认所有买卖点都启用，除非明确禁用
    enable_buy1 = not args.disable_buy1
    enable_buy2 = not args.disable_buy2
    enable_buy3 = not args.disable_buy3
    enable_sell1 = not args.disable_sell1
    enable_sell2 = not args.disable_sell2
    enable_sell3 = not args.disable_sell3
    
    run_backtest(
        symbol=args.symbol,
        username=args.username,
        password=args.password,
        start_date=args.start_date,
        end_date=args.end_date,
        enable_buy1=enable_buy1,
        enable_buy2=enable_buy2,
        enable_buy3=enable_buy3,
        enable_sell1=enable_sell1,
        enable_sell2=enable_sell2,
        enable_sell3=enable_sell3,
        fee_rate=args.fee_rate,
        slippage_bp=args.slippage_bp,
    )

