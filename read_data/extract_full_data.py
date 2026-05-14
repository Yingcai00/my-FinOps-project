#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
提取Excel中的完整数据，包括成本编码和价格
"""

import zipfile
import re
from xml.etree import ElementTree as ET

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
    
    # 打印表头（第1行）
    print("\n表头（第1行）:")
    if 1 in data:
        for col in sorted(data[1].keys()):
            print(f"  {col}: {data[1][col]}")
    
    # 打印第2行（第一条数据）作为示例
    print("\n第2行数据示例:")
    if 2 in data:
        for col in sorted(data[2].keys()):
            print(f"  {col}: {data[2][col]}")
    
    # 提取第2-46行的完整数据
    print("\n提取第2-46行的完整数据:")
    
    all_rows = []
    for row_num in range(2, 47):
        if row_num in data:
            row_data = data[row_num]
            all_rows.append({
                'row': row_num,
                'A': row_data.get('A', ''),  # 成本编码
                'B': row_data.get('B', ''),  # 成本分类
                'C': row_data.get('C', ''),  # 成本池
                'D': row_data.get('D', ''),  # 成本项
                'E': row_data.get('E', ''),  # 地域
                'F': row_data.get('F', ''),  # 公摊池
                'G': row_data.get('G', ''),  # 公摊类型
                'H': row_data.get('H', ''),  # 描述
                'I': row_data.get('I', ''),  # 单价
                'J': row_data.get('J', ''),  # 折旧月限
                'K': row_data.get('K', ''),  # 折旧月价
                'L': row_data.get('L', ''),  # 数量
                'M': row_data.get('M', ''),  # 单位
                'N': row_data.get('N', ''),  # 账期
                'O': row_data.get('O', ''),  # 月成本
                'P': row_data.get('P', ''),  # 公摊比例
                'Q': row_data.get('Q', ''),  # 公摊后月总成本
                'R': row_data.get('R', ''),  # CPU
                'S': row_data.get('S', ''),  # MEM
                'T': row_data.get('T', ''),  # Disk
            })
    
    # 填充合并单元格的值（向前填充）
    last_category = ''
    last_pool = ''
    for row in all_rows:
        if row.get('B'):
            last_category = row['B']
        else:
            row['B'] = last_category
        
        if row.get('C'):
            last_pool = row['C']
        else:
            row['C'] = last_pool
    
    # 生成JavaScript数据
    print("\n生成JavaScript数据...")
    
    js_lines = ['// 模拟数据 - 2026-02的数据（含成本编码和完整价格）', 'const feb2026Data = [']
    
    for i, row in enumerate(all_rows, 1):
        code = row.get('A', '')
        category = row.get('B', '')
        pool = row.get('C', '')
        name = row.get('D', '')
        region = row.get('E', '')
        share_pool = row.get('F', '')
        share_type = row.get('G', '')
        description = row.get('H', '')
        unit_price = row.get('I', '')
        depre_months = row.get('J', '')
        depre_monthly = row.get('K', '')
        quantity = row.get('L', '')
        unit = row.get('M', '')
        cost_month = row.get('N', '')
        monthly_cost = row.get('O', '')
        share_ratio = row.get('P', '')
        shared_cost = row.get('Q', '')
        cpu = row.get('R', '')
        mem = row.get('S', '')
        disk = row.get('T', '')
        
        js_line = f"    {{ id: {i}, code: '{code}', category: '{category}', pool: '{pool}', name: '{name}', region: '{region}', sharePool: '{share_pool}', shareType: '{share_type}', description: '{description}', unitPrice: '{unit_price}', depreciationMonths: '{depre_months}', depreciationMonthly: '{depre_monthly}', quantity: '{quantity}', unit: '{unit}', costMonth: '2026-02', monthlyCost: '{monthly_cost}', shareRatio: '{share_ratio}', sharedCost: '{shared_cost}', cpuTotal: '{cpu}', memTotal: '{mem}', diskTotal: '{disk}' }}"
        
        if i < len(all_rows):
            js_line += ","
        
        js_lines.append(js_line)
    
    js_lines.append("];")
    
    # 保存到文件
    output_file = 'js_data_with_code.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(js_lines))
    
    print(f"\n数据已保存到 {output_file}")
    print(f"共提取 {len(all_rows)} 行数据")
    
    # 打印前5行作为示例
    print("\n前5行数据示例:")
    for row in all_rows[:5]:
        print(f"  编码:{row.get('A',''):<8} 分类:{row.get('B',''):<10} 池:{row.get('C',''):<10} 名称:{row.get('D',''):<30} 单价:{row.get('I',''):<10}")
