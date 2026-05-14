import json
import re

from repo_paths import HTML_DIR

# 读取HTML文件
with open(HTML_DIR / 'asset-ledger-management.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 找到assetData数组的开始位置
start_marker = 'const assetData = ['
start_idx = html_content.find(start_marker)
if start_idx == -1:
    print("未找到assetData开始标记")
    exit(1)

# 找到assetData数组的结束位置
# 找到subdivideData数组的开始位置
subdivide_marker = 'const subdivideData = ['
subdivide_idx = html_content.find(subdivide_marker, start_idx)
if subdivide_idx == -1:
    print("未找到subdivideData开始标记")
    exit(1)

# 从subdivide_idx向前查找];
for i in range(subdivide_idx, start_idx, -1):
    if html_content[i:i+2] == '];':
        asset_data_end = i + 2
        break
else:
    print("未找到assetData数组的结束位置")
    exit(1)

# 提取assetData数组
asset_data_str = html_content[start_idx:asset_data_end]

# 提取JSON数据
json_str = asset_data_str.replace('const assetData = ', '').rstrip(';')

# 解析JSON
data = json.loads(json_str)

print(f"Asset data count in HTML: {len(data)}")
print(f"First asset: {data[0]}")
print(f"Last asset: {data[-1]}")
