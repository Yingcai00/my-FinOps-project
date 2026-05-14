import zipfile
import re

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
    
    # 检查特定索引
    indices = [14, 15, 16, 191, 192, 193]
    print("Checking specific indices:")
    for idx in indices:
        if idx < len(shared_strings):
            print(f"  {idx}: {shared_strings[idx]}")
        else:
            print(f"  {idx}: OUT OF RANGE")
