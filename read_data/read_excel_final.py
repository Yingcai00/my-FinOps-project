import zipfile
import re

# 读取Excel文件
xlsx_path = 'FinOps成本-产品模型20260224.xlsx'

def read_sheet(z, sheet_name, shared_strings):
    """读取指定的sheet并返回数据"""
    with z.open(f'xl/worksheets/{sheet_name}.xml') as f:
        sheet_content = f.read().decode('utf-8')
        
        # 提取所有行数据
        rows = re.findall(r'<row[^>]*>(.*?)</row>', sheet_content, re.DOTALL)
        
        print(f"Total rows: {len(rows)}")
        print()
        
        # 读取表头（第1行）
        header_row = []
        if rows:
            header = rows[0]
            cells = re.findall(r'<c([^>]*)>(.*?)</c>', header, re.DOTALL)
            for attrs, cell in cells:
                val = ''
                # 检查是否是共享字符串
                if 't="s"' in attrs:
                    # 提取v标签中的索引
                    v_match = re.search(r'<v>(\d+)</v>', cell)
                    if v_match:
                        idx = int(v_match.group(1))
                        if idx < len(shared_strings):
                            val = shared_strings[idx]
                elif 't="str"' in attrs:
                    # 内联字符串
                    t_match = re.search(r'<t>([^<]*)</t>', cell)
                    if t_match:
                        val = t_match.group(1)
                else:
                    # 直接值（数字）
                    v_match = re.search(r'<v>([^<]*)</v>', cell)
                    if v_match:
                        val = v_match.group(1)
                header_row.append(val)
        
        return header_row

with zipfile.ZipFile(xlsx_path, 'r') as z:
    # 读取sharedStrings.xml获取所有文本
    shared_strings = []
    if 'xl/sharedStrings.xml' in z.namelist():
        with z.open('xl/sharedStrings.xml') as f:
            content = f.read().decode('utf-8')
            # 提取所有<t>标签中的文本
            matches = re.findall(r'<t[^>]*>([^<]*)</t>', content)
            shared_strings = matches
    
    # 读取资产管理sheet（sheet1.xml）
    print("=== Sheet 1: 资产管理 ===")
    asset_header = read_sheet(z, 'sheet1', shared_strings)
    print("Header row:")
    print(asset_header)
    print()
    
    # 读取服务价格表2（sheet2.xml）
    print("=== Sheet 2: 服务价格表2 ===")
    price_header = read_sheet(z, 'sheet2', shared_strings)
    print("Header row:")
    print(price_header)
    print()
    
    # 读取计量台账（sheet3.xml）
    print("=== Sheet 3: 计量台账 ===")
    metering_header = read_sheet(z, 'sheet3', shared_strings)
    print("Header row:")
    print(metering_header)
    print()
    
    # 读取账单（sheet4.xml）
    print("=== Sheet 4: 账单 ===")
    bill_header = read_sheet(z, 'sheet4', shared_strings)
    print("Header row:")
    print(bill_header)
    print()
