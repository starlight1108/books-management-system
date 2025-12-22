# 图书馆管理系统 - 完整API文档

## 1. 系统概述

本系统是一个完整的图书馆管理系统，提供图书管理、会员管理、借阅管理、统计分析等功能。

### 1.1 技术栈
- 后端：Flask + SQLAlchemy
- 认证：JWT Token
- 数据库：SQLite

### 1.2 基础信息
- 基础URL：`http://localhost:5000`
- 认证方式：Bearer Token
- 数据格式：JSON

## 2. 认证接口

### 2.1 用户注册
```
POST /auth/register
```

**请求参数：**
```json
{
  "name": "用户名",
  "password": "密码（至少6位数字）",
  "phone": "手机号（可选）"
}
```

**响应示例：**
```json
{
  "message": "注册成功",
  "access_token": "jwt_token",
  "user": {
    "id": 1,
    "name": "用户名",
    "role": "user"
  }
}
```

### 2.2 用户登录
```
POST /auth/login
```

**请求参数：**
```json
{
  "name": "用户名",
  "password": "密码"
}
```

**响应示例：**
```json
{
  "message": "登录成功",
  "access_token": "jwt_token",
  "user": {
    "id": 1,
    "name": "用户名",
    "role": "user"
  }
}
```

### 2.3 获取用户信息
```
GET /auth/profile
```

**认证要求：** JWT Token

**响应示例：**
```json
{
  "user": {
    "id": 1,
    "name": "用户名",
    "phone": "手机号",
    "join_date": "2024-01-01T00:00:00",
    "status": "active",
    "role": "user",
    "max_borrow_limit": 5
  }
}
```

### 2.4 修改密码
```
POST /auth/change-password
```

**认证要求：** JWT Token

**请求参数：**
```json
{
  "old_password": "旧密码",
  "new_password": "新密码（至少6位数字）"
}
```

## 3. 图书管理接口

### 3.1 获取图书列表
```
GET /books
```

**查询参数：**
- `page`：页码（默认1）
- `per_page`：每页数量（默认10）
- `search`：搜索关键词（书名、作者、ISBN）
- `category`：分类筛选

**响应示例：**
```json
{
  "books": [
    {
      "id": 1,
      "title": "图书标题",
      "author": "作者",
      "isbn": "ISBN号",
      "publisher": "出版社",
      "publish_date": "2023-01-01",
      "category": "分类",
      "total_copies": 10,
      "available_copies": 8,
      "location": "位置",
      "description": "描述"
    }
  ],
  "total": 100,
  "pages": 10,
  "current_page": 1
}
```

### 3.2 获取单个图书信息
```
GET /books/{book_id}
```

### 3.3 添加图书
```
POST /books
```

**认证要求：** 管理员权限

**请求参数：**
```json
{
  "title": "图书标题（必填）",
  "author": "作者（必填）",
  "isbn": "ISBN号（必填）",
  "publisher": "出版社",
  "publish_date": "2023-01-01",
  "category": "分类",
  "total_copies": 10,
  "location": "位置",
  "description": "描述"
}
```

### 3.4 更新图书信息
```
PUT /books/{book_id}
```

**认证要求：** 管理员权限

### 3.5 删除图书
```
DELETE /books/{book_id}
```

**认证要求：** 管理员权限

### 3.6 获取图书分类
```
GET /books/categories
```

## 4. 会员管理接口

### 4.1 获取会员列表
```
GET /members
```

**认证要求：** 管理员权限

**查询参数：**
- `page`：页码（默认1）
- `per_page`：每页数量（默认10）
- `search`：搜索关键词（姓名、邮箱、手机号）
- `status`：状态筛选

### 4.2 获取单个会员信息
```
GET /members/{member_id}
```

**认证要求：** 本人或管理员权限

### 4.3 添加会员
```
POST /members
```

**认证要求：** 管理员权限

**请求参数：**
```json
{
  "name": "姓名（必填）",
  "email": "邮箱（必填）",
  "password": "密码（必填）",
  "phone": "手机号",
  "address": "地址",
  "join_date": "2024-01-01",
  "status": "active",
  "max_borrow_limit": 5
}
```

### 4.4 更新会员信息
```
PUT /members/{member_id}
```

**认证要求：** 本人或管理员权限

### 4.5 删除会员
```
DELETE /members/{member_id}
```

**认证要求：** 管理员权限

### 4.6 获取会员借阅记录
```
GET /members/{member_id}/borrows
```

**认证要求：** 本人或管理员权限

## 5. 借阅管理接口

### 5.1 获取借阅记录列表
```
GET /borrows
```

**认证要求：** JWT Token

**查询参数：**
- `page`：页码（默认1）
- `per_page`：每页数量（默认10）
- `status`：状态筛选
- `overdue_only`：是否只显示逾期记录

### 5.2 借阅图书
```
POST /borrows
```

**认证要求：** JWT Token

**请求参数：**
```json
{
  "book_id": "图书ID（必填）",
  "member_id": "会员ID（管理员可选）",
  "borrow_days": "借阅天数（默认30）"
}
```

### 5.3 归还图书
```
PUT /borrows/{borrow_id}/return
```

**认证要求：** 借阅者本人或管理员权限

### 5.4 更新借阅记录
```
PUT /borrows/{borrow_id}
```

**认证要求：** 管理员权限

### 5.5 删除借阅记录
```
DELETE /borrows/{borrow_id}
```

**认证要求：** 管理员权限

## 6. 统计接口

### 6.1 获取系统统计
```
GET /statistics
```

**响应示例：**
```json
{
  "total_books": 1000,
  "total_members": 500,
  "borrowed_books": 150,
  "available_books": 850,
  "overdue_books": 10,
  "today_borrows": 5,
  "today_returns": 3,
  "category_stats": {
    "文学": 300,
    "科技": 200,
    "历史": 150
  },
  "borrow_trend": {
    "2024-01-01": 10,
    "2024-01-02": 15
  },
  "popular_books": [
    {"title": "热门图书1", "borrow_count": 50},
    {"title": "热门图书2", "borrow_count": 45}
  ],
  "active_members": [
    {"name": "活跃会员1", "borrow_count": 20},
    {"name": "活跃会员2", "borrow_count": 18}
  ]
}
```

### 6.2 获取概览统计
```
GET /statistics/overview
```

## 7. 错误码说明

| 状态码 | 说明 | 常见场景 |
|-------|------|----------|
| 200 | 成功 | 请求成功 |
| 201 | 创建成功 | 新增数据成功 |
| 400 | 请求错误 | 参数错误、数据验证失败 |
| 401 | 未授权 | Token无效或过期 |
| 403 | 禁止访问 | 权限不足 |
| 404 | 资源不存在 | 数据不存在 |
| 500 | 服务器错误 | 服务器内部错误 |

## 8. 测试账号

### 8.1 管理员账号
- 用户名：starlight
- 密码：88888888
- 角色：admin

### 8.2 普通用户账号
- 用户名：李四
- 密码：123456
- 角色：user

## 9. 测试示例

### 9.1 完整借阅流程测试

```javascript
// 1. 用户登录
const loginResponse = await fetch('/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: '李四',
    password: '123456'
  })
});

const loginData = await loginResponse.json();
const token = loginData.access_token;

// 2. 获取图书列表
const booksResponse = await fetch('/books?per_page=5', {
  headers: { 'Authorization': `Bearer ${token}` }
});
const booksData = await booksResponse.json();

// 3. 借阅图书
const borrowResponse = await fetch('/borrows', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    book_id: booksData.books[0].id
  })
});

// 4. 查看借阅记录
const borrowsResponse = await fetch('/borrows', {
  headers: { 'Authorization': `Bearer ${token}` }
});
```

### 9.2 管理员操作测试

```javascript
// 1. 管理员登录
const adminLoginResponse = await fetch('/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    name: 'starlight',
    password: '88888888'
  })
});

const adminLoginData = await adminLoginResponse.json();
const adminToken = adminLoginData.access_token;

// 2. 添加新图书
const addBookResponse = await fetch('/books', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${adminToken}`
  },
  body: JSON.stringify({
    title: '测试图书',
    author: '测试作者',
    isbn: '9781234567890',
    category: '测试分类',
    total_copies: 5
  })
});

// 3. 查看系统统计
const statsResponse = await fetch('/statistics', {
  headers: { 'Authorization': `Bearer ${adminToken}` }
});
```

## 10. 注意事项

1. **认证头格式**：所有需要认证的接口都需要在请求头中添加 `Authorization: Bearer {token}`
2. **数据格式**：所有请求和响应都使用JSON格式
3. **日期格式**：日期字段使用ISO格式（YYYY-MM-DD或YYYY-MM-DDTHH:mm:ss）
4. **分页参数**：列表接口都支持分页，默认每页10条
5. **权限控制**：注意不同角色的权限差异，普通用户只能操作自己的数据
6. **错误处理**：所有接口都有统一的错误响应格式

## 11. 接口测试工具推荐

- **Postman**：推荐使用Postman进行API测试
- **curl**：命令行工具测试
- **浏览器开发者工具**：前端调试时使用
- **Swagger UI**：可考虑集成Swagger生成可视化文档

---

*文档版本：v1.0*  
*最后更新：2024-12-18*