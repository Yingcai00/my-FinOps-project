import pandas as pd

# 读取Excel文件
excel_file = '私有云服务目录.xlsx'
try:
    # 读取第一个工作表
    df = pd.read_excel(excel_file, sheet_name=0)
    
    # 打印列名
    print("列名:")
    print(df.columns.tolist())
    
    # 分析数据结构
    print("\n分析服务分类结构:")
    
    current_category = None
    current_service = None
    categories = {}
    
    for index, row in df.iterrows():
        # 获取第一列的值（服务分类）
        category = str(row.iloc[0]) if pd.notna(row.iloc[0]) else None
        # 获取第二列的值（服务名称）
        service = str(row.iloc[1]) if pd.notna(row.iloc[1]) else None
        # 获取第三列的值（规格簇）
        cluster = str(row.iloc[2]) if pd.notna(row.iloc[2]) else None
        # 获取第四列的值（具体规格）
        spec = str(row.iloc[3]) if pd.notna(row.iloc[3]) else None
        
        # 跳过NaN值
        if category == 'nan' and service == 'nan' and cluster == 'nan' and spec == 'nan':
            continue
        
        # 更新当前分类
        if category and category != 'nan':
            current_category = category
            if current_category not in categories:
                categories[current_category] = {}
        
        # 更新当前服务
        if service and service != 'nan':
            current_service = service
            if current_service not in categories[current_category]:
                categories[current_category][current_service] = []
        
        # 添加规格簇
        if cluster and cluster != 'nan' and current_category and current_service:
            if cluster not in categories[current_category][current_service]:
                categories[current_category][current_service].append(cluster)
        
    # 打印服务分类结构
    print("\n服务分类结构:")
    for category, services in categories.items():
        print(f"\n一级分类: {category}")
        for service, clusters in services.items():
            print(f"  二级分类: {service}")
            for cluster in clusters:
                print(f"    三级分类: {cluster}")
    
    # 生成JavaScript对象
    print("\n生成JavaScript服务分类对象:")
    print("const serviceCategoryData = {")
    for category, services in categories.items():
        print(f"  '{category}': {{")
        for service, clusters in services.items():
            print(f"    '{service}': [")
            for i, cluster in enumerate(clusters):
                if i < len(clusters) - 1:
                    print(f"      '{cluster}',")
                else:
                    print(f"      '{cluster}'")
            print("    ],")
        print("  },")
    print("};")
    
    print("\n分析完成！")
    
except Exception as e:
    print(f"读取文件时出错: {e}")
