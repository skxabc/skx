"""
对比突破前高策略中，回看10天和20天的效果
"""
import subprocess
import sys
import re

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

results_10 = []
results_20 = []

print("=" * 100)
print("对比测试：突破前高策略 - 回看10天 vs 回看20天")
print("=" * 100)

# 测试回看10天
print("\n【测试1：回看10天】")
print("-" * 100)
for name, symbol in stocks:
    print(f"测试: {name} ({symbol})")
    cmd = [
        sys.executable,
        "ma_cross_inside_bar_strategy.py",
        "--symbol", symbol,
        "--username", username,
        "--password", password,
        "--high-lookback", "10",
        "--trend-ma", "0",
        "--vol-mult", "0",
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
        
        total_ret = None
        success_rate = None
        trade_count = None
        
        ret_match = re.search(r'总收益\s+([-\d.]+)%', output)
        if ret_match:
            total_ret = float(ret_match.group(1))
        
        sr_match = re.search(r'胜率:\s+([\d.]+)%', output)
        if sr_match:
            success_rate = float(sr_match.group(1))
        
        tc_match = re.search(r'成交轮数\(买卖对\):\s+(\d+)', output)
        if tc_match:
            trade_count = int(tc_match.group(1))
        
        results_10.append({
            "name": name,
            "symbol": symbol,
            "total_ret": total_ret,
            "success_rate": success_rate,
            "trade_count": trade_count,
        })
        print(f"  ✓ {name}: 收益 {total_ret:.2f}%")
    except Exception as e:
        print(f"  ✗ {name}: 错误 - {e}")
        results_10.append({
            "name": name,
            "symbol": symbol,
            "error": str(e)
        })

# 测试回看20天
print("\n【测试2：回看20天】")
print("-" * 100)
for name, symbol in stocks:
    print(f"测试: {name} ({symbol})")
    cmd = [
        sys.executable,
        "ma_cross_inside_bar_strategy.py",
        "--symbol", symbol,
        "--username", username,
        "--password", password,
        "--high-lookback", "20",
        "--trend-ma", "0",
        "--vol-mult", "0",
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
        
        total_ret = None
        success_rate = None
        trade_count = None
        
        ret_match = re.search(r'总收益\s+([-\d.]+)%', output)
        if ret_match:
            total_ret = float(ret_match.group(1))
        
        sr_match = re.search(r'胜率:\s+([\d.]+)%', output)
        if sr_match:
            success_rate = float(sr_match.group(1))
        
        tc_match = re.search(r'成交轮数\(买卖对\):\s+(\d+)', output)
        if tc_match:
            trade_count = int(tc_match.group(1))
        
        results_20.append({
            "name": name,
            "symbol": symbol,
            "total_ret": total_ret,
            "success_rate": success_rate,
            "trade_count": trade_count,
        })
        print(f"  ✓ {name}: 收益 {total_ret:.2f}%")
    except Exception as e:
        print(f"  ✗ {name}: 错误 - {e}")
        results_20.append({
            "name": name,
            "symbol": symbol,
            "error": str(e)
        })

# 输出对比结果
print("\n" + "=" * 100)
print("对比结果汇总")
print("=" * 100)
print(f"{'股票名称':<12} {'回看10天收益%':<15} {'回看20天收益%':<15} {'回看10天交易':<15} {'回看20天交易':<15} {'更优':<10}")
print("-" * 100)

for i in range(len(stocks)):
    name = stocks[i][0]
    r10 = results_10[i]
    r20 = results_20[i]
    
    if "error" in r10 or "error" in r20:
        print(f"{name:<12} {'错误':<15} {'错误':<15}")
    else:
        ret10_str = f"{r10['total_ret']:.2f}%" if r10['total_ret'] is not None else "N/A"
        ret20_str = f"{r20['total_ret']:.2f}%" if r20['total_ret'] is not None else "N/A"
        tc10_str = str(r10['trade_count']) if r10['trade_count'] is not None else "N/A"
        tc20_str = str(r20['trade_count']) if r20['trade_count'] is not None else "N/A"
        
        if r10['total_ret'] is not None and r20['total_ret'] is not None:
            better = "10天" if r10['total_ret'] > r20['total_ret'] else "20天" if r20['total_ret'] > r10['total_ret'] else "持平"
        else:
            better = "N/A"
        
        print(f"{name:<12} {ret10_str:<15} {ret20_str:<15} {tc10_str:<15} {tc20_str:<15} {better:<10}")

print("-" * 100)

# 统计对比
valid_10 = [r for r in results_10 if "error" not in r and r['total_ret'] is not None]
valid_20 = [r for r in results_20 if "error" not in r and r['total_ret'] is not None]

if valid_10 and valid_20:
    avg_10 = sum(r['total_ret'] for r in valid_10) / len(valid_10)
    avg_20 = sum(r['total_ret'] for r in valid_20) / len(valid_20)
    
    win_10 = sum(1 for r in valid_10 if r['total_ret'] > 0)
    win_20 = sum(1 for r in valid_20 if r['total_ret'] > 0)
    
    avg_tc_10 = sum(r['trade_count'] for r in valid_10 if r['trade_count'] is not None) / len([r for r in valid_10 if r['trade_count'] is not None])
    avg_tc_20 = sum(r['trade_count'] for r in valid_20 if r['trade_count'] is not None) / len([r for r in valid_20 if r['trade_count'] is not None])
    
    print(f"\n整体对比:")
    print(f"  平均收益: 回看10天 {avg_10:.2f}% vs 回看20天 {avg_20:.2f}% (差异: {avg_20 - avg_10:+.2f}%)")
    print(f"  盈利标的: 回看10天 {win_10}/{len(valid_10)} vs 回看20天 {win_20}/{len(valid_20)}")
    print(f"  平均交易次数: 回看10天 {avg_tc_10:.1f} vs 回看20天 {avg_tc_20:.1f}")
    
    # 统计哪个参数更优
    better_10 = sum(1 for i in range(len(valid_10)) if valid_10[i]['total_ret'] > valid_20[i]['total_ret'])
    better_20 = sum(1 for i in range(len(valid_20)) if valid_20[i]['total_ret'] > valid_10[i]['total_ret'])
    
    print(f"\n标的对比:")
    print(f"  回看10天更优: {better_10}只")
    print(f"  回看20天更优: {better_20}只")
    
    if avg_20 > avg_10:
        print(f"\n结论: 回看20天平均收益更高 {avg_20 - avg_10:.2f}个百分点")
    elif avg_10 > avg_20:
        print(f"\n结论: 回看10天平均收益更高 {avg_10 - avg_20:.2f}个百分点")
    else:
        print(f"\n结论: 两种参数效果相当")

print("=" * 100)

