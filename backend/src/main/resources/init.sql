-- 创建数据库
CREATE DATABASE IF NOT EXISTS finops DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

USE finops;

-- 用户表
CREATE TABLE IF NOT EXISTS users (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(100) NOT NULL,
    role VARCHAR(20) NOT NULL,
    name VARCHAR(50) NOT NULL,
    email VARCHAR(100),
    phone VARCHAR(20),
    department_id BIGINT,
    enabled BOOLEAN DEFAULT TRUE,
    created_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 部门表
CREATE TABLE IF NOT EXISTS departments (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    code VARCHAR(20) UNIQUE NOT NULL,
    parent_id BIGINT,
    manager_id BIGINT,
    description TEXT,
    created_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 成本项表
CREATE TABLE IF NOT EXISTS cost_items (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    category VARCHAR(50) NOT NULL,
    subcategory VARCHAR(50) NOT NULL,
    unit_price DECIMAL(18,2) NOT NULL,
    depreciation_months INT NOT NULL,
    quantity INT NOT NULL,
    unit VARCHAR(20) NOT NULL,
    monthly_cost DECIMAL(18,2),
    depreciation_monthly_price DECIMAL(18,2),
    share_type VARCHAR(20) NOT NULL,
    region VARCHAR(50) NOT NULL,
    share_dimension VARCHAR(50) NOT NULL,
    description TEXT,
    cost_code VARCHAR(50) UNIQUE,
    data_source VARCHAR(50) NOT NULL,
    cpu_total INT DEFAULT 0,
    memory_total INT DEFAULT 0,
    storage_total INT DEFAULT 0,
    traffic_total INT DEFAULT 0,
    cost_month VARCHAR(7) NOT NULL,
    created_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    INDEX idx_category (category),
    INDEX idx_cost_month (cost_month)
);

-- 产品表
CREATE TABLE IF NOT EXISTS products (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL,
    code VARCHAR(50) UNIQUE NOT NULL,
    description TEXT,
    bottleneck_resource VARCHAR(50) NOT NULL,
    pricing_formula TEXT NOT NULL,
    enabled BOOLEAN DEFAULT TRUE,
    created_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 产品成本关联表
CREATE TABLE IF NOT EXISTS product_cost_relations (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    product_id BIGINT NOT NULL,
    cost_item_id BIGINT NOT NULL,
    ratio DECIMAL(10,4) NOT NULL,
    created_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (cost_item_id) REFERENCES cost_items(id) ON DELETE CASCADE,
    INDEX idx_product_id (product_id)
);

-- 用量记录表
CREATE TABLE IF NOT EXISTS usage_records (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    product_id BIGINT NOT NULL,
    department_id BIGINT NOT NULL,
    project_id BIGINT,
    user_id BIGINT,
    amount DECIMAL(18,2) NOT NULL,
    usage_date DATETIME NOT NULL,
    usage_month VARCHAR(7) NOT NULL,
    created_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE,
    INDEX idx_usage_month (usage_month),
    INDEX idx_department_product (department_id, product_id)
);

-- 账单表
CREATE TABLE IF NOT EXISTS bills (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    department_id BIGINT NOT NULL,
    month VARCHAR(7) NOT NULL,
    total_amount DECIMAL(18,2) NOT NULL,
    status VARCHAR(20) NOT NULL DEFAULT '待审核',
    creator_id BIGINT,
    approver_id BIGINT,
    approve_time DATETIME,
    remark TEXT,
    created_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE,
    UNIQUE KEY uk_department_month (department_id, month),
    INDEX idx_month (month)
);

-- 账单明细表
CREATE TABLE IF NOT EXISTS bill_items (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    bill_id BIGINT NOT NULL,
    product_id BIGINT NOT NULL,
    amount DECIMAL(18,2) NOT NULL,
    unit_price DECIMAL(18,2) NOT NULL,
    subtotal DECIMAL(18,2) NOT NULL,
    created_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (bill_id) REFERENCES bills(id) ON DELETE CASCADE,
    FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
    INDEX idx_bill_id (bill_id)
);

-- 配置表
CREATE TABLE IF NOT EXISTS configurations (
    id BIGINT PRIMARY KEY AUTO_INCREMENT,
    key VARCHAR(50) UNIQUE NOT NULL,
    value TEXT NOT NULL,
    description TEXT,
    created_time DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- 插入初始数据
-- 插入默认管理员用户
INSERT INTO users (username, password, role, name, enabled) 
VALUES ('admin', '$2a$10$eW7kH7G3h8I9j0K1L2M3N4O5P6Q7R8S9T0U1V2W3X4Y5Z6A7B8C9D0E', 'ADMIN', '系统管理员', TRUE)
ON DUPLICATE KEY UPDATE password = VALUES(password);

-- 插入默认部门
INSERT INTO departments (name, code) 
VALUES ('总经办', 'GM'), ('技术部', 'TECH'), ('财务部', 'FIN'), ('运维部', 'OPS')
ON DUPLICATE KEY UPDATE name = VALUES(name);

-- 插入默认配置
INSERT INTO configurations (key, value, description) 
VALUES 
('system.name', 'FinOps财务运营管理平台', '系统名称'),
('system.version', '1.0.0', '系统版本'),
('cost.calculation.enable', 'true', '启用成本计算'),
('bill.generation.day', '5', '每月账单生成日')
ON DUPLICATE KEY UPDATE value = VALUES(value);
