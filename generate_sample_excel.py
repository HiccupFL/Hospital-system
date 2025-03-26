import pandas as pd
from datetime import datetime, timedelta
import os

# 确保目录存在
os.makedirs('d:/DeskTop/hospital/data', exist_ok=True)

# 创建样例数据
data = [
    {
        '药品名称': '阿莫西林胶囊',
        '厂商': '哈药集团制药总厂',
        '生产日期': (datetime.now() - timedelta(days=60)).strftime('%Y-%m-%d'),
        '使用截止日期': (datetime.now() + timedelta(days=300)).strftime('%Y-%m-%d'),
        '最少保有数量': 100,
        '现有数量': 150
    },
    {
        '药品名称': '布洛芬片',
        '厂商': '上海信谊药厂有限公司',
        '生产日期': (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d'),
        '使用截止日期': (datetime.now() + timedelta(days=270)).strftime('%Y-%m-%d'),
        '最少保有数量': 80,
        '现有数量': 75
    },
    {
        '药品名称': '头孢克肟胶囊',
        '厂商': '国药集团致君(深圳)制药有限公司',
        '生产日期': (datetime.now() - timedelta(days=120)).strftime('%Y-%m-%d'),
        '使用截止日期': (datetime.now() + timedelta(days=240)).strftime('%Y-%m-%d'),
        '最少保有数量': 50,
        '现有数量': 65
    },
    {
        '药品名称': '盐酸氨溴索口服溶液',
        '厂商': '北京双鹤药业股份有限公司',
        '生产日期': (datetime.now() - timedelta(days=150)).strftime('%Y-%m-%d'),
        '使用截止日期': (datetime.now() + timedelta(days=15)).strftime('%Y-%m-%d'),
        '最少保有数量': 30,
        '现有数量': 25
    },
    {
        '药品名称': '复方感冒灵颗粒',
        '厂商': '江西民济药业股份有限公司',
        '生产日期': (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d'),
        '使用截止日期': (datetime.now() + timedelta(days=180)).strftime('%Y-%m-%d'),
        '最少保有数量': 60,
        '现有数量': 90
    },
    {
        '药品名称': '维生素C片',
        '厂商': '华北制药股份有限公司',
        '生产日期': (datetime.now() - timedelta(days=200)).strftime('%Y-%m-%d'),
        '使用截止日期': (datetime.now() + timedelta(days=500)).strftime('%Y-%m-%d'),
        '最少保有数量': 120,
        '现有数量': 200
    },
    {
        '药品名称': '甲硝唑片',
        '厂商': '华润双鹤药业股份有限公司',
        '生产日期': (datetime.now() - timedelta(days=100)).strftime('%Y-%m-%d'),
        '使用截止日期': (datetime.now() - timedelta(days=10)).strftime('%Y-%m-%d'),
        '最少保有数量': 40,
        '现有数量': 35
    },
    {
        '药品名称': '复方板蓝根颗粒',
        '厂商': '广州白云山和记黄埔中药有限公司',
        '生产日期': (datetime.now() - timedelta(days=80)).strftime('%Y-%m-%d'),
        '使用截止日期': (datetime.now() + timedelta(days=650)).strftime('%Y-%m-%d'),
        '最少保有数量': 70,
        '现有数量': 120
    },
    {
        '药品名称': '盐酸左氧氟沙星片',
        '厂商': '齐鲁制药有限公司',
        '生产日期': (datetime.now() - timedelta(days=110)).strftime('%Y-%m-%d'),
        '使用截止日期': (datetime.now() + timedelta(days=250)).strftime('%Y-%m-%d'),
        '最少保有数量': 45,
        '现有数量': 40
    },
    {
        '药品名称': '硝苯地平缓释片',
        '厂商': '北京诺华制药有限公司',
        '生产日期': (datetime.now() - timedelta(days=130)).strftime('%Y-%m-%d'),
        '使用截止日期': (datetime.now() + timedelta(days=600)).strftime('%Y-%m-%d'),
        '最少保有数量': 55,
        '现有数量': 80
    }
]

# 创建DataFrame
df = pd.DataFrame(data)

# 保存为Excel文件
excel_path = 'd:/DeskTop/hospital/data/药品样例数据.xlsx'
df.to_excel(excel_path, index=False)

print(f"样例Excel文件已生成: {excel_path}")