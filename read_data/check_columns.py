#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
检查Excel中的列结构
"""

import zipfile
import re

# Excel文件路径
excel_file = 'FinOps成本-产品模型20260208.xlsx'

# 打开Excel文件（实际上是zip文件）
with zipfile.ZipFile(excel_file, 'r') as z:
    # 读取共享字符串
    with z.open('xl/sharedStrings.xml') as f:
        shared_strings_content = f.read().decode('utf-8')
    
    # 解析共享字符串
    si_pattern = r'<si>(.*?)</si>'
    si_matches = re.findall(si_pattern, shared_strings_content, re.DOTALL)
    
    shared_strings = []
    for si in si_matches:
        t_pattern = r'<t[^>]*>(.*?)</t>'
        t_matches = re.findall(t_pattern, si, re.DOTALL)
        text = ''.join(t_matches)
        shared_strings.append(text)
    
    # 读取第一个工作表
    with z.open('xl/worksheets/sheet1.xml') as f:
        sheet_content = f.read().decode('utf-8')
    
    # 解析单元格
    cell_pattern = r'<c r="([A-Z]+)(\d+)"[^>]*?(?: t="s")?[^>]*>(?:<v>(.*?)</v>)?</c>'
    cells = re.findall(cell_pattern, sheet_content)
    
    # 组织数据
    data = {}
    for col, row, value in cells:
        row_num = int(row)
        if row_num not in data:
            data[row_num] = {}
        
        if value and value.isdigit():
            idx = int(value)
            if idx < len(shared_strings):
                data[row_num][col] = shared_strings[idx]
            else:
                data[row_num][col] = value
        else:
            data[row_num][col] = value
    
    # 打印第2行（表头）
    print("表头（第2行）:")
    if 2 in data:
        for col in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U']:
            val = data[2].get(col, '')
            print(f"  {col}: {val}")
    
    # 打印第3行（第一条数据）
    print("\n第3行（第一条数据）:")
    if 3 in data:
        for col in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']:
            val = data[3].get(col, '')
            print(f"  {col}: {val}")
    
    # 打印第19行（有价格数据的一行）
    print("\n第19行（有价格数据）:")
    if 19 in data:
        for col in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']:
            val = data[19].get(col, '')
            print(f"  {col}: {val}")
