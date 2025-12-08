"""
市场数据获取模块 - 获取A股和港股主要指数数据
支持多个数据源，按优先级自动切换
"""
import pandas as pd
import numpy as np
import akshare as ak
from datetime import datetime, timedelta
from typing import Optional, Dict
import warnings
import time
import os
warnings.filterwarnings('ignore')

# 尝试导入tushare（可选）
try:
    import tushare as ts
    TUSHARE_AVAILABLE = True
except ImportError:
    TUSHARE_AVAILABLE = False

# 尝试导入yfinance（可选）
try:
    import yfinance as yf
    YFINANCE_AVAILABLE = True
except ImportError:
    YFINANCE_AVAILABLE = False


class MarketDataFetcher:
    """市场数据获取类，支持多数据源"""
    
    # A股主要指数代码（包含tushare代码映射）
    A_SHARE_INDICES = {
        'sh': {'code': '000001', 'name': '上证指数', 'ts_code': '000001.SH'},
        'sz': {'code': '399001', 'name': '深证成指', 'ts_code': '399001.SZ'},
        'cyb': {'code': '399006', 'name': '创业板指', 'ts_code': '399006.SZ'},
        'hs300': {'code': '000300', 'name': '沪深300', 'ts_code': '000300.SH'},
    }
    
    # 港股主要指数代码
    HK_INDICES = {
        'hsi': {'code': 'HSI', 'name': '恒生指数', 'yf_code': '^HSI'},
        'hsc': {'code': 'HSCEI', 'name': '恒生国企指数', 'yf_code': '^HSCE'},
        'hsci': {'code': 'HSCI', 'name': '恒生科技指数', 'yf_code': '^HSTECH'},
    }
    
    def __init__(self, tushare_token: Optional[str] = None):
        """
        初始化市场数据获取器
        
        Args:
            tushare_token: Tushare API token（可选，但强烈推荐使用以获得更稳定的数据）
                          获取方式：https://tushare.pro/register?reg=1
        """
        self.tushare_pro = None
        if tushare_token:
            if TUSHARE_AVAILABLE:
                ts.set_token(tushare_token)
                self.tushare_pro = ts.pro_api()
                print("✓ Tushare已初始化，将优先使用Tushare数据源")
            else:
                print("⚠️  Tushare未安装，请运行: pip install tushare")
        elif TUSHARE_AVAILABLE:
            # 尝试从环境变量读取
            token = os.getenv('TUSHARE_TOKEN')
            if token:
                ts.set_token(token)
                self.tushare_pro = ts.pro_api()
                print("✓ 从环境变量读取Tushare token")
            else:
                print("⚠️  未提供Tushare token，将使用免费数据源（可能不稳定）")
                print("   建议：注册Tushare获取token: https://tushare.pro/register?reg=1")
    
    def get_index_data(self, index_code: str, market: str = 'A', 
                      days: int = 250) -> Optional[pd.DataFrame]:
        """
        获取指数K线数据
        
        Args:
            index_code: 指数代码
            market: 'A' 表示A股，'H' 表示港股
            days: 获取最近多少天的数据
            
        Returns:
            包含OHLCV数据的DataFrame，列名：date, open, high, low, close, volume
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)
        
        try:
            if market == 'A':
                return self._get_a_share_index(index_code, start_date, end_date)
            elif market == 'H':
                return self._get_hk_index(index_code, start_date, end_date)
            else:
                print(f"不支持的市场类型: {market}")
                return None
        except Exception as e:
            print(f"获取指数数据失败 {index_code}: {e}")
            return None
    
    def _get_a_share_index(self, index_code: str, 
                          start_date: datetime, 
                          end_date: datetime) -> Optional[pd.DataFrame]:
        """
        获取A股指数数据
        按优先级尝试：1. Tushare（最稳定） 2. akshare（免费但可能不稳定）
        """
        start_str = start_date.strftime('%Y%m%d')
        end_str = end_date.strftime('%Y%m%d')
        
        # 方法1：优先使用Tushare（最稳定）
        if self.tushare_pro:
            try:
                # 查找对应的tushare代码
                ts_code = None
                for key, info in self.A_SHARE_INDICES.items():
                    if info['code'] == index_code:
                        ts_code = info.get('ts_code')
                        break
                
                if ts_code:
                    print(f"  使用Tushare数据源...")
                    # 尝试使用index_daily接口
                    try:
                        df = self.tushare_pro.index_daily(ts_code=ts_code, 
                                                          start_date=start_str,
                                                          end_date=end_str)
                        if not df.empty:
                            # 标准化列名
                            df = df.rename(columns={
                                'trade_date': 'date',
                                'open': 'open',
                                'high': 'high',
                                'low': 'low',
                                'close': 'close',
                                'vol': 'volume'
                            })
                            df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
                            df = df.sort_values('date').reset_index(drop=True)
                            return self._process_dataframe(df)
                    except Exception as e1:
                        # 如果index_daily没有权限，尝试使用其他接口
                        # 注意：免费版可能没有指数日线数据权限，直接跳过
                        print(f"  Tushare index_daily接口无权限，尝试备用数据源...")
                        pass
            except Exception as e:
                print(f"  Tushare获取失败: {e}，尝试备用数据源...")
        
        # 方法2：使用akshare（免费但可能不稳定）
        max_retries = 3
        retry_delay = 2  # 秒
        
        for attempt in range(max_retries):
            try:
                print(f"  使用akshare数据源...")
                # 根据指数代码判断是哪个交易所
                if index_code.startswith('000'):
                    # 上交所指数
                    df = ak.index_zh_a_hist(symbol=index_code, period="daily",
                                           start_date=start_str, end_date=end_str)
                elif index_code.startswith('399'):
                    # 深交所指数
                    df = ak.index_zh_a_hist(symbol=index_code, period="daily",
                                           start_date=start_str, end_date=end_str)
                else:
                    print(f"不支持的A股指数代码: {index_code}")
                    return None
                
                if df.empty:
                    if attempt < max_retries - 1:
                        time.sleep(retry_delay)
                        continue
                    return None
                
                # 如果成功获取数据，跳出循环
                break
                
            except Exception as e:
                if attempt < max_retries - 1:
                    print(f"  获取失败，{retry_delay}秒后重试 ({attempt+1}/{max_retries})...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # 指数退避
                else:
                    print(f"获取A股指数数据失败 {index_code}: {e}")
                    return None
        
        # 处理数据
        return self._process_dataframe(df, index_code)
    
    def _process_dataframe(self, df: pd.DataFrame, index_code: str = None) -> Optional[pd.DataFrame]:
        """统一处理DataFrame，标准化列名和数据类型"""
        try:
            # 标准化列名
            column_mapping = {
                '日期': 'date',
                '开盘': 'open',
                '收盘': 'close',
                '最高': 'high',
                '最低': 'low',
                '成交量': 'volume',
                '成交额': 'amount'
            }
            
            for old_col, new_col in column_mapping.items():
                if old_col in df.columns:
                    df = df.rename(columns={old_col: new_col})
            
            # 确保有必要的列
            required_cols = ['date', 'open', 'high', 'low', 'close']
            if not all(col in df.columns for col in required_cols):
                # 尝试使用位置索引
                if len(df.columns) >= 5:
                    df.columns = ['date', 'open', 'close', 'high', 'low'] + list(df.columns[5:])
            
            # 处理日期列
            if 'date' in df.columns:
                if df['date'].dtype == 'object':
                    # 尝试多种日期格式
                    try:
                        df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
                    except:
                        df['date'] = pd.to_datetime(df['date'])
            
            # 确保数值列为数值类型
            for col in ['open', 'close', 'high', 'low']:
                if col in df.columns:
                    df[col] = pd.to_numeric(df[col], errors='coerce')
            
            # 如果有volume列，也转换为数值
            if 'volume' in df.columns:
                df['volume'] = pd.to_numeric(df['volume'], errors='coerce')
            
            df = df.dropna(subset=['open', 'close', 'high', 'low'])
            df = df.sort_values('date').reset_index(drop=True)
            
            # 只返回必要的列
            result_cols = ['date', 'open', 'high', 'low', 'close']
            if 'volume' in df.columns:
                result_cols.append('volume')
            
            return df[result_cols]
            
        except Exception as e:
            if index_code:
                print(f"处理指数数据失败 {index_code}: {e}")
            return None
    
    def _get_hk_index(self, index_code: str,
                     start_date: datetime,
                     end_date: datetime) -> Optional[pd.DataFrame]:
        """
        获取港股指数数据
        按优先级尝试：1. Tushare（如果可用） 2. yfinance
        """
        start_str = start_date.strftime('%Y%m%d')
        end_str = end_date.strftime('%Y%m%d')
        
        # 方法1：优先使用Tushare（如果可用）
        if self.tushare_pro:
            try:
                # Tushare港股指数代码映射
                ts_code_map = {
                    'HSI': 'HSI.HI',
                    'HSCEI': 'HSCEI.HI',
                    'HSCI': 'HSCI.HI',
                }
                
                if index_code in ts_code_map:
                    print(f"  使用Tushare数据源...")
                    try:
                        df = self.tushare_pro.index_daily(ts_code=ts_code_map[index_code],
                                                          start_date=start_str,
                                                          end_date=end_str)
                        if not df.empty:
                            df = df.rename(columns={
                                'trade_date': 'date',
                                'open': 'open',
                                'high': 'high',
                                'low': 'low',
                                'close': 'close',
                                'vol': 'volume'
                            })
                            df['date'] = pd.to_datetime(df['date'], format='%Y%m%d')
                            df = df.sort_values('date').reset_index(drop=True)
                            return self._process_dataframe(df)
                    except Exception as e1:
                        # 如果index_daily没有权限，直接跳过
                        print(f"  Tushare index_daily接口无权限，尝试备用数据源...")
                        pass
            except Exception as e:
                print(f"  Tushare获取失败: {e}，尝试备用数据源...")
        
        # 方法2：使用yfinance
        if not YFINANCE_AVAILABLE:
            print("  yfinance未安装，无法获取港股数据")
            return None
        
        max_retries = 3
        retry_delay = 5  # 秒，yfinance需要更长延时
        
        # yfinance港股指数代码映射
        symbol_map = {
            'HSI': '^HSI',      # 恒生指数
            'HSCEI': '^HSCE',   # 恒生国企指数
            'HSCI': '^HSTECH',  # 恒生科技指数
        }
        
        if index_code not in symbol_map:
            print(f"不支持的港股指数代码: {index_code}")
            return None
        
        for attempt in range(max_retries):
            try:
                print(f"  使用yfinance数据源...")
                # 使用yfinance获取港股指数数据
                ticker = yf.Ticker(symbol_map[index_code])
                df = ticker.history(start=start_date, end=end_date)
                
                if df.empty:
                    if attempt < max_retries - 1:
                        print(f"  数据为空，{retry_delay}秒后重试 ({attempt+1}/{max_retries})...")
                        time.sleep(retry_delay)
                        retry_delay *= 2
                        continue
                    return None
                
                # 如果成功获取数据，跳出循环
                break
                
            except Exception as e:
                error_msg = str(e)
                if "Rate limited" in error_msg or "Too Many Requests" in error_msg:
                    if attempt < max_retries - 1:
                        wait_time = retry_delay * (attempt + 1)  # 递增等待时间
                        print(f"  请求过于频繁，等待{wait_time}秒后重试 ({attempt+1}/{max_retries})...")
                        time.sleep(wait_time)
                        retry_delay *= 2
                    else:
                        print(f"获取港股指数数据失败 {index_code}: {e}")
                        return None
                else:
                    if attempt < max_retries - 1:
                        print(f"  获取失败，{retry_delay}秒后重试 ({attempt+1}/{max_retries})...")
                        time.sleep(retry_delay)
                        retry_delay *= 2
                    else:
                        print(f"获取港股指数数据失败 {index_code}: {e}")
                        return None
        
        # 处理yfinance返回的数据
        try:
            # 转换数据格式
            df = df.reset_index()
            if 'Date' in df.columns:
                df['date'] = pd.to_datetime(df['Date'])
            elif 'Datetime' in df.columns:
                df['date'] = pd.to_datetime(df['Datetime'])
            else:
                df['date'] = pd.to_datetime(df.index)
            
            # 标准化列名
            column_mapping = {
                'Open': 'open',
                'High': 'high',
                'Low': 'low',
                'Close': 'close',
                'Volume': 'volume'
            }
            
            for old_col, new_col in column_mapping.items():
                if old_col in df.columns:
                    df = df.rename(columns={old_col: new_col})
            
            return self._process_dataframe(df, index_code)
            
        except Exception as e:
            print(f"处理港股指数数据失败 {index_code}: {e}")
            return None
    
    def get_market_indices(self, market: str = 'A') -> Dict[str, pd.DataFrame]:
        """
        获取市场主要指数数据
        
        Args:
            market: 'A' 表示A股，'H' 表示港股
            
        Returns:
            字典，key为指数简称，value为DataFrame
        """
        indices = self.A_SHARE_INDICES if market == 'A' else self.HK_INDICES
        result = {}
        
        for key, index_info in indices.items():
            print(f"正在获取 {index_info['name']} ({index_info['code']}) 数据...")
            df = self.get_index_data(index_info['code'], market=market)
            if df is not None and not df.empty:
                result[key] = df
                print(f"  ✓ {index_info['name']} 数据获取成功，共 {len(df)} 条记录")
            else:
                print(f"  ✗ {index_info['name']} 数据获取失败")
            
            # 避免请求过快，不同市场使用不同延时
            if market == 'A':
                time.sleep(1)  # A股数据源需要更长延时
            else:
                time.sleep(2)  # 港股yfinance需要更长延时避免限流
        
        return result

