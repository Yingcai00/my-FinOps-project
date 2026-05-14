/**
 * FinOps 原型：顶栏展示当前登录人（sessionStorage）。
 * 正式环境以服务端鉴权为准，参见 docs/superpowers/specs/2026-05-08-finops-rbac-data-permission-product-spec.md §7。
 */
(function () {
    'use strict';

    var STORAGE_KEY = 'finops_demo_session_v1';

    var DEFAULT_SESSION = {
        displayName: '演示用户（系统管理员）',
        loginId: 'admin.demo',
        tenantName: '演示租户 A',
        roles: ['系统管理员'],
        department: '信息技术部'
    };

    var PRESETS = {
        tenant_admin: {
            displayName: '演示用户（系统管理员）',
            loginId: 'admin.demo',
            tenantName: '演示租户 A',
            roles: ['系统管理员'],
            department: '信息技术部'
        },
        ops_admin: {
            displayName: '演示用户（私有云运营管理员）',
            loginId: 'ops.demo',
            tenantName: '演示租户 A',
            roles: ['私有云运营管理员'],
            department: '云运营中心'
        },
        dept_head: {
            displayName: '演示用户（部门负责人）',
            loginId: 'dept.demo',
            tenantName: '演示租户 A',
            roles: ['部门负责人'],
            department: '研发中心 / 平台组'
        },
        biz_user: {
            displayName: '演示用户（业务用户）',
            loginId: 'user.demo',
            tenantName: '演示租户 A',
            roles: ['业务用户'],
            department: '研发中心'
        }
    };

    function escapeHtml(str) {
        if (str == null || str === '') return '';
        var d = document.createElement('div');
        d.textContent = String(str);
        return d.innerHTML;
    }

    function loadSession() {
        try {
            var raw = sessionStorage.getItem(STORAGE_KEY);
            if (raw) {
                var o = JSON.parse(raw);
                if (o && typeof o === 'object') return o;
            }
        } catch (e) {}
        sessionStorage.setItem(STORAGE_KEY, JSON.stringify(DEFAULT_SESSION));
        return DEFAULT_SESSION;
    }

    function saveSession(s) {
        try {
            sessionStorage.setItem(STORAGE_KEY, JSON.stringify(s));
        } catch (e) {}
    }

    function ensureBrandBlock(hc) {
        if (hc.querySelector('.header-brand')) return;
        var h1 = hc.querySelector('h1');
        if (!h1) return;
        var brand = document.createElement('div');
        brand.className = 'header-brand';
        brand.style.cssText =
            'display:flex;flex-direction:column;gap:2px;align-items:flex-start;min-width:0;flex:1;';
        var sub = hc.querySelector('.header-sub');
        hc.insertBefore(brand, h1);
        brand.appendChild(h1);
        if (sub) brand.appendChild(sub);
    }

    function mount() {
        var hc = document.querySelector('.header-content');
        if (!hc) return;
        ensureBrandBlock(hc);
        var mountEl = document.getElementById('finopsHeaderUserRoot');
        if (!mountEl) {
            mountEl = document.createElement('div');
            mountEl.id = 'finopsHeaderUserRoot';
            mountEl.className = 'finops-header-user-root';
            mountEl.style.cssText =
                'margin-left:auto;display:flex;align-items:center;gap:12px;flex-wrap:wrap;justify-content:flex-end;';
            hc.appendChild(mountEl);
        }
        var s = loadSession();
        var roles = Array.isArray(s.roles) ? s.roles.join('、') : s.roles || '—';
        var dept = s.department ? ' · ' + escapeHtml(s.department) : '';
        mountEl.innerHTML =
            '<div class="finops-header-user-text" style="text-align:right;line-height:1.35;opacity:.95;font-size:13px;color:inherit;">' +
            '<div><strong style="font-weight:600">' +
            escapeHtml(s.displayName || '—') +
            '</strong> <span style="opacity:.85;font-weight:400;">（' +
            escapeHtml(s.loginId || '') +
            '）</span></div>' +
            '<div style="font-size:12px;opacity:.88">' +
            escapeHtml(s.tenantName || '—') +
            ' · ' +
            escapeHtml(roles) +
            dept +
            '</div></div>';
    }

    function applyPreset(key) {
        var p = PRESETS[key];
        if (!p) return;
        saveSession(p);
        mount();
    }

    function init() {
        loadSession();
        mount();
    }

    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    window.FinOpsSession = {
        STORAGE_KEY: STORAGE_KEY,
        loadSession: loadSession,
        saveSession: saveSession,
        applyPreset: applyPreset,
        remountHeader: mount,
        PRESETS: PRESETS
    };
})();
