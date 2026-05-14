import pandas as pd
import json

# 读取Excel文件
excel_file = '资产细分_2026-04-14 1945.xlsx'
df = pd.read_excel(excel_file)

# 处理数据，转换为JavaScript对象格式
subdivide_data = []

for index, row in df.iterrows():
    subdivide_item = {
        "id": index + 1,
        "name": str(row.get('名称', '')),
        "calculateCost": bool(row.get('是否计算成本', True))
    }
    subdivide_data.append(subdivide_item)

# 生成JavaScript代码
js_code = f"const subdivideData = {json.dumps(subdivide_data, ensure_ascii=False, indent=2)};"

# 保存到文件
with open('asset_subdivide_data.js', 'w', encoding='utf-8') as f:
    f.write(js_code)

print(f"\n成功读取并转换数据，共 {len(subdivide_data)} 条资产细分记录")
print("数据已保存到 asset_subdivide_data.js 文件")
