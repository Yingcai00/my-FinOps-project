import pandas as pd

# 读取Excel文件
excel_file = '私有云服务目录.xlsx'
try:
    # 读取所有工作表
    excel_data = pd.ExcelFile(excel_file)
    print(f"工作表名称: {excel_data.sheet_names}")
    
    # 读取第一个工作表
    df = pd.read_excel(excel_file, sheet_name=0)
    
    # 打印列名
    print("\n列名:")
    print(df.columns.tolist())
    
    # 打印前5行数据
    print("\n前5行数据:")
    print(df.head())
    
    # 打印数据类型
    print("\n数据类型:")
    print(df.dtypes)
    
    # 打印数据量
    print(f"\n数据量: {len(df)} 行")
    
except Exception as e:
    print(f"读取文件时出错: {e}")