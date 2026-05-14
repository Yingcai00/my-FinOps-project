import pandas as pd
import json

# 读取Excel文件
excel_file = '资产规格_2026-04-14 1919.xlsx'
df = pd.read_excel(excel_file)

# 查看数据结构
print("Excel文件列名:")
print(df.columns.tolist())

print("\n前5行数据:")
print(df.head())

# 处理数据，转换为JavaScript对象格式
spec_data = []

for index, row in df.iterrows():
    spec_item = {
        "id": index + 1,
        "name": str(row.get('名称', '')),
        "cpu": str(row.get('CPU', '')),
        "cpuModel": str(row.get('CPU型号', '')),
        "memory": str(row.get('内存大小', '')),
        "mechanicalHardDrive": str(row.get('机械硬盘大小', '')),
        "solidStateDrive": str(row.get('固态硬盘大小', '')),
        "videoMemory": str(row.get('显存大小', '')),
        "gpuModel": str(row.get('GPU型号', '')),
        "finopsCategory": str(row.get('资产细分', ''))
    }
    spec_data.append(spec_item)

# 生成JavaScript代码
js_code = f"const specData = {json.dumps(spec_data, ensure_ascii=False, indent=2)};"

# 保存到文件
with open('asset_specs_data.js', 'w', encoding='utf-8') as f:
    f.write(js_code)

print(f"\n成功读取并转换数据，共 {len(spec_data)} 条资产规格记录")
print("数据已保存到 asset_specs_data.js 文件")
