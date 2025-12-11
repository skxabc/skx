"""
基于 JQData 的突破前高+内外包线回测示例，增强了过滤和风控参数。

策略规则（多头为例）：
- 放量突破前高时建仓（全仓）：收盘价突破最近 N 天（默认20天）的最高价，且成交量放大。
- 高低点比较只考虑"有效 K 线"：若当日 K 线被前一有效 K 线完全包含，则忽略当日 K 线；若当日 K 线完全包住前一有效 K 线，则忽略前一有效 K 线。被忽略的 K 线后续比较中都不再使用。
- 持仓期间，若当日低点跌破前一有效 K 线的低点，则清仓。
- 其余情况继续持有；被忽略的 K 线不触发任何操作。

使用方法：
- 将 JQData 账号、密码填入 `JQ_USERNAME` 与 `JQ_PASSWORD`（当前默认空字符串）。
- 通过环境变量 `JQ_SYMBOL` 指定标的代码，示例默认为 '000001.XSHE'。需替换为“优比选”对应的证券代码。
- 回测区间：从今日向前 15 个月到向前 3 个月。
"""
from jqdatasdk import *
from datetime import date
import os
import argparse
from typing import List, Tuple, Optional, Dict, Any

import numpy as np
import pandas as pd
from dateutil.relativedelta import relativedelta
from jqdatasdk import auth, logout, get_price


def parse_date(value: str) -> date:
    """解析 YYYY-MM-DD 格式日期，错误则提示帮助信息。"""
    try:
        return date.fromisoformat(value)
    except Exception as exc:  # noqa: BLE001
        raise argparse.ArgumentTypeError("日期格式需为 YYYY-MM-DD") from exc


def _add_effective_bar(effective: List[int], highs, lows, idx: int) -> Tuple[bool, int]:
    """
    根据内包/外包关系更新有效 K 线列表。

    返回 (是否纳入有效, 更新前的上一根有效 K 线下标或 None)。
    """
    while effective:
        last = effective[-1]
        # 当日被上一有效 K 线完全包含 -> 忽略当日
        if highs[idx] <= highs[last] and lows[idx] >= lows[last]:
            return False, last
        # 当日完全包住上一有效 K 线 -> 移除上一有效 K 线，继续比较更早的
        if highs[idx] >= highs[last] and lows[idx] <= lows[last]:
            effective.pop()
            continue
        break
    prev = effective[-1] if effective else None
    effective.append(idx)
    return True, prev


def run_backtest(
    symbol: str = "000001.XSHE",
    username: str = "18813098345",
    password: str = "Shitou+6819815",
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    high_lookback: int = 10,
    trend_ma: Optional[int] = 20,
    vol_lookback: int = 10,
    vol_mult: float = 1.0,
    atr_lookback: int = 14,
    atr_mult: float = 2.0,
    simple_stop_pct: Optional[float] = None,
    max_hold_days: Optional[int] = None,
    disable_break_stop: bool = False,
    fee_rate: float = 0.0005,
    slippage_bp: float = 1.0,
    silent: bool = False,
    skip_auth: bool = False,
) -> Optional[Dict[str, Any]]:
    today = date.today()
    # 默认区间：向前 15 个月到向前 3 个月，再与账号权限窗口取交集
    raw_start = start_date or (today - relativedelta(months=15))
    raw_end = end_date or (today - relativedelta(months=3))
    permission_start = date(2024, 9, 1)
    permission_end = date(2025, 9, 8)
    start_date = max(raw_start, permission_start)
    end_date = min(raw_end, permission_end)
    if start_date >= end_date:
        msg = f"可用区间为空，请检查权限或手动调整时间。当前计算区间: {start_date} ~ {end_date}"
        if not silent:
            print(msg)
        return None

    if not skip_auth:
        auth(username, password)
    try:
        fq_mode = None if symbol.endswith("XHKG") else "pre"
        df = get_price(
            symbol,
            start_date=start_date,
            end_date=end_date,
            frequency="daily",
            fields=["open", "close", "high", "low", "volume"],
            skip_paused=not symbol.endswith("XHKG"),  # 港股通无需停牌过滤
            fq=fq_mode,
        )
        if df.empty:
            msg = f"未取到数据，请检查代码或权限: {symbol}"
            if not silent:
                print(msg)
            return None

        # 计算前高（最近 high_lookback 天的最高价）
        df["prev_high"] = df["high"].rolling(high_lookback).max().shift(1)  # shift(1) 表示前一日的前高
        if trend_ma:
            df["ma_trend"] = df["close"].rolling(trend_ma).mean()
        df["vol_mean"] = df["volume"].rolling(vol_lookback).mean()
        # ATR
        tr1 = df["high"] - df["low"]
        tr2 = (df["high"] - df["close"].shift()).abs()
        tr3 = (df["low"] - df["close"].shift()).abs()
        tr = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)
        df["atr"] = tr.rolling(atr_lookback).mean()

        highs, lows, closes = df["high"].values, df["low"].values, df["close"].values
        effective: List[int] = []

        cash = 1.0  # 初始资金
        shares = 0.0
        trades: List[Tuple[Any, str, float]] = []
        peak_close = None
        entry_idx = None

        for i in range(len(df)):
            # 放量突破前高开仓
            if shares == 0:
                # 突破前高：收盘价突破前 high_lookback 天的最高价
                cond_break_high = (
                    i >= high_lookback
                    and pd.notna(df["prev_high"].iloc[i])
                    and closes[i] > df["prev_high"].iloc[i]
                )
                # 趋势过滤（可选）
                cond_trend = True if trend_ma is None else closes[i] > df["ma_trend"].iloc[i]
                # 量能过滤：要求放量
                cond_vol = True if vol_mult <= 0 else (pd.notna(df["vol_mean"].iloc[i]) and df["volume"].iloc[i] > df["vol_mean"].iloc[i] * vol_mult)
                if cond_break_high and cond_trend and cond_vol:
                    cost = closes[i] * (fee_rate + slippage_bp / 10000)
                    shares = cash / (closes[i] + cost)
                    cash = 0.0
                    trades.append((df.index[i], "BUY", closes[i]))
                    peak_close = closes[i]
                    entry_idx = i

            included, prev_eff = _add_effective_bar(effective, highs, lows, i)

            # 持仓中的止损检查
            if shares > 0:
                # 破前有效低点（可关闭）
                stop_break = False
                if not disable_break_stop and included and prev_eff is not None:
                    stop_break = lows[i] < lows[prev_eff]
                
                # 移动止损（简化版或ATR版）
                stop_trail = False
                if peak_close is not None:
                    peak_close = max(peak_close, closes[i])
                    
                    # 简化版：固定百分比移动止损
                    if simple_stop_pct is not None and simple_stop_pct > 0:
                        trail_stop = peak_close * (1 - simple_stop_pct / 100)
                        stop_trail = closes[i] < trail_stop
                    # ATR版：基于ATR的移动止损
                    elif atr_mult < 9999 and pd.notna(df["atr"].iloc[i]):
                        trail_stop = peak_close - atr_mult * df["atr"].iloc[i]
                        stop_trail = closes[i] < trail_stop
                
                # 时间止损
                hold_days = i - entry_idx if entry_idx is not None else 0
                time_exit = max_hold_days is not None and hold_days >= max_hold_days

                if stop_break or stop_trail or time_exit:
                    sell_price = closes[i]
                    cost = sell_price * (fee_rate + slippage_bp / 10000)
                    cash = shares * (sell_price - cost)
                    trades.append((df.index[i], "SELL", sell_price))
                    shares = 0.0
                    peak_close = None
                    entry_idx = None

        final_value = cash + shares * closes[-1]
        # 统计成交对（买->卖）及绩效
        trade_pairs: List[Dict[str, float]] = []
        buy_price = None
        for ts, side, px in trades:
            if side == "BUY":
                buy_price = px
            elif side == "SELL" and buy_price is not None:
                pnl = px - buy_price
                ret = pnl / buy_price
                trade_pairs.append({"buy": buy_price, "sell": px, "pnl": pnl, "ret": ret})
                buy_price = None

        win_trades = [t for t in trade_pairs if t["pnl"] > 0]
        loss_trades = [t for t in trade_pairs if t["pnl"] < 0]
        success_rate = len(win_trades) / len(trade_pairs) * 100 if trade_pairs else 0.0
        avg_win = sum(t["pnl"] for t in win_trades) / len(win_trades) if win_trades else 0.0
        avg_loss = sum(t["pnl"] for t in loss_trades) / len(loss_trades) if loss_trades else 0.0
        win_loss_ratio = (avg_win / abs(avg_loss)) if avg_loss != 0 else float("inf") if avg_win > 0 else 0.0
        total_ret = final_value - 1.0

        result = {
            "symbol": symbol,
            "start_date": start_date,
            "end_date": end_date,
            "trades": trades,
            "trade_pairs": trade_pairs,
            "final_value": final_value,
            "total_ret": total_ret,
            "success_rate": success_rate,
            "win_loss_ratio": win_loss_ratio,
            "avg_win": avg_win,
            "avg_loss": avg_loss,
            "win_count": len(win_trades),
            "loss_count": len(loss_trades),
            "total_trades": len(trade_pairs),
            "has_position": shares > 0,
        }

        if not silent:
            print(f"回测标的: {symbol}")
            print(f"区间: {start_date} ~ {end_date}")
            if disable_break_stop:
                print(f"跌破前日K线新低止损: 已关闭")
            else:
                print(f"跌破前日K线新低止损: 已启用")
            if simple_stop_pct is not None:
                print(f"移动止损: 简化版（固定{simple_stop_pct}%回撤）")
            elif atr_mult < 9999:
                print(f"移动止损: ATR版（{atr_lookback}日ATR × {atr_mult}）")
            else:
                print(f"移动止损: 已关闭")
            print(f"交易次数(指令): {len(trades)}, 成交轮数(买卖对): {len(trade_pairs)}")
            for t in trades:
                print(f"{t[0].date()} {t[1]} @ {t[2]:.2f}")
            print("--- 绩效汇总 ---")
            print(f"期末资产: {final_value:.4f} (总收益 {total_ret*100:.2f}%)")
            print(f"胜率: {success_rate:.2f}%  | 盈亏比: {win_loss_ratio:.2f}")
            print(f"平均盈利(每笔): {avg_win:.4f}  | 平均亏损(每笔): {avg_loss:.4f}")
            if trade_pairs:
                print(f"样本笔数: 胜 {len(win_trades)} / 负 {len(loss_trades)} / 总 {len(trade_pairs)}")
            if shares > 0:
                print("注意：仍有持仓未平仓，未计入胜率和盈亏比。")

        return result
    finally:
        if not skip_auth:
            logout()


def run_batch_backtest(
    symbols: List[str],
    username: str = "18813098345",
    password: str = "Shitou+6819815",
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    high_lookback: int = 20,
    trend_ma: Optional[int] = 20,
    vol_lookback: int = 10,
    vol_mult: float = 1.0,
    atr_lookback: int = 14,
    atr_mult: float = 2.0,
    simple_stop_pct: Optional[float] = None,
    max_hold_days: Optional[int] = None,
    disable_break_stop: bool = False,
    fee_rate: float = 0.0005,
    slippage_bp: float = 1.0,
) -> None:
    """批量回测多个标的"""
    if len(symbols) > 10:
        print(f"错误：最多支持10个标的，当前提供 {len(symbols)} 个")
        return

    # 批量回测时只登录一次
    auth(username, password)
    try:
        results = []
        print(f"开始批量回测 {len(symbols)} 个标的...")
        print("=" * 80)

        for idx, symbol in enumerate(symbols, 1):
            print(f"\n[{idx}/{len(symbols)}] 回测标的: {symbol}")
            print("-" * 80)
            result = run_backtest(
                symbol=symbol,
                username=username,
                password=password,
                start_date=start_date,
                end_date=end_date,
                high_lookback=high_lookback,
                trend_ma=trend_ma,
                vol_lookback=vol_lookback,
                vol_mult=vol_mult,
                atr_lookback=atr_lookback,
                atr_mult=atr_mult,
                simple_stop_pct=simple_stop_pct,
                max_hold_days=max_hold_days,
                disable_break_stop=disable_break_stop,
                fee_rate=fee_rate,
                slippage_bp=slippage_bp,
                silent=False,
                skip_auth=True,  # 批量回测时跳过登录
            )
            if result:
                results.append(result)

        # 汇总统计
        if results:
            print("\n" + "=" * 80)
            print("批量回测汇总统计")
            print("=" * 80)
            print(f"{'标的代码':<15} {'总收益%':<10} {'胜率%':<10} {'盈亏比':<10} {'交易次数':<10}")
            print("-" * 80)

            total_ret_sum = 0.0
            total_trades = 0
            total_wins = 0
            total_losses = 0
            win_ret_sum = 0.0
            loss_ret_sum = 0.0

            for r in results:
                symbol_short = r["symbol"].split(".")[0]
                print(
                    f"{symbol_short:<15} "
                    f"{r['total_ret']*100:>8.2f}%  "
                    f"{r['success_rate']:>8.2f}%  "
                    f"{r['win_loss_ratio']:>8.2f}  "
                    f"{r['total_trades']:>8}"
                )
                total_ret_sum += r["total_ret"]
                total_trades += r["total_trades"]
                total_wins += r["win_count"]
                total_losses += r["loss_count"]

            avg_ret = total_ret_sum / len(results) if results else 0.0
            overall_success_rate = (total_wins / total_trades * 100) if total_trades > 0 else 0.0

            print("-" * 80)
            print(f"平均收益: {avg_ret*100:.2f}%")
            print(f"整体胜率: {overall_success_rate:.2f}% ({total_wins}/{total_trades})")
            print(f"成功标的: {sum(1 for r in results if r['total_ret'] > 0)}/{len(results)}")
            print(f"失败标的: {sum(1 for r in results if r['total_ret'] <= 0)}/{len(results)}")

            # 详细交易记录汇总
            print("\n" + "=" * 80)
            print("详细交易记录汇总")
            print("=" * 80)
            for r in results:
                symbol_short = r["symbol"].split(".")[0]
                print(f"\n【{symbol_short} ({r['symbol']})】")
                print("-" * 80)
                if r["trades"]:
                    print(f"{'日期':<12} {'操作':<6} {'价格':<10} {'盈亏':<10}")
                    print("-" * 80)
                    buy_price = None
                    for ts, side, px in r["trades"]:
                        if side == "BUY":
                            buy_price = px
                            print(f"{ts.date()} {side:<6} {px:>8.2f}")
                        elif side == "SELL" and buy_price is not None:
                            pnl = px - buy_price
                            pnl_pct = (pnl / buy_price) * 100
                            pnl_str = f"{pnl:+.2f} ({pnl_pct:+.2f}%)"
                            print(f"{ts.date()} {side:<6} {px:>8.2f} {pnl_str:>15}")
                            buy_price = None
                        else:
                            print(f"{ts.date()} {side:<6} {px:>8.2f}")
                else:
                    print("无交易记录")
        else:
            print("\n所有标的回测均失败，请检查数据权限或代码。")
    except Exception as e:
        print(f"批量回测出错: {e}")
    finally:
        logout()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="放量突破前高 + 内外包线回测（JQData）",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("--symbol", default=None, help="单个标的代码，例如 000001.XSHE（与--symbols二选一）")
    parser.add_argument("--symbols", default=None, help="多个标的代码，逗号分隔，最多10个，例如 '000001.XSHE,600000.XSHG'（与--symbol二选一）")
    parser.add_argument("--username", default=os.getenv("JQ_USERNAME", "18813098345"), help="JQData 账号，默认取环境变量 JQ_USERNAME")
    parser.add_argument("--password", default=os.getenv("JQ_PASSWORD", "Shitou+6819815"), help="JQData 密码，默认取环境变量 JQ_PASSWORD")
    parser.add_argument("--start-date", type=parse_date, default=None, help="回测开始日期，格式 YYYY-MM-DD；不填则默认向前15个月")
    parser.add_argument("--end-date", type=parse_date, default=None, help="回测结束日期，格式 YYYY-MM-DD；不填则默认向前3个月")
    parser.add_argument("--high-lookback", type=int, default=20, help="前高回看周期（天数），默认20天")
    parser.add_argument("--trend-ma", type=int, default=20, help="趋势过滤均线周期，设为0关闭，默认20")
    parser.add_argument("--vol-lookback", type=int, default=10, help="量能均线回看周期，默认10")
    parser.add_argument("--vol-mult", type=float, default=1.0, help="量能倍数，默认1.0（要求成交量>=均值），设为0关闭")
    parser.add_argument("--atr-lookback", type=int, default=14, help="ATR计算周期，默认14")
    parser.add_argument("--atr-mult", type=float, default=2.0, help="ATR止损倍数，默认2.0，设为9999关闭")
    parser.add_argument("--simple-stop-pct", type=float, default=None, help="简化移动止损百分比（如5表示5%%），设置后使用简化版，忽略ATR止损")
    parser.add_argument("--max-hold-days", type=int, default=None, help="最长持仓天数，默认None（不限制）")
    parser.add_argument("--disable-break-stop", action="store_true", help="关闭跌破前日K线新低止损，仅使用移动止损")
    parser.add_argument("--fee-rate", type=float, default=0.0005, help="单边手续费率，默认0.0005（万5）")
    parser.add_argument("--slippage-bp", type=float, default=1.0, help="滑点（基点），默认1.0（1bp=0.01%%）")
    args = parser.parse_args()

    # 基本校验：开始 < 结束
    if args.start_date and args.end_date and args.start_date >= args.end_date:
        parser.error("开始日期需早于结束日期")

    # 确定标的列表
    if args.symbols:
        # 批量回测模式
        symbols = [s.strip() for s in args.symbols.split(",") if s.strip()]
        if not symbols:
            parser.error("--symbols 参数不能为空")
        if len(symbols) > 10:
            parser.error(f"最多支持10个标的，当前提供 {len(symbols)} 个")
        run_batch_backtest(
            symbols=symbols,
            username=args.username,
            password=args.password,
            start_date=args.start_date,
            end_date=args.end_date,
            high_lookback=args.high_lookback,
            trend_ma=args.trend_ma if args.trend_ma > 0 else None,
            vol_lookback=args.vol_lookback,
            vol_mult=args.vol_mult if args.vol_mult > 0 else 0,
            atr_lookback=args.atr_lookback,
            atr_mult=args.atr_mult,
            simple_stop_pct=args.simple_stop_pct,
            max_hold_days=args.max_hold_days,
            disable_break_stop=args.disable_break_stop,
            fee_rate=args.fee_rate,
            slippage_bp=args.slippage_bp,
        )
    else:
        # 单个回测模式
        symbol = args.symbol or os.getenv("JQ_SYMBOL", "000001.XSHE")
        run_backtest(
            symbol=symbol,
            username=args.username,
            password=args.password,
            start_date=args.start_date,
            end_date=args.end_date,
            high_lookback=args.high_lookback,
            trend_ma=args.trend_ma if args.trend_ma > 0 else None,
            vol_lookback=args.vol_lookback,
            vol_mult=args.vol_mult if args.vol_mult > 0 else 0,
            atr_lookback=args.atr_lookback,
            atr_mult=args.atr_mult,
            simple_stop_pct=args.simple_stop_pct,
            max_hold_days=args.max_hold_days,
            disable_break_stop=args.disable_break_stop,
            fee_rate=args.fee_rate,
            slippage_bp=args.slippage_bp,
        )

