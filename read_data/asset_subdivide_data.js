const subdivideData = [
  {
    "id": 1,
    "name": "NPU服务器-300I",
    "calculateCost": true
  },
  {
    "id": 2,
    "name": "NPU服务器-910B",
    "calculateCost": true
  },
  {
    "id": 3,
    "name": "块存储-SAN",
    "calculateCost": true
  },
  {
    "id": 4,
    "name": "块存储-SAN(DellNetWorker)",
    "calculateCost": true
  },
  {
    "id": 5,
    "name": "块存储-SAN(NBU)",
    "calculateCost": true
  },
  {
    "id": 6,
    "name": "块存储-SAN(A300)",
    "calculateCost": true
  },
  {
    "id": 7,
    "name": "块存储-SAN(NetApp8020)",
    "calculateCost": true
  },
  {
    "id": 8,
    "name": "块存储-SAN(NetApp2552)",
    "calculateCost": true
  },
  {
    "id": 9,
    "name": "GPU服务器-RTX4000",
    "calculateCost": true
  },
  {
    "id": 10,
    "name": "GPU服务器-RTX2060",
    "calculateCost": true
  },
  {
    "id": 11,
    "name": "网络准入(公用)",
    "calculateCost": true
  },
  {
    "id": 12,
    "name": "数据安全(公用)",
    "calculateCost": true
  },
  {
    "id": 13,
    "name": "产品安全(公用)",
    "calculateCost": true
  },
  {
    "id": 14,
    "name": "GPU服务器-P4000",
    "calculateCost": true
  },
  {
    "id": 15,
    "name": "GPU服务器-P6000",
    "calculateCost": true
  },
  {
    "id": 16,
    "name": "GPU服务器-T4",
    "calculateCost": true
  },
  {
    "id": 17,
    "name": "GPU服务器-A5000",
    "calculateCost": true
  },
  {
    "id": 18,
    "name": "GPU服务器-RTX8000",
    "calculateCost": true
  },
  {
    "id": 19,
    "name": "GPU服务器-RTX6000",
    "calculateCost": true
  },
  {
    "id": 20,
    "name": "GPU服务器-RTX3080",
    "calculateCost": true
  },
  {
    "id": 21,
    "name": "GPU服务器-RTX2080TI",
    "calculateCost": true
  },
  {
    "id": 22,
    "name": "动力系统",
    "calculateCost": true
  },
  {
    "id": 23,
    "name": "容器管理软件",
    "calculateCost": true
  },
  {
    "id": 24,
    "name": "PC机/未查到",
    "calculateCost": true
  },
  {
    "id": 25,
    "name": "GPU服务器-P2200",
    "calculateCost": true
  },
  {
    "id": 26,
    "name": "无线控制器",
    "calculateCost": true
  },
  {
    "id": 27,
    "name": "负载均衡(办公网)",
    "calculateCost": true
  },
  {
    "id": 28,
    "name": "网络防火墙(办公网)",
    "calculateCost": true
  },
  {
    "id": 29,
    "name": "路由器(办公网)",
    "calculateCost": true
  },
  {
    "id": 30,
    "name": "交换机(办公网)",
    "calculateCost": true
  },
  {
    "id": 31,
    "name": "无线AP",
    "calculateCost": true
  },
  {
    "id": 32,
    "name": "上网行为管理(办公网)",
    "calculateCost": true
  },
  {
    "id": 33,
    "name": "漏洞扫描(数据中心)",
    "calculateCost": true
  },
  {
    "id": 34,
    "name": "流量探针(数据中心)",
    "calculateCost": true
  },
  {
    "id": 35,
    "name": "产品安全(数据中心)",
    "calculateCost": true
  },
  {
    "id": 36,
    "name": "数据安全(数据中心)",
    "calculateCost": true
  },
  {
    "id": 37,
    "name": "堡垒机(数据中心)",
    "calculateCost": true
  },
  {
    "id": 38,
    "name": "安全防火墙(数据中心)",
    "calculateCost": true
  },
  {
    "id": 39,
    "name": "负载均衡(数据中心)",
    "calculateCost": true
  },
  {
    "id": 40,
    "name": "上网行为管理(数据中心)",
    "calculateCost": true
  },
  {
    "id": 41,
    "name": "路由器(数据中心)",
    "calculateCost": true
  },
  {
    "id": 42,
    "name": "交换机(数据中心)",
    "calculateCost": true
  },
  {
    "id": 43,
    "name": "网络防火墙(数据中心)",
    "calculateCost": true
  },
  {
    "id": 44,
    "name": "块存储-SAN(威联通服务器)",
    "calculateCost": true
  },
  {
    "id": 45,
    "name": "GPU服务器-H800",
    "calculateCost": true
  },
  {
    "id": 46,
    "name": "GPU服务器-H100",
    "calculateCost": true
  },
  {
    "id": 47,
    "name": "GPU服务器-A800",
    "calculateCost": true
  },
  {
    "id": 48,
    "name": "GPU服务器-A40",
    "calculateCost": true
  },
  {
    "id": 49,
    "name": "GPU服务器-A10",
    "calculateCost": true
  },
  {
    "id": 50,
    "name": "GPU服务器-RTX4090",
    "calculateCost": true
  },
  {
    "id": 51,
    "name": "GPU服务器-RTX3090",
    "calculateCost": true
  },
  {
    "id": 52,
    "name": "大数据类超大存储",
    "calculateCost": true
  },
  {
    "id": 53,
    "name": "大数据类存储-高速IO",
    "calculateCost": true
  },
  {
    "id": 54,
    "name": "大数据类存储-机械大盘",
    "calculateCost": true
  },
  {
    "id": 55,
    "name": "大数据类存储-机械多盘",
    "calculateCost": true
  },
  {
    "id": 56,
    "name": "国产化服务器",
    "calculateCost": true
  },
  {
    "id": 57,
    "name": "小型单机应用",
    "calculateCost": true
  },
  {
    "id": 58,
    "name": "高速编译型应用",
    "calculateCost": true
  },
  {
    "id": 59,
    "name": "高性能容器应用",
    "calculateCost": true
  },
  {
    "id": 60,
    "name": "标准通用服务器-虚拟化类应用",
    "calculateCost": true
  },
  {
    "id": 61,
    "name": "标准通用服务器-容器应用",
    "calculateCost": true
  }
];