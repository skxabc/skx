"""
趋势判断系统主程序
判断A股和港股市场是处于上升趋势、震荡还是下降趋势
"""
import sys
from datetime import datetime
from typing import Dict, List
import pandas as pd

from market_data import MarketDataFetcher
from trend_judge import TrendJudge, TrendType


class MarketTrendAnalyzer:
    """市场趋势分析器"""
    
    def __init__(self, tushare_token: str = None):
        """
        初始化分析器
        
        Args:
            tushare_token: Tushare API token（可选，但强烈推荐使用以获得更稳定的数据）
        """
        self.data_fetcher = MarketDataFetcher(tushare_token=tushare_token)
        self.trend_judge = TrendJudge()
    
    def analyze_market(self, market: str = 'A') -> Dict:
        """
        分析市场趋势
        
        Args:
            market: 'A' 表示A股，'H' 表示港股
            
        Returns:
            包含市场趋势分析结果的字典
        """
        print(f"\n{'='*60}")
        print(f"开始分析{'A股' if market == 'A' else '港股'}市场趋势...")
        print(f"{'='*60}\n")
        
        # 获取市场主要指数数据
        indices_data = self.data_fetcher.get_market_indices(market=market)
        
        if not indices_data:
            print(f"无法获取{'A股' if market == 'A' else '港股'}市场数据")
            return {
                'market': market,
                'trend': TrendType.UNKNOWN,
                'confidence': 0,
                'indices': {}
            }
        
        # 对每个指数进行趋势判断
        index_results = {}
        trend_scores = []
        confidences = []
        
        for index_key, df in indices_data.items():
            index_name = self._get_index_name(index_key, market)
            print(f"\n分析 {index_name}...")
            print(f"  数据量: {len(df)} 条")
            
            if len(df) < 60:
                print(f"  ⚠️  数据量不足，无法进行准确判断")
                continue
            
            # 判断趋势
            result = self.trend_judge.judge_trend(df)
            index_results[index_key] = {
                'name': index_name,
                'result': result
            }
            
            trend_scores.append(result['trend_value'])
            confidences.append(result['confidence'])
            
            # 打印结果
            self._print_index_result(index_name, result)
        
        # 综合判断市场整体趋势
        if trend_scores:
            avg_trend_score = sum(trend_scores) / len(trend_scores)
            avg_confidence = sum(confidences) / len(confidences)
            
            if avg_trend_score > 0.3:
                overall_trend = TrendType.UP
            elif avg_trend_score < -0.3:
                overall_trend = TrendType.DOWN
            else:
                overall_trend = TrendType.SIDEWAYS
        else:
            overall_trend = TrendType.UNKNOWN
            avg_trend_score = 0
            avg_confidence = 0
        
        # 打印综合结果
        print(f"\n{'='*60}")
        print(f"{'A股' if market == 'A' else '港股'}市场整体趋势判断:")
        print(f"{'='*60}")
        print(f"趋势类型: {overall_trend.value}")
        print(f"趋势强度: {avg_trend_score:.3f}")
        print(f"置信度: {avg_confidence:.2%}")
        print(f"{'='*60}\n")
        
        return {
            'market': market,
            'trend': overall_trend,
            'trend_value': avg_trend_score,
            'confidence': avg_confidence,
            'indices': index_results,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
    
    def _get_index_name(self, index_key: str, market: str) -> str:
        """获取指数名称"""
        if market == 'A':
            index_map = {
                'sh': '上证指数',
                'sz': '深证成指',
                'cyb': '创业板指',
                'hs300': '沪深300'
            }
        else:
            index_map = {
                'hsi': '恒生指数',
                'hsc': '恒生国企指数',
                'hsci': '恒生科技指数'
            }
        return index_map.get(index_key, index_key)
    
    def _print_index_result(self, index_name: str, result: Dict):
        """打印单个指数的判断结果"""
        trend = result['trend']
        confidence = result['confidence']
        indicators = result['indicators']
        price_change = result['price_change']
        
        print(f"  趋势: {trend.value}")
        print(f"  置信度: {confidence:.2%}")
        print(f"  当前价格: {indicators['current_price']:.2f}")
        
        if indicators['ma_short']:
            print(f"  短期均线(20日): {indicators['ma_short']:.2f}")
        if indicators['ma_long']:
            print(f"  长期均线(60日): {indicators['ma_long']:.2f}")
        if indicators['rsi']:
            print(f"  RSI: {indicators['rsi']:.2f}")
        
        print(f"  价格变化: 1日={price_change['1d']:.2%}, "
              f"5日={price_change['5d']:.2%}, "
              f"20日={price_change['20d']:.2%}")
        
        # 打印各指标信号
        signals = result['signals']
        print(f"  指标信号:")
        print(f"    MA: {signals['ma']['signal']:.2f} (强度: {signals['ma']['strength']:.2f})")
        print(f"    MACD: {signals['macd']['signal']:.2f} (强度: {signals['macd']['strength']:.2f})")
        print(f"    动量: {signals['momentum']['signal']:.2f} (强度: {signals['momentum']['strength']:.2f})")
    
    def analyze_all_markets(self) -> Dict:
        """分析所有市场"""
        results = {}
        
        # 分析A股
        results['A'] = self.analyze_market(market='A')
        
        # 分析港股
        results['H'] = self.analyze_market(market='H')
        
        # 打印总结
        self._print_summary(results)
        
        return results
    
    def _print_summary(self, results: Dict):
        """打印总结"""
        print(f"\n{'='*60}")
        print("市场趋势判断总结")
        print(f"{'='*60}")
        
        for market_key, result in results.items():
            market_name = 'A股' if market_key == 'A' else '港股'
            trend = result['trend']
            confidence = result['confidence']
            
            print(f"\n{market_name}:")
            print(f"  趋势: {trend.value}")
            print(f"  置信度: {confidence:.2%}")
            
            # 策略建议
            strategy = self._get_strategy_suggestion(trend)
            print(f"  策略建议: {strategy}")
        
        print(f"\n{'='*60}\n")
    
    def _get_strategy_suggestion(self, trend: TrendType) -> str:
        """根据趋势获取策略建议"""
        if trend == TrendType.UP:
            return "上升趋势 - 建议使用上升追踪策略"
        elif trend == TrendType.DOWN:
            return "下降趋势 - 建议空仓等待"
        elif trend == TrendType.SIDEWAYS:
            return "震荡市场 - 建议使用震荡策略"
        else:
            return "趋势不明 - 建议谨慎操作"


def main():
    """主函数"""
    import argparse
    
    parser = argparse.ArgumentParser(description='市场趋势判断系统')
    parser.add_argument('--market', type=str, choices=['A', 'H', 'all'], 
                       default='all', help='要分析的市场: A( A股), H(港股), all(全部)')
    parser.add_argument('--output', type=str, help='输出结果到文件（JSON格式）')
    parser.add_argument('--tushare-token', type=str, 
                       help='Tushare API token（推荐使用以获得更稳定的数据）')
    
    args = parser.parse_args()
    
    analyzer = MarketTrendAnalyzer(tushare_token=args.tushare_token)
    
    if args.market == 'all':
        results = analyzer.analyze_all_markets()
    elif args.market == 'A':
        results = {'A': analyzer.analyze_market(market='A')}
    else:
        results = {'H': analyzer.analyze_market(market='H')}
    
    # 如果需要输出到文件
    if args.output:
        import json
        # 将枚举类型转换为字符串
        def convert_to_dict(obj):
            if isinstance(obj, TrendType):
                return obj.value
            elif isinstance(obj, dict):
                return {k: convert_to_dict(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [convert_to_dict(item) for item in obj]
            else:
                return obj
        
        output_data = convert_to_dict(results)
        with open(args.output, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, ensure_ascii=False, indent=2)
        print(f"\n结果已保存到: {args.output}")


if __name__ == '__main__':
    main()

