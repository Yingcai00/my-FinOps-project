import json

# 读取asset_data.js文件
with open('asset_data.js', 'r', encoding='utf-8') as f:
    content = f.read()

# 提取JSON数据
json_str = content.replace('const assetData = ', '').rstrip(';')

# 解析JSON
data = json.loads(json_str)

print(f"Asset data count: {len(data)}")
print(f"First asset: {data[0]}")
print(f"Last asset: {data[-1]}")
