import zipfile
import re
import json

# 读取Excel文件
xlsx_path = 'FinOps成本-产品模型20260208.xlsx'

data_rows = []

with zipfile.ZipFile(xlsx_path, 'r') as z:
    # 读取sharedStrings.xml获取所有文本
    shared_strings = []
    if 'xl/sharedStrings.xml' in z.namelist():
        with z.open('xl/sharedStrings.xml') as f:
            content = f.read().decode('utf-8')
            # 提取所有<t>标签中的文本
            matches = re.findall(r'<t[^>]*>([^<]*)</t>', content)
            shared_strings = matches
    
    print("Shared strings (first 50):")
    for i, s in enumerate(shared_strings[:50]):
        print(f"  {i}: {s}")
    print()
    
    # 读取sheet1.xml
    with z.open('xl/worksheets/sheet1.xml') as f:
        sheet_content = f.read().decode('utf-8')
        
        # 提取所有行数据
        rows = re.findall(r'<row[^>]*>(.*?)</row>', sheet_content, re.DOTALL)
        
        print(f"Total rows: {len(rows)}")
        print()
        
        # 从第2行到第46行（索引1到45）
        for i in range(1, min(46, len(rows))):
            row = rows[i]
            # 提取单元格值 - 改进匹配以获取r属性（单元格位置）
            cells = re.findall(r'<c([^>]*)>(.*?)</c>', row, re.DOTALL)
            row_data = []
            for attrs, cell in cells:
                # 检查是否是共享字符串
                if 't="s"' in attrs:
                    # 提取v标签中的索引
                    v_match = re.search(r'<v>(\d+)</v>', cell)
                    if v_match:
                        idx = int(v_match.group(1))
                        if idx < len(shared_strings):
                            row_data.append(shared_strings[idx])
                        else:
                            row_data.append('')
                    else:
                        row_data.append('')
                elif 't="str"' in attrs:
                    # 内联字符串
                    t_match = re.search(r'<t>([^<]*)</t>', cell)
                    if t_match:
                        row_data.append(t_match.group(1))
                    else:
                        row_data.append('')
                else:
                    # 直接值（数字）
                    v_match = re.search(r'<v>([^<]*)</v>', cell)
                    if v_match:
                        row_data.append(v_match.group(1))
                    else:
                        row_data.append('')
            data_rows.append(row_data)

# 打印所有行数据
print("\nData rows:")
for idx, row in enumerate(data_rows):
    print(f"Row {idx+2}: {row}")
