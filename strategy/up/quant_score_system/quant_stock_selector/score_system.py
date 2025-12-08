"""
评分系统模块 - 基于基本面、成长性、波动率等指标进行评分
"""
import pandas as pd
import numpy as np
from typing import Dict, List
from data_fetcher import DataFetcher


class ScoreSystem:
    """股票评分系统"""
    
    def __init__(self, data_fetcher: DataFetcher):
        """
        初始化评分系统
        
        Args:
            data_fetcher: 数据获取器实例
        """
        self.data_fetcher = data_fetcher
        
        # 评分权重配置
        self.weights = {
            'fundamental': 0.3,  # 基本面权重
            'growth': 0.3,      # 成长性权重
            'volatility': 0.2,   # 波动率权重（越低越好，适合趋势策略）
            'market_cap': 0.2,   # 市值权重
        }
        
        # 市值最小阈值（亿元）
        self.min_market_cap = 50.0
    
    def calculate_fundamental_score(self, info: Dict) -> float:
        """
        计算基本面得分
        
        Args:
            info: 股票基本信息字典
            
        Returns:
            基本面得分 (0-100)
        """
        score = 50.0  # 基础分
        
        # PE评分（越低越好，但要在合理范围）
        if info.get('pe_ratio') is not None:
            pe = info['pe_ratio']
            if 0 < pe < 15:
                score += 20
            elif 15 <= pe < 30:
                score += 10
            elif 30 <= pe < 50:
                score += 5
            elif pe >= 50:
                score -= 10
        
        # PB评分（越低越好）
        if info.get('pb_ratio') is not None:
            pb = info['pb_ratio']
            if 0 < pb < 2:
                score += 15
            elif 2 <= pb < 4:
                score += 8
            elif pb >= 4:
                score -= 5
        
        # ROE评分（越高越好）
        if info.get('roe') is not None:
            roe = info['roe']
            if roe > 20:
                score += 15
            elif roe > 15:
                score += 10
            elif roe > 10:
                score += 5
            elif roe < 5:
                score -= 10
        
        return max(0, min(100, score))
    
    def calculate_growth_score(self, info: Dict) -> float:
        """
        计算成长性得分
        
        Args:
            info: 股票基本信息字典
            
        Returns:
            成长性得分 (0-100)
        """
        score = 50.0  # 基础分
        
        # 营收增长率评分
        if info.get('revenue_growth') is not None:
            revenue_growth = info['revenue_growth']
            if revenue_growth > 30:
                score += 25
            elif revenue_growth > 20:
                score += 15
            elif revenue_growth > 10:
                score += 8
            elif revenue_growth > 0:
                score += 3
            elif revenue_growth < -10:
                score -= 15
            elif revenue_growth < 0:
                score -= 5
        
        # 利润增长率评分
        if info.get('profit_growth') is not None:
            profit_growth = info['profit_growth']
            if profit_growth > 30:
                score += 25
            elif profit_growth > 20:
                score += 15
            elif profit_growth > 10:
                score += 8
            elif profit_growth > 0:
                score += 3
            elif profit_growth < -10:
                score -= 15
            elif profit_growth < 0:
                score -= 5
        
        return max(0, min(100, score))
    
    def calculate_volatility_score(self, volatility: float) -> float:
        """
        计算波动率得分（对于趋势策略，适中的波动率更好）
        
        Args:
            volatility: 年化波动率（百分比）
            
        Returns:
            波动率得分 (0-100)
        """
        # 对于上升趋势策略，适中的波动率（15-30%）最好
        # 太低（<10%）可能趋势不明显，太高（>50%）风险太大
        if volatility == 0:
            return 0
        
        if 15 <= volatility <= 30:
            return 100
        elif 10 <= volatility < 15:
            return 80
        elif 30 < volatility <= 40:
            return 70
        elif 5 <= volatility < 10:
            return 60
        elif 40 < volatility <= 50:
            return 50
        elif volatility < 5:
            return 40
        else:  # > 50%
            return 20
    
    def calculate_market_cap_score(self, market_cap: float) -> float:
        """
        计算市值得分
        
        Args:
            market_cap: 市值（亿元）
            
        Returns:
            市值得分 (0-100)
        """
        if market_cap < self.min_market_cap:
            return 0
        
        # 市值越大，流动性越好，但也要考虑成长空间
        if 50 <= market_cap < 200:
            return 100  # 中小盘，成长性好
        elif 200 <= market_cap < 500:
            return 90   # 中盘
        elif 500 <= market_cap < 1000:
            return 80   # 中大盘
        elif 1000 <= market_cap < 3000:
            return 70   # 大盘
        else:
            return 60   # 超大盘
    
    def calculate_total_score(self, info: Dict, volatility: float) -> float:
        """
        计算总分
        
        Args:
            info: 股票基本信息字典
            volatility: 波动率
            
        Returns:
            总分 (0-100)
        """
        # 市值筛选
        if info.get('market_cap', 0) < self.min_market_cap:
            return 0
        
        # 计算各项得分
        fundamental_score = self.calculate_fundamental_score(info)
        growth_score = self.calculate_growth_score(info)
        volatility_score = self.calculate_volatility_score(volatility)
        market_cap_score = self.calculate_market_cap_score(info.get('market_cap', 0))
        
        # 加权平均
        total_score = (
            fundamental_score * self.weights['fundamental'] +
            growth_score * self.weights['growth'] +
            volatility_score * self.weights['volatility'] +
            market_cap_score * self.weights['market_cap']
        )
        
        return round(total_score, 2)
    
    def score_stocks(self, stock_list: pd.DataFrame, top_n: int = 50) -> pd.DataFrame:
        """
        对股票列表进行评分和筛选
        
        Args:
            stock_list: 股票列表DataFrame，包含code和market列
            top_n: 返回前N只股票
            
        Returns:
            包含评分结果的DataFrame
        """
        results = []
        
        print(f"开始评分 {len(stock_list)} 只股票...")
        
        import time
        
        for idx, row in stock_list.iterrows():
            code = row['code']
            market = row['market']
            name = row.get('name', code)
            
            if idx % 10 == 0:
                print(f"进度: {idx+1}/{len(stock_list)} - 当前处理: {code}")
            
            # 添加延时避免API速率限制
            if idx > 0:
                time.sleep(2)  # 每次请求间隔2秒，避免速率限制
            
            try:
                # 获取基本信息
                info = self.data_fetcher.get_stock_basic_info(code, market)
                
                # 获取K线数据计算波动率
                kline_df = self.data_fetcher.get_stock_kline(code, market, 
                                                            period='daily')
                if kline_df.empty:
                    continue
                
                volatility = self.data_fetcher.calculate_volatility(kline_df)
                
                # 计算总分
                total_score = self.calculate_total_score(info, volatility)
                
                if total_score > 0:  # 只保留通过筛选的股票
                    results.append({
                        'code': code,
                        'name': name,
                        'market': market,
                        'market_cap': info.get('market_cap', 0),
                        'pe_ratio': info.get('pe_ratio'),
                        'pb_ratio': info.get('pb_ratio'),
                        'roe': info.get('roe'),
                        'revenue_growth': info.get('revenue_growth'),
                        'profit_growth': info.get('profit_growth'),
                        'volatility': volatility,
                        'total_score': total_score,
                        'fundamental_score': self.calculate_fundamental_score(info),
                        'growth_score': self.calculate_growth_score(info),
                        'volatility_score': self.calculate_volatility_score(volatility),
                        'market_cap_score': self.calculate_market_cap_score(info.get('market_cap', 0)),
                    })
            except Exception as e:
                print(f"评分 {code} 失败: {e}")
                continue
        
        if not results:
            return pd.DataFrame()
        
        # 转换为DataFrame并排序
        result_df = pd.DataFrame(results)
        result_df = result_df.sort_values('total_score', ascending=False)
        result_df = result_df.head(top_n).reset_index(drop=True)
        
        return result_df

