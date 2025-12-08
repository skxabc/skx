"""
趋势判断模块 - 判断市场是处于上升趋势、震荡还是下降趋势
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from enum import Enum


class TrendType(Enum):
    """趋势类型枚举"""
    UP = "上升趋势"
    DOWN = "下降趋势"
    SIDEWAYS = "震荡"
    UNKNOWN = "未知"


class TrendJudge:
    """趋势判断类"""
    
    def __init__(self, short_ma: int = 20, long_ma: int = 60, 
                 macd_fast: int = 12, macd_slow: int = 26, macd_signal: int = 9,
                 rsi_period: int = 14, bb_period: int = 20, bb_std: float = 2.0):
        """
        初始化趋势判断器
        
        Args:
            short_ma: 短期均线周期（默认20日）
            long_ma: 长期均线周期（默认60日）
            macd_fast: MACD快线周期
            macd_slow: MACD慢线周期
            macd_signal: MACD信号线周期
            rsi_period: RSI周期
            bb_period: 布林带周期
            bb_std: 布林带标准差倍数
        """
        self.short_ma = short_ma
        self.long_ma = long_ma
        self.macd_fast = macd_fast
        self.macd_slow = macd_slow
        self.macd_signal = macd_signal
        self.rsi_period = rsi_period
        self.bb_period = bb_period
        self.bb_std = bb_std
    
    def calculate_ma(self, df: pd.DataFrame, period: int) -> pd.Series:
        """计算移动平均线"""
        return df['close'].rolling(window=period).mean()
    
    def calculate_macd(self, df: pd.DataFrame) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        计算MACD指标
        
        Returns:
            (DIF, DEA, MACD)
        """
        ema_fast = df['close'].ewm(span=self.macd_fast, adjust=False).mean()
        ema_slow = df['close'].ewm(span=self.macd_slow, adjust=False).mean()
        dif = ema_fast - ema_slow
        dea = dif.ewm(span=self.macd_signal, adjust=False).mean()
        macd = (dif - dea) * 2
        return dif, dea, macd
    
    def calculate_rsi(self, df: pd.DataFrame, period: int = None) -> pd.Series:
        """计算RSI指标"""
        if period is None:
            period = self.rsi_period
        
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
        
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_bollinger_bands(self, df: pd.DataFrame) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        计算布林带
        
        Returns:
            (上轨, 中轨, 下轨)
        """
        ma = df['close'].rolling(window=self.bb_period).mean()
        std = df['close'].rolling(window=self.bb_period).std()
        upper = ma + (std * self.bb_std)
        lower = ma - (std * self.bb_std)
        return upper, ma, lower
    
    def calculate_indicators(self, df: pd.DataFrame) -> pd.DataFrame:
        """计算所有技术指标"""
        df = df.copy()
        
        # 移动平均线
        df['ma_short'] = self.calculate_ma(df, self.short_ma)
        df['ma_long'] = self.calculate_ma(df, self.long_ma)
        
        # MACD
        df['macd_dif'], df['macd_dea'], df['macd'] = self.calculate_macd(df)
        
        # RSI
        df['rsi'] = self.calculate_rsi(df)
        
        # 布林带
        df['bb_upper'], df['bb_middle'], df['bb_lower'] = self.calculate_bollinger_bands(df)
        
        # 价格变化率
        df['price_change'] = df['close'].pct_change()
        df['price_change_5'] = df['close'].pct_change(periods=5)
        df['price_change_20'] = df['close'].pct_change(periods=20)
        
        return df
    
    def judge_by_ma(self, df: pd.DataFrame) -> Dict[str, float]:
        """
        基于移动平均线判断趋势
        
        Returns:
            包含趋势信号的字典
        """
        if len(df) < self.long_ma:
            return {'signal': 0, 'strength': 0}
        
        latest = df.iloc[-1]
        prev = df.iloc[-2] if len(df) > 1 else latest
        
        # 当前价格与均线的关系
        price_above_short = latest['close'] > latest['ma_short']
        price_above_long = latest['close'] > latest['ma_long']
        short_above_long = latest['ma_short'] > latest['ma_long']
        
        # 均线方向
        ma_short_up = latest['ma_short'] > prev['ma_short']
        ma_long_up = latest['ma_long'] > prev['ma_long']
        
        # 计算信号强度（-1到1之间）
        signal = 0
        strength = 0
        
        # 上升趋势信号
        if price_above_short and price_above_long and short_above_long:
            if ma_short_up and ma_long_up:
                signal = 1  # 强烈上升
                strength = 0.8
            else:
                signal = 0.5  # 温和上升
                strength = 0.5
        # 下降趋势信号
        elif not price_above_short and not price_above_long and not short_above_long:
            if not ma_short_up and not ma_long_up:
                signal = -1  # 强烈下降
                strength = 0.8
            else:
                signal = -0.5  # 温和下降
                strength = 0.5
        # 震荡信号
        else:
            signal = 0
            strength = 0.3
        
        return {'signal': signal, 'strength': strength}
    
    def judge_by_macd(self, df: pd.DataFrame) -> Dict[str, float]:
        """
        基于MACD判断趋势
        
        Returns:
            包含趋势信号的字典
        """
        if len(df) < self.macd_slow:
            return {'signal': 0, 'strength': 0}
        
        latest = df.iloc[-1]
        prev = df.iloc[-2] if len(df) > 1 else latest
        
        # MACD金叉死叉
        macd_cross_up = (latest['macd_dif'] > latest['macd_dea'] and 
                        prev['macd_dif'] <= prev['macd_dea'])
        macd_cross_down = (latest['macd_dif'] < latest['macd_dea'] and 
                          prev['macd_dif'] >= prev['macd_dea'])
        
        # MACD在零轴上方还是下方
        macd_above_zero = latest['macd_dif'] > 0
        macd_below_zero = latest['macd_dif'] < 0
        
        signal = 0
        strength = 0
        
        # 上升趋势：MACD在零轴上方，且DIF在DEA上方
        if macd_above_zero and latest['macd_dif'] > latest['macd_dea']:
            if macd_cross_up:
                signal = 1  # 金叉，强烈上升
                strength = 0.9
            else:
                signal = 0.6  # 持续上升
                strength = 0.6
        # 下降趋势：MACD在零轴下方，且DIF在DEA下方
        elif macd_below_zero and latest['macd_dif'] < latest['macd_dea']:
            if macd_cross_down:
                signal = -1  # 死叉，强烈下降
                strength = 0.9
            else:
                signal = -0.6  # 持续下降
                strength = 0.6
        # 震荡
        else:
            signal = 0
            strength = 0.3
        
        return {'signal': signal, 'strength': strength}
    
    def judge_by_rsi(self, df: pd.DataFrame) -> Dict[str, float]:
        """
        基于RSI判断趋势
        
        Returns:
            包含趋势信号的字典
        """
        if len(df) < self.rsi_period:
            return {'signal': 0, 'strength': 0}
        
        latest = df.iloc[-1]
        rsi = latest['rsi']
        
        signal = 0
        strength = 0
        
        # RSI超买超卖判断
        if rsi > 70:
            signal = -0.3  # 超买，可能回调
            strength = 0.4
        elif rsi < 30:
            signal = 0.3  # 超卖，可能反弹
            strength = 0.4
        elif rsi > 50:
            signal = 0.2  # 偏强
            strength = 0.3
        elif rsi < 50:
            signal = -0.2  # 偏弱
            strength = 0.3
        else:
            signal = 0
            strength = 0.2
        
        return {'signal': signal, 'strength': strength}
    
    def judge_by_bollinger(self, df: pd.DataFrame) -> Dict[str, float]:
        """
        基于布林带判断趋势
        
        Returns:
            包含趋势信号的字典
        """
        if len(df) < self.bb_period:
            return {'signal': 0, 'strength': 0}
        
        latest = df.iloc[-1]
        price = latest['close']
        upper = latest['bb_upper']
        middle = latest['bb_middle']
        lower = latest['bb_lower']
        
        # 布林带宽度（衡量波动性）
        bb_width = (upper - lower) / middle
        
        signal = 0
        strength = 0
        
        # 价格在布林带中的位置
        if price > upper:
            signal = 0.3  # 突破上轨，可能继续上涨
            strength = 0.4
        elif price < lower:
            signal = -0.3  # 跌破下轨，可能继续下跌
            strength = 0.4
        elif price > middle:
            signal = 0.1  # 在中轨上方
            strength = 0.2
        elif price < middle:
            signal = -0.1  # 在中轨下方
            strength = 0.2
        else:
            signal = 0
            strength = 0.1
        
        # 如果布林带收窄，可能是震荡
        if bb_width < 0.1:  # 布林带宽度小于10%
            signal = signal * 0.5  # 降低信号强度
            strength = strength * 0.7
        
        return {'signal': signal, 'strength': strength}
    
    def judge_by_price_momentum(self, df: pd.DataFrame) -> Dict[str, float]:
        """
        基于价格动量判断趋势
        
        Returns:
            包含趋势信号的字典
        """
        if len(df) < 20:
            return {'signal': 0, 'strength': 0}
        
        latest = df.iloc[-1]
        
        signal = 0
        strength = 0
        
        # 短期、中期价格变化
        change_5 = latest['price_change_5']
        change_20 = latest['price_change_20']
        
        if pd.notna(change_5) and pd.notna(change_20):
            # 短期和中期都上涨
            if change_5 > 0.02 and change_20 > 0.05:  # 5日涨2%以上，20日涨5%以上
                signal = 0.8
                strength = 0.7
            # 短期和中期都下跌
            elif change_5 < -0.02 and change_20 < -0.05:  # 5日跌2%以上，20日跌5%以上
                signal = -0.8
                strength = 0.7
            # 短期上涨但中期下跌（可能反弹）
            elif change_5 > 0.02 and change_20 < -0.05:
                signal = 0.3
                strength = 0.4
            # 短期下跌但中期上涨（可能回调）
            elif change_5 < -0.02 and change_20 > 0.05:
                signal = -0.3
                strength = 0.4
            # 震荡
            else:
                signal = 0
                strength = 0.2
        
        return {'signal': signal, 'strength': strength}
    
    def judge_trend(self, df: pd.DataFrame) -> Dict:
        """
        综合判断趋势
        
        Args:
            df: 包含OHLCV数据的DataFrame
            
        Returns:
            包含趋势判断结果的字典
        """
        if df is None or df.empty:
            return {
                'trend': TrendType.UNKNOWN,
                'confidence': 0,
                'signals': {},
                'indicators': {}
            }
        
        # 计算技术指标
        df_with_indicators = self.calculate_indicators(df)
        
        # 获取各项指标信号
        ma_signal = self.judge_by_ma(df_with_indicators)
        macd_signal = self.judge_by_macd(df_with_indicators)
        rsi_signal = self.judge_by_rsi(df_with_indicators)
        bb_signal = self.judge_by_bollinger(df_with_indicators)
        momentum_signal = self.judge_by_price_momentum(df_with_indicators)
        
        # 加权综合信号（权重可调整）
        weights = {
            'ma': 0.3,
            'macd': 0.25,
            'momentum': 0.2,
            'rsi': 0.15,
            'bb': 0.1
        }
        
        # 计算加权平均信号
        total_signal = (
            ma_signal['signal'] * weights['ma'] * ma_signal['strength'] +
            macd_signal['signal'] * weights['macd'] * macd_signal['strength'] +
            momentum_signal['signal'] * weights['momentum'] * momentum_signal['strength'] +
            rsi_signal['signal'] * weights['rsi'] * rsi_signal['strength'] +
            bb_signal['signal'] * weights['bb'] * bb_signal['strength']
        )
        
        # 计算总强度
        total_strength = (
            ma_signal['strength'] * weights['ma'] +
            macd_signal['strength'] * weights['macd'] +
            momentum_signal['strength'] * weights['momentum'] +
            rsi_signal['strength'] * weights['rsi'] +
            bb_signal['strength'] * weights['bb']
        )
        
        # 判断趋势类型
        if total_signal > 0.3:
            trend = TrendType.UP
        elif total_signal < -0.3:
            trend = TrendType.DOWN
        else:
            trend = TrendType.SIDEWAYS
        
        # 获取最新数据
        latest = df_with_indicators.iloc[-1]
        
        return {
            'trend': trend,
            'trend_value': total_signal,
            'confidence': min(total_strength, 1.0),
            'signals': {
                'ma': ma_signal,
                'macd': macd_signal,
                'rsi': rsi_signal,
                'bb': bb_signal,
                'momentum': momentum_signal
            },
            'indicators': {
                'current_price': float(latest['close']),
                'ma_short': float(latest['ma_short']) if pd.notna(latest['ma_short']) else None,
                'ma_long': float(latest['ma_long']) if pd.notna(latest['ma_long']) else None,
                'rsi': float(latest['rsi']) if pd.notna(latest['rsi']) else None,
                'macd_dif': float(latest['macd_dif']) if pd.notna(latest['macd_dif']) else None,
                'macd_dea': float(latest['macd_dea']) if pd.notna(latest['macd_dea']) else None,
            },
            'price_change': {
                '1d': float(latest['price_change']) if pd.notna(latest['price_change']) else 0,
                '5d': float(latest['price_change_5']) if pd.notna(latest['price_change_5']) else 0,
                '20d': float(latest['price_change_20']) if pd.notna(latest['price_change_20']) else 0,
            }
        }

