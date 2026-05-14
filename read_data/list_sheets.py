import zipfile
import xml.etree.ElementTree as ET

# 读取Excel文件
xlsx_path = 'FinOps成本-产品模型20260224.xlsx'

with zipfile.ZipFile(xlsx_path, 'r') as z:
    # 读取workbook.xml获取sheet名称
    with z.open('xl/workbook.xml') as f:
        tree = ET.parse(f)
        root = tree.getroot()
        
        # 命名空间
        ns = {'ns': 'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
        
        # 提取sheet名称
        sheets = root.findall('.//ns:sheet', ns)
        print("Sheet names:")
        for i, sheet in enumerate(sheets):
            sheet_name = sheet.get('name')
            sheet_id = sheet.get('sheetId')
            r_id = sheet.get('{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id')
            print(f"  Sheet {i+1}: {sheet_name} (sheetId: {sheet_id}, rId: {r_id})")