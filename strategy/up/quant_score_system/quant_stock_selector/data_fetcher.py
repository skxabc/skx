"""
数据获取模块 - 支持A股和港股数据获取
"""
import pandas as pd
import numpy as np
import akshare as ak
import tushare as ts
import yfinance as yf
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import warnings
warnings.filterwarnings('ignore')


class DataFetcher:
    """数据获取类，支持A股和港股"""
    
    def __init__(self, tushare_token: Optional[str] = None):
        """
        初始化数据获取器
        
        Args:
            tushare_token: Tushare API token（可选，用于获取更详细的基本面数据）
        """
        self.tushare_token = tushare_token
        if tushare_token:
            ts.set_token(tushare_token)
            self.pro = ts.pro_api()
    
    def get_stock_list(self, market: str = 'A') -> pd.DataFrame:
        """
        获取股票列表
        
        Args:
            market: 'A' 表示A股，'H' 表示港股，'HGT' 表示港股通
            
        Returns:
            包含股票代码和名称的DataFrame
        """
        if market == 'A':
            # 获取A股列表
            try:
                stock_list = ak.stock_info_a_code_name()
                stock_list.columns = ['code', 'name']
                stock_list['market'] = 'A'
                return stock_list
            except Exception as e:
                print(f"获取A股列表失败: {e}")
                return pd.DataFrame()
        elif market == 'H':
            # 获取港股列表
            import time
            max_retries = 3
            for retry in range(max_retries):
                try:
                    # 使用港股实时行情获取列表
                    stock_list = ak.stock_hk_spot_em()
                    if not stock_list.empty:
                        # 提取代码和名称列
                        if '代码' in stock_list.columns:
                            stock_list = stock_list[['代码', '名称']].copy()
                            stock_list.columns = ['code', 'name']
                        elif 'code' in stock_list.columns:
                            stock_list = stock_list[['code', 'name']].copy()
                        else:
                            # 尝试使用第一列和第二列
                            stock_list = stock_list.iloc[:, [0, 1]].copy()
                            stock_list.columns = ['code', 'name']
                        stock_list['market'] = 'H'
                        return stock_list
                except Exception as e:
                    if retry < max_retries - 1:
                        print(f"   获取港股列表失败（重试 {retry+1}/{max_retries}）: {e}")
                        time.sleep(2)
                    else:
                        print(f"获取港股列表失败: {e}")
            return pd.DataFrame()
        elif market == 'HGT':
            # 获取港股通股票列表
            import time
            max_retries = 3
            for retry in range(max_retries):
                try:
                    # 使用港股通成份股API
                    hgt_list = ak.stock_hk_ggt_components_em()
                    if not hgt_list.empty:
                        # 提取代码和名称列
                        if '代码' in hgt_list.columns:
                            hgt_list = hgt_list[['代码', '名称']].copy()
                            hgt_list.columns = ['code', 'name']
                        elif 'code' in hgt_list.columns:
                            hgt_list = hgt_list[['code', 'name']].copy()
                        else:
                            # 尝试使用第一列和第二列
                            hgt_list = hgt_list.iloc[:, [0, 1]].copy()
                            hgt_list.columns = ['code', 'name']
                        hgt_list['market'] = 'H'
                        print(f"   成功获取 {len(hgt_list)} 只港股通股票")
                        return hgt_list
                    else:
                        # 如果港股通列表为空，降级为获取所有港股
                        print("   港股通列表为空，尝试获取所有港股...")
                        return self.get_stock_list(market='H')
                except Exception as e:
                    if retry < max_retries - 1:
                        print(f"   获取港股通列表失败（重试 {retry+1}/{max_retries}）: {e}")
                        time.sleep(2)
                    else:
                        print(f"获取港股通列表失败: {e}")
                        # 降级为获取所有港股
                        try:
                            print("   尝试获取所有港股...")
                            return self.get_stock_list(market='H')
                        except:
                            return pd.DataFrame()
            return pd.DataFrame()
        else:
            return pd.DataFrame()
    
    def get_stock_kline(self, code: str, market: str = 'A', 
                       start_date: str = None, end_date: str = None,
                       period: str = 'daily') -> pd.DataFrame:
        """
        获取股票K线数据
        
        Args:
            code: 股票代码
            market: 'A' 表示A股，'H' 表示港股
            start_date: 开始日期，格式 'YYYYMMDD'
            end_date: 结束日期，格式 'YYYYMMDD'
            period: 周期，'daily' 表示日线
            
        Returns:
            包含OHLCV数据的DataFrame
        """
        if end_date is None:
            end_date = datetime.now().strftime('%Y%m%d')
        if start_date is None:
            start_date = (datetime.now() - timedelta(days=365)).strftime('%Y%m%d')
        
        try:
            if market == 'A':
                # A股数据
                df = ak.stock_zh_a_hist(symbol=code, period=period, 
                                       start_date=start_date.replace('-', ''),
                                       end_date=end_date.replace('-', ''),
                                       adjust="qfq")
                if df.empty:
                    return pd.DataFrame()
                df.columns = ['date', 'open', 'close', 'high', 'low', 'volume', 
                            'turnover', 'amplitude', 'change_pct', 'change_amount', 
                            'turnover_rate']
                df['date'] = pd.to_datetime(df['date'])
                df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
                df = df.sort_values('date').reset_index(drop=True)
                return df
            elif market == 'H':
                # 港股数据 - 优先使用akshare
                try:
                    # 使用akshare获取港股日线数据
                    import time
                    time.sleep(1)  # 添加延时避免速率限制
                    
                    # akshare港股代码格式：00700 -> 00700
                    df = ak.stock_hk_daily(symbol=code, adjust="qfq")
                    if df.empty:
                        return pd.DataFrame()
                    
                    # 标准化列名
                    if '日期' in df.columns:
                        df = df.rename(columns={'日期': 'date', '开盘': 'open', '收盘': 'close', 
                                               '最高': 'high', '最低': 'low', '成交量': 'volume'})
                    elif 'date' in df.columns:
                        pass  # 已经是标准格式
                    else:
                        # 尝试使用前几列
                        df.columns = ['date', 'open', 'close', 'high', 'low', 'volume'] + list(df.columns[6:])
                    
                    df['date'] = pd.to_datetime(df['date'])
                    df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
                    df = df.sort_values('date').reset_index(drop=True)
                    
                    # 筛选日期范围
                    if start_date:
                        start_dt = pd.to_datetime(start_date)
                        df = df[df['date'] >= start_dt]
                    if end_date:
                        end_dt = pd.to_datetime(end_date)
                        df = df[df['date'] <= end_dt]
                    
                    return df
                except Exception as e1:
                    # 如果akshare失败，尝试yfinance
                    try:
                        if len(code) == 5 and code.startswith('0'):
                            yf_code = code[1:] + '.HK'
                        else:
                            yf_code = code + '.HK'
                        
                        import time
                        time.sleep(2)  # yfinance需要更长延时
                        
                        stock = yf.Ticker(yf_code)
                        df = stock.history(start=start_date, end=end_date)
                        if df.empty:
                            return pd.DataFrame()
                        df = df.reset_index()
                        df.columns = [col.lower() if col != 'Date' else 'date' for col in df.columns]
                        df['date'] = pd.to_datetime(df['date'])
                        df = df[['date', 'open', 'high', 'low', 'close', 'volume']]
                        df = df.sort_values('date').reset_index(drop=True)
                        return df
                    except Exception as e2:
                        print(f"获取 {code} K线数据失败 (akshare: {e1}, yfinance: {e2})")
                        return pd.DataFrame()
        except Exception as e:
            print(f"获取 {code} K线数据失败: {e}")
            return pd.DataFrame()
    
    def get_stock_basic_info(self, code: str, market: str = 'A') -> Dict:
        """
        获取股票基本信息（市值、基本面等）
        
        Args:
            code: 股票代码
            market: 'A' 表示A股，'H' 表示港股
            
        Returns:
            包含基本信息的字典
        """
        info = {
            'code': code,
            'market': market,
            'market_cap': 0,  # 市值（亿元）
            'pe_ratio': None,  # 市盈率
            'pb_ratio': None,  # 市净率
            'roe': None,  # 净资产收益率
            'revenue_growth': None,  # 营收增长率
            'profit_growth': None,  # 利润增长率
        }
        
        try:
            if market == 'A':
                # A股基本信息
                stock_info = ak.stock_individual_info_em(symbol=code)
                if not stock_info.empty:
                    info_dict = dict(zip(stock_info['item'], stock_info['value']))
                    
                    # 提取市值
                    if '总市值' in info_dict:
                        market_cap_str = str(info_dict['总市值'])
                        if '亿' in market_cap_str:
                            info['market_cap'] = float(market_cap_str.replace('亿', ''))
                        elif '万' in market_cap_str:
                            info['market_cap'] = float(market_cap_str.replace('万', '')) / 10000
                    
                    # 提取PE
                    if '市盈率' in info_dict:
                        pe_str = str(info_dict['市盈率'])
                        try:
                            info['pe_ratio'] = float(pe_str)
                        except:
                            pass
                    
                    # 提取PB
                    if '市净率' in info_dict:
                        pb_str = str(info_dict['市净率'])
                        try:
                            info['pb_ratio'] = float(pb_str)
                        except:
                            pass
                
                # 获取财务数据（成长性指标）
                try:
                    financial_data = ak.stock_financial_abstract_ths(symbol=code)
                    if not financial_data.empty and len(financial_data) >= 2:
                        # 计算营收增长率
                        revenue_cols = [col for col in financial_data.columns if '营业收入' in str(col)]
                        if revenue_cols:
                            revenues = financial_data[revenue_cols[0]].dropna()
                            if len(revenues) >= 2:
                                info['revenue_growth'] = ((revenues.iloc[-1] - revenues.iloc[-2]) / 
                                                         abs(revenues.iloc[-2])) * 100
                        
                        # 计算利润增长率
                        profit_cols = [col for col in financial_data.columns if '净利润' in str(col)]
                        if profit_cols:
                            profits = financial_data[profit_cols[0]].dropna()
                            if len(profits) >= 2:
                                info['profit_growth'] = ((profits.iloc[-1] - profits.iloc[-2]) / 
                                                        abs(profits.iloc[-2])) * 100
                except:
                    pass
                    
            elif market == 'H':
                # 港股基本信息 - 优先使用akshare
                import time
                try:
                    # 尝试使用akshare获取港股基本信息
                    time.sleep(0.5)
                    stock_info = ak.stock_hk_spot_em()
                    if not stock_info.empty:
                        # 查找对应股票
                        code_col = None
                        for col in stock_info.columns:
                            if '代码' in str(col) or 'code' in str(col).lower():
                                code_col = col
                                break
                        
                        if code_col:
                            stock_row = stock_info[stock_info[code_col] == code]
                            if not stock_row.empty:
                                # 提取市值等信息
                                for col in stock_info.columns:
                                    val = stock_row[col].iloc[0] if col in stock_row.columns else None
                                    if pd.notna(val):
                                        val_str = str(val)
                                        # 市值
                                        if '市值' in str(col) or 'market' in str(col).lower():
                                            if '亿' in val_str:
                                                try:
                                                    info['market_cap'] = float(val_str.replace('亿', '').replace(',', ''))
                                                except:
                                                    pass
                                        # PE
                                        if '市盈率' in str(col) or 'pe' in str(col).lower():
                                            try:
                                                info['pe_ratio'] = float(val_str.replace(',', ''))
                                            except:
                                                pass
                                        # PB
                                        if '市净率' in str(col) or 'pb' in str(col).lower():
                                            try:
                                                info['pb_ratio'] = float(val_str.replace(',', ''))
                                            except:
                                                pass
                except Exception as e1:
                    pass
                
                # 如果akshare失败，尝试yfinance（但需要更长延时）
                if info['market_cap'] == 0:
                    try:
                        if len(code) == 5 and code.startswith('0'):
                            yf_code = code[1:] + '.HK'
                        else:
                            yf_code = code + '.HK'
                        
                        time.sleep(2)  # yfinance需要更长延时
                        
                        stock = yf.Ticker(yf_code)
                        info_dict = stock.info
                        
                        if 'marketCap' in info_dict:
                            info['market_cap'] = info_dict['marketCap'] / 1e8  # 转换为亿元
                        if 'trailingPE' in info_dict:
                            info['pe_ratio'] = info_dict['trailingPE']
                        if 'priceToBook' in info_dict:
                            info['pb_ratio'] = info_dict['priceToBook']
                        if 'returnOnEquity' in info_dict:
                            info['roe'] = info_dict['returnOnEquity'] * 100
                        
                        # 获取财务数据计算增长率
                        try:
                            financials = stock.financials
                            if not financials.empty and 'Total Revenue' in financials.index:
                                revenues = financials.loc['Total Revenue'].dropna()
                                if len(revenues) >= 2:
                                    info['revenue_growth'] = ((revenues.iloc[0] - revenues.iloc[1]) / 
                                                             abs(revenues.iloc[1])) * 100
                        except:
                            pass
                    except Exception as e2:
                        # 如果都失败，至少尝试从K线数据估算市值
                        pass
                    
        except Exception as e:
            print(f"获取 {code} 基本信息失败: {e}")
        
        return info
    
    def calculate_volatility(self, kline_df: pd.DataFrame, window: int = 20) -> float:
        """
        计算波动率
        
        Args:
            kline_df: K线数据
            window: 计算窗口
            
        Returns:
            波动率（年化）
        """
        if kline_df.empty or len(kline_df) < window:
            return 0.0
        
        try:
            returns = kline_df['close'].pct_change().dropna()
            if len(returns) < window:
                return 0.0
            volatility = returns.tail(window).std() * np.sqrt(252) * 100  # 年化波动率
            return volatility
        except:
            return 0.0

