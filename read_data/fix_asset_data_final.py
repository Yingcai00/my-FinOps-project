import re

# 读取HTML文件
from repo_paths import HTML_DIR
with open(HTML_DIR / 'asset-ledger-management.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 找到assetData数组的开始位置
asset_data_start = html_content.find('const assetData = [')
if asset_data_start == -1:
    print("未找到assetData开始标记")
    exit(1)

# 找到assetData数组的结束位置
# 找到下一个变量定义的开始位置
next_var_marker = '// 资产列表相关变量'
next_var_idx = html_content.find(next_var_marker, asset_data_start)
if next_var_idx == -1:
    print("未找到下一个变量定义标记")
    exit(1)

# 从next_var_idx向前查找];
asset_data_end = -1
for i in range(next_var_idx, asset_data_start, -1):
    if html_content[i:i+2] == '];':
        asset_data_end = i + 2
        break

if asset_data_end == -1:
    print("未找到assetData数组的结束位置")
    exit(1)

# 提取assetData数组
asset_data = html_content[asset_data_start:asset_data_end]

# 找到filteredAssetData初始化的位置
filtered_asset_data_start = html_content.find('let filteredAssetData = [...assetData];')
if filtered_asset_data_start == -1:
    print("未找到filteredAssetData初始化位置")
    exit(1)

# 找到filteredAssetData初始化之前的位置
# 找到"// 资产列表相关变量"这一行
asset_list_vars = html_content.find('// 资产列表相关变量', 0, filtered_asset_data_start)
if asset_list_vars == -1:
    print("未找到资产列表相关变量标记")
    exit(1)

# 构建新的HTML内容
# 1. 保留从开始到资产列表相关变量之前的内容
# 2. 插入assetData数组
# 3. 保留从资产列表相关变量到assetData数组开始之前的内容
# 4. 保留从assetData数组结束之后到文件结束的内容

new_html = html_content[:asset_list_vars] + asset_data + '\n\n' + html_content[asset_list_vars:asset_data_start] + html_content[asset_data_end:]

# 保存更新后的HTML文件
with open(HTML_DIR / 'asset-ledger-management.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("HTML文件已更新，assetData数组已移到正确位置")
