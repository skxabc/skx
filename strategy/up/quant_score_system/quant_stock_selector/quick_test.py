"""
快速测试脚本 - 只处理5只股票进行快速验证
"""
import pandas as pd
import os
from datetime import datetime
from data_fetcher import DataFetcher
from score_system import ScoreSystem
from trading_strategy import TradingStrategy

# 测试用的5只港股通股票
TEST_STOCKS = [
    {'code': '00700', 'name': '腾讯控股', 'market': 'H'},
    {'code': '09988', 'name': '阿里巴巴-SW', 'market': 'H'},
    {'code': '03690', 'name': '美团-W', 'market': 'H'},
    {'code': '00939', 'name': '建设银行', 'market': 'H'},
    {'code': '01299', 'name': '友邦保险', 'market': 'H'},
]

def main():
    print("=" * 60)
    print("港股通选股系统 - 快速测试（5只股票）")
    print("=" * 60)
    
    data_fetcher = DataFetcher()
    score_system = ScoreSystem(data_fetcher)
    strategy = TradingStrategy()
    
    print("\n开始评分选股...")
    hgt_stocks = pd.DataFrame(TEST_STOCKS)
    
    scored_stocks = score_system.score_stocks(hgt_stocks, top_n=5)
    
    if scored_stocks.empty:
        print("\n未找到符合条件的股票")
        return
    
    print("\n选股结果：")
    print("=" * 120)
    for idx, row in scored_stocks.iterrows():
        print(f"{idx+1}. {row['code']} {row['name']} - 总分: {row['total_score']:.2f}, 市值: {row['market_cap']:.2f}亿")
    
    # 保存结果
    output_dir = "output"
    os.makedirs(output_dir, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(output_dir, f"hgt_selected_stocks_{timestamp}.xlsx")
    scored_stocks.to_excel(output_file, index=False)
    print(f"\n结果已保存到: {output_file}")

if __name__ == "__main__":
    main()


