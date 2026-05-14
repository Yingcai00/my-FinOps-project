import zipfile
import re
import json

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
        
        # 读取第2行作为表头
        headers = {}
        for row_num, row_content in rows:
            if row_num == '2':
                cells = re.findall(r'<c[^>]*r="([A-Z]+)2"[^>]*>(.*?)</c>', row_content, re.DOTALL)
                for col, cell in cells:
                    val = ''
                    if '<v>' in cell:
                        v_match = re.search(r'<v>(\d+)</v>', cell)
                        if v_match:
                            idx = int(v_match.group(1))
                            if idx < len(shared_strings):
                                val = shared_strings[idx]
                    headers[col] = val
                break
        
        # 读取数据行（第3行到第46行）
        data_rows = []
        for row_num, row_content in rows:
            rnum = int(row_num)
            if 3 <= rnum <= 46:
                cells = re.findall(r'<c[^>]*r="([A-Z]+)' + row_num + r'"[^>]*>(.*?)</c>', row_content, re.DOTALL)
                row_data = {'_row': rnum}
                for col, cell in cells:
                    val = ''
                    if '<v>' in cell:
                        v_match = re.search(r'<v>([^<]*)</v>', cell)
                        if v_match:
                            v = v_match.group(1)
                            # 检查是否是共享字符串
                            if 't="s"' in cell:
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
                'diskTotal': row.get('S', ''),
                'trafficTotal': row.get('T', '')
            }
            js_data.append(item)
        
        # 输出JavaScript格式的数据
        print("const feb2026Data = [")
        for item in js_data:
            print(f"    {{ id: {item['id']}, category: '{item['category']}', pool: '{item['pool']}', name: '{item['name']}', region: '{item['region']}', sharePool: '{item['sharePool']}', shareType: '{item['shareType']}', description: '{item['description']}', unitPrice: '{item['unitPrice']}', depreciationMonths: '{item['depreciationMonths']}', depreciationMonthly: '{item['depreciationMonthly']}', quantity: '{item['quantity']}', unit: '{item['unit']}', costMonth: '{item['costMonth']}', monthlyCost: '{item['monthlyCost']}', shareRatio: '{item['shareRatio']}', sharedCost: '{item['sharedCost']}', cpuTotal: '{item['cpuTotal']}', memTotal: '{item['memTotal']}', diskTotal: '{item['diskTotal']}', trafficTotal: '{item['trafficTotal']}' }},"),
        print("];")
