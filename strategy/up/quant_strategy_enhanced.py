#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国平安量化策略回测系统（增强版）
策略规则：
1. 高点越来越高就持有
2. 跌破前一日低点就清仓
3. K线包含处理：被包含的K线忽略，后续判断不考虑忽略的K线
"""

import pandas as pd
import numpy as np
import akshare as ak
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# 尝试导入matplotlib用于可视化（可选）
try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    HAS_PLOT = True
except ImportError:
    HAS_PLOT = False
    print("提示: 安装 matplotlib 可以查看可视化图表: pip install matplotlib")


class KlineProcessor:
    """K线包含处理类"""
    
    def __init__(self):
        self.klines = []
        self.ignored_indices = set()
    
    def add_kline(self, date, high, low, open_price, close):
        """添加K线数据"""
        kline = {
            'date': date,
            'high': float(high),
            'low': float(low),
            'open': float(open_price),
            'close': float(close),
            'ignored': False
        }
        self.klines.append(kline)
        self.process_containment()
    
    def is_contained(self, k1, k2):
        """判断K线是否包含关系"""
        return (k1['high'] <= k2['high'] and k1['low'] >= k2['low']) or \
               (k1['high'] >= k2['high'] and k1['low'] <= k2['low'])
    
    def find_prev_valid_kline(self, current_index):
        """找到前一根有效的K线"""
        for i in range(current_index - 1, -1, -1):
            if i not in self.ignored_indices:
                return i
        return -1
    
    def process_containment(self, verbose=False):
        """处理K线包含关系"""
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
                        if verbose:
                            print(f"  K线 {current['date']} 被前一根包含，已忽略")
                    else:
                        self.ignored_indices.add(prev_index)
                        if verbose:
                            print(f"  前一根K线 {previous['date']} 被当前K线包含，已忽略")
                    processed = True
                    break
    
    def get_valid_klines(self):
        """获取所有有效的K线"""
        return [kline for i, kline in enumerate(self.klines) if i not in self.ignored_indices]


class TradingStrategy:
    """交易策略类"""
    
    def __init__(self, verbose=True):
        self.processor = KlineProcessor()
        self.holding = False
        self.entry_price = 0
        self.trades = []
        self.verbose = verbose
    
    def add_kline(self, date, high, low, open_price, close):
        """添加K线并执行策略"""
        self.processor.add_kline(date, high, low, open_price, close)
        self.execute_strategy()
    
    def execute_strategy(self):
        """执行交易策略"""
        valid_klines = self.processor.get_valid_klines()
        
        if len(valid_klines) < 2:
            return
        
        current = valid_klines[-1]
        previous = valid_klines[-2]
        
        # 策略1：高点越来越高就持有
        if current['high'] > previous['high']:
            if not self.holding:
                self.holding = True
                self.entry_price = current['high']
                self.trades.append({
                    'date': current['date'],
                    'action': 'BUY',
                    'price': self.entry_price,
                    'reason': f"高点突破: {current['high']:.2f} > {previous['high']:.2f}"
                })
                if self.verbose:
                    print(f"  [{current['date']}] 买入 @ {self.entry_price:.2f} - {self.trades[-1]['reason']}")
        
        # 策略2：跌破前一日低点就清仓
        if self.holding and current['low'] < previous['low']:
            exit_price = current['low']
            profit = ((exit_price - self.entry_price) / self.entry_price) * 100
            self.holding = False
            self.trades.append({
                'date': current['date'],
                'action': 'SELL',
                'price': exit_price,
                'entry_price': self.entry_price,
                'profit': profit,
                'reason': f"跌破前低: {current['low']:.2f} < {previous['low']:.2f}"
            })
            if self.verbose:
                print(f"  [{current['date']}] 卖出 @ {exit_price:.2f} - 收益率: {profit:.2f}% - {self.trades[-1]['reason']}")
            self.entry_price = 0
    
    def get_statistics(self):
        """获取策略统计信息"""
        if not self.trades:
            return {
                'total_trades': 0,
                'win_trades': 0,
                'loss_trades': 0,
                'win_rate': 0,
                'total_return': 0,
                'avg_profit': 0,
                'max_profit': 0,
                'max_loss': 0,
                'paired_trades': []
            }
        
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
                paired_trades.append({
                    'buy': buy_trades[buy_idx],
                    'sell': sell_trades[sell_idx],
                    'profit': sell_trades[sell_idx]['profit']
                })
                buy_idx += 1
                sell_idx += 1
            else:
                sell_idx += 1
        
        if not paired_trades:
            return {
                'total_trades': 0,
                'win_trades': 0,
                'loss_trades': 0,
                'win_rate': 0,
                'total_return': 0,
                'avg_profit': 0,
                'max_profit': 0,
                'max_loss': 0,
                'paired_trades': []
            }
        
        profits = [t['profit'] for t in paired_trades]
        win_trades = [p for p in profits if p > 0]
        loss_trades = [p for p in profits if p <= 0]
        
        return {
            'total_trades': len(paired_trades),
            'win_trades': len(win_trades),
            'loss_trades': len(loss_trades),
            'win_rate': len(win_trades) / len(paired_trades) * 100 if paired_trades else 0,
            'total_return': sum(profits),
            'avg_profit': np.mean(profits) if profits else 0,
            'max_profit': max(profits) if profits else 0,
            'max_loss': min(profits) if profits else 0,
            'paired_trades': paired_trades
        }


def fetch_stock_data_akshare(symbol='601318', start_date='20230101', end_date=None):
    """使用akshare获取股票数据"""
    try:
        df = ak.stock_zh_a_hist(symbol=symbol, period="daily", start_date=start_date, 
                                end_date=end_date, adjust="qfq")
        if df.empty:
            return None
        
        # 处理列名
        if '日期' in df.columns:
            df = df.rename(columns={'日期': 'date'})
        if 'date' not in df.columns and len(df.columns) > 0:
            df.columns.values[0] = 'date'
        
        # 标准化列名
        column_map = {
            '开盘': 'open', '收盘': 'close', '最高': 'high', '最低': 'low', '成交量': 'volume',
            'Open': 'open', 'Close': 'close', 'High': 'high', 'Low': 'low'
        }
        for old, new in column_map.items():
            if old in df.columns:
                df = df.rename(columns={old: new})
        
        # 确保有必要的列
        required_cols = ['date', 'open', 'close', 'high', 'low']
        if not all(col in df.columns for col in required_cols):
            # 尝试使用位置索引
            if len(df.columns) >= 5:
                df.columns = ['date', 'open', 'close', 'high', 'low'] + list(df.columns[5:])
        
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        for col in ['open', 'close', 'high', 'low']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df = df.dropna(subset=['open', 'close', 'high', 'low'])
        df = df.sort_values('date').reset_index(drop=True)
        
        return df
    except Exception as e:
        print(f"  akshare获取失败: {e}")
        return None


def generate_mock_data():
    """生成模拟数据"""
    dates = pd.date_range(start='2023-01-01', end='2024-12-31', freq='D')
    dates = [d for d in dates if d.weekday() < 5]
    
    np.random.seed(42)
    base_price = 50.0
    data = []
    
    for i, date in enumerate(dates[:252]):
        trend = np.sin(i * 0.1) * 2
        volatility = np.random.rand() * 3
        open_price = base_price + trend + (np.random.rand() - 0.5) * volatility
        close = open_price + (np.random.rand() - 0.5) * volatility
        high = max(open_price, close) + np.random.rand() * volatility
        low = min(open_price, close) - np.random.rand() * volatility
        
        data.append({
            'date': date.strftime('%Y-%m-%d'),
            'open': round(open_price, 2),
            'close': round(close, 2),
            'high': round(high, 2),
            'low': round(low, 2),
            'volume': int(np.random.rand() * 1000000)
        })
        
        base_price = close
    
    return pd.DataFrame(data)


def backtest_strategy(df, verbose=True):
    """回测策略"""
    if verbose:
        print("\n" + "="*60)
        print("开始回测策略...")
        print("="*60)
    
    strategy = TradingStrategy(verbose=verbose)
    
    for idx, row in df.iterrows():
        strategy.add_kline(
            date=row['date'],
            high=row['high'],
            low=row['low'],
            open_price=row['open'],
            close=row['close']
        )
    
    # 强制平仓
    if strategy.holding:
        last_kline = strategy.processor.get_valid_klines()[-1]
        exit_price = last_kline['close']
        profit = ((exit_price - strategy.entry_price) / strategy.entry_price) * 100
        strategy.trades.append({
            'date': last_kline['date'],
            'action': 'SELL',
            'price': exit_price,
            'entry_price': strategy.entry_price,
            'profit': profit,
            'reason': '回测结束，强制平仓'
        })
        if verbose:
            print(f"\n  [{last_kline['date']}] 回测结束，强制平仓 @ {exit_price:.2f} - 收益率: {profit:.2f}%")
        strategy.holding = False
    
    return strategy


def print_results(strategy, df):
    """打印回测结果"""
    stats = strategy.get_statistics()
    
    print("\n" + "="*60)
    print("回测结果统计")
    print("="*60)
    print(f"回测期间: {df['date'].min()} 至 {df['date'].max()}")
    print(f"总交易日: {len(df)} 天")
    print(f"有效K线数: {len(strategy.processor.get_valid_klines())} 根")
    print(f"忽略K线数: {len(strategy.processor.ignored_indices)} 根")
    print(f"\n交易统计:")
    print(f"  总交易次数: {stats['total_trades']} 次")
    print(f"  盈利次数: {stats['win_trades']} 次")
    print(f"  亏损次数: {stats['loss_trades']} 次")
    print(f"  胜率: {stats['win_rate']:.2f}%")
    print(f"  总收益率: {stats['total_return']:.2f}%")
    print(f"  平均收益率: {stats['avg_profit']:.2f}%")
    print(f"  最大单笔盈利: {stats['max_profit']:.2f}%")
    print(f"  最大单笔亏损: {stats['max_loss']:.2f}%")
    
    if stats['paired_trades']:
        print(f"\n交易明细 (前10笔):")
        for i, trade in enumerate(stats['paired_trades'][:10], 1):
            print(f"  交易 {i}:")
            print(f"    买入: {trade['buy']['date']} @ {trade['buy']['price']:.2f}")
            print(f"    卖出: {trade['sell']['date']} @ {trade['sell']['price']:.2f}")
            print(f"    收益率: {trade['profit']:.2f}%")
        
        if len(stats['paired_trades']) > 10:
            print(f"  ... (还有 {len(stats['paired_trades']) - 10} 笔交易)")
    
    print("\n" + "="*60)


def main():
    """主函数"""
    print("="*60)
    print("中国平安量化策略回测系统（增强版）")
    print("="*60)
    
    # 获取数据
    print("\n正在获取 601318 (中国平安) 的历史数据...")
    df = fetch_stock_data_akshare(symbol='601318', start_date='20230101')
    
    if df is None or df.empty:
        print("无法从网络获取数据，使用模拟数据进行演示...")
        df = generate_mock_data()
        print(f"生成 {len(df)} 条模拟数据")
    else:
        print(f"成功获取 {len(df)} 条数据，日期范围: {df['date'].min()} 至 {df['date'].max()}")
    
    # 回测策略
    strategy = backtest_strategy(df, verbose=False)  # 设置为False可以减少输出
    
    # 打印结果
    print_results(strategy, df)
    
    # 保存结果
    if strategy.trades:
        trades_df = pd.DataFrame(strategy.trades)
        output_file = '/Users/user/Downloads/trading_results.csv'
        trades_df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"\n交易记录已保存到: {output_file}")


if __name__ == '__main__':
    main()

