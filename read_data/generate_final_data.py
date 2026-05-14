#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成完整的JavaScript数据 - 最终版
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
    
    # 解析共享字符串 - 修正版
    # 使用更精确的模式来提取si标签内容
    si_pattern = r'<si[^>]*>(.*?)</si>'
    si_matches = re.findall(si_pattern, shared_strings_content, re.DOTALL)
    
    shared_strings = []
    for si in si_matches:
        # 提取所有<t>标签的文本，包括富文本
        t_pattern = r'<t[^>]*>([^<]*)</t>'
        t_matches = re.findall(t_pattern, si)
        text = ''.join(t_matches)
        shared_strings.append(text)
    
    print(f"共享字符串数量: {len(shared_strings)}")
    print(f"前10个共享字符串: {shared_strings[:10]}")
    
    # 读取第一个工作表
    with z.open('xl/worksheets/sheet1.xml') as f:
        sheet_content = f.read().decode('utf-8')
    
    # 解析单元格 - 更精确的模式
    # 格式: <c r="A1" t="s"><v>0</v></c> 或 <c r="A1"><v>123</v></c>
    cell_pattern = r'<c r="([A-Z]+)(\d+)"([^>]*)>(?:<v>([^<]*)</v>)?</c>'
    cells = re.findall(cell_pattern, sheet_content)
    
    # 组织数据
    data = {}
    for col, row, attrs, value in cells:
        row_num = int(row)
        if row_num not in data:
            data[row_num] = {}
        
        # 检查是否是共享字符串类型
        if 't="s"' in attrs and value:
            try:
                idx = int(value)
                if 0 <= idx < len(shared_strings):
                    data[row_num][col] = shared_strings[idx]
                else:
                    data[row_num][col] = value
            except:
                data[row_num][col] = value
        else:
            # 数字类型
            data[row_num][col] = value
    
    # 打印第2行（表头）确认
    print("\n表头（第2行）:")
    if 2 in data:
        for col in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']:
            val = data[2].get(col, '')
            print(f"  {col}: {val}")
    
    # 打印第3行（第一条数据）确认
    print("\n第3行（第一条数据）:")
    if 3 in data:
        for col in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T']:
            val = data[3].get(col, '')
            print(f"  {col}: {val}")
    
    # 提取第3-46行的完整数据
    all_rows = []
    for row_num in range(3, 47):
        if row_num in data:
            row_data = data[row_num]
            all_rows.append({
                'row': row_num,
                'A': row_data.get('A', ''),  # 成本分类
                'B': row_data.get('B', ''),  # 成本池
                'C': row_data.get('C', ''),  # 成本项
                'D': row_data.get('D', ''),  # 地域
                'E': row_data.get('E', ''),  # 公摊池
                'F': row_data.get('F', ''),  # 公摊类型
                'G': row_data.get('G', ''),  # 描述
                'H': row_data.get('H', ''),  # 单价
                'I': row_data.get('I', ''),  # 折旧月限
                'J': row_data.get('J', ''),  # 折旧月价
                'K': row_data.get('K', ''),  # 数量
                'L': row_data.get('L', ''),  # 单位
                'M': row_data.get('M', ''),  # 账期
                'N': row_data.get('N', ''),  # 月成本
                'O': row_data.get('O', ''),  # 公摊比例
                'P': row_data.get('P', ''),  # 公摊后月总成本
                'Q': row_data.get('Q', ''),  # CPU
                'R': row_data.get('R', ''),  # MEM
                'S': row_data.get('S', ''),  # Disk
            })
    
    # 填充合并单元格的值（向前填充）
    last_category = ''
    last_pool = ''
    for row in all_rows:
        if row.get('A'):
            last_category = row['A']
        else:
            row['A'] = last_category
        
        if row.get('B'):
            last_pool = row['B']
        else:
            row['B'] = last_pool
    
    # 生成成本编码映射
    category_codes = {
        '设备费用': 'DEV',
        '运营费用': 'OPS',
        '软件平台': 'SW',
        '基础设施': 'INF',
        '网络带宽': 'NET'
    }
    
    # 生成JavaScript数据
    print("\n生成JavaScript数据...")
    
    js_lines = ['// 模拟数据 - 2026-02的数据（含成本编码和完整价格）', 'const feb2026Data = [']
    
    for i, row in enumerate(all_rows, 1):
        category = row.get('A', '')
        pool = row.get('B', '')
        name = row.get('C', '')
        region = row.get('D', '')
        share_pool = row.get('E', '')
        share_type = row.get('F', '')
        description = row.get('G', '')
        unit_price = row.get('H', '')
        depre_months = row.get('I', '')
        depre_monthly = row.get('J', '')
        quantity = row.get('K', '')
        unit = row.get('L', '')
        cost_month = row.get('M', '')
        monthly_cost = row.get('N', '')
        share_ratio = row.get('O', '')
        shared_cost = row.get('P', '')
        cpu = row.get('Q', '')
        mem = row.get('R', '')
        disk = row.get('S', '')
        
        # 生成成本编码
        cat_code = category_codes.get(category, 'OTH')
        code = f"{cat_code}-{i:03d}"
        
        # 转义特殊字符
        name = name.replace("'", "\\'")
        description = description.replace("'", "\\'") if description else ''
        
        js_line = f"    {{ id: {i}, code: '{code}', category: '{category}', pool: '{pool}', name: '{name}', region: '{region}', sharePool: '{share_pool}', shareType: '{share_type}', description: '{description}', unitPrice: '{unit_price}', depreciationMonths: '{depre_months}', depreciationMonthly: '{depre_monthly}', quantity: '{quantity}', unit: '{unit}', costMonth: '2026-02', monthlyCost: '{monthly_cost}', shareRatio: '{share_ratio}', sharedCost: '{shared_cost}', cpuTotal: '{cpu}', memTotal: '{mem}', diskTotal: '{disk}' }}"
        
        if i < len(all_rows):
            js_line += ","
        
        js_lines.append(js_line)
    
    js_lines.append("];")
    
    # 保存到文件
    output_file = 'js_final_data.txt'
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(js_lines))
    
    print(f"\n数据已保存到 {output_file}")
    print(f"共提取 {len(all_rows)} 行数据")
    
    # 打印前5行作为示例
    print("\n前5行数据示例:")
    for i, row in enumerate(all_rows[:5], 1):
        cat_code = category_codes.get(row.get('A', ''), 'OTH')
        code = f"{cat_code}-{i:03d}"
        print(f"  编码:{code:<12} 分类:{row.get('A',''):<10} 池:{row.get('B',''):<10} 名称:{row.get('C',''):<30} 单价:{row.get('H',''):<10}")
    
    # 打印有价格数据的行
    print("\n有价格数据的行:")
    for i, row in enumerate(all_rows, 1):
        if row.get('H') or row.get('N'):
            cat_code = category_codes.get(row.get('A', ''), 'OTH')
            code = f"{cat_code}-{i:03d}"
            print(f"  编码:{code:<12} 名称:{row.get('C',''):<30} 单价:{row.get('H',''):<10} 月成本:{row.get('N',''):<10}")
