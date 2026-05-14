import re

# 读取HTML文件
from repo_paths import HTML_DIR
with open(HTML_DIR / 'asset-ledger-management.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# 找到第一个assetData数组的开始和结束行
first_asset_data_start_line = -1
first_asset_data_end_line = -1
bracket_count = 0
for i, line in enumerate(lines):
    if 'const assetData = [' in line:
        first_asset_data_start_line = i
        bracket_count = 1
    elif first_asset_data_start_line != -1:
        bracket_count += line.count('[')
        bracket_count -= line.count(']')
        if bracket_count == 0:
            first_asset_data_end_line = i
            break

if first_asset_data_start_line == -1 or first_asset_data_end_line == -1:
    print("未找到第一个assetData数组")
    exit(1)

# 找到第二个assetData数组的开始和结束行
second_asset_data_start_line = -1
second_asset_data_end_line = -1
bracket_count = 0
for i, line in enumerate(lines[first_asset_data_end_line + 1:]):
    if 'const assetData = [' in line:
        second_asset_data_start_line = first_asset_data_end_line + 1 + i
        bracket_count = 1
    elif second_asset_data_start_line != -1:
        bracket_count += line.count('[')
        bracket_count -= line.count(']')
        if bracket_count == 0:
            second_asset_data_end_line = first_asset_data_end_line + 1 + i
            break

if second_asset_data_start_line == -1 or second_asset_data_end_line == -1:
    print("未找到第二个assetData数组")
    exit(1)

# 构建新的行列表，删除第二个assetData数组
new_lines = []
new_lines.extend(lines[:second_asset_data_start_line])
new_lines.extend(lines[second_asset_data_end_line + 1:])

# 保存更新后的HTML文件
with open(HTML_DIR / 'asset-ledger-management.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"HTML文件已更新，删除了第{second_asset_data_start_line+1}行到第{second_asset_data_end_line+1}行的重复assetData数组")
