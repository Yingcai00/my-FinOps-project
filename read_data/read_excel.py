import pandas as pd
import json

# 读取Excel文件
excel_file = 'FinOps服务目录-20260317.xlsx'
try:
    # 读取所有工作表
    excel_data = pd.ExcelFile(excel_file)
    print(f"工作表名称: {excel_data.sheet_names}")
    
    # 读取第一个工作表
    df = pd.read_excel(excel_file, sheet_name=0)
    
    # 打印列名
    print("\n列名:")
    print(df.columns.tolist())
    
    # 打印前10行数据
    print("\n前10行数据:")
    print(df.head(10))
    
    # 打印数据量
    print(f"\n数据量: {len(df)} 行")
    
    # 生成JSON数据
    service_data = []
    for index, row in df.iterrows():
        # 处理NaN值
        def get_value(key, default=''):
            value = row.get(key, default)
            if pd.isna(value):
                return default
            return value
        
        service_item = {
            "id": index + 1,
            "serviceCode": f"SVC{str(index + 1).zfill(3)}",
            "categoryLevel1": get_value('服务分类', ''),
            "categoryLevel2": get_value('服务名称', ''),
            "categoryLevel3": get_value('规格簇', ''),
            "service": f"{get_value('服务分类', '')}-{get_value('服务名称', '')}",
            "serviceName": get_value('规格名称', ''),
            "description": get_value('描述', ''),
            "cpuSpec": str(get_value('CPU规格(C)', '0')),
            "cpuModel": get_value('CPU型号', ''),
            "memSpec": str(get_value('MEM规格(GB)', '0')),
            "sasDisk": str(get_value('SAS_DISK规格（TB）', '0')),
            "ssdDisk": str(get_value('SSD_DISK(TB)', '0')),
            "gpuModel": get_value('显卡型号', ''),
            "gpuMem": str(get_value('显存(GB)', '0')),
            "costPool": get_value('关联成本池', ''),
            "billingResource": get_value('计费资源', ''),
            "serviceFee": float(get_value('服务费', 0)),
            "storageFee": float(get_value('存储费', 0)),
            "unitPrice": float(get_value('单价', 0)),
            "aliyunPrice": float(get_value('阿里云参考价', 0)),
            "unit": get_value('单位', ''),
            "month": "2026-02"
        }
        service_data.append(service_item)
    
    # 保存为JSON文件
    with open('service_data.json', 'w', encoding='utf-8') as f:
        json.dump(service_data, f, ensure_ascii=False, indent=2)
    
    print("\n数据已保存到service_data.json文件")
    
except Exception as e:
    print(f"读取文件时出错: {e}")
    import traceback
    traceback.print_exc()