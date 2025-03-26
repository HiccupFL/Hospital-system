import pandas as pd
from datetime import datetime

def import_excel(file_path):
    """
    从Excel文件导入药品数据
    """
    # 读取Excel文件
    df = pd.read_excel(file_path)
    
    # 验证必要的列是否存在
    required_columns = ['药品名称', '厂商', '生产日期', '使用截止日期', '最少保有数量', '现有数量']
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"Excel文件缺少必要的列: {col}")
    
    # 转换数据为字典列表
    medicines = []
    for _, row in df.iterrows():
        # 处理日期格式
        production_date = row['生产日期']
        if isinstance(production_date, str):
            production_date = datetime.strptime(production_date, '%Y-%m-%d').strftime('%Y-%m-%d')
        else:
            production_date = production_date.strftime('%Y-%m-%d')
            
        expiry_date = row['使用截止日期']
        if isinstance(expiry_date, str):
            expiry_date = datetime.strptime(expiry_date, '%Y-%m-%d').strftime('%Y-%m-%d')
        else:
            expiry_date = expiry_date.strftime('%Y-%m-%d')
        
        medicine = {
            'name': row['药品名称'],
            'manufacturer': row['厂商'],
            'production_date': production_date,
            'expiry_date': expiry_date,
            'min_quantity': int(row['最少保有数量']),
            'current_quantity': int(row['现有数量'])
        }
        medicines.append(medicine)
    
    return medicines

def export_excel(medicines, file_path):
    """
    导出药品数据到Excel文件
    """
    # 转换数据为DataFrame
    data = []
    for medicine in medicines:
        data.append({
            '药品名称': medicine['name'],
            '厂商': medicine['manufacturer'],
            '生产日期': medicine['production_date'],
            '使用截止日期': medicine['expiry_date'],
            '最少保有数量': medicine['min_quantity'],
            '现有数量': medicine['current_quantity']
        })
    
    df = pd.DataFrame(data)
    
    # 保存到Excel文件
    df.to_excel(file_path, index=False)