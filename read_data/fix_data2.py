import zipfile
import re

# 读取Excel文件
xlsx_path = 'FinOps成本-产品模型20260208.xlsx'

with zipfile.ZipFile(xlsx_path, 'r') as z:
    # 读取sharedStrings.xml获取所有文本
    shared_strings = []
    if 'xl/sharedStrings.xml' in z.namelist():
        with z.open('xl/sharedStrings.xml') as f:
            content = f.read().decode('utf-8')
            matches = re.findall(r'<t[^>]*>([^<]*)</t>', content)
            shared_strings = matches
    
    # 读取sheet1.xml
    with z.open('xl/worksheets/sheet1.xml') as f:
        sheet_content = f.read().decode('utf-8')
        
        # 提取所有行数据
        rows = re.findall(r'<row[^>]*r="(\d+)"[^>]*>(.*?)</row>', sheet_content, re.DOTALL)
        
        # 读取数据行（第3行到第46行）
        data_rows = []
        for row_num, row_content in rows:
            rnum = int(row_num)
            if 3 <= rnum <= 46:
                # 修复正则表达式 - 正确匹配单元格
                cells = re.findall(r'<c[^>]*r="([A-Z]+)\d+"([^>]*)>([^<]*(?:<v>[^<]*</v>[^<]*)?)</c>', row_content)
                row_data = {'_row': rnum}
                for col, attrs, cell_inner in cells:
                    val = ''
                    if '<v>' in cell_inner:
                        v_match = re.search(r'<v>([^<]*)</v>', cell_inner)
                        if v_match:
                            v = v_match.group(1)
                            # 检查是否是共享字符串
                            if 't="s"' in attrs:
                                idx = int(v)
                                if idx < len(shared_strings):
                                    val = shared_strings[idx]
                            else:
                                val = v
                    row_data[col] = val
                data_rows.append(row_data)
        
        # 生成JavaScript数据
        js_data = []
        for idx, row in enumerate(data_rows):
            item = {
                'id': idx + 1,
                'category': row.get('A', ''),
                'pool': row.get('B', ''),
                'name': row.get('C', ''),
                'region': row.get('D', ''),
                'sharePool': row.get('E', ''),
                'shareType': row.get('F', ''),
                'description': row.get('G', ''),
                'unitPrice': row.get('H', ''),
                'depreciationMonths': row.get('I', ''),
                'depreciationMonthly': row.get('J', ''),
                'quantity': row.get('K', ''),
                'unit': row.get('L', ''),
                'costMonth': '2026-02',
                'monthlyCost': row.get('N', ''),
                'shareRatio': row.get('O', ''),
                'sharedCost': row.get('P', ''),
                'cpuTotal': row.get('Q', ''),
                'memTotal': row.get('R', ''),
                'diskTotal': row.get('S', '')
            }
            js_data.append(item)
        
        # 输出JavaScript格式的数据到文件
        with open('js_data_fixed2.txt', 'w', encoding='utf-8') as f:
            f.write("// 模拟数据 - 2026-02的数据（根据Excel字段结构）\n")
            f.write("const feb2026Data = [\n")
            for item in js_data:
                f.write(f"    {{ id: {item['id']}, category: '{item['category']}', pool: '{item['pool']}', name: '{item['name']}', region: '{item['region']}', sharePool: '{item['sharePool']}', shareType: '{item['shareType']}', description: '{item['description']}', unitPrice: '{item['unitPrice']}', depreciationMonths: '{item['depreciationMonths']}', depreciationMonthly: '{item['depreciationMonthly']}', quantity: '{item['quantity']}', unit: '{item['unit']}', costMonth: '{item['costMonth']}', monthlyCost: '{item['monthlyCost']}', shareRatio: '{item['shareRatio']}', sharedCost: '{item['sharedCost']}', cpuTotal: '{item['cpuTotal']}', memTotal: '{item['memTotal']}', diskTotal: '{item['diskTotal']}' }},\n")
            f.write("];\n")
        
        print("Data written to js_data_fixed2.txt")
        print(f"Total records: {len(js_data)}")
        
        # 打印前10行验证
        print("\nFirst 10 rows:")
        for i, item in enumerate(js_data[:10]):
            print(f"Row {i+1}: category={item['category']}, pool={item['pool']}, name={item['name']}")
