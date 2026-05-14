import re

# 读取HTML文件
from repo_paths import HTML_DIR
with open(HTML_DIR / 'asset-ledger-management.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# 读取asset_data.js文件
with open('asset_data.js', 'r', encoding='utf-8') as f:
    asset_data_content = f.read()

# 找到"// 资产列表相关变量"这一行
asset_list_vars = html_content.find('// 资产列表相关变量')
if asset_list_vars == -1:
    print("未找到资产列表相关变量标记")
    exit(1)

# 构建新的HTML内容，在资产列表相关变量之前插入assetData数组
new_html = html_content[:asset_list_vars] + asset_data_content + '\n\n' + html_content[asset_list_vars:]

# 保存更新后的HTML文件
with open(HTML_DIR / 'asset-ledger-management.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("HTML文件已更新，assetData数组已添加到正确位置")
