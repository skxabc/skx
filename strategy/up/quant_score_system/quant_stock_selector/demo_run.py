"""
演示版本 - 使用模拟数据展示选股和策略回测功能
"""
import pandas as pd
import numpy as np
import os
from datetime import datetime, timedelta
from score_system import ScoreSystem
from trading_strategy import TradingStrategy


class DemoDataFetcher:
    """演示用数据获取器 - 生成模拟数据"""
    
    def get_stock_basic_info(self, code: str, market: str = 'H') -> dict:
        """生成模拟的基本信息"""
        # 为不同股票生成不同的模拟数据
        np.random.seed(hash(code) % 1000)
        
        info = {
            'code': code,
            'market': market,
            'market_cap': np.random.uniform(50, 5000),  # 市值50-5000亿
            'pe_ratio': np.random.uniform(5, 50),
            'pb_ratio': np.random.uniform(0.5, 5),
            'roe': np.random.uniform(5, 30),
            'revenue_growth': np.random.uniform(-10, 50),
            'profit_growth': np.random.uniform(-20, 60),
        }
        return info
    
    def get_stock_kline(self, code: str, market: str = 'H', 
                       start_date: str = None, end_date: str = None,
                       period: str = 'daily') -> pd.DataFrame:
        """生成模拟的K线数据"""
        if end_date is None:
            end_date = datetime.now()
        else:
            end_date = pd.to_datetime(end_date)
        
        if start_date is None:
            start_date = end_date - timedelta(days=365)
        else:
            start_date = pd.to_datetime(start_date)
        
        # 生成交易日
        dates = pd.bdate_range(start=start_date, end=end_date)
        
        # 为不同股票生成不同的价格走势
        np.random.seed(hash(code) % 1000)
        
        # 生成价格序列（带趋势）
        n = len(dates)
        base_price = np.random.uniform(10, 200)
        trend = np.random.choice([-1, 0, 1]) * np.random.uniform(0.01, 0.05)
        noise = np.random.normal(0, 0.02, n)
        
        prices = base_price * (1 + np.cumsum(trend + noise))
        prices = np.maximum(prices, base_price * 0.5)  # 防止价格过低
        
        # 生成OHLC
        opens = prices * (1 + np.random.normal(0, 0.01, n))
        closes = prices * (1 + np.random.normal(0, 0.01, n))
        highs = np.maximum(opens, closes) * (1 + np.abs(np.random.normal(0, 0.01, n)))
        lows = np.minimum(opens, closes) * (1 - np.abs(np.random.normal(0, 0.01, n)))
        volumes = np.random.uniform(1000000, 10000000, n)
        
        df = pd.DataFrame({
            'date': dates,
            'open': opens,
            'high': highs,
            'low': lows,
            'close': closes,
            'volume': volumes
        })
        
        return df
    
    def calculate_volatility(self, kline_df: pd.DataFrame, window: int = 20) -> float:
        """计算波动率"""
        if kline_df.empty or len(kline_df) < window:
            return 0.0
        
        try:
            returns = kline_df['close'].pct_change().dropna()
            if len(returns) < window:
                return 0.0
            volatility = returns.tail(window).std() * np.sqrt(252) * 100
            return volatility
        except:
            return 0.0


def main():
    """演示主函数"""
    print("=" * 60)
    print("港股通选股系统 - 演示版本（使用模拟数据）")
    print("=" * 60)
    
    # 使用演示数据获取器
    demo_fetcher = DemoDataFetcher()
    
    # 创建评分系统（需要适配演示数据获取器）
    class DemoScoreSystem(ScoreSystem):
        def __init__(self, data_fetcher):
            self.data_fetcher = data_fetcher
            self.weights = {
                'fundamental': 0.3,
                'growth': 0.3,
                'volatility': 0.2,
                'market_cap': 0.2,
            }
            self.min_market_cap = 50.0
    
    score_system = DemoScoreSystem(demo_fetcher)
    strategy = TradingStrategy()
    
    # 港股通股票列表
    hgt_stocks = pd.DataFrame([
        {'code': '00700', 'name': '腾讯控股', 'market': 'H'},
        {'code': '09988', 'name': '阿里巴巴-SW', 'market': 'H'},
        {'code': '03690', 'name': '美团-W', 'market': 'H'},
        {'code': '01810', 'name': '小米集团-W', 'market': 'H'},
        {'code': '00939', 'name': '建设银行', 'market': 'H'},
        {'code': '01299', 'name': '友邦保险', 'market': 'H'},
        {'code': '02318', 'name': '中国平安', 'market': 'H'},
        {'code': '00388', 'name': '香港交易所', 'market': 'H'},
        {'code': '02020', 'name': '安踏体育', 'market': 'H'},
        {'code': '01024', 'name': '快手-W', 'market': 'H'},
        {'code': '02269', 'name': '药明生物', 'market': 'H'},
        {'code': '02319', 'name': '蒙牛乳业', 'market': 'H'},
        {'code': '01398', 'name': '工商银行', 'market': 'H'},
        {'code': '03988', 'name': '中国银行', 'market': 'H'},
        {'code': '00857', 'name': '中国石油股份', 'market': 'H'},
        {'code': '00941', 'name': '中国移动', 'market': 'H'},
        {'code': '02382', 'name': '舜宇光学科技', 'market': 'H'},
        {'code': '00728', 'name': '中国电信', 'market': 'H'},
        {'code': '01088', 'name': '中国神华', 'market': 'H'},
        {'code': '01177', 'name': '中国生物制药', 'market': 'H'},
    ])
    
    print(f"\n1. 开始对 {len(hgt_stocks)} 只港股通股票进行评分...")
    print("   评分标准：")
    print("   - 基本面（30%）：PE、PB、ROE")
    print("   - 成长性（30%）：营收增长率、利润增长率")
    print("   - 波动率（20%）：适合趋势策略的波动率范围")
    print("   - 市值（20%）：市值大于50亿")
    
    # 评分选股
    results = []
    for idx, row in hgt_stocks.iterrows():
        code = row['code']
        name = row['name']
        market = row['market']
        
        print(f"   处理 {idx+1}/{len(hgt_stocks)}: {code} {name}")
        
        # 获取基本信息
        info = demo_fetcher.get_stock_basic_info(code, market)
        
        # 获取K线数据
        kline_df = demo_fetcher.get_stock_kline(code, market)
        if kline_df.empty:
            continue
        
        # 计算波动率
        volatility = demo_fetcher.calculate_volatility(kline_df)
        
        # 计算总分
        total_score = score_system.calculate_total_score(info, volatility)
        
        if total_score > 0:
            results.append({
                'code': code,
                'name': name,
                'market': market,
                'market_cap': info['market_cap'],
                'pe_ratio': info['pe_ratio'],
                'pb_ratio': info['pb_ratio'],
                'roe': info['roe'],
                'revenue_growth': info['revenue_growth'],
                'profit_growth': info['profit_growth'],
                'volatility': volatility,
                'total_score': total_score,
                'fundamental_score': score_system.calculate_fundamental_score(info),
                'growth_score': score_system.calculate_growth_score(info),
                'volatility_score': score_system.calculate_volatility_score(volatility),
                'market_cap_score': score_system.calculate_market_cap_score(info['market_cap']),
            })
    
    if not results:
        print("\n未找到符合条件的股票")
        return
    
    # 排序并选取前10只
    scored_stocks = pd.DataFrame(results)
    scored_stocks = scored_stocks.sort_values('total_score', ascending=False)
    scored_stocks = scored_stocks.head(10).reset_index(drop=True)
    
    # 显示选股结果
    print("\n2. 港股通选股结果（前10只）：")
    print("=" * 140)
    header = f"{'排名':<6}{'代码':<12}{'名称':<25}{'市场':<8}{'总分':<8}{'市值(亿)':<12}{'PE':<10}{'PB':<10}{'ROE%':<10}{'波动率%':<12}{'营收增长%':<12}"
    print(header)
    print("-" * 140)
    
    for idx, row in scored_stocks.iterrows():
        name = str(row['name'])[:23]
        print(f"{idx+1:<6}{row['code']:<12}{name:<25}{row['market']:<8}"
              f"{row['total_score']:<8.2f}{row['market_cap']:<12.2f}"
              f"{row['pe_ratio']:<10.2f}{row['pb_ratio']:<10.2f}{row['roe']:<10.2f}"
              f"{row['volatility']:<12.2f}{row['revenue_growth']:<12.2f}")
    
    # 保存结果
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"hgt_selected_stocks_demo_{timestamp}.xlsx")
    scored_stocks.to_excel(output_file, index=False)
    print(f"\n3. 选股结果已保存到: {output_file}")
    
    # 策略回测
    print("\n4. 对选出的股票进行策略回测...")
    print("=" * 140)
    
    backtest_results = []
    
    for idx, row in scored_stocks.iterrows():
        code = row['code']
        market = row['market']
        name = row['name']
        
        print(f"\n回测 {code} ({name})...")
        
        # 获取K线数据
        kline_df = demo_fetcher.get_stock_kline(code, market)
        
        if kline_df.empty or len(kline_df) < 60:
            print(f"  K线数据不足，跳过")
            continue
        
        # 回测
        result = strategy.backtest(kline_df, initial_capital=100000)
        
        if result:
            backtest_results.append({
                'code': code,
                'name': name,
                'market': market,
                'total_return': result['total_return'],
                'win_rate': result['win_rate'],
                'total_trades': result['total_trades'],
                'avg_profit': result['avg_profit'],
                'max_profit': result['max_profit'],
                'max_loss': result['max_loss']
            })
            
            print(f"  总收益率: {result['total_return']:.2f}%")
            print(f"  胜率: {result['win_rate']:.2f}%")
            print(f"  交易次数: {result['total_trades']}")
            print(f"  平均盈亏: {result['avg_profit']:.2f}")
            if result['max_profit'] > 0:
                print(f"  最大盈利: {result['max_profit']:.2f}")
            if result['max_loss'] < 0:
                print(f"  最大亏损: {result['max_loss']:.2f}")
    
    # 保存回测结果
    if backtest_results:
        backtest_df = pd.DataFrame(backtest_results)
        backtest_file = os.path.join(output_dir, f"hgt_backtest_results_demo_{timestamp}.xlsx")
        backtest_df.to_excel(backtest_file, index=False)
        print(f"\n5. 回测结果已保存到: {backtest_file}")
        
        # 显示回测汇总
        print("\n回测汇总统计：")
        print("=" * 140)
        print(f"  平均收益率: {backtest_df['total_return'].mean():.2f}%")
        print(f"  最高收益率: {backtest_df['total_return'].max():.2f}%")
        print(f"  最低收益率: {backtest_df['total_return'].min():.2f}%")
        print(f"  平均胜率: {backtest_df['win_rate'].mean():.2f}%")
        print(f"  总交易次数: {backtest_df['total_trades'].sum()}")
        print(f"  平均交易次数: {backtest_df['total_trades'].mean():.2f}")
        
        # 显示收益排名
        print("\n收益率排名：")
        sorted_results = backtest_df.sort_values('total_return', ascending=False)
        for idx, row in sorted_results.iterrows():
            print(f"  {row['code']} ({row['name']}): {row['total_return']:.2f}%")
    
    # 显示当前信号
    print("\n6. 获取当前交易信号...")
    print("=" * 140)
    
    for idx, row in scored_stocks.head(5).iterrows():
        code = row['code']
        market = row['market']
        name = row['name']
        
        kline_df = demo_fetcher.get_stock_kline(code, market)
        
        if not kline_df.empty:
            signal = strategy.get_current_signal(kline_df)
            print(f"\n{code} ({name}):")
            print(f"  信号: {signal['signal']}")
            print(f"  持仓: {'是' if signal['position'] else '否'}")
            if 'price' in signal:
                print(f"  当前价: {signal['price']:.2f}")
    
    print("\n" + "=" * 60)
    print("演示完成！")
    print("=" * 60)
    print(f"\n注意：这是使用模拟数据的演示版本")
    print(f"实际使用时，请运行 select_hgt_stocks_manual.py 获取真实数据")


if __name__ == "__main__":
    main()


