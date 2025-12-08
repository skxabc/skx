#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国平安量化策略回测系统（可视化版）
"""

import pandas as pd
import numpy as np
import akshare as ak
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

try:
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    from matplotlib.patches import Rectangle
    plt.rcParams['font.sans-serif'] = ['Arial Unicode MS', 'SimHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    HAS_PLOT = True
except ImportError:
    HAS_PLOT = False
    print("请先安装matplotlib: pip install matplotlib")


class KlineProcessor:
    """K线包含处理类"""
    
    def __init__(self):
        self.klines = []
        self.ignored_indices = set()
    
    def add_kline(self, date, high, low, open_price, close):
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
    """交易策略类"""
    
    def __init__(self, verbose=False):
        self.processor = KlineProcessor()
        self.holding = False
        self.entry_price = 0
        self.trades = []
        self.verbose = verbose
        self.equity_curve = [100]  # 初始资金100
        self.dates = []
    
    def add_kline(self, date, high, low, open_price, close):
        self.processor.add_kline(date, high, low, open_price, close)
        self.execute_strategy(date, close)
    
    def execute_strategy(self, date, close):
        # 先更新日期和权益曲线
        if len(self.dates) == 0:
            self.dates.append(date)
            self.equity_curve.append(100)
        else:
            self.dates.append(date)
            # 更新权益曲线
            if self.holding:
                current_return = ((close - self.entry_price) / self.entry_price) * 100
                self.equity_curve.append(self.equity_curve[-1] * (1 + current_return / 100))
            else:
                self.equity_curve.append(self.equity_curve[-1])
        
        valid_klines = self.processor.get_valid_klines()
        
        if len(valid_klines) < 2:
            return
        
        current = valid_klines[-1]
        previous = valid_klines[-2]
        
        # 买入信号
        if current['high'] > previous['high']:
            if not self.holding:
                self.holding = True
                self.entry_price = current['high']
                self.trades.append({
                    'date': current['date'],
                    'action': 'BUY',
                    'price': self.entry_price,
                    'reason': f"高点突破"
                })
        
        # 卖出信号
        if self.holding and current['low'] < previous['low']:
            exit_price = current['low']
            profit_pct = ((exit_price - self.entry_price) / self.entry_price) * 100
            # 更新权益曲线（使用卖出价格）
            if len(self.equity_curve) > 0:
                self.equity_curve[-1] = self.equity_curve[-1] * (1 + profit_pct / 100)
            
            self.holding = False
            self.trades.append({
                'date': current['date'],
                'action': 'SELL',
                'price': exit_price,
                'entry_price': self.entry_price,
                'profit': profit_pct,
                'reason': f"跌破前低"
            })
            self.entry_price = 0
    
    def get_statistics(self):
        if not self.trades:
            return {}
        
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
            return {}
        
        profits = [t['profit'] for t in paired_trades]
        win_trades = [p for p in profits if p > 0]
        
        return {
            'total_trades': len(paired_trades),
            'win_trades': len(win_trades),
            'loss_trades': len(paired_trades) - len(win_trades),
            'win_rate': len(win_trades) / len(paired_trades) * 100 if paired_trades else 0,
            'total_return': sum(profits),
            'avg_profit': np.mean(profits) if profits else 0,
            'max_profit': max(profits) if profits else 0,
            'max_loss': min(profits) if profits else 0,
            'paired_trades': paired_trades,
            'final_equity': self.equity_curve[-1]
        }


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


def fetch_stock_data(symbol='601318', start_date='20230101'):
    """获取股票数据"""
    try:
        df = ak.stock_zh_a_hist(symbol=symbol, period="daily", start_date=start_date, 
                                end_date=None, adjust="qfq")
        if df.empty:
            return None
        
        if '日期' in df.columns:
            df = df.rename(columns={'日期': 'date'})
        if len(df.columns) >= 5:
            df.columns = ['date', 'open', 'close', 'high', 'low'] + list(df.columns[5:])
        
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        for col in ['open', 'close', 'high', 'low']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df = df.dropna(subset=['open', 'close', 'high', 'low'])
        df = df.sort_values('date').reset_index(drop=True)
        return df
    except:
        return None


def plot_strategy_results(df, strategy):
    """绘制策略结果"""
    if not HAS_PLOT:
        print("无法绘图：matplotlib未安装")
        return
    
    fig = plt.figure(figsize=(16, 12))
    
    # 准备数据
    dates = pd.to_datetime(df['date'])
    valid_klines = strategy.processor.get_valid_klines()
    valid_dates = [pd.to_datetime(k['date']) for k in valid_klines]
    valid_highs = [k['high'] for k in valid_klines]
    valid_lows = [k['low'] for k in valid_klines]
    valid_closes = [k['close'] for k in valid_klines]
    
    # 获取交易信号
    buy_signals = [t for t in strategy.trades if t['action'] == 'BUY']
    sell_signals = [t for t in strategy.trades if t['action'] == 'SELL']
    buy_dates = [pd.to_datetime(t['date']) for t in buy_signals]
    buy_prices = [t['price'] for t in buy_signals]
    sell_dates = [pd.to_datetime(t['date']) for t in sell_signals]
    sell_prices = [t['price'] for t in sell_signals]
    
    # 子图1：K线图和交易信号
    ax1 = plt.subplot(3, 1, 1)
    
    # 绘制有效K线
    ax1.plot(valid_dates, valid_closes, 'b-', linewidth=1.5, label='收盘价', alpha=0.7)
    ax1.fill_between(valid_dates, valid_lows, valid_highs, alpha=0.2, color='blue', label='价格区间')
    
    # 绘制所有K线（灰色，被忽略的）
    ax1.plot(dates, df['close'], 'gray', linewidth=0.5, alpha=0.3, label='原始K线（部分被忽略）')
    
    # 买入信号
    if buy_dates:
        ax1.scatter(buy_dates, buy_prices, color='green', marker='^', s=150, 
                   zorder=5, label='买入信号', edgecolors='darkgreen', linewidths=2)
    
    # 卖出信号
    if sell_dates:
        ax1.scatter(sell_dates, sell_prices, color='red', marker='v', s=150, 
                   zorder=5, label='卖出信号', edgecolors='darkred', linewidths=2)
    
    ax1.set_title('中国平安量化策略 - K线图与交易信号', fontsize=14, fontweight='bold')
    ax1.set_ylabel('价格 (元)', fontsize=12)
    ax1.legend(loc='upper left', fontsize=10)
    ax1.grid(True, alpha=0.3)
    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax1.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    
    # 子图2：权益曲线
    ax2 = plt.subplot(3, 1, 2)
    # 确保日期和权益曲线长度一致
    equity_dates = pd.to_datetime(strategy.dates[:len(strategy.equity_curve)])
    equity_values = strategy.equity_curve[:len(equity_dates)]
    ax2.plot(equity_dates, equity_values, 'g-', linewidth=2, label='策略权益曲线')
    ax2.axhline(y=100, color='gray', linestyle='--', linewidth=1, label='初始资金')
    
    # 标注最终收益
    final_return = (strategy.equity_curve[-1] - 100) / 100 * 100
    ax2.text(0.02, 0.98, f'最终收益率: {final_return:.2f}%', 
             transform=ax2.transAxes, fontsize=12, fontweight='bold',
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    ax2.set_title('策略权益曲线', fontsize=14, fontweight='bold')
    ax2.set_ylabel('权益 (初始=100)', fontsize=12)
    ax2.legend(loc='upper left', fontsize=10)
    ax2.grid(True, alpha=0.3)
    ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
    ax2.xaxis.set_major_locator(mdates.MonthLocator(interval=2))
    
    # 子图3：交易收益分布
    ax3 = plt.subplot(3, 1, 3)
    stats = strategy.get_statistics()
    if stats and 'paired_trades' in stats:
        profits = [t['profit'] for t in stats['paired_trades']]
        colors = ['green' if p > 0 else 'red' for p in profits]
        bars = ax3.bar(range(len(profits)), profits, color=colors, alpha=0.7, edgecolor='black')
        
        # 标注数值
        for i, (bar, profit) in enumerate(zip(bars, profits)):
            height = bar.get_height()
            ax3.text(bar.get_x() + bar.get_width()/2., height,
                    f'{profit:.1f}%', ha='center', va='bottom' if height > 0 else 'top',
                    fontsize=9, fontweight='bold')
        
        ax3.axhline(y=0, color='black', linestyle='-', linewidth=1)
        ax3.set_title('单笔交易收益率分布', fontsize=14, fontweight='bold')
        ax3.set_xlabel('交易序号', fontsize=12)
        ax3.set_ylabel('收益率 (%)', fontsize=12)
        ax3.grid(True, alpha=0.3, axis='y')
    
    plt.tight_layout()
    
    # 保存图片
    output_file = '/Users/user/Downloads/strategy_visualization.png'
    plt.savefig(output_file, dpi=300, bbox_inches='tight')
    print(f"\n图表已保存到: {output_file}")
    
    # 显示图表
    plt.show()


def main():
    print("="*60)
    print("中国平安量化策略回测系统（可视化版）")
    print("="*60)
    
    # 获取数据
    print("\n正在获取数据...")
    df = fetch_stock_data(symbol='601318', start_date='20230101')
    
    if df is None or df.empty:
        print("使用模拟数据进行演示...")
        df = generate_mock_data()
    
    print(f"数据准备完成: {len(df)} 条记录")
    
    # 回测策略
    print("\n开始回测策略...")
    strategy = TradingStrategy(verbose=False)
    
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
            'reason': '回测结束'
        })
        strategy.holding = False
    
    # 打印统计
    stats = strategy.get_statistics()
    if stats:
        print("\n" + "="*60)
        print("回测结果统计")
        print("="*60)
        print(f"总交易次数: {stats['total_trades']} 次")
        print(f"盈利次数: {stats['win_trades']} 次")
        print(f"亏损次数: {stats['loss_trades']} 次")
        print(f"胜率: {stats['win_rate']:.2f}%")
        print(f"总收益率: {stats['total_return']:.2f}%")
        print(f"最终权益: {stats['final_equity']:.2f} (初始=100)")
        print("="*60)
    
    # 绘制图表
    if HAS_PLOT:
        print("\n正在生成可视化图表...")
        plot_strategy_results(df, strategy)
    else:
        print("\n无法生成图表，请安装matplotlib")


if __name__ == '__main__':
    main()

