import zipfile
import re

# 读取Excel文件
xlsx_path = 'FinOps成本-产品模型20260208.xlsx'

with zipfile.ZipFile(xlsx_path, 'r') as z:
    # 读取sheet1.xml
    with z.open('xl/worksheets/sheet1.xml') as f:
        sheet_content = f.read().decode('utf-8')
        
        # 查找所有row标签
        row_matches = re.findall(r'<row[^>]*r="(\d+)"', sheet_content)
        
        print(f"Total rows found: {len(row_matches)}")
        print("Row numbers:", row_matches)
