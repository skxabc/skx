#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
从已获取的完整数据中筛选过去一年进行回测
由于网络问题，使用之前成功获取的数据重新计算过去一年的表现
"""

import pandas as pd
import numpy as np
import akshare as ak
import time
import warnings
warnings.filterwarnings('ignore')

HK_STOCKS = {
    '德林控股': '01709',
    '趣志集团': '01691',
    '中国光大控股': '00165',
    '国泰君安国际': '01788',
    '众安在线': '06060',
    '瑞声科技': '02018',
    '小米集团': '01810',
    '李宁': '02331'
}


class KlineProcessor:
    def __init__(self):
        self.klines = []
        self.ignored_indices = set()
    
    def add_kline(self, date, high, low, open_price, close):
        kline = {'date': date, 'high': float(high), 'low': float(low), 
                'open': float(open_price), 'close': float(close), 'ignored': False}
        self.klines.append(kline)
        self.process_containment()
    
    def is_contained(self, k1, k2):
        return (k1['high'] <= k2['high'] and k1['low'] >= k2['low']) or \
               (k1['high'] >= k2['high'] and k1['low'] <= k2['low'])
    
    def find_prev_valid_kline(self, current_index):
        for i in range(current_index - 1, -1, -1):
            if i not in self.ignored_indices:
                return i
        return -1
    
    def process_containment(self):
        if len(self.klines) < 2:
            return
        processed = True
        while processed:
            processed = False
            for i in range(1, len(self.klines)):
                if i in self.ignored_indices:
                    continue
                prev_index = self.find_prev_valid_kline(i)
                if prev_index == -1:
                    continue
                current = self.klines[i]
                previous = self.klines[prev_index]
                if self.is_contained(current, previous):
                    if current['high'] <= previous['high'] and current['low'] >= previous['low']:
                        self.ignored_indices.add(i)
                    else:
                        self.ignored_indices.add(prev_index)
                    processed = True
                    break
    
    def get_valid_klines(self):
        return [kline for i, kline in enumerate(self.klines) if i not in self.ignored_indices]


class TradingStrategy:
    def __init__(self):
        self.processor = KlineProcessor()
        self.holding = False
        self.entry_price = 0
        self.trades = []
    
    def add_kline(self, date, high, low, open_price, close):
        self.processor.add_kline(date, high, low, open_price, close)
        self.execute_strategy()
    
    def execute_strategy(self):
        valid_klines = self.processor.get_valid_klines()
        if len(valid_klines) < 2:
            return
        current = valid_klines[-1]
        previous = valid_klines[-2]
        if current['high'] > previous['high']:
            if not self.holding:
                self.holding = True
                self.entry_price = current['high']
                self.trades.append({'date': current['date'], 'action': 'BUY', 'price': self.entry_price})
        if self.holding and current['low'] < previous['low']:
            exit_price = current['low']
            profit = ((exit_price - self.entry_price) / self.entry_price) * 100
            self.holding = False
            self.trades.append({'date': current['date'], 'action': 'SELL', 'price': exit_price,
                              'entry_price': self.entry_price, 'profit': profit})
            self.entry_price = 0
    
    def get_statistics(self):
        if not self.trades:
            return {'total_trades': 0, 'win_trades': 0, 'loss_trades': 0, 'win_rate': 0,
                   'total_return': 0, 'avg_profit': 0, 'max_profit': 0, 'max_loss': 0,
                   'valid_klines': len(self.processor.get_valid_klines()),
                   'ignored_klines': len(self.processor.ignored_indices)}
        buy_trades = [t for t in self.trades if t['action'] == 'BUY']
        sell_trades = [t for t in self.trades if t['action'] == 'SELL']
        paired_trades = []
        buy_idx = 0
        sell_idx = 0
        while buy_idx < len(buy_trades) and sell_idx < len(sell_trades):
            if buy_trades[buy_idx]['date'] < sell_trades[sell_idx]['date']:
                if buy_idx + 1 < len(buy_trades) and buy_trades[buy_idx + 1]['date'] < sell_trades[sell_idx]['date']:
                    buy_idx += 1
                    continue
                paired_trades.append({'buy': buy_trades[buy_idx], 'sell': sell_trades[sell_idx],
                                     'profit': sell_trades[sell_idx]['profit']})
                buy_idx += 1
                sell_idx += 1
            else:
                sell_idx += 1
        if not paired_trades:
            return {'total_trades': 0, 'win_trades': 0, 'loss_trades': 0, 'win_rate': 0,
                   'total_return': 0, 'avg_profit': 0, 'max_profit': 0, 'max_loss': 0,
                   'valid_klines': len(self.processor.get_valid_klines()),
                   'ignored_klines': len(self.processor.ignored_indices)}
        profits = [t['profit'] for t in paired_trades]
        win_trades = [p for p in profits if p > 0]
        return {'total_trades': len(paired_trades), 'win_trades': len(win_trades),
               'loss_trades': len(paired_trades) - len(win_trades),
               'win_rate': len(win_trades) / len(paired_trades) * 100 if paired_trades else 0,
               'total_return': sum(profits), 'avg_profit': np.mean(profits) if profits else 0,
               'max_profit': max(profits) if profits else 0, 'max_loss': min(profits) if profits else 0,
               'valid_klines': len(self.processor.get_valid_klines()),
               'ignored_klines': len(self.processor.ignored_indices), 'paired_trades': paired_trades}


def fetch_hk_data_with_retry(symbol, max_retries=3):
    """带重试的数据获取"""
    for attempt in range(max_retries):
        try:
            df = ak.stock_hk_hist(symbol=symbol, period="daily", start_date="20220101", adjust="qfq")
            if df is not None and not df.empty:
                return df
        except Exception as e:
            if attempt < max_retries - 1:
                time.sleep(2)  # 等待2秒后重试
                continue
            print(f"    获取失败 (尝试 {attempt+1}/{max_retries}): {e}")
    return None


def backtest_stock_1year(stock_name, symbol):
    """回测单只股票过去一年"""
    print(f"\n正在回测: {stock_name} ({symbol})")
    
    # 获取数据（带重试）
    df = fetch_hk_data_with_retry(symbol)
    
    if df is None or df.empty:
        print(f"  ❌ 无法获取数据")
        return None
    
    # 处理列名
    if '日期' in df.columns:
        df = df.rename(columns={'日期': 'date'})
    if len(df.columns) >= 5:
        df.columns = ['date', 'open', 'close', 'high', 'low'] + list(df.columns[5:])
    
    df['date'] = pd.to_datetime(df['date'])
    for col in ['open', 'close', 'high', 'low']:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna(subset=['open', 'close', 'high', 'low']).sort_values('date')
    
    # 筛选过去一年：2023-12-01 至 2024-12-01
    start_date = pd.to_datetime('2023-12-01')
    end_date = pd.to_datetime('2024-12-01')
    df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    
    if df.empty:
        print(f"  ❌ 筛选后无数据")
        return None
    
    df['date'] = df['date'].dt.strftime('%Y-%m-%d')
    print(f"  ✓ 获取到 {len(df)} 条数据，日期: {df['date'].min()} 至 {df['date'].max()}")
    
    # 回测
    strategy = TradingStrategy()
    for _, row in df.iterrows():
        strategy.add_kline(row['date'], row['high'], row['low'], row['open'], row['close'])
    
    # 强制平仓
    if strategy.holding:
        last_kline = strategy.processor.get_valid_klines()[-1]
        exit_price = last_kline['close']
        profit = ((exit_price - strategy.entry_price) / strategy.entry_price) * 100
        strategy.trades.append({'date': last_kline['date'], 'action': 'SELL', 'price': exit_price,
                              'entry_price': strategy.entry_price, 'profit': profit})
        strategy.holding = False
    
    stats = strategy.get_statistics()
    stats.update({'stock_name': stock_name, 'symbol': symbol,
                 'data_period': f"{df['date'].min()} 至 {df['date'].max()}", 'total_days': len(df)})
    return stats


def main():
    print("="*80)
    print("港股通股票批量回测 - 过去一年数据 (2023-12-01 至 2024-12-01)")
    print("="*80)
    
    results = []
    for stock_name, symbol in HK_STOCKS.items():
        stats = backtest_stock_1year(stock_name, symbol)
        if stats:
            results.append(stats)
        time.sleep(1)  # 避免请求过快
    
    if not results:
        print("\n❌ 没有成功回测任何股票")
        return
    
    # 生成报告
    print("\n" + "="*80)
    print("回测结果对比")
    print("="*80)
    
    df_results = pd.DataFrame([{
        '股票名称': r['stock_name'], '股票代码': r['symbol'], '数据期间': r['data_period'],
        '交易日数': r['total_days'], '有效K线': r['valid_klines'], '忽略K线': r['ignored_klines'],
        '交易次数': r['total_trades'], '盈利次数': r['win_trades'], '亏损次数': r['loss_trades'],
        '胜率(%)': f"{r['win_rate']:.2f}", '总收益率(%)': f"{r['total_return']:.2f}",
        '平均收益率(%)': f"{r['avg_profit']:.2f}", '最大盈利(%)': f"{r['max_profit']:.2f}",
        '最大亏损(%)': f"{r['max_loss']:.2f}"
    } for r in results])
    
    df_results['总收益率_数值'] = df_results['总收益率(%)'].str.replace('%', '').astype(float)
    df_results = df_results.sort_values('总收益率_数值', ascending=False).drop('总收益率_数值', axis=1)
    
    print("\n" + df_results.to_string(index=False))
    
    output_file = '/Users/user/Downloads/hk_stocks_backtest_1year_results.csv'
    df_results.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"\n✓ 结果已保存到: {output_file}")
    
    print("\n" + "="*80)
    print("收益率排名")
    print("="*80)
    for i, (_, row) in enumerate(df_results.iterrows(), 1):
        print(f"{i}. {row['股票名称']} ({row['股票代码']}): "
              f"总收益率 {row['总收益率(%)']}, 胜率 {row['胜率(%)']}%, 交易次数 {row['交易次数']}")
    
    print("\n" + "="*80)
    print("统计摘要")
    print("="*80)
    returns = df_results['总收益率(%)'].str.replace('%', '').astype(float)
    win_rates = df_results['胜率(%)'].str.replace('%', '').astype(float)
    print(f"成功回测股票数: {len(results)}")
    print(f"平均总收益率: {returns.mean():.2f}%")
    print(f"最高总收益率: {returns.max():.2f}%")
    print(f"最低总收益率: {returns.min():.2f}%")
    print(f"平均胜率: {win_rates.mean():.2f}%")
    print("="*80)


if __name__ == '__main__':
    main()

