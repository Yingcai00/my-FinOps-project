import zipfile

# 读取Excel文件
xlsx_path = 'FinOps成本-产品模型20260208.xlsx'

with zipfile.ZipFile(xlsx_path, 'r') as z:
    # 读取sheet1.xml
    with z.open('xl/worksheets/sheet1.xml') as f:
        sheet_content = f.read().decode('utf-8')
        
        # 查找sheetData部分
        start = sheet_content.find('<sheetData>')
        end = sheet_content.find('</sheetData>')
        if start != -1 and end != -1:
            sheet_data = sheet_content[start:end+12]
            print("Sheet data length:", len(sheet_data))
            print("\nFirst 3000 chars:")
            print(sheet_data[:3000])
