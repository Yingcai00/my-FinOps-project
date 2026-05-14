import re

# 读取HTML文件
from repo_paths import HTML_DIR
with open(HTML_DIR / 'asset-ledger-management.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到assetData数组的开始和结束行
asset_data_start_line = -1
asset_data_end_line = -1
bracket_count = 0
for i, line in enumerate(lines):
    if 'const assetData = [' in line:
        asset_data_start_line = i
        bracket_count = 1
    elif asset_data_start_line != -1:
        bracket_count += line.count('[')
        bracket_count -= line.count(']')
        if bracket_count == 0:
            asset_data_end_line = i
            break

if asset_data_start_line == -1 or asset_data_end_line == -1:
    print("未找到assetData数组")
    exit(1)

# 提取assetData数组
asset_data_lines = lines[asset_data_start_line:asset_data_end_line + 1]

# 找到filteredAssetData初始化的行
filtered_asset_data_line = -1
for i, line in enumerate(lines):
    if 'let filteredAssetData = [...assetData];' in line:
        filtered_asset_data_line = i
        break

if filtered_asset_data_line == -1:
    print("未找到filteredAssetData初始化")
    exit(1)

# 找到"// 资产列表相关变量"这一行
asset_list_vars_line = -1
for i in range(filtered_asset_data_line, 0, -1):
    if '// 资产列表相关变量' in lines[i]:
        asset_list_vars_line = i
        break

if asset_list_vars_line == -1:
    print("未找到资产列表相关变量标记")
    exit(1)

# 构建新的行列表
new_lines = []
# 1. 保留从开始到资产列表相关变量之前的内容
new_lines.extend(lines[:asset_list_vars_line])
# 2. 插入assetData数组
new_lines.extend(asset_data_lines)
new_lines.append('\n')
# 3. 保留从资产列表相关变量到assetData数组开始之前的内容
new_lines.extend(lines[asset_list_vars_line:asset_data_start_line])
# 4. 保留从assetData数组结束之后到文件结束的内容
new_lines.extend(lines[asset_data_end_line + 1:])

# 保存更新后的HTML文件
with open(HTML_DIR / 'asset-ledger-management.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"HTML文件已更新，assetData数组已从第{asset_data_start_line+1}行移到第{asset_list_vars_line+1}行之前")
