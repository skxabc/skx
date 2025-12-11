"""
批量测试多个股票的突破前高策略（ma_cross_inside_bar_strategy.py）
"""
import subprocess
import sys
import re
from collections import defaultdict

# 股票列表
stocks = [
    ("华大基因", "300676.XSHE"),
    ("昭衍新药", "603127.XSHG"),
    ("中信建投", "601066.XSHG"),
    ("复星医药", "600196.XSHG"),
    ("贵州茅台", "600519.XSHG"),
    ("邮储银行", "601658.XSHG"),
    ("中国电建", "601669.XSHG"),
    ("三六零", "601360.XSHG"),
]

username = "18813098345"
password = "Shitou+6819815"

results = []

print("=" * 100)
print("批量测试突破前高策略（一买一卖）")
print("=" * 100)

for name, symbol in stocks:
    print(f"\n正在测试: {name} ({symbol})")
    print("-" * 100)
    
    cmd = [
        sys.executable,
        "ma_cross_inside_bar_strategy.py",
        "--symbol", symbol,
        "--username", username,
        "--password", password,
        "--trend-ma", "0",  # 关闭趋势过滤
        "--vol-mult", "0",  # 关闭量能过滤（简化测试）
    ]
    
    try:
        result = subprocess.run(
            cmd,
            cwd="/home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skxtest/skx/strategy/JQData",
            capture_output=True,
            text=True,
            timeout=60
        )
        
        output = result.stdout + result.stderr
        
        # 解析结果
        total_ret = None
        success_rate = None
        win_loss_ratio = None
        trade_count = None
        win_count = None
        loss_count = None
        
        # 提取总收益
        ret_match = re.search(r'总收益\s+([-\d.]+)%', output)
        if ret_match:
            total_ret = float(ret_match.group(1))
        
        # 提取胜率
        sr_match = re.search(r'胜率:\s+([\d.]+)%', output)
        if sr_match:
            success_rate = float(sr_match.group(1))
        
        # 提取盈亏比
        wlr_match = re.search(r'盈亏比:\s+([\d.]+|inf)', output)
        if wlr_match:
            wlr_str = wlr_match.group(1)
            win_loss_ratio = float('inf') if wlr_str == 'inf' else float(wlr_str)
        
        # 提取交易次数
        tc_match = re.search(r'成交轮数\(买卖对\):\s+(\d+)', output)
        if tc_match:
            trade_count = int(tc_match.group(1))
        
        # 提取胜负笔数
        wc_match = re.search(r'胜\s+(\d+)\s+/\s+负\s+(\d+)', output)
        if wc_match:
            win_count = int(wc_match.group(1))
            loss_count = int(wc_match.group(2))
        
        results.append({
            "name": name,
            "symbol": symbol,
            "total_ret": total_ret,
            "success_rate": success_rate,
            "win_loss_ratio": win_loss_ratio,
            "trade_count": trade_count,
            "win_count": win_count,
            "loss_count": loss_count,
            "output": output
        })
        
        print(f"✓ 完成: {name}")
        
    except subprocess.TimeoutExpired:
        print(f"✗ 超时: {name}")
        results.append({
            "name": name,
            "symbol": symbol,
            "error": "超时"
        })
    except Exception as e:
        print(f"✗ 错误: {name} - {e}")
        results.append({
            "name": name,
            "symbol": symbol,
            "error": str(e)
        })

# 输出汇总对比
print("\n" + "=" * 100)
print("测试结果汇总对比（突破前高策略）")
print("=" * 100)
print(f"{'股票名称':<12} {'代码':<15} {'总收益%':<10} {'胜率%':<10} {'盈亏比':<10} {'交易次数':<10} {'胜/负':<10}")
print("-" * 100)

for r in results:
    if "error" in r:
        print(f"{r['name']:<12} {r['symbol']:<15} {'错误':<10}")
    else:
        total_ret_str = f"{r['total_ret']:.2f}%" if r['total_ret'] is not None else "N/A"
        sr_str = f"{r['success_rate']:.2f}%" if r['success_rate'] is not None else "N/A"
        wlr_str = f"{r['win_loss_ratio']:.2f}" if r['win_loss_ratio'] != float('inf') and r['win_loss_ratio'] is not None else "inf" if r['win_loss_ratio'] == float('inf') else "N/A"
        tc_str = str(r['trade_count']) if r['trade_count'] is not None else "N/A"
        wl_str = f"{r['win_count']}/{r['loss_count']}" if r['win_count'] is not None and r['loss_count'] is not None else "N/A"
        
        print(f"{r['name']:<12} {r['symbol']:<15} {total_ret_str:<10} {sr_str:<10} {wlr_str:<10} {tc_str:<10} {wl_str:<10}")

print("-" * 100)

# 统计信息
valid_results = [r for r in results if "error" not in r and r['total_ret'] is not None]
if valid_results:
    avg_ret = sum(r['total_ret'] for r in valid_results) / len(valid_results)
    positive_count = sum(1 for r in valid_results if r['total_ret'] > 0)
    negative_count = sum(1 for r in valid_results if r['total_ret'] <= 0)
    
    print(f"\n统计信息:")
    print(f"  平均收益: {avg_ret:.2f}%")
    print(f"  盈利标的: {positive_count}/{len(valid_results)}")
    print(f"  亏损标的: {negative_count}/{len(valid_results)}")
    
    # 按收益排序
    sorted_results = sorted(valid_results, key=lambda x: x['total_ret'] if x['total_ret'] is not None else -999, reverse=True)
    print(f"\n收益排名:")
    for i, r in enumerate(sorted_results[:5], 1):
        print(f"  {i}. {r['name']} ({r['symbol']}): {r['total_ret']:.2f}%")

print("=" * 100)

