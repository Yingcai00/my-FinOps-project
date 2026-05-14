import re

# 读取asset_data.js文件
from repo_paths import HTML_DIR
with open('asset_data.js', 'r', encoding='utf-8') as f:
    asset_data_content = f.read()

# 读取HTML文件
with open(HTML_DIR / 'asset-ledger-management.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 找到assetData数组的开始位置
start_marker = '// 模拟B类资产数据（基于图片识别）'
start_idx = html_content.find(start_marker)
if start_idx == -1:
    print("未找到assetData开始标记")
    exit(1)

# 找到const assetData = [ 的位置
const_start = html_content.find('const assetData = [', start_idx)
if const_start == -1:
    print("未找到const assetData = [")
    exit(1)

# 找到subdivideData数组的开始位置（assetData结束后的下一个数组）
subdivide_marker = 'const subdivideData = ['
subdivide_idx = html_content.find(subdivide_marker, const_start)
if subdivide_idx == -1:
    print("未找到subdivideData开始标记")
    exit(1)

# 找到subdivideData数组的结束位置
# 向前查找subdivideData之前的]; 
# 实际上我们需要找到assetData数组的结束位置，即subdivideData之前的那个];
# 让我们从subdivide_idx向前查找
search_start = subdivide_idx
for i in range(search_start, const_start, -1):
    if html_content[i:i+2] == '];':
        # 找到了assetData数组的结束位置
        asset_data_end = i + 2
        break
else:
    print("未找到assetData数组的结束位置")
    exit(1)

# 替换assetData数组
new_html = html_content[:const_start] + asset_data_content + html_content[asset_data_end:]

# 保存更新后的HTML文件
with open(HTML_DIR / 'asset-ledger-management.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("HTML文件已更新，assetData数据已替换")
print(f"assetData数组从第{const_start}行到第{asset_data_end}行已被替换")
