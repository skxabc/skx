#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
策略选股逻辑评估分析
分析该量化策略适合什么样的股票特征
"""

import pandas as pd
import numpy as np

# 从回测结果分析
BACKTEST_RESULTS_2YEAR = {
    '国泰君安国际': {'return': -86.39, 'win_rate': 14.29, 'trades': 84, 'max_profit': 128.93, 'max_loss': -17.01},
    '中国光大控股': {'return': -213.95, 'win_rate': 18.25, 'trades': 126, 'max_profit': 51.41, 'max_loss': -15.53},
    '小米集团': {'return': -371.96, 'win_rate': 24.03, 'trades': 154, 'max_profit': 35.79, 'max_loss': -11.70},
    '众安在线': {'return': -407.16, 'win_rate': 15.44, 'trades': 136, 'max_profit': 59.96, 'max_loss': -20.75},
    '德林控股': {'return': -417.26, 'win_rate': 10.53, 'trades': 114, 'max_profit': 22.59, 'max_loss': -23.23},
    '瑞声科技': {'return': -558.51, 'win_rate': 17.72, 'trades': 158, 'max_profit': 25.00, 'max_loss': -18.29},
    '李宁': {'return': -594.48, 'win_rate': 15.58, 'trades': 154, 'max_profit': 36.45, 'max_loss': -26.12},
    '趣志集团': {'return': -615.70, 'win_rate': 16.13, 'trades': 124, 'max_profit': 22.08, 'max_loss': -84.48}
}

BACKTEST_RESULTS_1YEAR = {
    '国泰君安国际': {'return': 55.25, 'win_rate': 20.00, 'trades': 15, 'max_profit': 118.75, 'max_loss': -14.33}
}


def analyze_strategy_characteristics():
    """分析策略特征"""
    print("="*80)
    print("策略特征分析")
    print("="*80)
    
    print("\n【策略核心逻辑】")
    print("1. 买入信号：高点突破前一根有效K线高点")
    print("2. 卖出信号：跌破前一根有效K线低点")
    print("3. K线包含处理：过滤被包含的K线，只关注关键突破点")
    
    print("\n【策略类型】")
    print("✓ 趋势跟踪策略（Trend Following）")
    print("✓ 突破策略（Breakout Strategy）")
    print("✓ 动量策略（Momentum Strategy）")
    
    print("\n【策略特点】")
    print("✓ 适合有明显趋势的市场")
    print("✓ 需要较大的价格波动空间")
    print("✓ 胜率低但单笔盈利可能很大")
    print("✗ 不适合震荡市场")
    print("✗ 频繁交易，交易成本高")
    print("✗ 在下跌趋势中表现差")


def analyze_stock_characteristics():
    """分析适合的股票特征"""
    print("\n" + "="*80)
    print("适合的股票特征分析")
    print("="*80)
    
    print("\n【1. 波动性要求】")
    print("✓ 需要中等偏高的波动性")
    print("  - 波动太小：难以产生有效突破，交易机会少")
    print("  - 波动太大：假突破多，止损频繁")
    print("  - 理想波动：日波动率 2-5%")
    print("  - 从回测看：最大单笔盈利可达118.75%，说明需要足够波动空间")
    
    print("\n【2. 趋势性要求】")
    print("✓ 需要明显的趋势性")
    print("  - 上涨趋势：策略表现最好（如国泰君安国际过去一年+55.25%）")
    print("  - 下跌趋势：策略表现最差（过去两年全部负收益）")
    print("  - 震荡市场：频繁交易，亏损累积")
    print("  - 理想情况：单边上涨或下跌趋势，避免横盘整理")
    
    print("\n【3. 流动性要求】")
    print("✓ 需要良好的流动性")
    print("  - 日均成交量：建议 > 1000万港币")
    print("  - 买卖价差：越小越好，减少滑点成本")
    print("  - 从回测看：交易频率高（平均每只股票100+次），需要足够流动性")
    
    print("\n【4. 市值特征】")
    print("✓ 适合中大型市值股票")
    print("  - 大型股：趋势相对稳定，但波动可能不足")
    print("  - 中型股：平衡波动性和趋势性（推荐）")
    print("  - 小型股：波动大但趋势不稳定，假突破多")
    print("  - 建议市值：50-500亿港币")
    
    print("\n【5. 行业特征】")
    print("✓ 适合周期性行业和成长性行业")
    print("  - 周期性行业：金融、地产、能源（如国泰君安国际表现较好）")
    print("  - 成长性行业：科技、消费（需要选择趋势明显的个股）")
    print("  - 防御性行业：公用事业、必需消费品（趋势性弱，不推荐）")
    
    print("\n【6. 技术形态要求】")
    print("✓ 适合有明显技术形态的股票")
    print("  - 上升通道：策略表现最佳")
    print("  - 下降通道：需要谨慎，可能持续亏损")
    print("  - 横盘整理：不推荐，频繁交易亏损")
    print("  - 突破形态：策略的核心，适合突破关键阻力位")


def analyze_backtest_results():
    """从回测结果分析"""
    print("\n" + "="*80)
    print("回测结果分析")
    print("="*80)
    
    print("\n【表现最好的股票特征】")
    print("1. 国泰君安国际（过去一年 +55.25%）")
    print("   - 行业：金融（周期性）")
    print("   - 特征：流动性好，波动适中")
    print("   - 交易次数：15次（相对较少，说明趋势明显）")
    print("   - 最大盈利：118.75%（单笔盈利大）")
    
    print("\n【表现最差的股票特征】")
    print("1. 趣志集团（过去两年 -615.70%）")
    print("   - 最大亏损：-84.48%（单笔亏损极大）")
    print("   - 可能原因：波动过大，假突破多")
    
    print("\n【关键发现】")
    print("1. 胜率普遍较低（10-24%），但单笔盈利可能很大")
    print("2. 交易频率高（100+次），说明在震荡市场中频繁交易")
    print("3. 过去一年表现明显好于过去两年，说明市场环境很重要")
    print("4. 金融股（国泰君安国际）表现相对较好")


def generate_stock_selection_criteria():
    """生成选股标准"""
    print("\n" + "="*80)
    print("选股逻辑建议")
    print("="*80)
    
    print("\n【核心选股逻辑】")
    print("="*60)
    print("策略适合：有明显趋势 + 中等波动 + 良好流动性的股票")
    print("="*60)
    
    print("\n【量化选股标准】")
    print("1. 技术指标筛选：")
    print("   ✓ 20日均线斜率 > 0（上升趋势）")
    print("   ✓ 价格在20日均线上方（趋势确认）")
    print("   ✓ 最近20日波动率：2-5%")
    print("   ✓ 最近20日最大涨幅 > 10%（有突破潜力）")
    
    print("\n2. 基本面筛选：")
    print("   ✓ 市值：50-500亿港币")
    print("   ✓ 日均成交额 > 1000万港币")
    print("   ✓ 行业：周期性或成长性行业")
    print("   ✓ 避免：公用事业、必需消费品等防御性行业")
    
    print("\n3. 市场环境筛选：")
    print("   ✓ 市场整体处于上升趋势")
    print("   ✓ 避免市场横盘整理期")
    print("   ✓ 关注市场波动率，避免极端波动期")
    
    print("\n【选股流程】")
    print("步骤1：筛选技术形态良好的股票（上升趋势）")
    print("步骤2：筛选波动性适中的股票（2-5%）")
    print("步骤3：筛选流动性良好的股票（成交额>1000万）")
    print("步骤4：筛选市值合适的股票（50-500亿）")
    print("步骤5：结合行业特征，选择周期性或成长性行业")
    print("步骤6：回测验证，选择回测表现较好的股票")
    
    print("\n【不适合的股票类型】")
    print("✗ 横盘整理的股票（频繁交易，亏损累积）")
    print("✗ 波动过小的股票（交易机会少）")
    print("✗ 波动过大的股票（假突破多，止损频繁）")
    print("✗ 流动性差的股票（滑点成本高）")
    print("✗ 防御性行业股票（趋势性弱）")
    print("✗ 处于明显下跌趋势的股票（持续亏损）")


def generate_recommendations():
    """生成优化建议"""
    print("\n" + "="*80)
    print("策略优化建议")
    print("="*80)
    
    print("\n【选股层面优化】")
    print("1. 添加趋势过滤：")
    print("   - 只选择20日均线向上的股票")
    print("   - 只选择价格在均线上方的股票")
    print("   - 避免在下跌趋势中使用策略")
    
    print("\n2. 添加波动性过滤：")
    print("   - 计算历史波动率，选择波动适中的股票")
    print("   - 避免波动过大或过小的股票")
    
    print("\n3. 添加成交量确认：")
    print("   - 突破时成交量放大，增加信号可靠性")
    print("   - 避免低成交量突破（可能是假突破）")
    
    print("\n【策略层面优化】")
    print("1. 优化止损机制：")
    print("   - 当前：跌破前低立即止损（可能过早）")
    print("   - 建议：使用ATR（平均真实波幅）设置止损")
    print("   - 或使用百分比止损（如-5%）")
    
    print("\n2. 添加趋势确认：")
    print("   - 结合移动平均线确认趋势")
    print("   - 只在趋势明确时交易")
    
    print("\n3. 减少交易频率：")
    print("   - 添加最小持仓时间限制")
    print("   - 避免在震荡市场中频繁交易")
    
    print("\n【风险管理建议】")
    print("1. 仓位管理：")
    print("   - 单只股票仓位不超过20%")
    print("   - 分散投资，降低单只股票风险")
    
    print("\n2. 市场环境判断：")
    print("   - 在上升趋势市场中使用策略")
    print("   - 在震荡或下跌市场中暂停或减少交易")
    
    print("\n3. 止损止盈：")
    print("   - 设置固定止损（如-5%）")
    print("   - 设置移动止盈（保护利润）")


def main():
    """主函数"""
    analyze_strategy_characteristics()
    analyze_stock_characteristics()
    analyze_backtest_results()
    generate_stock_selection_criteria()
    generate_recommendations()
    
    print("\n" + "="*80)
    print("总结")
    print("="*80)
    print("\n该策略最适合：")
    print("✓ 有明显上升趋势的股票")
    print("✓ 中等波动性（日波动2-5%）")
    print("✓ 良好流动性（日均成交>1000万）")
    print("✓ 中大型市值（50-500亿）")
    print("✓ 周期性或成长性行业")
    print("✓ 在上升趋势市场中使用")
    print("\n该策略不适合：")
    print("✗ 横盘整理的股票")
    print("✗ 波动过大或过小的股票")
    print("✗ 流动性差的股票")
    print("✗ 防御性行业股票")
    print("✗ 下跌趋势中的股票")
    print("="*80)


if __name__ == '__main__':
    main()

