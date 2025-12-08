#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中国平安量化策略回测系统
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


class KlineProcessor:
    """K线包含处理类"""
    
    def __init__(self):
        self.klines = []
        self.ignored_indices = set()  # 被忽略的K线索引
    
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
        """判断K线是否包含关系
        k1被k2包含：k1.high <= k2.high and k1.low >= k2.low
        k2被k1包含：k1.high >= k2.high and k1.low <= k2.low
        """
        return (k1['high'] <= k2['high'] and k1['low'] >= k2['low']) or \
               (k1['high'] >= k2['high'] and k1['low'] <= k2['low'])
    
    def find_prev_valid_kline(self, current_index):
        """找到前一根有效的（未被忽略的）K线"""
        for i in range(current_index - 1, -1, -1):
            if i not in self.ignored_indices:
                return i
        return -1
    
    def process_containment(self):
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
                    # 判断谁包含谁
                    if current['high'] <= previous['high'] and current['low'] >= previous['low']:
                        # 当前K线被前一根包含，忽略当前K线
                        self.ignored_indices.add(i)
                        print(f"  K线 {current['date']} 被前一根包含，已忽略")
                    else:
                        # 前一根K线被当前K线包含，忽略前一根
                        self.ignored_indices.add(prev_index)
                        print(f"  前一根K线 {previous['date']} 被当前K线包含，已忽略")
                    processed = True
                    break
    
    def get_valid_klines(self):
        """获取所有有效的（未被忽略的）K线"""
        return [kline for i, kline in enumerate(self.klines) if i not in self.ignored_indices]


class TradingStrategy:
    """交易策略类"""
    
    def __init__(self):
        self.processor = KlineProcessor()
        self.holding = False  # 是否持仓
        self.entry_price = 0  # 入场价格
        self.trades = []  # 交易记录
        self.equity_curve = []  # 权益曲线
    
    def add_kline(self, date, high, low, open_price, close):
        """添加K线并执行策略"""
        self.processor.add_kline(date, high, low, open_price, close)
        self.execute_strategy()
    
    def execute_strategy(self):
        """执行交易策略"""
        valid_klines = self.processor.get_valid_klines()
        
        if len(valid_klines) < 2:
            return
        
        # 获取最后两根有效K线
        current = valid_klines[-1]
        previous = valid_klines[-2]
        
        # 策略1：如果高点越来越高就持有
        if current['high'] > previous['high']:
            if not self.holding:
                # 买入
                self.holding = True
                self.entry_price = current['high']
                self.trades.append({
                    'date': current['date'],
                    'action': 'BUY',
                    'price': self.entry_price,
                    'reason': f"高点突破: {current['high']:.2f} > {previous['high']:.2f}"
                })
                print(f"  [{current['date']}] 买入 @ {self.entry_price:.2f} - {self.trades[-1]['reason']}")
        
        # 策略2：如果跌破前一日低点就清仓
        if self.holding and current['low'] < previous['low']:
            # 卖出
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
                'max_loss': 0
            }
        
        # 计算买卖配对
        buy_trades = [t for t in self.trades if t['action'] == 'BUY']
        sell_trades = [t for t in self.trades if t['action'] == 'SELL']
        
        # 配对交易
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
                'max_loss': 0
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


def fetch_stock_data(symbol='601318', start_date='20230101', end_date=None):
    """获取股票历史数据"""
    print(f"正在获取 {symbol} (中国平安) 的历史数据...")
    
    try:
        # 中国平安的代码是 601318（上交所）
        # 尝试多种方法获取数据
        df = None
        
        # 方法1：使用akshare获取
        try:
            df = ak.stock_zh_a_hist(symbol=symbol, period="daily", start_date=start_date, 
                                    end_date=end_date, adjust="qfq")
            if not df.empty:
                # 重命名列（根据akshare返回的实际列名）
                if len(df.columns) >= 6:
                    df = df.iloc[:, :6]  # 只取前6列
                    df.columns = ['date', 'open', 'close', 'high', 'low', 'volume']
        except Exception as e1:
            print(f"  方法1失败: {e1}")
        
        # 方法2：如果方法1失败，尝试使用股票代码映射
        if df is None or df.empty:
            try:
                # 尝试使用股票名称
                df = ak.stock_zh_a_hist(symbol=symbol, period="daily", start_date=start_date, 
                                        end_date=end_date, adjust="")
            except Exception as e2:
                print(f"  方法2失败: {e2}")
        
        if df is None or df.empty:
            print("  无法从网络获取数据，使用模拟数据进行演示...")
            return generate_mock_data()
        
        # 确保日期格式正确
        if 'date' in df.columns:
            df['date'] = pd.to_datetime(df['date']).dt.strftime('%Y-%m-%d')
        elif '日期' in df.columns:
            df['date'] = pd.to_datetime(df['日期']).dt.strftime('%Y-%m-%d')
            df = df.rename(columns={'日期': 'date'})
        
        # 确保列名正确
        column_mapping = {
            '开盘': 'open', '收盘': 'close', '最高': 'high', '最低': 'low', '成交量': 'volume',
            'Open': 'open', 'Close': 'close', 'High': 'high', 'Low': 'low', 'Volume': 'volume'
        }
        for old_col, new_col in column_mapping.items():
            if old_col in df.columns:
                df = df.rename(columns={old_col: new_col})
        
        # 按日期排序
        df = df.sort_values('date').reset_index(drop=True)
        
        # 确保数据类型正确
        for col in ['open', 'close', 'high', 'low']:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        # 删除缺失值
        df = df.dropna(subset=['open', 'close', 'high', 'low'])
        
        print(f"  成功获取 {len(df)} 条数据，日期范围: {df['date'].min()} 至 {df['date'].max()}")
        return df
    
    except Exception as e:
        print(f"  获取数据失败: {e}")
        print("  使用模拟数据进行演示...")
        return generate_mock_data()


def generate_mock_data():
    """生成模拟数据用于测试"""
    dates = pd.date_range(start='2023-01-01', end='2024-12-31', freq='D')
    dates = [d for d in dates if d.weekday() < 5]  # 只保留工作日
    
    np.random.seed(42)
    base_price = 50.0
    data = []
    
    for i, date in enumerate(dates[:252]):  # 约一年的交易日
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
    
    df = pd.DataFrame(data)
    print(f"生成 {len(df)} 条模拟数据")
    return df


def backtest_strategy(df):
    """回测策略"""
    print("\n" + "="*60)
    print("开始回测策略...")
    print("="*60)
    
    strategy = TradingStrategy()
    
    # 逐日处理K线
    for idx, row in df.iterrows():
        strategy.add_kline(
            date=row['date'],
            high=row['high'],
            low=row['low'],
            open_price=row['open'],
            close=row['close']
        )
    
    # 如果最后还持仓，以最后收盘价卖出
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
        print(f"\n交易明细:")
        for i, trade in enumerate(stats['paired_trades'][:10], 1):  # 只显示前10笔
            print(f"  交易 {i}:")
            print(f"    买入: {trade['buy']['date']} @ {trade['buy']['price']:.2f}")
            print(f"    卖出: {trade['sell']['date']} @ {trade['sell']['price']:.2f}")
            print(f"    收益率: {trade['profit']:.2f}%")
            print(f"    原因: {trade['buy']['reason']} -> {trade['sell']['reason']}")
        
        if len(stats['paired_trades']) > 10:
            print(f"  ... (还有 {len(stats['paired_trades']) - 10} 笔交易)")
    
    print("\n" + "="*60)


def main():
    """主函数"""
    print("="*60)
    print("中国平安量化策略回测系统")
    print("="*60)
    
    # 获取数据 - 中国平安代码 601318
    df = fetch_stock_data(symbol='601318', start_date='20230101')
    
    if df is None or df.empty:
        print("无法获取数据，程序退出")
        return
    
    # 回测策略
    strategy = backtest_strategy(df)
    
    # 打印结果
    print_results(strategy, df)
    
    # 保存结果到CSV
    if strategy.trades:
        trades_df = pd.DataFrame(strategy.trades)
        output_file = '/Users/user/Downloads/trading_results.csv'
        trades_df.to_csv(output_file, index=False, encoding='utf-8-sig')
        print(f"\n交易记录已保存到: {output_file}")


if __name__ == '__main__':
    main()

