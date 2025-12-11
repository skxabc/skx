#!/usr/bin/env python3
"""测试跌破前日K线新低止损和移动止损的冲突情况"""

import sys
sys.path.insert(0, '.')
from ma_cross_inside_bar_strategy import run_backtest
from jqdatasdk import auth, logout

auth('18813098345', 'Shitou+6819815')

stock = '000001.XSHE'
print('='*80)
print('测试：跌破前日K线新低止损 vs 移动止损')
print('='*80)

# 测试1：同时启用两种止损
print('\n【测试1：同时启用两种止损】')
result1 = run_backtest(
    symbol=stock,
    username='18813098345',
    password='Shitou+6819815',
    high_lookback=20,
    trend_ma=20,
    vol_mult=1.0,
    simple_stop_pct=5.0,
    skip_auth=True,
    silent=True
)

if result1:
    print(f'总收益: {result1["total_ret"]*100:.2f}%')
    print(f'胜率: {result1["success_rate"]:.2f}%')
    print(f'交易次数: {result1["total_trades"]}')
    print('交易记录:')
    for ts, side, px in result1["trades"]:
        print(f'  {ts.date()} {side} @ {px:.2f}')

logout()

