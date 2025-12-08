"""
测试脚本 - 测试单个指数的数据获取
"""
import sys
from market_data import MarketDataFetcher
from trend_judge import TrendJudge

def test_index(index_code, market='A'):
    """测试单个指数的数据获取和趋势判断"""
    print(f"\n测试 {index_code} ({market}股市场)")
    print("="*60)
    
    fetcher = MarketDataFetcher()
    judge = TrendJudge()
    
    # 获取数据
    print(f"正在获取数据...")
    df = fetcher.get_index_data(index_code, market=market, days=250)
    
    if df is None or df.empty:
        print(f"❌ 数据获取失败")
        return None
    
    print(f"✓ 数据获取成功，共 {len(df)} 条记录")
    print(f"  日期范围: {df['date'].min()} 至 {df['date'].max()}")
    print(f"  最新收盘价: {df.iloc[-1]['close']:.2f}")
    
    # 判断趋势
    print(f"\n正在分析趋势...")
    result = judge.judge_trend(df)
    
    print(f"\n趋势判断结果:")
    print(f"  趋势类型: {result['trend'].value}")
    print(f"  趋势强度: {result['trend_value']:.3f}")
    print(f"  置信度: {result['confidence']:.2%}")
    print(f"  当前价格: {result['indicators']['current_price']:.2f}")
    
    if result['indicators']['ma_short']:
        print(f"  20日均线: {result['indicators']['ma_short']:.2f}")
    if result['indicators']['ma_long']:
        print(f"  60日均线: {result['indicators']['ma_long']:.2f}")
    if result['indicators']['rsi']:
        print(f"  RSI: {result['indicators']['rsi']:.2f}")
    
    return result

if __name__ == '__main__':
    # 测试A股指数
    print("="*60)
    print("A股指数测试")
    print("="*60)
    
    # 尝试上证指数
    test_index('000001', 'A')
    
    # 等待一下再测试港股
    import time
    print("\n等待5秒后测试港股...")
    time.sleep(5)
    
    print("\n" + "="*60)
    print("港股指数测试")
    print("="*60)
    
    # 尝试恒生指数
    test_index('HSI', 'H')

