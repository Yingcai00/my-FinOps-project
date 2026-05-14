import zipfile

# 读取Excel文件
xlsx_path = 'FinOps成本-产品模型20260208.xlsx'

with zipfile.ZipFile(xlsx_path, 'r') as z:
    # 读取sheet1.xml
    with z.open('xl/worksheets/sheet1.xml') as f:
        sheet_content = f.read().decode('utf-8')
        
        # 打印前5000个字符查看结构
        print(sheet_content[:5000])
