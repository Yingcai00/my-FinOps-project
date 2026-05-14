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
    
    print(f"Total shared strings: {len(shared_strings)}")
    
    # 读取sheet1.xml
    with z.open('xl/worksheets/sheet1.xml') as f:
        sheet_content = f.read().decode('utf-8')
        
        # 提取所有行数据
        rows = re.findall(r'<row[^>]*>(.*?)</row>', sheet_content, re.DOTALL)
        
        print(f"Total rows: {len(rows)}")
        
        # 读取第2行作为表头
        header_row = None
        for row in rows:
            if 'r="2"' in row:
                header_row = row
                break
        
        headers = {}
        if header_row:
            cells = re.findall(r'<c[^>]*r="([A-Z]+)2"[^>]*>(.*?)</c>', header_row, re.DOTALL)
            for col, cell in cells:
                val = ''
                if '<v>' in cell:
                    v_match = re.search(r'<v>(\d+)</v>', cell)
                    if v_match:
                        idx = int(v_match.group(1))
                        if idx < len(shared_strings):
                            val = shared_strings[idx]
                headers[col] = val
        
        print("\nHeaders:")
        for col in sorted(headers.keys()):
            print(f"  {col}: {headers[col]}")
        
        # 读取数据行（第3行到第46行）
        data_rows = []
        for row in rows:
            r_match = re.search(r'r="(\d+)"', row)
            if r_match:
                row_num = int(r_match.group(1))
                if 3 <= row_num <= 46:
                    cells = re.findall(r'<c[^>]*r="([A-Z]+)' + str(row_num) + r'"[^>]*>(.*?)</c>', row, re.DOTALL)
                    row_data = {'_row': row_num}
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
        
        # 打印前5行
        for row in data_rows[:5]:
            print(f"\nRow {row['_row']}:")
            for col in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']:
                if col in row:
                    print(f"  {headers.get(col, col)}({col}): {row[col]}")
