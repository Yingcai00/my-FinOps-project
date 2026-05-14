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
        
        # 读取所有行并解析
        all_data = []
        for row in rows:
            # 获取行号
            r_match = re.search(r'r="(\d+)"', row)
            if r_match:
                row_num = int(r_match.group(1))
                cells = re.findall(r'<c[^>]*r="([A-Z]+)(\d+)"[^>]*>(.*?)</c>', row, re.DOTALL)
                row_data = {'_row': row_num}
                for col, _, cell in cells:
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
                all_data.append(row_data)
        
        # 打印前10行查看结构
        print("\nFirst 10 rows:")
        for row in all_data[:10]:
            print(f"Row {row['_row']}: A={row.get('A', '')}, B={row.get('B', '')}, C={row.get('C', '')}")
