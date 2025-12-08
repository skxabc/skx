"""
港股通选股脚本 - 手动指定港股通股票列表（用于网络不稳定时）
"""
import pandas as pd
import os
from datetime import datetime
from data_fetcher import DataFetcher
from score_system import ScoreSystem
from trading_strategy import TradingStrategy


# 常见港股通股票代码列表（示例）
COMMON_HGT_STOCKS = [
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
    {'code': '02007', 'name': '碧桂园', 'market': 'H'},
    {'code': '03328', 'name': '交通银行', 'market': 'H'},
    {'code': '00688', 'name': '中国海外发展', 'market': 'H'},
    {'code': '00175', 'name': '吉利汽车', 'market': 'H'},
    {'code': '00267', 'name': '中信股份', 'market': 'H'},
    {'code': '00386', 'name': '中国石油化工股份', 'market': 'H'},
    {'code': '00489', 'name': '东风集团股份', 'market': 'H'},
    {'code': '00548', 'name': '深圳高速公路股份', 'market': 'H'},
    {'code': '00604', 'name': '深圳控股', 'market': 'H'},
    {'code': '00688', 'name': '中国海外发展', 'market': 'H'},
]


def main():
    """港股通选股主函数"""
    print("=" * 60)
    print("港股通选股系统 - 上升趋势策略")
    print("=" * 60)
    
    # 初始化组件
    print("\n1. 初始化数据获取器...")
    data_fetcher = DataFetcher()
    
    print("\n2. 初始化评分系统...")
    score_system = ScoreSystem(data_fetcher)
    
    print("\n3. 初始化交易策略...")
    strategy = TradingStrategy()
    
    # 使用手动指定的港股通股票列表
    print("\n4. 使用预设的港股通股票列表...")
    hgt_stocks = pd.DataFrame(COMMON_HGT_STOCKS)
    # 为了加快速度，先只处理前20只
    if len(hgt_stocks) > 20:
        print(f"   共 {len(hgt_stocks)} 只港股通股票，先处理前20只以加快速度...")
        hgt_stocks = hgt_stocks.head(20)
    else:
        print(f"   共 {len(hgt_stocks)} 只港股通股票")
    
    # 评分选股
    print("\n5. 开始评分选股...")
    print("   评分标准：")
    print("   - 基本面（30%）：PE、PB、ROE")
    print("   - 成长性（30%）：营收增长率、利润增长率")
    print("   - 波动率（20%）：适合趋势策略的波动率范围")
    print("   - 市值（20%）：市值大于50亿")
    print(f"\n   正在对 {len(hgt_stocks)} 只股票进行评分，请耐心等待...")
    print("   注意：数据获取可能需要较长时间，请耐心等待...")
    
    scored_stocks = score_system.score_stocks(hgt_stocks, top_n=10)
    
    if scored_stocks.empty:
        print("\n   未找到符合条件的股票")
        print("   可能原因：")
        print("   1. 数据获取失败")
        print("   2. 所有股票都不满足筛选条件（如市值小于50亿）")
        return
    
    # 显示选股结果
    print("\n6. 港股通选股结果（前10只）：")
    print("=" * 140)
    header = f"{'排名':<6}{'代码':<12}{'名称':<25}{'市场':<8}{'总分':<8}{'市值(亿)':<12}{'PE':<10}{'PB':<10}{'ROE%':<10}{'波动率%':<12}{'营收增长%':<12}"
    print(header)
    print("-" * 140)
    
    for idx, row in scored_stocks.iterrows():
        name = str(row['name'])[:23] if pd.notna(row['name']) else 'N/A'
        pe = f"{row['pe_ratio']:.2f}" if pd.notna(row['pe_ratio']) else 'N/A'
        pb = f"{row['pb_ratio']:.2f}" if pd.notna(row['pb_ratio']) else 'N/A'
        roe = f"{row['roe']:.2f}" if pd.notna(row['roe']) else 'N/A'
        revenue_growth = f"{row['revenue_growth']:.2f}" if pd.notna(row['revenue_growth']) else 'N/A'
        
        print(f"{idx+1:<6}{row['code']:<12}{name:<25}{row['market']:<8}"
              f"{row['total_score']:<8.2f}{row['market_cap']:<12.2f}"
              f"{pe:<10}{pb:<10}{roe:<10}"
              f"{row['volatility']:<12.2f}{revenue_growth:<12}")
    
    # 保存结果
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"hgt_selected_stocks_{timestamp}.xlsx")
    
    scored_stocks.to_excel(output_file, index=False)
    print(f"\n7. 结果已保存到: {output_file}")
    
    # 对选出的股票进行策略回测
    print("\n8. 对选出的股票进行策略回测...")
    print("=" * 140)
    
    backtest_results = []
    
    for idx, row in scored_stocks.iterrows():
        code = row['code']
        market = row['market']
        name = row['name']
        
        print(f"\n回测 {code} ({name})...")
        
        # 获取K线数据
        kline_df = data_fetcher.get_stock_kline(code, market, period='daily')
        
        if kline_df.empty or len(kline_df) < 60:  # 至少需要60个交易日
            print(f"  K线数据不足（仅{len(kline_df)}条），跳过")
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
        backtest_file = os.path.join(output_dir, f"hgt_backtest_results_{timestamp}.xlsx")
        backtest_df.to_excel(backtest_file, index=False)
        print(f"\n9. 回测结果已保存到: {backtest_file}")
        
        # 显示回测汇总
        print("\n回测汇总：")
        print(f"  平均收益率: {backtest_df['total_return'].mean():.2f}%")
        print(f"  平均胜率: {backtest_df['win_rate'].mean():.2f}%")
        print(f"  总交易次数: {backtest_df['total_trades'].sum()}")
    else:
        print("\n9. 没有足够的K线数据进行回测")
    
    # 显示当前信号
    print("\n10. 获取当前交易信号...")
    print("=" * 140)
    
    for idx, row in scored_stocks.iterrows():
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
                if 'high' in signal and signal['high']:
                    print(f"  最高价: {signal['high']:.2f}")
                if 'low' in signal and signal['low']:
                    print(f"  最低价: {signal['low']:.2f}")
    
    print("\n" + "=" * 60)
    print("港股通选股完成！")
    print("=" * 60)
    print(f"\n最终选出的10只股票已保存到: {output_file}")


if __name__ == "__main__":
    main()

