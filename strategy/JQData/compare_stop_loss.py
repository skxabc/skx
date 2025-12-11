#!/usr/bin/env python3
"""对比简化移动止损和ATR移动止损的效果"""

import sys
from ma_cross_inside_bar_strategy import run_backtest
from jqdatasdk import auth, logout

def compare_stop_loss(stocks, simple_pct=5.0, atr_mult=2.0):
    """对比两种止损方式"""
    auth('18813098345', 'Shitou+6819815')
    
    try:
        print('='*80)
        print(f'对比测试：简化{simple_pct}%止损 vs ATR {atr_mult}倍止损')
        print('='*80)
        print(f'{"股票代码":<15} {"止损方式":<15} {"总收益%":<10} {"胜率%":<10} {"盈亏比":<10} {"交易次数":<10}')
        print('-'*80)
        
        results = []
        for stock in stocks:
            # 简化5%止损
            result1 = run_backtest(
                symbol=stock,
                username='18813098345',
                password='Shitou+6819815',
                high_lookback=20,
                trend_ma=20,
                vol_mult=1.0,
                simple_stop_pct=simple_pct,
                skip_auth=True,
                silent=True
            )
            
            # ATR止损
            result2 = run_backtest(
                symbol=stock,
                username='18813098345',
                password='Shitou+6819815',
                high_lookback=20,
                trend_ma=20,
                vol_mult=1.0,
                atr_mult=atr_mult,
                skip_auth=True,
                silent=True
            )
            
            if result1 and result2:
                stock_short = stock.split('.')[0]
                print(f'{stock_short:<15} 简化{simple_pct}%止损  {result1["total_ret"]*100:>8.2f}%  {result1["success_rate"]:>8.2f}%  {result1["win_loss_ratio"]:>8.2f}  {result1["total_trades"]:>8}')
                print(f'{stock_short:<15} ATR {atr_mult}倍止损  {result2["total_ret"]*100:>8.2f}%  {result2["success_rate"]:>8.2f}%  {result2["win_loss_ratio"]:>8.2f}  {result2["total_trades"]:>8}')
                
                diff = result1['total_ret'] - result2['total_ret']
                if abs(diff) > 0.0001:  # 有差异
                    print(f'{"差异":<15} {diff*100:>+8.2f}%  (简化版 - ATR版)')
                print('-'*80)
                
                results.append({
                    'stock': stock,
                    'simple': result1,
                    'atr': result2,
                    'diff': diff
                })
        
        # 汇总统计
        if results:
            print('\n汇总统计:')
            print('-'*80)
            simple_total = sum(r['simple']['total_ret'] for r in results)
            atr_total = sum(r['atr']['total_ret'] for r in results)
            simple_avg = simple_total / len(results)
            atr_avg = atr_total / len(results)
            
            simple_wins = sum(1 for r in results if r['simple']['total_ret'] > 0)
            atr_wins = sum(1 for r in results if r['atr']['total_ret'] > 0)
            
            print(f'简化{simple_pct}%止损: 平均收益={simple_avg*100:.2f}%, 盈利股票={simple_wins}/{len(results)}')
            print(f'ATR {atr_mult}倍止损: 平均收益={atr_avg*100:.2f}%, 盈利股票={atr_wins}/{len(results)}')
            print(f'平均差异: {(simple_avg - atr_avg)*100:+.2f}% (简化版 - ATR版)')
            
    finally:
        logout()

if __name__ == '__main__':
    # 测试之前用过的股票列表
    test_stocks = [
        '000001.XSHE',  # 平安银行
        '600000.XSHG',  # 浦发银行
        '000002.XSHE',  # 万科A
        '600519.XSHG',  # 贵州茅台
        '000858.XSHE',  # 五粮液
    ]
    
    compare_stop_loss(test_stocks, simple_pct=5.0, atr_mult=2.0)

