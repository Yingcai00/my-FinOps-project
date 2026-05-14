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
            # 提取所有<t>标签中的文本
            matches = re.findall(r'<t[^>]*>([^<]*)</t>', content)
            shared_strings = matches
    
    print("All shared strings:")
    for i, s in enumerate(shared_strings):
        print(f"  {i}: {repr(s)}")
