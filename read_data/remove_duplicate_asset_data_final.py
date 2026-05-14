import re

# 读取HTML文件
from repo_paths import HTML_DIR
with open(HTML_DIR / 'asset-ledger-management.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 找到第一个assetData数组的开始位置（第817行附近的那个）
first_asset_data_start = html_content.find('const assetData = [')
if first_asset_data_start == -1:
    print("未找到assetData开始标记")
    exit(1)

# 找到第一个assetData数组的结束位置
# 找到下一个变量定义的开始位置
next_var_marker = '// 资产列表相关变量'
next_var_idx = html_content.find(next_var_marker, first_asset_data_start)
if next_var_idx == -1:
    print("未找到下一个变量定义标记")
    exit(1)

# 从next_var_idx向前查找];
first_asset_data_end = -1
for i in range(next_var_idx, first_asset_data_start, -1):
    if html_content[i:i+2] == '];':
        first_asset_data_end = i + 2
        break

if first_asset_data_end == -1:
    print("未找到第一个assetData数组的结束位置")
    exit(1)

# 构建新的HTML内容，删除第一个assetData数组
new_html = html_content[:first_asset_data_start] + html_content[first_asset_data_end:]

# 保存更新后的HTML文件
with open(HTML_DIR / 'asset-ledger-management.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("HTML文件已更新，重复的assetData数组已删除")
