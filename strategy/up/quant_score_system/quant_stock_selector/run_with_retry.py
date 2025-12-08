"""
带重试机制的港股通选股脚本
如果遇到API限制，会自动等待后重试
"""
import time
import sys
from select_hgt_stocks_manual import main as run_selection

def main_with_retry(max_retries=3, wait_time=60):
    """带重试的主函数"""
    for attempt in range(max_retries):
        print(f"\n{'='*60}")
        print(f"尝试运行选股系统 (第 {attempt+1}/{max_retries} 次)")
        print(f"{'='*60}\n")
        
        try:
            run_selection()
            print("\n选股完成！")
            return
        except KeyboardInterrupt:
            print("\n用户中断")
            return
        except Exception as e:
            print(f"\n运行出错: {e}")
            if attempt < max_retries - 1:
                print(f"\n等待 {wait_time} 秒后重试...")
                time.sleep(wait_time)
            else:
                print("\n已达到最大重试次数，请稍后再试")
                print("建议：")
                print("1. 等待更长时间（10-15分钟）后重试")
                print("2. 检查网络连接")
                print("3. 考虑使用付费数据源")

if __name__ == "__main__":
    # 如果遇到速率限制，等待5分钟后重试
    main_with_retry(max_retries=2, wait_time=300)


