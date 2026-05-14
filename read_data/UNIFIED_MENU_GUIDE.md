# FinOps统一菜单与交互适配指南

## 1. 概述

本指南旨在为FinOps财务运营管理平台的所有页面提供统一的菜单和交互系统，确保所有页面具有一致的用户体验和视觉风格。

## 2. 文件结构

```
FinOpsV2.0/
├── css/
│   └── common.css              # 通用样式文件
├── js/
│   └── common.js               # 通用JavaScript库
├── components/
│   ├── header.html             # 头部组件
│   └── sidebar.html            # 侧边栏组件
├── template.html               # 页面模板
├── index.html                 # 主页（成本管理）
├── cost-overview.html         # 成本总览页
├── cost-analysis.html          # 成本分析页
├── cost-optimization.html     # 成本优化页
├── cost-detail.html           # 成本详情页
└── login.html                # 登录页
```

## 3. 核心组件

### 3.1 通用样式文件 (css/common.css)

包含所有页面的通用样式，包括：
- 头部样式
- 侧边栏样式
- 菜单项样式
- 卡片样式
- 按钮样式
- 表格样式
- 表单样式
- 标签页样式
- 模态框样式
- 工具提示样式
- 响应式设计

### 3.2 通用JavaScript库 (js/common.js)

提供以下功能：
- 用户认证管理（登录、登出）
- API请求封装
- 侧边栏交互
- 标签页切换
- 模态框控制
- 消息提示
- 确认对话框
- 工具函数（格式化金额、日期等）

### 3.3 头部组件 (components/header.html)

包含：
- 系统标题
- 用户信息显示
- 退出按钮

### 3.4 侧边栏组件 (components/sidebar.html)

包含完整的菜单结构：
- 成本管理（成本总览、成本分析）
- 产品管理（产品列表、定价管理）
- 计费管理（用量记录、用量统计）
- 账单管理（部门账单、账单审核）
- 系统管理（用户管理、角色权限、系统配置）

## 4. 页面适配步骤

### 4.1 基础页面结构

每个页面都应该遵循以下结构：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FinOps财务运营管理平台 - 页面标题</title>
    <!-- 引入通用样式 -->
    <link rel="stylesheet" href="css/common.css">
</head>
<body>
    <!-- 头部容器 -->
    <div id="header-container"></div>

    <!-- 主容器 -->
    <div class="container">
        <!-- 侧边栏容器 -->
        <div id="sidebar-container"></div>
        
        <!-- 内容区域 -->
        <div class="content">
            <!-- 页面具体内容 -->
        </div>
    </div>

    <!-- 引入通用JavaScript -->
    <script src="js/common.js"></script>
    
    <!-- 页面初始化 -->
    <script>
        // 加载头部组件
        fetch('components/header.html')
            .then(response => response.text())
            .then(html => {
                document.getElementById('header-container').innerHTML = html;
            });

        // 加载侧边栏组件
        fetch('components/sidebar.html')
            .then(response => response.text())
            .then(html => {
                document.getElementById('sidebar-container').innerHTML = html;
                // 侧边栏加载完成后初始化
                setTimeout(() => {
                    FinOps.initSidebar();
                    FinOps.markActiveMenu();
                }, 100);
            });
    </script>
</body>
</html>
```

### 4.2 页面适配检查清单

- [ ] 引入通用样式文件 `css/common.css`
- [ ] 引入通用JavaScript库 `js/common.js`
- [ ] 添加头部容器 `#header-container`
- [ ] 添加侧边栏容器 `#sidebar-container`
- [ ] 添加页面初始化脚本
- [ ] 移除页面内联样式（使用通用样式）
- [ ] 移除页面内联JavaScript（使用通用库）
- [ ] 确保菜单项与当前页面匹配

## 5. 统一交互功能

### 5.1 侧边栏折叠/展开

侧边栏支持折叠和展开功能，点击折叠按钮即可切换。

### 5.2 菜单项高亮

系统会自动根据当前页面URL高亮对应的菜单项。

### 5.3 标签页切换

使用统一的标签页样式和交互逻辑：

```html
<div class="tab-container">
    <div class="tabs">
        <div class="tab active" data-tab="detail">详情</div>
        <div class="tab" data-tab="analysis">分析</div>
    </div>
    <div class="tab-content">
        <div class="tab-pane active" id="detail-tab">详情内容</div>
        <div class="tab-pane" id="analysis-tab">分析内容</div>
    </div>
</div>
```

### 5.4 模态框

使用统一的模态框样式：

```html
<div class="modal" id="modal-id">
    <div class="modal-content">
        <div class="modal-header">
            <div class="modal-title">标题</div>
            <button class="modal-close">×</button>
        </div>
        <div class="modal-body">
            内容
        </div>
        <div class="modal-footer">
            <button class="btn btn-default">取消</button>
            <button class="btn btn-primary">确定</button>
        </div>
    </div>
</div>
```

控制模态框：

```javascript
// 显示模态框
FinOps.showModal('modal-id');

// 隐藏模态框
FinOps.hideModal('modal-id');
```

### 5.5 消息提示

使用统一的消息提示：

```javascript
// 成功消息
FinOps.showMessage('操作成功', 'success');

// 错误消息
FinOps.showMessage('操作失败', 'error');

// 警告消息
FinOps.showMessage('请注意', 'warning');

// 信息消息
FinOps.showMessage('提示信息', 'info');
```

### 5.6 确认对话框

使用统一的确认对话框：

```javascript
FinOps.showConfirm('确定要删除吗？', function() {
    // 确认后的操作
    console.log('用户确认删除');
});
```

## 6. API请求

使用统一的API请求方法：

```javascript
// GET请求
FinOps.api.get('/cost/items').then(data => {
    console.log(data);
});

// POST请求
FinOps.api.post('/cost/items', { name: '测试' }).then(data => {
    console.log(data);
});

// PUT请求
FinOps.api.put('/cost/items/1', { name: '更新' }).then(data => {
    console.log(data);
});

// DELETE请求
FinOps.api.delete('/cost/items/1').then(data => {
    console.log(data);
});
```

## 7. 工具函数

### 7.1 格式化金额

```javascript
const formatted = FinOps.formatMoney(1234567.89);
// 输出: ¥1,234,567.89
```

### 7.2 格式化日期

```javascript
const formatted = FinOps.formatDate(new Date(), 'YYYY-MM-DD HH:mm:ss');
// 输出: 2026-01-30 14:30:00
```

### 7.3 防抖函数

```javascript
const debouncedFn = FinOps.debounce(function() {
    console.log('防抖执行');
}, 300);
```

### 7.4 节流函数

```javascript
const throttledFn = FinOps.throttle(function() {
    console.log('节流执行');
}, 300);
```

## 8. 现有页面适配

### 8.1 已适配的页面

以下页面已经完成统一适配：
- `index_new.html` - 主页（成本管理）
- `cost-overview_new.html` - 成本总览页

### 8.2 待适配的页面

以下页面需要按照本指南进行适配：
- `cost-analysis.html` - 成本分析页
- `cost-optimization.html` - 成本优化页
- `cost-detail.html` - 成本详情页
- `login.html` - 登录页（特殊处理）

## 9. 登录页适配

登录页不需要头部和侧边栏，只需要引入通用样式：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>FinOps财务运营管理平台 - 登录</title>
    <!-- 引入通用样式 -->
    <link rel="stylesheet" href="css/common.css">
</head>
<body>
    <!-- 登录表单 -->
    <div class="login-container">
        <!-- 登录内容 -->
    </div>

    <!-- 引入通用JavaScript -->
    <script src="js/common.js"></script>
    
    <!-- 登录逻辑 -->
    <script>
        document.querySelector('.login-form').addEventListener('submit', function(e) {
            e.preventDefault();
            const username = document.getElementById('username').value;
            const password = document.getElementById('password').value;
            
            FinOps.login(username, password).then(result => {
                if (result.success) {
                    window.location.href = 'index.html';
                } else {
                    FinOps.showMessage(result.message, 'error');
                }
            });
        });
    </script>
</body>
</html>
```

## 10. 样式覆盖

如果页面需要特殊样式，可以在页面头部添加额外的样式：

```html
<style>
    /* 页面特定样式 */
    .page-specific {
        /* 自定义样式 */
    }
</style>
```

## 11. JavaScript扩展

如果页面需要额外的JavaScript功能，可以在页面初始化脚本中添加：

```javascript
// 页面特定功能
function initPageSpecificFeatures() {
    // 页面特定逻辑
}

// 在组件加载完成后调用
fetch('components/sidebar.html')
    .then(response => response.text())
    .then(html => {
        document.getElementById('sidebar-container').innerHTML = html;
        setTimeout(() => {
            FinOps.initSidebar();
            FinOps.markActiveMenu();
            initPageSpecificFeatures(); // 调用页面特定功能
        }, 100);
    });
```

## 12. 最佳实践

### 12.1 保持一致性

- 所有页面使用相同的头部和侧边栏
- 所有按钮使用统一的样式类
- 所有表单使用统一的样式类
- 所有消息提示使用统一的API

### 12.2 性能优化

- 使用组件懒加载
- 使用防抖和节流函数
- 避免重复的DOM操作
- 使用事件委托

### 12.3 可访问性

- 确保所有交互元素都有适当的标签
- 确保键盘导航支持
- 确保颜色对比度符合标准

### 12.4 响应式设计

- 使用媒体查询适配不同屏幕尺寸
- 确保移动端体验良好
- 测试不同设备的兼容性

## 13. 故障排除

### 13.1 组件加载失败

如果组件加载失败，检查：
- 组件文件路径是否正确
- 服务器是否正常运行
- 浏览器控制台是否有错误信息

### 13.2 样式不生效

如果样式不生效，检查：
- 通用样式文件是否正确引入
- 样式优先级是否正确
- 浏览器缓存是否需要清除

### 13.3 JavaScript错误

如果出现JavaScript错误，检查：
- 通用JavaScript库是否正确引入
- 页面初始化脚本是否正确
- 浏览器控制台的错误信息

## 14. 总结

通过使用统一的菜单和交互系统，可以确保：

1. **一致性**：所有页面具有统一的视觉风格和交互体验
2. **可维护性**：修改一处即可影响所有页面
3. **可扩展性**：新增页面可以快速复用现有组件
4. **用户体验**：用户在不同页面间切换时体验一致

请按照本指南对所有页面进行适配，确保整个系统的一致性和可维护性。

---

**文档版本**: v1.0
**编制日期**: 2026-01-30
**编制人**: 全栈产品专家
