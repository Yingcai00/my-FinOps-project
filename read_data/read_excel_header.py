import zipfile
import re

# 读取Excel文件
xlsx_path = 'FinOps成本-产品模型20260224.xlsx'

with zipfile.ZipFile(xlsx_path, 'r') as z:
    # 读取sharedStrings.xml获取所有文本
    shared_strings = []
    if 'xl/sharedStrings.xml' in z.namelist():
        with z.open('xl/sharedStrings.xml') as f:
            content = f.read().decode('utf-8')
            matches = re.findall(r'<t[^>]*>([^<]*)</t>', content)
            shared_strings = matches
    
    # 读取sheet4.xml（服务价格表2）
    with z.open('xl/worksheets/sheet4.xml') as f:
        sheet_content = f.read().decode('utf-8')
        
        # 提取第1行（表头）
        rows = re.findall(r'<row[^>]*>(.*?)</row>', sheet_content, re.DOTALL)
        
        if len(rows) > 0:
            header_row = rows[0]
            cells = re.findall(r'<c([^>]*)>(.*?)</c>', header_row, re.DOTALL)
            
            print("Header row:")
            for attrs, cell in cells:
                r_match = re.search(r'r="([A-Z]+)(\d+)"', attrs)
                if r_match:
                    col = r_match.group(1)
                    val = ''
                    if 't="s"' in attrs:
                        v_match = re.search(r'<v>(\d+)</v>', cell)
                        if v_match:
                            idx = int(v_match.group(1))
                            if idx < len(shared_strings):
                                val = shared_strings[idx]
                    elif 't="str"' in attrs:
                        t_match = re.search(r'<t>([^<]*)</t>', cell)
                        if t_match:
                            val = t_match.group(1)
                    else:
                        v_match = re.search(r'<v>([^<]*)</v>', cell)
                        if v_match:
                            val = v_match.group(1)
                    print(f"  Column {col}: {val}")
