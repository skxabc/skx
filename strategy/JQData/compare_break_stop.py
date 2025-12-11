#!/usr/bin/env python3
"""对比启用和关闭跌破前日K线新低止损的效果"""

from ma_cross_inside_bar_strategy import run_backtest
from jqdatasdk import auth, logout

auth('18813098345', 'Shitou+6819815')

stocks = ['000001.XSHE', '600000.XSHG', '600519.XSHG']
print('='*80)
print('对比：启用 vs 关闭跌破前日K线新低止损（使用简化5%移动止损）')
print('='*80)

for stock in stocks:
    print(f'\n【{stock}】')
    print('-'*80)
    
    # 启用跌破前日K线新低止损
    r1 = run_backtest(
        symbol=stock,
        username='18813098345',
        password='Shitou+6819815',
        high_lookback=20,
        trend_ma=20,
        vol_mult=1.0,
        simple_stop_pct=5.0,
        disable_break_stop=False,
        skip_auth=True,
        silent=True
    )
    
    # 关闭跌破前日K线新低止损
    r2 = run_backtest(
        symbol=stock,
        username='18813098345',
        password='Shitou+6819815',
        high_lookback=20,
        trend_ma=20,
        vol_mult=1.0,
        simple_stop_pct=5.0,
        disable_break_stop=True,
        skip_auth=True,
        silent=True
    )
    
    if r1 and r2:
        print(f'启用跌破前日新低止损: 收益={r1["total_ret"]*100:.2f}%, 胜率={r1["success_rate"]:.2f}%, 盈亏比={r1["win_loss_ratio"]:.2f}, 交易={r1["total_trades"]}')
        print(f'关闭跌破前日新低止损: 收益={r2["total_ret"]*100:.2f}%, 胜率={r2["success_rate"]:.2f}%, 盈亏比={r2["win_loss_ratio"]:.2f}, 交易={r2["total_trades"]}')
        diff = r2["total_ret"] - r1["total_ret"]
        print(f'差异: {diff*100:+.2f}% (关闭 - 启用)')

logout()

