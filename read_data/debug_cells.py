import zipfile
import re

# 读取Excel文件
xlsx_path = 'FinOps成本-产品模型20260208.xlsx'

with zipfile.ZipFile(xlsx_path, 'r') as z:
    # 读取sheet1.xml
    with z.open('xl/worksheets/sheet1.xml') as f:
        sheet_content = f.read().decode('utf-8')
        
        # 查找第4行的B4单元格
        match = re.search(r'<c[^>]*r="B4"[^>]*>(.*?)</c>', sheet_content, re.DOTALL)
        if match:
            print("B4 cell content:")
            print(match.group(0))
        else:
            print("B4 not found")
        
        # 查找第3行的B3单元格
        match = re.search(r'<c[^>]*r="B3"[^>]*>(.*?)</c>', sheet_content, re.DOTALL)
        if match:
            print("\nB3 cell content:")
            print(match.group(0))
