#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提取Excel中的完整数据，包括成本编码和价格 - 修正版
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
        # 提取所有<t>标签的文本
        t_pattern = r'<t[^>]*>(.*?)</t>'
        t_matches = re.findall(t_pattern, si, re.DOTALL)
        text = ''.join(t_matches)
        shared_strings.append(text)
    
    print(f"共享字符串数量: {len(shared_strings)}")
    
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
        
        # 如果是共享字符串，查找实际值
        if value and value.isdigit():
            idx = int(value)
            if idx < len(shared_strings):
                data[row_num][col] = shared_strings[idx]
            else:
                data[row_num][col] = value
        else:
            data[row_num][col] = value
    
    # 打印所有行的列数据，用于调试
    print("\n前5行的列数据:")
    for row_num in range(1, 6):
        if row_num in data:
            print(f"\n第{row_num}行:")
            for col in sorted(data[row_num].keys()):
                val = data[row_num][col][:30] if data[row_num][col] else ''
                print(f"  {col}: {val}")
