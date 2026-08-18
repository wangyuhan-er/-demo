# ============================================================
# 理财服务智能推荐系统 - 最终版
# 功能：用户画像设置 → 产品浏览 → 收藏夹（购买入口）→ 产品PK对比（纯对比）
# 产品池：PR1 10只 + PR2 10只 = 20只（无PR3、无混合类）
# 运行方式：streamlit run理财服务_demo.py
# ============================================================

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# ============================================================
# 一、页面配置
# ============================================================

st.set_page_config(
    page_title="理财服务智能推荐",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# 二、CSS样式（简洁为主，无需额外复杂样式）
# ============================================================

st.markdown("""
<style>
    .profile-bar {
        background: #f0f5ff;
        border-radius: 12px;
        padding: 14px 24px;
        margin-bottom: 16px;
        border: 1px solid #d0ddee;
        display: flex;
        justify-content: space-between;
        align-items: center;
        flex-wrap: wrap;
        gap: 10px;
    }
    .profile-item { display: flex; align-items: center; gap: 6px; font-size: 14px; color: #1a3c6e; }
    .profile-item .label { color: #6b7a8f; font-weight: 400; }
    .profile-item .value { font-weight: 600; color: #1a3c6e; }
    .profile-item .badge {
        background: #1a3c6e; color: white; padding: 2px 12px;
        border-radius: 12px; font-size: 12px; font-weight: 600;
    }
    .clickable { cursor: pointer; color: #1a3c6e; text-decoration: underline; }
    .holding-card {
        background: #f8faff; border-radius: 8px; padding: 12px 16px;
        border: 1px solid #d0ddee; margin-top: 8px;
    }
    .holding-card .h-name { font-weight: 600; color: #1a3c6e; }
    .holding-card .h-info { font-size: 13px; color: #555; margin-top: 4px; }
    .product-card {
        background: white; border-radius: 10px; padding: 16px 18px;
        border: 1px solid #e8ecf2; box-shadow: 0 2px 4px rgba(0,0,0,0.04);
        transition: 0.2s; height: 100%;
    }
    .product-card:hover { box-shadow: 0 4px 16px rgba(0,0,0,0.08); border-color: #b0c8e0; }
    .product-name { font-size: 15px; font-weight: 600; color: #1a3c6e; }
    .product-code { font-size: 12px; color: #999; margin-bottom: 4px; }
    .product-yield { font-size: 24px; font-weight: 700; color: #2e7d32; }
    .product-yield-label { font-size: 12px; color: #888; }
    .product-tag {
        display: inline-block; padding: 2px 10px; border-radius: 12px;
        font-size: 11px; font-weight: 600; margin-right: 4px;
    }
    .tag-pr1 { background: #e3f2fd; color: #0d47a1; }
    .tag-pr2 { background: #e8f5e9; color: #1b5e20; }
    .product-meta { font-size: 13px; color: #555; margin-top: 6px; line-height: 1.6; }
    .product-meta span { margin-right: 12px; }
    .action-bar {
        position: fixed; bottom: 0; left: 0; right: 0;
        background: white; padding: 10px 24px;
        box-shadow: 0 -4px 20px rgba(0,0,0,0.08);
        border-top: 2px solid #1a3c6e;
        z-index: 1000;
        display: flex; justify-content: space-between; align-items: center;
        flex-wrap: wrap;
        gap: 8px;
    }
    .wishlist-popup {
        background: #f8faff; border-radius: 10px; padding: 12px 16px;
        border: 1px solid #d0ddee; margin-top: 8px;
        max-height: 260px; overflow-y: auto;
    }
    .wishlist-item {
        display: flex; justify-content: space-between; align-items: center;
        padding: 6px 0; border-bottom: 1px solid #eee;
    }
    .wishlist-item:last-child { border-bottom: none; }
    .knowledge-grid {
        display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 10px; margin: 12px 0;
    }
    .knowledge-item {
        background: #f8faff; border-radius: 8px; padding: 12px 16px;
        border: 1px solid #e0e8f0; cursor: pointer; text-align: center;
        transition: 0.2s;
    }
    .knowledge-item:hover { background: #e3ecf5; border-color: #1a3c6e; }
    .knowledge-item .term { font-weight: 600; color: #1a3c6e; font-size: 14px; }
    .knowledge-detail {
        background: #f8faff; border-radius: 10px; padding: 20px 24px;
        border-left: 4px solid #1a3c6e; margin: 12px 0;
    }
    .knowledge-detail .term { font-weight: 700; color: #1a3c6e; font-size: 18px; }
    .knowledge-detail .desc { font-size: 15px; color: #333; margin: 8px 0; white-space: pre-line; }
    .knowledge-detail .ref { font-size: 14px; color: #6b7a8f; }
    .detail-grid {
        display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
        gap: 12px; margin: 12px 0;
    }
    .detail-item {
        background: #f8faff; border-radius: 8px; padding: 12px 16px;
        border: 1px solid #e0e8f0;
    }
    .detail-item .label { font-size: 12px; color: #888; }
    .detail-item .value { font-size: 16px; font-weight: 600; color: #1a3c6e; margin-top: 4px; }
    .footer-note { color: #bbb; font-size: 12px; text-align: center; margin-top: 40px; padding-top: 16px; border-top: 1px solid #eee; }
    .stButton button { border-radius: 6px; font-weight: 500; }
    .stCheckbox label { font-size: 14px; }
    .css-1d391kg { padding-bottom: 80px; }
</style>
""", unsafe_allow_html=True)

# ============================================================
# 三、产品数据库（PR1 10只 + PR2 10只 = 20只）
# ============================================================

PRODUCTS = [
    # ---------- PR1级产品（10只） ----------
    {
        "名称": "工银理财·添利宝鑫享",
        "代码": "21GS2699",
        "风险等级": "PR1",
        "风险标签": "低风险",
        "产品类型": "固定收益类",
        "起购金额": 1,
        "成立以来年化": 2.15,
        "近1月年化": 2.10,
        "流动性": "无固定期限",
        "持有期限": "无固定期限",
        "产品规模": 385,
        "购买人次": "超千万",
        "业绩比较基准": "2.0%-2.5%",
        "单位净值": 1.0215,
        "累计净值": 1.0215,
        "适合人群": "保守型投资者，追求本金安全",
        "投资范围": "主要投资于货币市场工具、债券等低风险资产"
    },
    {
        "名称": "工银理财'添利宝'净值型",
        "代码": "XLT1801",
        "风险等级": "PR1",
        "风险标签": "低风险",
        "产品类型": "固定收益类",
        "起购金额": 1,
        "成立以来年化": 1.95,
        "近1月年化": 1.88,
        "流动性": "无固定期限",
        "持有期限": "无固定期限",
        "产品规模": 200,
        "购买人次": "较高",
        "业绩比较基准": "1.8%-2.3%",
        "单位净值": 1.0150,
        "累计净值": 1.0150,
        "适合人群": "保守型投资者",
        "投资范围": "主要投资于货币市场工具、银行存款等"
    },
    {
        "名称": "工银理财·天天鑫添益",
        "代码": "22G2866B",
        "风险等级": "PR1",
        "风险标签": "低风险",
        "产品类型": "固定收益类",
        "起购金额": 1,
        "成立以来年化": 2.13,
        "近1月年化": 2.10,
        "流动性": "每日开放",
        "持有期限": "无固定期限",
        "产品规模": 120,
        "购买人次": "较高",
        "业绩比较基准": "2.0%-2.6%",
        "单位净值": 1.0320,
        "累计净值": 1.0320,
        "适合人群": "稳健型投资者",
        "投资范围": "主要投资于债券、同业存单等固定收益类资产"
    },
    {
        "名称": "工银理财·添利宝鑫享(2号)",
        "代码": "22GS2699",
        "风险等级": "PR1",
        "风险标签": "低风险",
        "产品类型": "现金管理类",
        "起购金额": 1,
        "成立以来年化": 2.08,
        "近1月年化": 2.05,
        "流动性": "无固定期限",
        "持有期限": "无固定期限",
        "产品规模": 150,
        "购买人次": "较高",
        "业绩比较基准": "1.9%-2.4%",
        "单位净值": 1.0185,
        "累计净值": 1.0185,
        "适合人群": "保守型投资者，需要高流动性",
        "投资范围": "主要投资于现金、银行存款、货币市场基金等"
    },
    {
        "名称": "工银理财·稳益系列",
        "代码": "23GS4001",
        "风险等级": "PR1",
        "风险标签": "低风险",
        "产品类型": "固定收益类",
        "起购金额": 1,
        "成立以来年化": 2.05,
        "近1月年化": 1.98,
        "流动性": "日开",
        "持有期限": "无固定期限",
        "产品规模": 80,
        "购买人次": "中等",
        "业绩比较基准": "1.8%-2.3%",
        "单位净值": 1.0125,
        "累计净值": 1.0125,
        "适合人群": "保守型投资者",
        "投资范围": "主要投资于高等级信用债、利率债等"
    },
    {
        "名称": "工银理财·全球添益系列",
        "代码": "23GS4002",
        "风险等级": "PR1",
        "风险标签": "低风险",
        "产品类型": "固定收益类(QDII)",
        "起购金额": 1,
        "成立以来年化": 2.20,
        "近1月年化": 2.15,
        "流动性": "日开",
        "持有期限": "无固定期限",
        "产品规模": 60,
        "购买人次": "中等",
        "业绩比较基准": "2.0%-2.8%",
        "单位净值": 1.0250,
        "累计净值": 1.0250,
        "适合人群": "稳健型投资者，希望分散境外资产",
        "投资范围": "主要投资于境外固定收益类资产"
    },
    {
        "名称": "工银理财·添利宝现金管理3号",
        "代码": "23GS2067",
        "风险等级": "PR1",
        "风险标签": "低风险",
        "产品类型": "现金管理类",
        "起购金额": 1,
        "成立以来年化": 2.10,
        "近1月年化": 2.05,
        "流动性": "开放净值型",
        "持有期限": "无固定期限",
        "产品规模": 100,
        "购买人次": "较高",
        "业绩比较基准": "1.9%-2.5%",
        "单位净值": 1.0160,
        "累计净值": 1.0160,
        "适合人群": "保守型投资者",
        "投资范围": "主要投资于现金、银行存款、货币市场工具等"
    },
    {
        "名称": "天天盈2号",
        "代码": "22GS2002",
        "风险等级": "PR1",
        "风险标签": "低风险",
        "产品类型": "现金管理类",
        "起购金额": 1,
        "成立以来年化": 2.08,
        "近1月年化": 2.02,
        "流动性": "每日可申赎",
        "持有期限": "无固定期限",
        "产品规模": 180,
        "购买人次": "较高",
        "业绩比较基准": "1.8%-2.4%",
        "单位净值": 1.0140,
        "累计净值": 1.0140,
        "适合人群": "保守型投资者",
        "投资范围": "主要投资于货币市场基金、银行存款等"
    },
    {
        "名称": "工银理财·低波红利策略",
        "代码": "23G2000D",
        "风险等级": "PR1",
        "风险标签": "低风险",
        "产品类型": "固定收益类",
        "起购金额": 1,
        "成立以来年化": 2.15,
        "近1月年化": 2.08,
        "流动性": "每日开放",
        "持有期限": "无固定期限",
        "产品规模": 90,
        "购买人次": "中等",
        "业绩比较基准": "2.0%-2.6%",
        "单位净值": 1.0280,
        "累计净值": 1.0280,
        "适合人群": "稳健型投资者",
        "投资范围": "主要投资于高股息、低波动策略的固定收益类资产"
    },
    {
        "名称": "工银理财·颐享鑫添益366天",
        "代码": "23GS5001",
        "风险等级": "PR1",
        "风险标签": "低风险",
        "产品类型": "固定收益类",
        "起购金额": 1,
        "成立以来年化": 2.45,
        "近1月年化": 2.30,
        "流动性": "持有期产品",
        "持有期限": "366天",
        "产品规模": 40,
        "购买人次": "中等",
        "业绩比较基准": "2.2%-2.8%",
        "单位净值": 1.0350,
        "累计净值": 1.0350,
        "适合人群": "稳健型投资者，可接受一定锁定期的投资者",
        "投资范围": "主要投资于优质信用债、利率债等"
    },
    # ---------- PR2级产品（10只） ----------
    {
        "名称": "工银理财·核心优选14天",
        "代码": "21GS5691",
        "风险等级": "PR2",
        "风险标签": "中低风险",
        "产品类型": "固定收益类",
        "起购金额": 1,
        "成立以来年化": 2.45,
        "近1月年化": 2.50,
        "流动性": "持有后每日可赎",
        "持有期限": "14天",
        "产品规模": 120,
        "购买人次": "较高",
        "业绩比较基准": "2.3%-3.0%",
        "单位净值": 1.0420,
        "累计净值": 1.0420,
        "适合人群": "稳健型投资者",
        "投资范围": "主要投资于信用债、金融债等固定收益类资产"
    },
    {
        "名称": "工银理财·鑫添益7天",
        "代码": "22GS2699",
        "风险等级": "PR2",
        "风险标签": "中低风险",
        "产品类型": "固定收益类",
        "起购金额": 1,
        "成立以来年化": 2.39,
        "近1月年化": 2.82,
        "流动性": "持有后每日可赎",
        "持有期限": "7天",
        "产品规模": 150,
        "购买人次": "较高",
        "业绩比较基准": "2.2%-2.9%",
        "单位净值": 1.0380,
        "累计净值": 1.0380,
        "适合人群": "稳健型投资者",
        "投资范围": "主要投资于短期信用债、同业存单等"
    },
    {
        "名称": "工银理财·鑫添益540天",
        "代码": "23GS5002",
        "风险等级": "PR2",
        "风险标签": "中低风险",
        "产品类型": "固定收益类",
        "起购金额": 1,
        "成立以来年化": 2.85,
        "近1月年化": 2.70,
        "流动性": "持有期产品",
        "持有期限": "540天",
        "产品规模": 50,
        "购买人次": "中等",
        "业绩比较基准": "2.6%-3.4%",
        "单位净值": 1.0550,
        "累计净值": 1.0550,
        "适合人群": "稳健型投资者，可接受较长期限锁定的投资者",
        "投资范围": "主要投资于中长期信用债、利率债等"
    },
    {
        "名称": "工银理财·鑫添益14天法人",
        "代码": "26G2085F",
        "风险等级": "PR2",
        "风险标签": "中低风险",
        "产品类型": "固定收益类",
        "起购金额": 1,
        "成立以来年化": 2.50,
        "近1月年化": 2.45,
        "流动性": "持有期产品",
        "持有期限": "14天",
        "产品规模": 60,
        "购买人次": "中等",
        "业绩比较基准": "2.3%-3.0%",
        "单位净值": 1.0400,
        "累计净值": 1.0400,
        "适合人群": "稳健型投资者",
        "投资范围": "主要投资于信用债、金融债等"
    },
    {
        "名称": "工银理财·低波红利增强",
        "代码": "23GS5003",
        "风险等级": "PR2",
        "风险标签": "中低风险",
        "产品类型": "固定收益类",
        "起购金额": 1,
        "成立以来年化": 2.65,
        "近1月年化": 3.00,
        "流动性": "工作日灵活申赎",
        "持有期限": "无固定期限",
        "产品规模": 80,
        "购买人次": "较高",
        "业绩比较基准": "2.4%-3.2%",
        "单位净值": 1.0480,
        "累计净值": 1.0480,
        "适合人群": "稳健型投资者",
        "投资范围": "主要投资于高股息策略的债券及固定收益类资产"
    },
    {
        "名称": "工银理财·鑫稳利一年期",
        "代码": "23GS5004",
        "风险等级": "PR2",
        "风险标签": "中低风险",
        "产品类型": "固定收益类",
        "起购金额": 1,
        "成立以来年化": 3.31,
        "近1月年化": 3.10,
        "流动性": "封闭式",
        "持有期限": "一年期",
        "产品规模": 70,
        "购买人次": "较高",
        "业绩比较基准": "3.0%-3.8%",
        "单位净值": 1.0650,
        "累计净值": 1.0650,
        "适合人群": "稳健型投资者，可接受一年锁定期的投资者",
        "投资范围": "主要投资于中高等级信用债、利率债等"
    },
    {
        "名称": "工银理财·鑫得利6个月定开",
        "代码": "23GS5005",
        "风险等级": "PR2",
        "风险标签": "中低风险",
        "产品类型": "固定收益类",
        "起购金额": 1,
        "成立以来年化": 2.90,
        "近1月年化": 2.80,
        "流动性": "定期开放",
        "持有期限": "6个月定开",
        "产品规模": 55,
        "购买人次": "中等",
        "业绩比较基准": "2.6%-3.4%",
        "单位净值": 1.0520,
        "累计净值": 1.0520,
        "适合人群": "稳健型投资者，可接受6个月锁定期的投资者",
        "投资范围": "主要投资于信用债、金融债等"
    },
    {
        "名称": "工银理财·颐享核心优选520天",
        "代码": "23GS5006",
        "风险等级": "PR2",
        "风险标签": "中低风险",
        "产品类型": "固定收益类",
        "起购金额": 1,
        "成立以来年化": 2.95,
        "近1月年化": 2.85,
        "流动性": "持有期产品",
        "持有期限": "520天",
        "产品规模": 35,
        "购买人次": "中等",
        "业绩比较基准": "2.6%-3.5%",
        "单位净值": 1.0580,
        "累计净值": 1.0580,
        "适合人群": "稳健型投资者，可接受中长期锁定期的投资者",
        "投资范围": "主要投资于优质信用债、利率债等"
    },
    {
        "名称": "工银理财·同业存单优选",
        "代码": "23GS5355",
        "风险等级": "PR2",
        "风险标签": "中低风险",
        "产品类型": "固定收益类",
        "起购金额": 1,
        "成立以来年化": 2.60,
        "近1月年化": 2.55,
        "流动性": "每日开放",
        "持有期限": "无固定期限",
        "产品规模": 45,
        "购买人次": "中等",
        "业绩比较基准": "2.2%-3.0%",
        "单位净值": 1.0450,
        "累计净值": 1.0450,
        "适合人群": "稳健型投资者",
        "投资范围": "主要投资于银行同业存单、短期信用债等"
    },
    {
        "名称": "工银理财·核心优选365天",
        "代码": "23GS5393",
        "风险等级": "PR2",
        "风险标签": "中低风险",
        "产品类型": "固定收益类",
        "起购金额": 1,
        "成立以来年化": 2.80,
        "近1月年化": 2.65,
        "流动性": "持有期产品",
        "持有期限": "365天",
        "产品规模": 40,
        "购买人次": "中等",
        "业绩比较基准": "2.5%-3.3%",
        "单位净值": 1.0500,
        "累计净值": 1.0500,
        "适合人群": "稳健型投资者，可接受一年锁定期的投资者",
        "投资范围": "主要投资于信用债、金融债等固定收益类资产"
    }
]

# ============================================================
# 四、金融知识库（严格采用计划书原文）
# ============================================================

FINANCIAL_KNOWLEDGE = {
    "风险等级": {
        "desc": "国内银行业通常将理财产品风险由低到高分为PR1、PR2、PR3、PR4、PR5五个等级，数字越大代表风险越高。\n\nPR1（低风险）：总体风险程度很低。产品保障本金，或本金损失可能性极小且具有较高流动性，投资方向主要为极低风险资产。\n\nPR2（中低风险）：总体风险程度较低。产品不保障本金，但本金损失可能性很小，适合风险偏好较低的投资者。",
        "ref": "风险等级是判断“这款产品是否适合我”的第一道门槛。用户只能购买风险等级等于或低于自身风险承受能力的产品。"
    },
    "成立以来年化": {
        "desc": "产品自成立至最新净值披露日的平均年化收益率，反映产品较长时间内的净值增长水平。",
        "ref": "衡量产品长期“赚钱能力”的指标。成立时间越短的产品，该数值越容易受到短期行情影响，建议结合近1月年化综合判断。"
    },
    "近1月年化": {
        "desc": "产品最近一个月的平均年化收益率，将最近一月的实际收益按年化方式换算得出。",
        "ref": "反映产品的近期表现。若近1月年化与成立以来年化差距较小，说明产品收益稳定；差距较大则说明近期波动明显。"
    },
    "起购金额": {
        "desc": "购买该产品所需的最低金额，投资者首次申购时不得低于此金额。",
        "ref": "结合自身收入水平和账户余额判断是否满足购买条件。"
    },
    "流动性": {
        "desc": "产品资金可取回的速度和便利程度。\n\n每日可申赎：每个工作日可申购或赎回，灵活性最高\n持有期产品：需持有满一定天数后方可赎回\n定期开放：仅在固定开放日可申赎",
        "ref": "流动性决定“急用钱时能否及时取出”。短期内可能需要用钱的资金，应优先选择“每日可申赎”产品。"
    },
    "持有期限": {
        "desc": "产品要求的最低持有时间，期间通常不可赎回。“无固定期限”表示无此要求。",
        "ref": "决定“这笔钱需要锁定多久”。近期可能有资金需求的用户，不应投入持有期较长的产品。"
    },
    "产品规模": {
        "desc": "该产品管理的资金总存量，通常以“亿元”为单位。",
        "ref": "产品规模反映市场认可度。规模较大的产品通常运营更成熟、流动性更好、清盘风险更低。"
    },
    "业绩比较基准": {
        "desc": "管理人基于产品性质、投资策略、过往经验等设定的投资目标，形式为单一值（如4.25%）或区间值（如3.5%-4.5%）。\n\n重要提示：业绩比较基准不代表产品的未来表现和实际收益，不构成收益承诺。",
        "ref": "可参考管理人的收益预期，但不应作为唯一依据，应结合历史实际收益表现综合判断。"
    },
    "单位净值": {
        "desc": "每份产品当前的价格，计算公式为：单位净值 = 产品总净资产 ÷ 产品总份额。",
        "ref": "决定购买一份产品需要多少钱。净值高低不代表产品好坏，不同产品的净值差异可能源于成立时间和累计收益不同。"
    },
    "累计净值": {
        "desc": "在单位净值基础上累加产品成立以来的累计分红，反映产品自成立以来的全部收益。",
        "ref": "累计净值是评价产品历史运作表现的重要参考，累计净值越高，说明产品历史上为投资者创造的累计收益越多。"
    }
}

# ============================================================
# 五、筛选引擎（五轮筛选）
# ============================================================

def apply_filters(products, user_profile):
    candidates = products.copy()
    filter_steps = []

    risk_mapping = {"保守型": ["PR1"], "稳健型": ["PR1", "PR2"]}
    allowed_risks = risk_mapping.get(user_profile["风险承受能力"], ["PR1"])
    candidates = [p for p in candidates if p["风险等级"] in allowed_risks]
    filter_steps.append({"轮次": "风险匹配", "说明": f"保留{user_profile['风险承受能力']}可购买产品", "数量": len(candidates)})

    experience = user_profile.get("投资经验", "无理财经验")
    type_priority = {
        "无理财经验": {"现金管理类": 2, "固定收益类": 1, "固定收益类(QDII)": 0},
        "仅有PR1持仓": {"现金管理类": 2, "固定收益类": 2, "固定收益类(QDII)": 1},
        "有PR2持仓": {"现金管理类": 1, "固定收益类": 2, "固定收益类(QDII)": 1}
    }
    priority = type_priority.get(experience, type_priority["无理财经验"])
    candidates = [p for p in candidates if p["产品类型"] in priority and priority[p["产品类型"]] > 0]
    filter_steps.append({"轮次": "类型匹配", "说明": f"根据投资经验筛选", "数量": len(candidates)})

    has_return = [p for p in candidates if p["近1月年化"] is not None]
    no_return = [p for p in candidates if p["近1月年化"] is None]
    sorted_products = sorted(has_return, key=lambda x: x["近1月年化"], reverse=True)
    keep_count = max(1, int(len(sorted_products) * 0.5))
    candidates = sorted_products[:keep_count] + no_return
    filter_steps.append({"轮次": "近1月年化", "说明": f"保留前50%（{keep_count}款）", "数量": len(candidates)})

    has_return2 = [p for p in candidates if p["成立以来年化"] is not None]
    no_return2 = [p for p in candidates if p["成立以来年化"] is None]
    sorted_products2 = sorted(has_return2, key=lambda x: x["成立以来年化"], reverse=True)
    keep_count2 = max(1, int(len(sorted_products2) * 0.3))
    candidates = sorted_products2[:keep_count2] + no_return2
    filter_steps.append({"轮次": "成立以来年化", "说明": f"保留前30%（{keep_count2}款）", "数量": len(candidates)})

    hot_keywords = ["超千万", "较高"]
    filtered_hot = [p for p in candidates if p["购买人次"] in hot_keywords]
    if len(filtered_hot) < 4:
        filtered_hot = candidates
    candidates = filtered_hot
    filter_steps.append({"轮次": "热度过滤", "说明": "保留热门产品", "数量": len(candidates)})

    return candidates, filter_steps

# ============================================================
# 六、辅助函数
# ============================================================

def get_user_summary(user_profile):
    risk = user_profile.get("风险承受能力", "稳健型")
    exp = user_profile.get("投资经验", "无理财经验")
    exp_map = {
        "无理财经验": "无",
        "仅有PR1持仓": "PR1产品（6个月）",
        "有PR2持仓": "PR2产品（3个月）"
    }
    return {
        "风险承受等级": risk,
        "可购买范围": "PR1" if risk == "保守型" else "PR1+PR2",
        "投资经验": exp_map.get(exp, "无"),
        "月均账户余额": "8,000元",
        "当前持有": exp_map.get(exp, "无")
    }

def get_holding_detail(exp):
    holdings = {
        "无理财经验": None,
        "仅有PR1持仓": {
            "名称": "工银理财·添利宝鑫享",
            "代码": "21GS2699",
            "持有金额": "5,000元",
            "持有天数": "180天（约6个月）",
            "持有方式": "一次性申购",
            "剩余期限": "无固定期限，随时可赎",
            "累计收益": "约52元",
            "年化收益": "2.15%"
        },
        "有PR2持仓": {
            "名称": "工银理财·鑫添益7天",
            "代码": "22GS2699",
            "持有金额": "10,000元",
            "持有天数": "90天（约3个月）",
            "持有方式": "定投（每月1日投入1000元）",
            "剩余期限": "下次定投赎回日：2026-11-01（约75天后）",
            "累计收益": "约98元",
            "年化收益": "2.82%"
        }
    }
    return holdings.get(exp)

def generate_yield_chart(product, metric_name):
    """生成单个产品的年化走势图（平滑曲线）"""
    import pandas as pd
    if metric_name == "近1月年化":
        base = product.get("近1月年化", 2.0)
        days = 30
        dates = pd.date_range(end=datetime.today(), periods=days, freq='D')
        np.random.seed(hash(product["代码"]) % 2**32)
        values = [base * (0.95 + 0.10 * np.sin(i/days * 2*np.pi) + 0.02*np.random.randn()) for i in range(days)]
        series = pd.Series(values).rolling(window=3, center=True).mean().bfill().ffill().tolist()
        y_title = "近1月年化收益率 (%)"
    else:
        base = product.get("成立以来年化", 2.0)
        days = 180
        dates = pd.date_range(end=datetime.today(), periods=days, freq='D')
        np.random.seed(hash(product["代码"] + "hist") % 2**32)
        trend = np.linspace(base*0.98, base*1.02, days)
        values = [trend[i] + 0.01*np.random.randn() for i in range(days)]
        series = pd.Series(values).rolling(window=5, center=True).mean().bfill().ffill().tolist()
        y_title = "成立以来年化收益率 (%)"

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=dates,
        y=series,
        mode='lines',
        name=metric_name,
        line=dict(color='#1a3c6e', width=2.5, shape='spline'),
        fill='tozeroy',
        fillcolor='rgba(26,60,110,0.1)'
    ))
    fig.update_xaxes(showgrid=True, gridcolor='lightgrey', gridwidth=0.5, tickangle=45, nticks=10)
    fig.update_yaxes(showgrid=True, gridcolor='lightgrey', gridwidth=0.5)
    fig.update_layout(
        height=240,
        margin=dict(l=40, r=20, t=40, b=50),
        template='plotly_white',
        xaxis_title="日期",
        yaxis_title=y_title,
        showlegend=False,
        hovermode='x unified'
    )
    return fig

def generate_compare_yield_charts(products):
    """对比页面展示两个独立的年化走势图"""
    import pandas as pd
    # 近1月年化走势
    fig1 = go.Figure()
    colors = ['#1a3c6e', '#2e7d32', '#d32f2f', '#f57c00', '#6a1b9a',
              '#00838f', '#4a148c', '#bf360c', '#1a237e', '#004d40']
    for idx, p in enumerate(products):
        base = p.get("近1月年化", 2.0)
        days = 30
        dates = pd.date_range(end=datetime.today(), periods=days, freq='D')
        np.random.seed(hash(p["代码"] + "cmp1") % 2**32)
        values = [base * (0.95 + 0.10 * np.sin(i/days * 2*np.pi + idx) + 0.02*np.random.randn()) for i in range(days)]
        series = pd.Series(values).rolling(window=3, center=True).mean().bfill().ffill().tolist()
        fig1.add_trace(go.Scatter(
            x=dates,
            y=series,
            mode='lines',
            name=p["名称"][:8],
            line=dict(color=colors[idx % len(colors)], width=2, shape='spline'),
            showlegend=True
        ))
    fig1.update_xaxes(showgrid=True, gridcolor='lightgrey', gridwidth=0.5, tickangle=45, nticks=8)
    fig1.update_yaxes(showgrid=True, gridcolor='lightgrey', gridwidth=0.5)
    fig1.update_layout(
        height=280,
        margin=dict(l=40, r=20, t=40, b=50),
        template='plotly_white',
        xaxis_title="日期",
        yaxis_title="近1月年化收益率 (%)",
        hovermode='x unified',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5, font=dict(size=9))
    )

    # 成立以来年化走势
    fig2 = go.Figure()
    for idx, p in enumerate(products):
        base = p.get("成立以来年化", 2.0)
        days = 180
        dates = pd.date_range(end=datetime.today(), periods=days, freq='D')
        np.random.seed(hash(p["代码"] + "cmp2") % 2**32)
        trend = np.linspace(base*0.98, base*1.02, days)
        values = [trend[i] + 0.01*np.random.randn() for i in range(days)]
        series = pd.Series(values).rolling(window=5, center=True).mean().bfill().ffill().tolist()
        fig2.add_trace(go.Scatter(
            x=dates,
            y=series,
            mode='lines',
            name=p["名称"][:8],
            line=dict(color=colors[idx % len(colors)], width=2, shape='spline'),
            showlegend=True
        ))
    fig2.update_xaxes(showgrid=True, gridcolor='lightgrey', gridwidth=0.5, tickangle=45, nticks=10)
    fig2.update_yaxes(showgrid=True, gridcolor='lightgrey', gridwidth=0.5)
    fig2.update_layout(
        height=280,
        margin=dict(l=40, r=20, t=40, b=50),
        template='plotly_white',
        xaxis_title="日期",
        yaxis_title="成立以来年化收益率 (%)",
        hovermode='x unified',
        legend=dict(orientation='h', yanchor='bottom', y=1.02, xanchor='center', x=0.5, font=dict(size=9))
    )
    return fig1, fig2

# ============================================================
# 七、页面函数（详情页、对比页、列表页等）
# ============================================================

def render_profile_bar():
    summary = get_user_summary(st.session_state.user_profile)
    col1, col2 = st.columns([5, 1])
    with col1:
        st.markdown(f"""
        <div class="profile-bar">
            <div class="profile-item">
                <span class="label">📌 风险承受等级</span>
                <span class="value">{summary['风险承受等级']}</span>
                <span class="badge">{summary['可购买范围']}</span>
            </div>
            <div class="profile-item">
                <span class="label">💰 月均账户余额</span>
                <span class="value">{summary['月均账户余额']}</span>
            </div>
            <div class="profile-item">
                <span class="label">📈 当前持有理财</span>
                <span class="clickable" onclick="document.getElementById('holding_btn').click();">{summary['当前持有']}</span>
                <div style="display:none;"><button id="holding_btn" onclick="st.session_state.show_holding=True">点击</button></div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("查看持有详情", key="show_holding_btn", help="点击查看当前持有产品详情"):
            st.session_state.show_holding = not st.session_state.get("show_holding", False)
            st.rerun()
    with col2:
        if st.button("✏️ 修改画像", use_container_width=True):
            st.session_state.show_editor = not st.session_state.get("show_editor", False)
            st.rerun()

def render_holding_detail():
    exp = st.session_state.user_profile.get("投资经验", "无理财经验")
    holding = get_holding_detail(exp)
    if holding is None:
        st.info("您当前未持有理财产品，可浏览下方产品列表开始配置。")
        return
    st.markdown(f"""
    <div class="holding-card">
        <div class="h-name">📈 {holding['名称']}（{holding['代码']}）</div>
        <div class="h-info">持有金额：{holding['持有金额']}</div>
        <div class="h-info">持有天数：{holding['持有天数']}</div>
        <div class="h-info">持有方式：{holding['持有方式']}</div>
        <div class="h-info">⏳ 剩余期限：{holding['剩余期限']}</div>
        <div class="h-info">累计收益：{holding['累计收益']}（年化 {holding['年化收益']}）</div>
    </div>
    """, unsafe_allow_html=True)
    if st.button("收起持有详情"):
        st.session_state.show_holding = False
        st.rerun()

def render_profile_editor():
    if not st.session_state.get("show_editor", False):
        return
    with st.expander("✏️ 编辑理财画像", expanded=True):
        st.info("风险承受能力由XGBoost模型计算，不可手动修改。以下选项仅用于演示不同画像下的产品推荐。")
        col1, col2 = st.columns(2)
        with col1:
            risk = st.selectbox(
                "风险承受能力（XGBoost输出）",
                ["保守型", "稳健型"],
                index=["保守型", "稳健型"].index(st.session_state.user_profile["风险承受能力"]),
                help="实际产品中该等级由XGBoost模型自动计算"
            )
        with col2:
            exp = st.selectbox(
                "投资经验",
                ["无理财经验", "仅有PR1持仓", "有PR2持仓"],
                index=["无理财经验", "仅有PR1持仓", "有PR2持仓"].index(st.session_state.user_profile["投资经验"])
            )
        col3, col4 = st.columns(2)
        with col3:
            product_types = st.multiselect(
                "产品类型偏好",
                ["现金管理类", "固定收益类", "固定收益类(QDII)"],
                default=["现金管理类", "固定收益类"]
            )
        with col4:
            liq = st.selectbox("流动性偏好", ["不限", "每日可申赎", "持有期产品", "定期开放"], index=0)

        if st.button("🔄 更新画像并重新筛选", type="primary"):
            st.session_state.user_profile["风险承受能力"] = risk
            st.session_state.user_profile["投资经验"] = exp
            candidates, steps = apply_filters(PRODUCTS, st.session_state.user_profile)
            if product_types:
                candidates = [p for p in candidates if p["产品类型"] in product_types]
            if liq != "不限":
                if liq == "每日可申赎":
                    candidates = [p for p in candidates if p["流动性"] in ["每日可申赎", "每日开放", "日开", "无固定期限", "开放净值型"]]
                elif liq == "持有期产品":
                    candidates = [p for p in candidates if "持有" in p["流动性"] or "最短持有" in p["持有期限"]]
                elif liq == "定期开放":
                    candidates = [p for p in candidates if "定开" in p["流动性"] or "定开" in p["持有期限"]]
            st.session_state.candidates = candidates
            st.session_state.filter_steps = steps
            st.session_state.show_editor = False
            st.rerun()

def render_knowledge_page():
    st.markdown("### ← 返回")
    if st.button("返回产品列表", key="back_knowledge"):
        st.session_state.page = "list"
        st.rerun()
    st.markdown("# 📖 理财指标知识库")
    st.markdown("点击下方指标名称，查看详细解释和参考价值")
    cols = st.columns(4)
    terms = list(FINANCIAL_KNOWLEDGE.keys())
    for i, term in enumerate(terms):
        with cols[i % 4]:
            if st.button(term, key=f"know_{i}", use_container_width=True):
                st.session_state.selected_knowledge = term
                st.rerun()
    if st.session_state.get("selected_knowledge"):
        term = st.session_state.selected_knowledge
        info = FINANCIAL_KNOWLEDGE[term]
        st.markdown(f"""
        <div class="knowledge-detail">
            <div class="term">{term}</div>
            <div class="desc">{info['desc'].replace(chr(10), '<br>')}</div>
            <div class="ref">💡 {info['ref']}</div>
        </div>
        """, unsafe_allow_html=True)

def render_product_detail(product):
    st.markdown("### ← 返回")
    if st.button("返回产品列表", key="back_detail"):
        st.session_state.page = "list"
        st.rerun()
    st.markdown(f"# {product['名称']}")
    st.markdown(f"**产品代码：** {product['代码']}  |  **风险等级：** {product['风险等级']}（{product['风险标签']}）")

    st.markdown("#### 📊 产品全维度信息")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="detail-grid">
            <div class="detail-item"><div class="label">产品类型</div><div class="value">{product['产品类型']}</div></div>
            <div class="detail-item"><div class="label">起购金额</div><div class="value">{product['起购金额']}元</div></div>
            <div class="detail-item"><div class="label">成立以来年化</div><div class="value">{product['成立以来年化']:.2f}%</div></div>
            <div class="detail-item"><div class="label">近1月年化</div><div class="value">{product['近1月年化']:.2f}%</div></div>
            <div class="detail-item"><div class="label">流动性</div><div class="value">{product['流动性']}</div></div>
            <div class="detail-item"><div class="label">持有期限</div><div class="value">{product['持有期限']}</div></div>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="detail-grid">
            <div class="detail-item"><div class="label">产品规模</div><div class="value">{product['产品规模']}亿元</div></div>
            <div class="detail-item"><div class="label">购买人次</div><div class="value">{product['购买人次']}</div></div>
            <div class="detail-item"><div class="label">业绩比较基准</div><div class="value">{product['业绩比较基准']}</div></div>
            <div class="detail-item"><div class="label">单位净值</div><div class="value">{product['单位净值']:.4f}</div></div>
            <div class="detail-item"><div class="label">累计净值</div><div class="value">{product['累计净值']:.4f}</div></div>
            <div class="detail-item"><div class="label">适合人群</div><div class="value" style="font-size:14px;">{product['适合人群']}</div></div>
        </div>
        """, unsafe_allow_html=True)
    st.markdown(f"<div style='margin-top:8px;'><strong>投资范围：</strong>{product['投资范围']}</div>", unsafe_allow_html=True)

    st.markdown("#### 📈 年化走势")
    col1, col2 = st.columns(2)
    with col1:
        fig1 = generate_yield_chart(product, "近1月年化")
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        fig2 = generate_yield_chart(product, "成立以来年化")
        st.plotly_chart(fig2, use_container_width=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        if product in st.session_state.get("wishlist", []):
            if st.button("❤️ 已收藏", use_container_width=True):
                st.session_state.wishlist = [p for p in st.session_state.wishlist if p["名称"] != product["名称"]]
                st.rerun()
        else:
            if st.button("⭐ 加入收藏", use_container_width=True):
                if product not in st.session_state.wishlist:
                    st.session_state.wishlist.append(product)
                    st.success("已加入收藏夹！")
                st.rerun()
    with col2:
        if product in st.session_state.get("compare_checklist", []):
            if st.button("✅ 已选对比", use_container_width=True):
                st.session_state.compare_checklist = [p for p in st.session_state.compare_checklist if p["名称"] != product["名称"]]
                st.rerun()
        else:
            if st.button("📊 加入对比", use_container_width=True):
                if product not in st.session_state.compare_checklist:
                    st.session_state.compare_checklist.append(product)
                    st.success("已加入对比列表！")
                st.rerun()
    with col3:
        st.button("💰 确认购买", use_container_width=True, type="primary")

def render_compare_page():
    st.markdown("### ← 返回")
    if st.button("返回产品列表", key="back_compare"):
        st.session_state.page = "list"
        st.rerun()
    products = st.session_state.compare_checklist
    if len(products) < 2:
        st.warning("请至少选择2款产品进行对比")
        return
    st.markdown(f"# 📊 产品PK对比（{len(products)}款）")

    st.markdown("#### 📋 指标对比")
    df = pd.DataFrame(products)
    df_display = df[["名称", "风险等级", "产品类型", "起购金额", "成立以来年化", "近1月年化", "流动性", "持有期限", "产品规模", "业绩比较基准"]].copy()
    df_display["成立以来年化"] = df_display["成立以来年化"].apply(lambda x: f"{x:.2f}%" if pd.notna(x) else "—")
    df_display["近1月年化"] = df_display["近1月年化"].apply(lambda x: f"{x:.2f}%" if pd.notna(x) else "—")
    df_display["产品规模"] = df_display["产品规模"].apply(lambda x: f"{x}亿元" if pd.notna(x) else "—")
    df_display["起购金额"] = df_display["起购金额"].apply(lambda x: "1元" if x == 1 else f"{x}元")
    def highlight_max(s):
        if s.name in ["成立以来年化", "近1月年化", "产品规模"]:
            max_val = s.max()
            return ['background-color: #e8f5e9; font-weight: 600;' if v == max_val else '' for v in s]
        return ['' for _ in s]
    st.dataframe(df_display.style.apply(highlight_max, axis=0), use_container_width=True, hide_index=True)

    st.markdown("#### 📈 年化走势对比")
    fig1, fig2 = generate_compare_yield_charts(products)
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.plotly_chart(fig2, use_container_width=True)

    st.markdown("#### 💡 适配建议")
    summary = get_user_summary(st.session_state.user_profile)
    if summary["风险承受等级"] == "保守型":
        st.info("💡 您的风险承受能力为保守型，建议优先选择PR1级产品，注重本金安全。")
    else:
        st.info("💡 您的风险承受能力为稳健型，可适当配置PR2级产品以获得更高收益。")

    # 对比页面仅对比，无购买按钮，购买在收藏夹完成

def render_wishlist():
    """收藏夹（购买入口）"""
    wishlist = st.session_state.get("wishlist", [])
    if not wishlist:
        return
    st.subheader("⭐ 我的收藏夹（可在此完成购买）")
    for idx, p in enumerate(wishlist):
        with st.container():
            col1, col2, col3, col4 = st.columns([3, 1.5, 1.5, 1])
            with col1:
                st.write(f"**{p['名称']}** ({p['代码']})")
                st.caption(f"成立以来年化 {p['成立以来年化']:.2f}% ｜ 近1月年化 {p['近1月年化']:.2f}% ｜ {p['风险等级']}")
            with col2:
                st.write(f"规模 {p['产品规模']}亿")
            with col3:
                if st.button("移除", key=f"remove_wish_{idx}"):
                    st.session_state.wishlist = [x for x in wishlist if x["代码"] != p["代码"]]
                    st.rerun()
            with col4:
                if st.button("💰 购买", key=f"buy_{idx}", type="primary"):
                    st.success(f"🎉 您已成功购买 {p['名称']}！")
        st.markdown("---")

def render_list_page():
    candidates = st.session_state.candidates
    col_know, col_empty = st.columns([1, 5])
    with col_know:
        if st.button("📖 金融知识", use_container_width=True):
            st.session_state.page = "knowledge"
            st.rerun()

    if candidates is None:
        st.info("👈 请在「编辑画像」中设置您的理财画像，点击「更新画像并重新筛选」开始智能匹配")
    elif len(candidates) == 0:
        st.warning("当前条件下暂无匹配产品，请调整筛选条件")
    else:
        if st.session_state.get("filter_steps"):
            cols = st.columns(len(st.session_state.filter_steps))
            for i, step in enumerate(st.session_state.filter_steps):
                with cols[i]:
                    st.metric(label=step["轮次"], value=f"{step['数量']} 款", delta=step["说明"])
        st.markdown(f"### ✅ 为您匹配 {len(candidates)} 款产品")
        st.caption("⭐ 收藏心仪产品 ｜  📊 勾选对比复选框，最多选择4款")
        for i in range(0, len(candidates), 3):
            cols = st.columns(3)
            for j in range(3):
                idx = i + j
                if idx >= len(candidates):
                    break
                p = candidates[idx]
                with cols[j]:
                    risk_tag = f"tag-{p['风险等级'].lower()}"
                    is_wished = p in st.session_state.get("wishlist", [])
                    is_compared = p in st.session_state.get("compare_checklist", [])
                    st.markdown(f"""
                    <div class="product-card">
                        <div class="product-name">{p['名称']}</div>
                        <div class="product-code">{p['代码']}</div>
                        <div>
                            <span class="product-tag {risk_tag}">{p['风险等级']}</span>
                            <span style="font-size:12px;color:#666;">{p['产品类型']}</span>
                        </div>
                        <div class="product-yield">{p['成立以来年化']:.2f}%</div>
                        <div class="product-yield-label">成立以来年化</div>
                        <div class="product-meta">
                            <span>💧 {p['流动性']}</span>
                            <span>📅 {p['持有期限']}</span>
                            <span>💰 {p['起购金额']}元起</span>
                        </div>
                        <div style="font-size:12px;color:#999;">规模 {p['产品规模']}亿 · {p['购买人次']}</div>
                    </div>
                    """, unsafe_allow_html=True)
                    col_a, col_b, col_c = st.columns(3)
                    with col_a:
                        if is_wished:
                            if st.button("❤️ 已收藏", key=f"wish_{idx}"):
                                st.session_state.wishlist = [x for x in st.session_state.wishlist if x["名称"] != p["名称"]]
                                st.rerun()
                        else:
                            if st.button("⭐ 收藏", key=f"wish_{idx}"):
                                if p not in st.session_state.wishlist:
                                    st.session_state.wishlist.append(p)
                                st.rerun()
                    with col_b:
                        if st.button("📖 详情", key=f"detail_{idx}"):
                            st.session_state.current_product = p
                            st.session_state.page = "detail"
                            st.rerun()
                    with col_c:
                        checked = st.checkbox("📊 对比", key=f"cmp_{idx}", value=is_compared)
                        if checked and not is_compared:
                            if len(st.session_state.compare_checklist) < 4:
                                st.session_state.compare_checklist.append(p)
                                st.rerun()
                            else:
                                st.warning("最多选择4款产品对比")
                        elif not checked and is_compared:
                            st.session_state.compare_checklist = [x for x in st.session_state.compare_checklist if x["名称"] != p["名称"]]
                            st.rerun()

# ============================================================
# 八、底部操作栏（含收藏夹展开和对比列表）
# ============================================================

def render_action_bar():
    wishlist = st.session_state.get("wishlist", [])
    compare_list = st.session_state.get("compare_checklist", [])
    if not wishlist and not compare_list:
        return
    with st.container():
        st.markdown("---")
        col1, col2, col3, col4 = st.columns([2.5, 2, 1.5, 1.5])
        with col1:
            if wishlist:
                names = [p["名称"][:12] + "..." if len(p["名称"]) > 12 else p["名称"] for p in wishlist]
                st.markdown(f"""
                <div style="background:#f8faff;border-radius:8px;padding:6px 14px;border:1px solid #d0ddee;cursor:pointer;">
                    <span style="font-weight:600;color:#1a3c6e;">⭐ 收藏夹</span>
                    <span style="color:#d32f2f;font-weight:600;margin-left:10px;">{len(wishlist)}款</span>
                    <span style="color:#666;font-size:13px;margin-left:10px;">{', '.join(names)}</span>
                </div>
                """, unsafe_allow_html=True)
                if st.button("📂 打开收藏夹", key="open_wishlist"):
                    st.session_state.show_wishlist = not st.session_state.get("show_wishlist", False)
                    st.rerun()
        with col2:
            if compare_list:
                cnames = [p["名称"][:12] + "..." if len(p["名称"]) > 12 else p["名称"] for p in compare_list]
                st.markdown(f"""
                <div style="background:#f0f7ff;border-radius:8px;padding:6px 14px;border:1px solid #1a3c6e;">
                    <span style="font-weight:600;color:#1a3c6e;">📊 对比列表</span>
                    <span style="color:#1a3c6e;font-weight:600;margin-left:10px;">{len(compare_list)}款</span>
                    <span style="color:#666;font-size:13px;margin-left:10px;">{', '.join(cnames)}</span>
                </div>
                """, unsafe_allow_html=True)
        with col3:
            if compare_list and len(compare_list) >= 2:
                if st.button("📊 开始对比", type="primary", use_container_width=True):
                    st.session_state.page = "compare"
                    st.rerun()
            elif compare_list:
                st.caption("请至少选择2款产品对比")
        with col4:
            if wishlist and st.button("🗑️ 清空收藏", use_container_width=True):
                st.session_state.wishlist = []
                st.rerun()
            if compare_list and st.button("🗑️ 清空对比", use_container_width=True):
                st.session_state.compare_checklist = []
                st.rerun()

# ============================================================
# 九、主程序
# ============================================================

def main():
    # 初始化session state
    if "user_profile" not in st.session_state:
        st.session_state.user_profile = {"风险承受能力": "稳健型", "投资经验": "无理财经验"}
    if "candidates" not in st.session_state:
        st.session_state.candidates = None
    if "filter_steps" not in st.session_state:
        st.session_state.filter_steps = None
    if "wishlist" not in st.session_state:
        st.session_state.wishlist = []
    if "compare_checklist" not in st.session_state:
        st.session_state.compare_checklist = []
    if "page" not in st.session_state:
        st.session_state.page = "list"
    if "current_product" not in st.session_state:
        st.session_state.current_product = None
    if "show_editor" not in st.session_state:
        st.session_state.show_editor = False
    if "selected_knowledge" not in st.session_state:
        st.session_state.selected_knowledge = None
    if "show_holding" not in st.session_state:
        st.session_state.show_holding = False
    if "show_wishlist" not in st.session_state:
        st.session_state.show_wishlist = False

    st.markdown("""
    <div style="display:flex;align-items:center;gap:10px;margin-bottom:2px;">
        <span style="font-size:26px;font-weight:700;color:#1a3c6e;">📊 理财服务</span>
        <span style="font-size:15px;color:#6b7a8f;">智能产品推荐</span>
    </div>
    <div style="color:#6b7a8f;font-size:13px;margin-bottom:12px;">
        根据您的风险偏好和投资经验，智能筛选匹配产品，收藏意向产品，PK对比后决策
    </div>
    """, unsafe_allow_html=True)

    render_profile_bar()

    if st.session_state.show_holding:
        render_holding_detail()
        st.markdown("---")

    render_profile_editor()

    # 页面路由
    if st.session_state.page == "knowledge":
        render_knowledge_page()
    elif st.session_state.page == "detail" and st.session_state.current_product:
        render_product_detail(st.session_state.current_product)
    elif st.session_state.page == "compare":
        render_compare_page()
    else:
        render_list_page()

    # 收藏夹展开（显示在列表和对比之前）
    if st.session_state.get("show_wishlist", False):
        render_wishlist()

    render_action_bar()

    st.markdown('<div class="footer-note">📌 本Demo为理财服务智能推荐系统演示，产品数据为模拟展示，不构成投资建议</div>', unsafe_allow_html=True)

if __name__ == "__main__":
    main()