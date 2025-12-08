"""
主程序 - 量化选股系统
"""
import pandas as pd
import os
from datetime import datetime
from data_fetcher import DataFetcher
from score_system import ScoreSystem
from trading_strategy import TradingStrategy


def main():
    """主函数"""
    print("=" * 60)
    print("量化选股系统 - 上升趋势策略")
    print("=" * 60)
    
    # 初始化组件
    print("\n1. 初始化数据获取器...")
    # 如果需要使用Tushare获取更详细数据，可以在这里设置token
    # tushare_token = "your_tushare_token"
    # data_fetcher = DataFetcher(tushare_token=tushare_token)
    data_fetcher = DataFetcher()
    
    print("\n2. 初始化评分系统...")
    score_system = ScoreSystem(data_fetcher)
    
    print("\n3. 初始化交易策略...")
    strategy = TradingStrategy()
    
    # 获取股票列表
    print("\n4. 获取股票列表...")
    print("   - 获取A股列表...")
    a_stocks = data_fetcher.get_stock_list(market='A')
    print(f"   找到 {len(a_stocks)} 只A股")
    
    print("   - 获取港股列表...")
    h_stocks = data_fetcher.get_stock_list(market='H')
    print(f"   找到 {len(h_stocks)} 只港股")
    
    # 合并股票列表
    all_stocks = pd.concat([a_stocks, h_stocks], ignore_index=True)
    print(f"\n   总计 {len(all_stocks)} 只股票")
    
    # 如果股票太多，可以随机采样一部分进行测试
    # 实际使用时建议分批处理或使用多进程
    if len(all_stocks) > 100:
        print("\n   股票数量较多，建议分批处理或使用多进程")
        print("   这里先采样前100只进行演示...")
        all_stocks = all_stocks.head(100)
    
    # 评分选股
    print("\n5. 开始评分选股...")
    print("   评分标准：")
    print("   - 基本面（30%）：PE、PB、ROE")
    print("   - 成长性（30%）：营收增长率、利润增长率")
    print("   - 波动率（20%）：适合趋势策略的波动率范围")
    print("   - 市值（20%）：市值大于50亿")
    
    scored_stocks = score_system.score_stocks(all_stocks, top_n=20)
    
    if scored_stocks.empty:
        print("\n   未找到符合条件的股票")
        return
    
    # 显示选股结果
    print("\n6. 选股结果：")
    print("=" * 120)
    print(f"{'排名':<6}{'代码':<12}{'名称':<20}{'市场':<8}{'总分':<8}{'市值(亿)':<12}{'PE':<8}{'波动率%':<10}{'营收增长%':<12}")
    print("-" * 120)
    
    for idx, row in scored_stocks.iterrows():
        print(f"{idx+1:<6}{row['code']:<12}{str(row['name'])[:18]:<20}{row['market']:<8}"
              f"{row['total_score']:<8.2f}{row['market_cap']:<12.2f}"
              f"{row['pe_ratio'] if pd.notna(row['pe_ratio']) else 'N/A':<8}"
              f"{row['volatility']:<10.2f}"
              f"{row['revenue_growth'] if pd.notna(row['revenue_growth']) else 'N/A':<12}")
    
    # 保存结果
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"selected_stocks_{timestamp}.xlsx")
    
    scored_stocks.to_excel(output_file, index=False)
    print(f"\n7. 结果已保存到: {output_file}")
    
    # 对选出的股票进行策略回测
    print("\n8. 对选出的股票进行策略回测...")
    print("=" * 120)
    
    backtest_results = []
    
    for idx, row in scored_stocks.head(10).iterrows():  # 只回测前10只
        code = row['code']
        market = row['market']
        name = row['name']
        
        print(f"\n回测 {code} ({name})...")
        
        # 获取K线数据
        kline_df = data_fetcher.get_stock_kline(code, market, period='daily')
        
        if kline_df.empty or len(kline_df) < 60:  # 至少需要60个交易日
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
                'avg_profit': result['avg_profit']
            })
            
            print(f"  总收益率: {result['total_return']:.2f}%")
            print(f"  胜率: {result['win_rate']:.2f}%")
            print(f"  交易次数: {result['total_trades']}")
            print(f"  平均盈亏: {result['avg_profit']:.2f}")
    
    # 保存回测结果
    if backtest_results:
        backtest_df = pd.DataFrame(backtest_results)
        backtest_file = os.path.join(output_dir, f"backtest_results_{timestamp}.xlsx")
        backtest_df.to_excel(backtest_file, index=False)
        print(f"\n9. 回测结果已保存到: {backtest_file}")
    
    # 显示当前信号
    print("\n10. 获取当前交易信号（前5只股票）...")
    print("=" * 120)
    
    for idx, row in scored_stocks.head(5).iterrows():
        code = row['code']
        market = row['market']
        name = row['name']
        
        kline_df = data_fetcher.get_stock_kline(code, market, period='daily')
        
        if not kline_df.empty:
            signal = strategy.get_current_signal(kline_df)
            print(f"\n{code} ({name}):")
            print(f"  信号: {signal['signal']}")
            print(f"  持仓: {'是' if signal['position'] else '否'}")
            if 'price' in signal:
                print(f"  当前价: {signal['price']:.2f}")
    
    print("\n" + "=" * 60)
    print("选股完成！")
    print("=" * 60)


if __name__ == "__main__":
    main()


