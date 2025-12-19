# 图书管理系统

这是一个基于Vue.js前端和Flask后端的图书管理系统，提供完整的图书管理功能，包括图书的增删改查、借阅管理、用户管理等。

## 功能特点

- 📚 图书管理：添加、编辑、删除、搜索图书
- 👥 用户管理：管理员和普通用户角色
- 📖 借阅管理：借书、还书、续借功能
- 📊 统计分析：借阅统计、热门图书等
- 🌐 响应式设计：适配不同设备屏幕

## 技术栈

### 前端
- Vue.js 3
- Element Plus UI组件库
- Axios HTTP客户端
- Vue Router 路由管理
- Pinia 状态管理

### 后端
- Flask Web框架
- SQLAlchemy ORM
- MySQL数据库
- JWT认证
- Flask-CORS跨域支持

## 快速开始

### 环境要求
- Node.js 16+
- Python 3.8+
- MySQL 5.7+

### 安装步骤

1. 克隆项目
```bash
git clone https://github.com/yourusername/library-management.git
cd library-management
```

2. 后端设置
```bash
cd 后端flask
pip install -r requirements.txt
```

3. 配置数据库
- 在MySQL中创建名为`library`的数据库
- 修改`后端flask/app.py`中的数据库连接信息

4. 初始化数据库
```bash
python run.py
```

5. 前端设置
```bash
cd ../前端vue
npm install
```

6. 启动应用

后端服务：
```bash
cd ../后端flask
python run.py
```

前端服务：
```bash
cd ../前端vue
npm run dev
```

7. 访问应用
打开浏览器访问 http://localhost:5173

## 默认账户

- 管理员：admin / admin123
- 普通用户：user / user123

## 项目结构

```
图书管理/pbl5/
├── 前端vue/          # Vue.js前端应用
│   ├── src/         # 源代码
│   ├── public/      # 静态资源
│   └── package.json # 依赖配置
├── 后端flask/         # Flask后端应用
│   ├── app.py       # 主应用文件
│   ├── models.py    # 数据模型
│   ├── routes.py    # API路由
│   └── run.py       # 启动脚本
└── README.md        # 项目说明文档
```

## 开发指南

### 添加新功能

1. 后端API开发
- 在`后端flask/routes.py`中添加新的路由
- 在`后端flask/models.py`中定义数据模型
- 确保API遵循RESTful规范

2. 前端页面开发
- 在`前端vue/src/views`中添加新页面
- 在`前端vue/src/components`中添加组件
- 在`前端vue/src/router/index.js`中添加路由

## 许可证

MIT License