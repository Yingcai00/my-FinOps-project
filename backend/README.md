# FinOps后端服务部署指南

## 系统要求

- **Java**: JDK 17或更高版本
- **Maven**: 3.8或更高版本
- **MySQL**: 8.0或更高版本
- **Redis**: 7.0或更高版本（可选，用于缓存）
- **RabbitMQ**: 3.10或更高版本（可选，用于消息队列）

## 安装步骤

### 1. 安装Java

1. 下载JDK 17或更高版本：[Oracle JDK](https://www.oracle.com/java/technologies/downloads/) 或 [OpenJDK](https://openjdk.org/)
2. 按照安装向导完成安装
3. 配置环境变量：
   - 添加 `JAVA_HOME` 环境变量，指向JDK安装目录
   - 将 `%JAVA_HOME%\bin` 添加到 `PATH` 环境变量
4. 验证安装：
   ```cmd
   java -version
   ```

### 2. 安装Maven

1. 下载Maven 3.8或更高版本：[Apache Maven](https://maven.apache.org/download.cgi)
2. 解压到指定目录
3. 配置环境变量：
   - 添加 `MAVEN_HOME` 环境变量，指向Maven安装目录
   - 将 `%MAVEN_HOME%\bin` 添加到 `PATH` 环境变量
4. 验证安装：
   ```cmd
   mvn -version
   ```

### 3. 安装MySQL

1. 下载MySQL 8.0或更高版本：[MySQL Community Server](https://dev.mysql.com/downloads/mysql/)
2. 按照安装向导完成安装
3. 启动MySQL服务
4. 创建数据库：
   ```sql
   CREATE DATABASE finops DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```
5. 执行初始化脚本：
   - 运行 `src/main/resources/init.sql` 文件，创建表结构和初始数据

### 4. 配置数据库连接

编辑 `src/main/resources/application-dev.yml` 文件，修改数据库连接信息：

```yaml
spring:
  datasource:
    url: jdbc:mysql://localhost:3306/finops?useUnicode=true&characterEncoding=utf8&useSSL=false&serverTimezone=Asia/Shanghai
    username: root  # 替换为你的MySQL用户名
    password: 123456  # 替换为你的MySQL密码
    driver-class-name: com.mysql.cj.jdbc.Driver
```

## 构建和启动

### 1. 构建项目

在项目根目录执行：

```cmd
mvn clean package -DskipTests
```

### 2. 启动服务

执行以下命令启动服务：

```cmd
java -jar target/finops-backend-1.0.0.jar
```

### 3. 验证服务

服务启动后，可通过以下地址访问：
- API文档：`http://localhost:8080/swagger-ui.html`
- 健康检查：`http://localhost:8080/actuator/health`

## 项目结构

```
backend/
├── src/
│   ├── main/
│   │   ├── java/com/finops/
│   │   │   ├── controller/     # 控制器层
│   │   │   ├── service/        # 服务层
│   │   │   ├── mapper/         # 数据访问层
│   │   │   ├── model/          # 数据模型
│   │   │   ├── config/         # 系统配置
│   │   │   ├── filter/         # 过滤器
│   │   │   ├── util/           # 工具类
│   │   │   └── FinOpsApplication.java  # 应用主类
│   │   └── resources/
│   │       ├── mapper/         # XML映射文件
│   │       ├── init.sql        # 数据库初始化脚本
│   │       ├── application.yml # 应用配置
│   │       └── application-dev.yml # 开发环境配置
│   └── test/                   # 测试代码
├── pom.xml                     # Maven配置
└── README.md                   # 项目说明
```

## API接口

### 认证接口
- `POST /api/v1/auth/login` - 用户登录

### 成本管理接口
- `POST /api/v1/cost/items` - 批量导入成本项
- `POST /api/v1/cost/items/sync` - 自动同步成本项
- `GET /api/v1/cost/items` - 获取成本项列表
- `POST /api/v1/cost/calculate` - 计算成本

### 产品管理接口
- `POST /api/v1/products` - 添加产品
- `GET /api/v1/products` - 获取产品列表
- `PUT /api/v1/products/{id}` - 更新产品
- `POST /api/v1/products/calculate` - 计算产品单价

### 计费管理接口
- `POST /api/v1/usage` - 记录使用量
- `POST /api/v1/usage/batch` - 批量记录使用量

### 账单管理接口
- `POST /api/v1/bills` - 生成部门账单
- `GET /api/v1/bills` - 获取账单列表
- `POST /api/v1/bills/{id}/approve` - 审核账单

### 配置管理接口
- `GET /api/v1/config/{key}` - 获取配置值
- `PUT /api/v1/config/{key}` - 更新配置值

## 常见问题

### 1. 数据库连接失败
- 检查MySQL服务是否启动
- 验证数据库连接信息是否正确
- 确认数据库用户权限是否足够

### 2. 端口占用
- 修改 `application.yml` 文件中的 `server.port` 配置
- 或者关闭占用该端口的其他服务

### 3. 依赖下载失败
- 检查网络连接
- 配置Maven镜像源，加速依赖下载

### 4. 服务启动缓慢
- 检查数据库连接速度
- 优化JVM参数，增加内存分配

## 技术栈

- **后端框架**: Spring Boot 3.2
- **ORM框架**: MyBatis-Plus 3.5
- **数据库**: MySQL 8.0
- **认证**: JWT
- **缓存**: Redis
- **消息队列**: RabbitMQ
- **API文档**: Swagger

## 联系方式

如果遇到问题，请联系系统管理员或查看项目文档。
