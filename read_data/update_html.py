import re

# 读取asset_data.js文件
from repo_paths import HTML_DIR
with open('asset_data.js', 'r', encoding='utf-8') as f:
    asset_data_content = f.read()

# 读取HTML文件
with open(HTML_DIR / 'asset-ledger-management.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 替换assetData定义
# 找到const assetData = [ 开始的位置
pattern = r'const assetData = \[.*?\];'
replacement = asset_data_content

html_content = re.sub(pattern, replacement, html_content, flags=re.DOTALL)

# 保存更新后的HTML文件
with open(HTML_DIR / 'asset-ledger-management.html', 'w', encoding='utf-8') as f:
    f.write(html_content)

print("HTML文件已更新，assetData数据已替换")
