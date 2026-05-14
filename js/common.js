// FinOps通用JavaScript库

const FinOps = {
    // 配置
    config: {
        apiBaseUrl: 'http://localhost:8080/api/v1',
        tokenKey: 'finops_token',
        userKey: 'finops_user'
    },

    // 用户信息
    currentUser: null,

    // 初始化
    init: function() {
        this.loadUserInfo();
        this.initSidebar();
        this.initTabs();
        this.initModals();
        this.checkAuth();
    },

    // 加载用户信息
    loadUserInfo: function() {
        const userStr = localStorage.getItem(this.config.userKey);
        if (userStr) {
            this.currentUser = JSON.parse(userStr);
            this.updateHeaderUserInfo();
        }
    },

    // 更新头部用户信息
    updateHeaderUserInfo: function() {
        const userAvatar = document.querySelector('.header-user-avatar');
        const userName = document.querySelector('.header-user-name');
        
        if (this.currentUser && userAvatar && userName) {
            userAvatar.textContent = this.currentUser.name ? this.currentUser.name.charAt(0) : 'U';
            userName.textContent = this.currentUser.name || this.currentUser.username;
        }
    },

    // 检查认证状态
    checkAuth: function() {
        const token = localStorage.getItem(this.config.tokenKey);
        const currentPage = window.location.pathname;
        
        // 如果不是登录页面且没有token，跳转到登录页
        if (!token && !currentPage.includes('login.html')) {
            window.location.href = 'login.html';
        }
    },

    // 登录
    login: function(username, password) {
        return fetch(`${this.config.apiBaseUrl}/auth/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ username, password })
        })
        .then(response => response.json())
        .then(data => {
            if (data.code === 200) {
                const { token, user } = data.data;
                localStorage.setItem(this.config.tokenKey, token);
                localStorage.setItem(this.config.userKey, JSON.stringify(user));
                this.currentUser = user;
                this.updateHeaderUserInfo();
                return { success: true };
            } else {
                return { success: false, message: data.message || '登录失败' };
            }
        })
        .catch(error => {
            console.error('登录错误:', error);
            return { success: false, message: '网络错误，请重试' };
        });
    },

    // 登出
    logout: function() {
        localStorage.removeItem(this.config.tokenKey);
        localStorage.removeItem(this.config.userKey);
        this.currentUser = null;
        window.location.href = 'login.html';
    },

    // 获取API请求头
    getHeaders: function() {
        const token = localStorage.getItem(this.config.tokenKey);
        return {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        };
    },

    // API请求
    api: {
        get: function(url) {
            return fetch(`${FinOps.config.apiBaseUrl}${url}`, {
                method: 'GET',
                headers: FinOps.getHeaders()
            })
            .then(response => response.json());
        },

        post: function(url, data) {
            return fetch(`${FinOps.config.apiBaseUrl}${url}`, {
                method: 'POST',
                headers: FinOps.getHeaders(),
                body: JSON.stringify(data)
            })
            .then(response => response.json());
        },

        put: function(url, data) {
            return fetch(`${FinOps.config.apiBaseUrl}${url}`, {
                method: 'PUT',
                headers: FinOps.getHeaders(),
                body: JSON.stringify(data)
            })
            .then(response => response.json());
        },

        delete: function(url) {
            return fetch(`${FinOps.config.apiBaseUrl}${url}`, {
                method: 'DELETE',
                headers: FinOps.getHeaders()
            })
            .then(response => response.json());
        }
    },

    // 初始化侧边栏
    initSidebar: function() {
        const collapseBtn = document.querySelector('.sidebar-collapse-btn');
        const sidebar = document.querySelector('.sidebar');
        
        if (!collapseBtn || !sidebar) return;

        let isCollapsed = false;

        collapseBtn.addEventListener('click', function() {
            isCollapsed = !isCollapsed;
            sidebar.classList.toggle('collapsed', isCollapsed);
            
            if (isCollapsed) {
                collapseBtn.textContent = '▶';
            } else {
                collapseBtn.textContent = '▼';
            }
        });

        // 菜单项点击事件
        document.querySelectorAll('.menu-item').forEach(menu => {
            menu.addEventListener('click', function(e) {
                const subMenu = this.nextElementSibling;
                if (subMenu && subMenu.classList.contains('sub-menu')) {
                    e.preventDefault();
                    this.classList.toggle('expanded');
                    subMenu.classList.toggle('expanded');
                }
            });
        });

        // 二级菜单点击事件
        document.querySelectorAll('.sub-menu-item').forEach(subMenu => {
            subMenu.addEventListener('click', function(e) {
                // 移除所有active类
                document.querySelectorAll('.menu-item, .sub-menu-item').forEach(item => {
                    item.classList.remove('active');
                });
                
                // 添加当前菜单的active类
                this.classList.add('active');
                
                // 添加父级菜单的active类
                const parentMenu = this.closest('li').parentElement.previousElementSibling;
                if (parentMenu) {
                    parentMenu.classList.add('active');
                    parentMenu.classList.add('expanded');
                    const subMenu = parentMenu.nextElementSibling;
                    if (subMenu) {
                        subMenu.classList.add('expanded');
                    }
                }
            });
        });

        // 标记当前页面的菜单项为active
        this.markActiveMenu();
    },

    // 标记当前页面的菜单项为active
    markActiveMenu: function() {
        const currentUrl = window.location.href;
        const menuItems = document.querySelectorAll('.menu-item, .sub-menu-item');
        
        menuItems.forEach(item => {
            const href = item.getAttribute('href');
            if (href && currentUrl.includes(href)) {
                item.classList.add('active');
                
                // 如果是二级菜单，也标记父级菜单为active
                if (item.classList.contains('sub-menu-item')) {
                    const parentMenu = item.closest('li').parentElement.previousElementSibling;
                    if (parentMenu) {
                        parentMenu.classList.add('active');
                        parentMenu.classList.add('expanded');
                        const subMenu = parentMenu.nextElementSibling;
                        if (subMenu) {
                            subMenu.classList.add('expanded');
                        }
                    }
                }
            }
        });
    },

    // 初始化标签页
    initTabs: function() {
        document.querySelectorAll('.tab').forEach(tab => {
            tab.addEventListener('click', function() {
                const tabContainer = this.closest('.tab-container');
                const tabId = this.dataset.tab;
                
                // 移除所有active类
                tabContainer.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                tabContainer.querySelectorAll('.tab-pane').forEach(p => p.classList.remove('active'));
                
                // 添加当前tab的active类
                this.classList.add('active');
                
                // 显示对应的tab-pane
                const tabPane = tabContainer.querySelector(`#${tabId}-tab`);
                if (tabPane) {
                    tabPane.classList.add('active');
                }
            });
        });
    },

    // 初始化模态框
    initModals: function() {
        document.querySelectorAll('.modal-close').forEach(btn => {
            btn.addEventListener('click', function() {
                const modal = this.closest('.modal');
                if (modal) {
                    modal.classList.remove('active');
                }
            });
        });

        document.querySelectorAll('.modal').forEach(modal => {
            modal.addEventListener('click', function(e) {
                if (e.target === this) {
                    this.classList.remove('active');
                }
            });
        });
    },

    // 显示模态框
    showModal: function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.add('active');
        }
    },

    // 隐藏模态框
    hideModal: function(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            modal.classList.remove('active');
        }
    },

    // 显示消息提示
    showMessage: function(message, type = 'info') {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message message-${type}`;
        messageDiv.textContent = message;
        messageDiv.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 12px 20px;
            border-radius: 4px;
            color: white;
            font-size: 14px;
            z-index: 9999;
            animation: slideIn 0.3s ease-out;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
        `;

        switch (type) {
            case 'success':
                messageDiv.style.backgroundColor = '#52c41a';
                break;
            case 'error':
                messageDiv.style.backgroundColor = '#ff4d4f';
                break;
            case 'warning':
                messageDiv.style.backgroundColor = '#faad14';
                break;
            default:
                messageDiv.style.backgroundColor = '#1890ff';
        }

        document.body.appendChild(messageDiv);

        setTimeout(() => {
            messageDiv.style.animation = 'slideOut 0.3s ease-in';
            setTimeout(() => {
                document.body.removeChild(messageDiv);
            }, 300);
        }, 3000);
    },

    // 显示确认对话框
    showConfirm: function(message, onConfirm) {
        const confirmDiv = document.createElement('div');
        confirmDiv.className = 'confirm-dialog-overlay';
        confirmDiv.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: rgba(0, 0, 0, 0.5);
            display: flex;
            align-items: center;
            justify-content: center;
            z-index: 1000;
        `;

        const confirmDialog = document.createElement('div');
        confirmDialog.className = 'confirm-dialog';
        confirmDialog.style.cssText = `
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
            width: 400px;
            padding: 24px;
        `;

        confirmDialog.innerHTML = `
            <div class="confirm-title" style="font-size: 16px; font-weight: 600; color: #333; margin-bottom: 16px;">确认</div>
            <div class="confirm-content" style="margin-bottom: 24px; color: #666;">${message}</div>
            <div class="confirm-actions" style="display: flex; justify-content: flex-end; gap: 12px;">
                <button class="btn btn-default confirm-cancel">取消</button>
                <button class="btn btn-primary confirm-ok">确定</button>
            </div>
        `;

        confirmDiv.appendChild(confirmDialog);
        document.body.appendChild(confirmDiv);

        confirmDialog.querySelector('.confirm-cancel').addEventListener('click', () => {
            document.body.removeChild(confirmDiv);
        });

        confirmDialog.querySelector('.confirm-ok').addEventListener('click', () => {
            document.body.removeChild(confirmDiv);
            if (onConfirm) onConfirm();
        });

        confirmDiv.addEventListener('click', (e) => {
            if (e.target === confirmDiv) {
                document.body.removeChild(confirmDiv);
            }
        });
    },

    // 格式化金额
    formatMoney: function(amount) {
        return '¥' + Number(amount).toLocaleString('zh-CN', {
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
        });
    },

    // 格式化日期
    formatDate: function(date, format = 'YYYY-MM-DD') {
        if (!date) return '';
        const d = new Date(date);
        const year = d.getFullYear();
        const month = String(d.getMonth() + 1).padStart(2, '0');
        const day = String(d.getDate()).padStart(2, '0');
        const hours = String(d.getHours()).padStart(2, '0');
        const minutes = String(d.getMinutes()).padStart(2, '0');
        const seconds = String(d.getSeconds()).padStart(2, '0');

        return format
            .replace('YYYY', year)
            .replace('MM', month)
            .replace('DD', day)
            .replace('HH', hours)
            .replace('mm', minutes)
            .replace('ss', seconds);
    },

    // 防抖函数
    debounce: function(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    },

    // 节流函数
    throttle: function(func, limit) {
        let inThrottle;
        return function(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
};

// 添加CSS动画
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    @keyframes slideOut {
        from {
            transform: translateX(0);
            opacity: 1;
        }
        to {
            transform: translateX(100%);
            opacity: 0;
        }
    }
`;
document.head.appendChild(style);

// 页面加载完成后初始化
document.addEventListener('DOMContentLoaded', function() {
    FinOps.init();
});
