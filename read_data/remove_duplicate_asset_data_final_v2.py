import re

# 读取HTML文件
from repo_paths import HTML_DIR
with open(HTML_DIR / 'asset-ledger-management.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 找到第一个assetData数组的开始位置（第5766行附近的那个）
first_asset_data_start = html_content.find('const assetData = [')
if first_asset_data_start == -1:
    print("未找到assetData开始标记")
    exit(1)

# 找到第一个assetData数组的结束位置
# 计算括号的数量，确保找到正确的结束位置
bracket_count = 0
first_asset_data_end = -1
for i in range(first_asset_data_start, len(html_content)):
    if html_content[i] == '[':
        bracket_count += 1
    elif html_content[i] == ']':
        bracket_count -= 1
        if bracket_count == 0:
            first_asset_data_end = i + 1
            break

if first_asset_data_end == -1:
    print("未找到第一个assetData数组的结束位置")
    exit(1)

# 找到第二个assetData数组的开始位置（第821行附近的那个）
second_asset_data_start = html_content.find('const assetData = [', first_asset_data_end)
if second_asset_data_start == -1:
    print("未找到第二个assetData开始标记")
    exit(1)

# 找到第二个assetData数组的结束位置
# 计算括号的数量，确保找到正确的结束位置
bracket_count = 0
second_asset_data_end = -1
for i in range(second_asset_data_start, len(html_content)):
    if html_content[i] == '[':
        bracket_count += 1
    elif html_content[i] == ']':
        bracket_count -= 1
        if bracket_count == 0:
            second_asset_data_end = i + 1
            break

if second_asset_data_end == -1:
    print("未找到第二个assetData数组的结束位置")
    exit(1)

# 构建新的HTML内容，删除第二个assetData数组
new_html = html_content[:second_asset_data_start] + html_content[second_asset_data_end:]

# 保存更新后的HTML文件
with open(HTML_DIR / 'asset-ledger-management.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("HTML文件已更新，重复的assetData数组已删除")
