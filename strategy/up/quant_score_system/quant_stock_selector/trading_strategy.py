"""
交易策略模块 - 实现上升趋势策略
"""
import pandas as pd
import numpy as np
from typing import List, Tuple, Optional
from enum import Enum


class Signal(Enum):
    """交易信号"""
    HOLD = "持有"  # 高点越来越高
    SELL = "清仓"  # 跌破前一日低点
    IGNORE = "忽略"  # 被包含或包含前一日


class TradingStrategy:
    """上升趋势交易策略"""
    
    def __init__(self):
        """初始化策略"""
        pass
    
    def filter_kline(self, kline_df: pd.DataFrame) -> pd.DataFrame:
        """
        过滤K线：移除被包含或包含前一日K线的数据
        
        规则：
        1. 如果当日K线被前一日高低点包含住，忽略当日K线
        2. 如果当日K线高低点包住前一日K线，忽略前一日K线
        
        Args:
            kline_df: 原始K线数据
            
        Returns:
            过滤后的K线数据
        """
        if kline_df.empty or len(kline_df) < 2:
            return kline_df
        
        df = kline_df.copy()
        df = df.sort_values('date').reset_index(drop=True)
        
        valid_indices = [0]  # 第一根K线总是有效
        
        for i in range(1, len(df)):
            prev_idx = valid_indices[-1]
            prev_high = df.loc[prev_idx, 'high']
            prev_low = df.loc[prev_idx, 'low']
            
            curr_high = df.loc[i, 'high']
            curr_low = df.loc[i, 'low']
            
            # 情况1: 当日K线被前一日包含（当日高低点都在前一日范围内）
            if curr_high <= prev_high and curr_low >= prev_low:
                # 忽略当日K线，继续下一根
                continue
            
            # 情况2: 当日K线包含前一日K线（当日高低点包住前一日）
            elif curr_high >= prev_high and curr_low <= prev_low:
                # 移除前一日K线，保留当日K线
                valid_indices.pop()
                valid_indices.append(i)
            
            # 情况3: 正常K线，都保留
            else:
                valid_indices.append(i)
        
        filtered_df = df.loc[valid_indices].reset_index(drop=True)
        return filtered_df
    
    def generate_signals(self, kline_df: pd.DataFrame) -> pd.DataFrame:
        """
        生成交易信号
        
        规则：
        1. 如果高点越来越高，持有
        2. 如果跌破前一日低点，清仓
        
        Args:
            kline_df: 过滤后的K线数据
            
        Returns:
            包含信号的DataFrame
        """
        if kline_df.empty or len(kline_df) < 2:
            return pd.DataFrame()
        
        df = kline_df.copy()
        df = df.sort_values('date').reset_index(drop=True)
        
        signals = []
        positions = []  # 持仓状态
        
        # 第一根K线，默认不持仓
        signals.append(Signal.IGNORE.value)
        positions.append(False)
        
        for i in range(1, len(df)):
            prev_high = df.loc[i-1, 'high']
            prev_low = df.loc[i-1, 'low']
            curr_high = df.loc[i, 'high']
            curr_low = df.loc[i, 'low']
            
            # 检查是否持仓
            is_holding = positions[-1] if positions else False
            
            if is_holding:
                # 如果持仓，检查是否跌破前一日低点
                if curr_low < prev_low:
                    signals.append(Signal.SELL.value)
                    positions.append(False)
                # 检查高点是否越来越高
                elif curr_high > prev_high:
                    signals.append(Signal.HOLD.value)
                    positions.append(True)
                else:
                    # 高点没有创新高，但也没跌破，继续持有
                    signals.append(Signal.HOLD.value)
                    positions.append(True)
            else:
                # 如果未持仓，检查是否高点越来越高（买入信号）
                if curr_high > prev_high:
                    signals.append(Signal.HOLD.value)
                    positions.append(True)
                else:
                    signals.append(Signal.IGNORE.value)
                    positions.append(False)
        
        df['signal'] = signals
        df['position'] = positions
        
        return df
    
    def backtest(self, kline_df: pd.DataFrame, initial_capital: float = 100000) -> dict:
        """
        回测策略
        
        Args:
            kline_df: K线数据
            initial_capital: 初始资金
            
        Returns:
            回测结果字典
        """
        if kline_df.empty:
            return {}
        
        # 过滤K线
        filtered_df = self.filter_kline(kline_df)
        
        if filtered_df.empty or len(filtered_df) < 2:
            return {}
        
        # 生成信号
        signal_df = self.generate_signals(filtered_df)
        
        if signal_df.empty:
            return {}
        
        # 执行回测
        capital = initial_capital
        position = 0  # 持仓数量
        entry_price = 0  # 入场价格
        trades = []  # 交易记录
        
        for i in range(len(signal_df)):
            signal = signal_df.loc[i, 'signal']
            price = signal_df.loc[i, 'close']
            date = signal_df.loc[i, 'date']
            
            if signal == Signal.HOLD.value and position == 0:
                # 买入
                position = capital / price
                entry_price = price
                capital = 0
                trades.append({
                    'date': date,
                    'action': '买入',
                    'price': price,
                    'shares': position
                })
            elif signal == Signal.SELL.value and position > 0:
                # 卖出
                capital = position * price
                profit = (price - entry_price) * position
                profit_pct = (price / entry_price - 1) * 100
                trades.append({
                    'date': date,
                    'action': '卖出',
                    'price': price,
                    'shares': position,
                    'profit': profit,
                    'profit_pct': profit_pct
                })
                position = 0
                entry_price = 0
        
        # 计算最终收益
        if position > 0:
            # 如果最后还持仓，按最后价格计算
            final_price = signal_df.iloc[-1]['close']
            final_capital = position * final_price
        else:
            final_capital = capital
        
        total_return = (final_capital / initial_capital - 1) * 100
        
        # 计算统计指标
        if trades:
            buy_trades = [t for t in trades if t['action'] == '买入']
            sell_trades = [t for t in trades if t.get('profit') is not None]
            
            if sell_trades:
                profits = [t['profit'] for t in sell_trades]
                win_rate = len([p for p in profits if p > 0]) / len(profits) * 100
                avg_profit = np.mean(profits)
                max_profit = max(profits)
                max_loss = min(profits)
            else:
                win_rate = 0
                avg_profit = 0
                max_profit = 0
                max_loss = 0
        else:
            win_rate = 0
            avg_profit = 0
            max_profit = 0
            max_loss = 0
        
        return {
            'initial_capital': initial_capital,
            'final_capital': final_capital,
            'total_return': total_return,
            'total_trades': len([t for t in trades if t['action'] == '卖出']),
            'win_rate': win_rate,
            'avg_profit': avg_profit,
            'max_profit': max_profit,
            'max_loss': max_loss,
            'trades': trades,
            'signal_df': signal_df
        }
    
    def get_current_signal(self, kline_df: pd.DataFrame) -> dict:
        """
        获取当前交易信号
        
        Args:
            kline_df: K线数据
            
        Returns:
            当前信号字典
        """
        if kline_df.empty or len(kline_df) < 2:
            return {'signal': '无数据', 'position': False}
        
        # 过滤K线
        filtered_df = self.filter_kline(kline_df)
        
        if filtered_df.empty or len(filtered_df) < 2:
            return {'signal': '无数据', 'position': False}
        
        # 生成信号
        signal_df = self.generate_signals(filtered_df)
        
        if signal_df.empty:
            return {'signal': '无数据', 'position': False}
        
        latest = signal_df.iloc[-1]
        
        return {
            'signal': latest['signal'],
            'position': latest['position'],
            'date': latest['date'],
            'price': latest['close'],
            'high': latest['high'],
            'low': latest['low']
        }


