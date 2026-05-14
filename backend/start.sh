#!/bin/bash

# 启动脚本

echo "=== FinOps后端服务启动脚本 ==="

# 检查Java环境
if ! command -v java &> /dev/null; then
    echo "错误: 未找到Java环境，请安装JDK 17或更高版本"
    exit 1
fi

JAVA_VERSION=$(java -version 2>&1 | grep -oP 'version "\K[0-9]+')
if [ "$JAVA_VERSION" -lt 17 ]; then
    echo "错误: Java版本过低，请安装JDK 17或更高版本"
    exit 1
fi

echo "Java环境检查通过"

# 检查Maven环境
if ! command -v mvn &> /dev/null; then
    echo "错误: 未找到Maven环境，请安装Maven 3.8或更高版本"
    exit 1
fi

echo "Maven环境检查通过"

# 构建项目
echo "开始构建项目..."
mvn clean package -DskipTests

if [ $? -ne 0 ]; then
    echo "错误: 项目构建失败"
    exit 1
fi

echo "项目构建成功"

# 启动应用
echo "开始启动应用..."
java -jar target/finops-backend-1.0.0.jar
