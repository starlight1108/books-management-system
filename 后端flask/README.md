# 图书管理系统 - Flask后端

这是一个基于Flask的图书管理系统后端API，提供图书管理、会员管理、借阅管理和统计功能。

## 项目结构

```
后端flask/
├── app/                    # 应用主目录
│   ├── __init__.py        # 应用工厂函数
│   ├── extensions.py      # 扩展初始化
│   ├── models/            # 数据模型
│   │   ├── __init__.py
│   │   ├── book.py        # 图书模型
│   │   ├── member.py      # 会员模型
│   │   └── borrow.py      # 借阅模型
│   └── routes/            # 路由模块
│       ├── __init__.py
│       ├── books.py       # 图书管理API
│       ├── members.py     # 会员管理API
│       ├── borrows.py     # 借阅管理API
│       └── statistics.py  # 统计API
├── config.py              # 配置文件
├── run.py                 # 应用入口
└── requirements.txt       # 依赖列表
```

## 功能特性

### 图书管理
- 图书CRUD操作
- 图书搜索和分类过滤
- 库存管理
- ISBN唯一性验证

### 会员管理
- 会员CRUD操作
- 会员状态管理
- 借阅限制设置
- 邮箱唯一性验证

### 借阅管理
- 图书借阅和归还
- 逾期管理
- 借阅记录查询
- 库存自动更新

### 统计功能
- 基础统计（图书总数、会员总数等）
- 借阅趋势分析
- 热门图书统计
- 活跃会员统计

## 安装和运行

### 1. 安装依赖
```bash
pip install -r requirements.txt
```

### 2. 运行应用
```bash
python run.py
```

应用将在 http://localhost:5000 启动

### 3. API测试
使用浏览器或Postman访问以下端点：
- 图书列表：GET http://localhost:5000/api/books
- 会员列表：GET http://localhost:5000/api/members
- 借阅记录：GET http://localhost:5000/api/borrows
- 统计数据：GET http://localhost:5000/api/statistics

## API文档

### 图书管理
- `GET /api/books` - 获取图书列表
- `POST /api/books` - 添加图书
- `GET /api/books/{id}` - 获取图书详情
- `PUT /api/books/{id}` - 更新图书
- `DELETE /api/books/{id}` - 删除图书

### 会员管理
- `GET /api/members` - 获取会员列表
- `POST /api/members` - 添加会员
- `GET /api/members/{id}` - 获取会员详情
- `PUT /api/members/{id}` - 更新会员
- `DELETE /api/members/{id}` - 删除会员

### 借阅管理
- `GET /api/borrows` - 获取借阅记录
- `POST /api/borrows` - 借阅图书
- `PUT /api/borrows/{id}/return` - 归还图书
- `PUT /api/borrows/{id}` - 更新借阅记录
- `DELETE /api/borrows/{id}` - 删除借阅记录

### 统计功能
- `GET /api/statistics` - 获取统计数据
- `GET /api/statistics/overview` - 获取概览数据

## 数据库

使用SQLite数据库，数据库文件将自动创建在项目根目录下的 `library.db`。

## 开发说明

- 使用Flask应用工厂模式
- 使用SQLAlchemy ORM进行数据库操作
- 支持CORS跨域请求
- 包含错误处理和输入验证
- 使用蓝图组织路由模块

## 注意事项

- 生产环境需要设置 `SECRET_KEY` 环境变量
- 建议在生产环境使用PostgreSQL或MySQL数据库
- 需要配置合适的CORS设置以匹配前端地址