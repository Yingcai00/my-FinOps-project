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
        
        # 提取所有行数据
        rows = re.findall(r'<row[^>]*>(.*?)</row>', sheet_content, re.DOTALL)
        
        print(f"Total rows: {len(rows)}")
        
        # 读取第2行作为表头（r="2"）
        header_row = None
        for row in rows:
            if 'r="2"' in row:
                header_row = row
                break
        
        if header_row:
            cells = re.findall(r'<c[^>]*r="([A-Z]+)2"[^>]*>(.*?)</c>', header_row, re.DOTALL)
            print("\nHeaders (Row 2):")
            headers = {}
            for col, cell in cells:
                val = ''
                if '<v>' in cell:
                    v_match = re.search(r'<v>(\d+)</v>', cell)
                    if v_match:
                        idx = int(v_match.group(1))
                        if idx < len(shared_strings):
                            val = shared_strings[idx]
                headers[col] = val
                print(f"  {col}: {val}")
        
        # 读取数据行（第3行到第46行）
        data_rows = []
        for row_num in range(3, 47):  # 3到46
            for row in rows:
                if f'r="{row_num}"' in row:
                    cells = re.findall(r'<c[^>]*r="([A-Z]+)' + str(row_num) + r'"[^>]*>(.*?)</c>', row, re.DOTALL)
                    row_data = {}
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
                    break
        
        # 打印数据行
        print(f"\nData rows (Row 3-46): {len(data_rows)} rows")
        for idx, row in enumerate(data_rows[:5]):  # 只打印前5行
            print(f"\nRow {idx+3}:")
            for col in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']:
                if col in row:
                    print(f"  {col}: {row[col]}")
