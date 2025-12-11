#!/usr/bin/env python3
"""简单对比简化止损和ATR止损"""

from ma_cross_inside_bar_strategy import run_backtest
from jqdatasdk import auth, logout

auth('18813098345', 'Shitou+6819815')

stocks = ['000001.XSHE', '600000.XSHG', '600519.XSHG']
print('='*80)
print('对比：简化5%止损 vs ATR 2.0倍止损')
print('='*80)

for stock in stocks:
    print(f'\n【{stock}】')
    
    # 简化5%止损
    r1 = run_backtest(
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
    
    # ATR 2.0倍止损
    r2 = run_backtest(
        symbol=stock,
        username='18813098345',
        password='Shitou+6819815',
        high_lookback=20,
        trend_ma=20,
        vol_mult=1.0,
        atr_mult=2.0,
        skip_auth=True,
        silent=True
    )
    
    if r1 and r2:
        print(f'简化5%:  收益={r1["total_ret"]*100:.2f}%, 胜率={r1["success_rate"]:.2f}%, 盈亏比={r1["win_loss_ratio"]:.2f}, 交易={r1["total_trades"]}')
        print(f'ATR 2.0: 收益={r2["total_ret"]*100:.2f}%, 胜率={r2["success_rate"]:.2f}%, 盈亏比={r2["win_loss_ratio"]:.2f}, 交易={r2["total_trades"]}')
        if abs(r1["total_ret"] - r2["total_ret"]) > 0.0001:
            print(f'差异: {(r1["total_ret"] - r2["total_ret"])*100:+.2f}%')

logout()

