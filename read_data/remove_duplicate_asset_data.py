import re

# 读取HTML文件
from repo_paths import HTML_DIR
with open(HTML_DIR / 'asset-ledger-management.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 找到第一个assetData数组的结束位置（第5871行附近的那个）
first_asset_data_start = html_content.find('const assetData = [')
if first_asset_data_start == -1:
    print("未找到assetData开始标记")
    exit(1)

# 找到第一个assetData数组的结束位置
# 找到第一个subdivideData数组的开始位置
subdivide_marker = 'const subdivideData = ['
subdivide_idx = html_content.find(subdivide_marker, first_asset_data_start)
if subdivide_idx == -1:
    print("未找到subdivideData开始标记")
    exit(1)

# 从subdivide_idx向前查找第一个];
for i in range(subdivide_idx, first_asset_data_start, -1):
    if html_content[i:i+2] == '];':
        first_asset_data_end = i + 2
        break
else:
    print("未找到第一个assetData数组的结束位置")
    exit(1)

# 找到第二个assetData数组的开始位置（第817行附近的那个）
second_asset_data_start = html_content.find('const assetData = [', first_asset_data_end)
if second_asset_data_start == -1:
    print("未找到第二个assetData开始标记")
    exit(1)

# 找到第二个assetData数组的结束位置
# 找到第二个subdivideData数组的开始位置
second_subdivide_idx = html_content.find(subdivide_marker, second_asset_data_start)
if second_subdivide_idx == -1:
    print("未找到第二个subdivideData开始标记")
    exit(1)

# 从second_subdivide_idx向前查找第二个];
for i in range(second_subdivide_idx, second_asset_data_start, -1):
    if html_content[i:i+2] == '];':
        second_asset_data_end = i + 2
        break
else:
    print("未找到第二个assetData数组的结束位置")
    exit(1)

# 构建新的HTML内容，删除第二个assetData数组
new_html = html_content[:second_asset_data_start] + html_content[second_asset_data_end:]

# 保存更新后的HTML文件
with open(HTML_DIR / 'asset-ledger-management.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("HTML文件已更新，重复的assetData数组已删除")
