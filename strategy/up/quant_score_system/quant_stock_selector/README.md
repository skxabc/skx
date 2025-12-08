# 量化选股系统 - 上升趋势策略

这是一个基于Python的量化选股系统，支持A股和港股（包括港股通）的选股和交易策略回测。

## 功能特点

1. **多市场支持**：支持A股和港股数据获取
2. **智能评分系统**：基于基本面、成长性、波动率、市值等多维度评分
3. **上升趋势策略**：实现特定的K线处理和交易信号生成
4. **策略回测**：对选出的股票进行策略回测，评估效果

## 评分系统

评分系统考虑以下因素：

- **基本面（30%）**：PE、PB、ROE等指标
- **成长性（30%）**：营收增长率、利润增长率
- **波动率（20%）**：适合趋势策略的波动率范围（15-30%最佳）
- **市值（20%）**：市值大于50亿，中小盘股评分更高

## 交易策略规则

1. **持有信号**：如果高点越来越高，持有
2. **清仓信号**：如果跌破前一日低点，清仓
3. **K线过滤**：
   - 如果当日K线被前一日高低点包含住，忽略当日K线
   - 如果当日K线高低点包住前一日K线，忽略前一日K线
   - 后续判断不再考虑被忽略的K线

## 安装依赖

```bash
pip install -r requirements.txt
```

## 使用方法

### 基本使用

```bash
python main.py
```

### 使用Tushare获取更详细数据（可选）

如果需要使用Tushare获取更详细的基本面数据，可以：

1. 注册Tushare账号：https://tushare.pro/
2. 获取Token
3. 修改 `main.py` 中的代码：

```python
tushare_token = "your_tushare_token"
data_fetcher = DataFetcher(tushare_token=tushare_token)
```

## 项目结构

```
quant_stock_selector/
├── data_fetcher.py      # 数据获取模块
├── score_system.py      # 评分系统模块
├── trading_strategy.py  # 交易策略模块
├── main.py             # 主程序
├── requirements.txt    # 依赖包
└── README.md          # 说明文档
```

## 输出文件

程序运行后会生成以下文件（保存在 `output/` 目录）：

1. `selected_stocks_YYYYMMDD_HHMMSS.xlsx` - 选股结果
2. `backtest_results_YYYYMMDD_HHMMSS.xlsx` - 回测结果

## 注意事项

1. **数据获取速度**：由于需要获取大量股票数据，程序运行时间可能较长。建议：
   - 分批处理股票
   - 使用多进程加速
   - 缓存已获取的数据

2. **API限制**：某些数据源可能有API调用频率限制，建议：
   - 添加适当的延时
   - 使用代理或VIP账号

3. **数据准确性**：本系统使用的免费数据源可能存在延迟或不完整的情况，实盘交易前请验证数据准确性。

4. **风险提示**：本系统仅供学习和研究使用，不构成投资建议。实盘交易需谨慎，注意风险控制。

## 自定义配置

可以在 `score_system.py` 中调整评分权重：

```python
self.weights = {
    'fundamental': 0.3,  # 基本面权重
    'growth': 0.3,      # 成长性权重
    'volatility': 0.2,   # 波动率权重
    'market_cap': 0.2,   # 市值权重
}
```

可以在 `score_system.py` 中调整市值阈值：

```python
self.min_market_cap = 50.0  # 最小市值（亿元）
```

## 许可证

MIT License


