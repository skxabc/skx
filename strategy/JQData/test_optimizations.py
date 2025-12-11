"""
测试各个优化项对收益的影响
"""
import subprocess
import sys

def run_test(name, args):
    """运行回测并提取总收益"""
    cmd = [
        sys.executable,
        "ma_cross_inside_bar_strategy.py",
        "--symbol", "000001.XSHE"
    ] + args
    result = subprocess.run(cmd, capture_output=True, text=True, cwd="/home/shikaixun/shikaixun_HDD/home/shikaixun/Code/skx/skxtest/skx/strategy/JQData")
    output = result.stdout + result.stderr
    # 提取总收益
    for line in output.split('\n'):
        if '总收益' in line:
            return line.strip()
    return "未找到收益信息"

print("=" * 60)
print("测试各个优化项对收益的影响")
print("=" * 60)

# 1. 基准版本（所有优化开启）
print("\n1. 基准版本（所有优化开启）")
print(run_test("基准", []))

# 2. 关闭趋势过滤
print("\n2. 关闭趋势过滤（--trend-ma 0）")
print(run_test("无趋势过滤", ["--trend-ma", "0"]))

# 3. 关闭量能过滤
print("\n3. 关闭量能过滤（--vol-mult 0）")
print(run_test("无量能过滤", ["--vol-mult", "0"]))

# 4. 关闭ATR追踪止损
print("\n4. 关闭ATR追踪止损（--atr-mult 9999，相当于无效）")
print(run_test("无ATR止损", ["--atr-mult", "9999"]))

# 5. 关闭手续费和滑点（看理论收益）
print("\n5. 关闭手续费和滑点（--fee-rate 0 --slippage-bp 0）")
print(run_test("无成本", ["--fee-rate", "0", "--slippage-bp", "0"]))

# 6. 只保留趋势过滤
print("\n6. 只保留趋势过滤（关闭量能和ATR）")
print(run_test("仅趋势", ["--vol-mult", "0", "--atr-mult", "9999"]))

# 7. 只保留量能过滤
print("\n7. 只保留量能过滤（关闭趋势和ATR）")
print(run_test("仅量能", ["--trend-ma", "0", "--atr-mult", "9999"]))

# 8. 只保留ATR止损
print("\n8. 只保留ATR止损（关闭趋势和量能）")
print(run_test("仅ATR", ["--trend-ma", "0", "--vol-mult", "0"]))

print("\n" + "=" * 60)
print("测试完成")
print("=" * 60)

