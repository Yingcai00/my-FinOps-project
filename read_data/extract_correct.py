import zipfile
import re
import json

# 读取Excel文件
xlsx_path = 'FinOps成本-产品模型20260208.xlsx'

with zipfile.ZipFile(xlsx_path, 'r') as z:
    # 读取sharedStrings.xml获取所有文本
    shared_strings = []
    if 'xl/sharedStrings.xml' in z.namelist():
        with z.open('xl/sharedStrings.xml') as f:
            content = f.read().decode('utf-8')
            matches = re.findall(r'<t[^>]*>([^<]*)</t>', content)
            shared_strings = matches
    
    # 读取sheet1.xml
    with z.open('xl/worksheets/sheet1.xml') as f:
        sheet_content = f.read().decode('utf-8')
        
        # 提取所有行数据 - 使用非贪婪匹配
        rows = re.findall(r'<row[^>]*r="(\d+)"[^>]*>(.*?)</row>', sheet_content, re.DOTALL)
        
        print(f"Total rows: {len(rows)}")
        
        # 读取第2行作为表头
        headers = {}
        for row_num, row_content in rows:
            if row_num == '2':
                cells = re.findall(r'<c[^>]*r="([A-Z]+)2"[^>]*>(.*?)</c>', row_content, re.DOTALL)
                for col, cell in cells:
                    val = ''
                    if '<v>' in cell:
                        v_match = re.search(r'<v>(\d+)</v>', cell)
                        if v_match:
                            idx = int(v_match.group(1))
                            if idx < len(shared_strings):
                                val = shared_strings[idx]
                    headers[col] = val
                break
        
        print("\nHeaders (Row 2):")
        for col in sorted(headers.keys()):
            print(f"  {col}: {headers[col]}")
        
        # 读取数据行（第3行到第46行）
        data_rows = []
        for row_num, row_content in rows:
            rnum = int(row_num)
            if 3 <= rnum <= 46:
                cells = re.findall(r'<c[^>]*r="([A-Z]+)' + row_num + r'"[^>]*>(.*?)</c>', row_content, re.DOTALL)
                row_data = {'_row': rnum}
                for col, cell in cells:
                    val = ''
                    if '<v>' in cell:
                        v_match = re.search(r'<v>([^<]*)</v>', cell)
                        if v_match:
                            v = v_match.group(1)
                            # 检查是否是共享字符串
                            if 't="s"' in cell:
                                idx = int(v)
                                if idx < len(shared_strings):
                                    val = shared_strings[idx]
                            else:
                                val = v
                    row_data[col] = val
                data_rows.append(row_data)
        
        print(f"\nData rows (3-46): {len(data_rows)}")
        
        # 打印前3行
        for row in data_rows[:3]:
            print(f"\nRow {row['_row']}:")
            for col in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']:
                if col in row:
                    header_name = headers.get(col, col)
                    print(f"  {header_name}({col}): {row[col]}")
