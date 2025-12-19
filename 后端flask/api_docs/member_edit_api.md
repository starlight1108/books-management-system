# 会员管理编辑功能API文档

## 1. 功能概述
后端提供完整的会员管理编辑API，支持管理员和普通用户对会员信息进行编辑操作，包含权限控制和数据验证。

## 2. 核心API列表

### 2.1 获取单个会员信息
```
GET /api/members/{member_id}
```

**权限要求**：
- 普通用户：只能获取自己的信息
- 管理员：可以获取所有用户的信息

**请求参数**：
- Path参数：`member_id` - 会员ID

**响应示例**：
```json
{
  "address": "北京市海淀区",
  "created_at": "2025-12-14T14:43:36",
  "current_borrows": 1,
  "email": "lisi@example.com",
  "id": 2,
  "join_date": "2024-02-20",
  "max_borrow_limit": 5,
  "name": "李四",
  "phone": "13888888888",
  "role": "user",
  "status": "inactive",
  "updated_at": "2025-12-18T03:05:47.560784"
}
```

### 2.2 更新会员信息
```
PUT /api/members/{member_id}
```

**权限要求**：
- 普通用户：只能更新自己的信息（仅能修改：name, phone, address, email, join_date）
- 管理员：可以更新所有用户的信息（可修改所有字段）

**请求参数**：
- Path参数：`member_id` - 会员ID
- Body参数：JSON格式的会员信息（部分或全部字段）

**支持的字段**：

| 字段名 | 类型 | 说明 | 普通用户可修改 | 管理员可修改 |
|-------|------|------|--------------|------------|
| name | string | 用户名（唯一） | ✅ | ✅ |
| email | string | 邮箱（唯一，可选） | ✅ | ✅ |
| phone | string | 手机号 | ✅ | ✅ |
| address | string | 地址 | ✅ | ✅ |
| join_date | string | 入会日期（YYYY-MM-DD格式） | ✅ | ✅ |
| status | string | 状态（active/inactive） | ❌ | ✅ |
| max_borrow_limit | integer | 最大借阅限制 | ❌ | ✅ |

**请求示例**：
```json
{
  "name": "李四（更新）",
  "phone": "13888888888",
  "address": "北京市海淀区",
  "status": "active",
  "max_borrow_limit": 10
}
```

**响应示例**：
```json
{
  "address": "北京市海淀区",
  "created_at": "2025-12-14T14:43:36",
  "email": "lisi@example.com",
  "id": 2,
  "join_date": "2024-02-20",
  "max_borrow_limit": 10,
  "name": "李四（更新）",
  "phone": "13888888888",
  "role": "user",
  "status": "active",
  "updated_at": "2025-12-18T03:05:47.560784"
}
```

## 3. 数据验证规则

### 3.1 必填字段
- 用户名（name）：创建和更新时都不能为空

### 3.2 唯一性验证
- 用户名（name）：系统中必须唯一
- 邮箱（email）：系统中必须唯一（如果提供）

### 3.3 格式验证
- 入会日期（join_date）：必须是YYYY-MM-DD格式

### 3.4 其他验证
- 会员状态（status）：只能是"active"或"inactive"
- 最大借阅限制（max_borrow_limit）：必须是正整数

## 4. 错误处理

### 4.1 常见错误码

| 状态码 | 错误信息 | 说明 |
|-------|---------|------|
| 400 | 用户名已存在 | 尝试使用已存在的用户名 |
| 400 | 邮箱已存在 | 尝试使用已存在的邮箱 |
| 400 | 入会日期格式错误，应为YYYY-MM-DD | 日期格式不正确 |
| 401 | Missing Authorization Header | 缺少认证token |
| 403 | Insufficient permissions | 权限不足 |
| 404 | 404 Not Found | 会员不存在 |
| 500 | Internal Server Error | 服务器内部错误 |

### 4.2 错误响应示例
```json
{
  "error": "用户名已存在"
}
```

## 5. 权限控制说明

- **普通用户**：
  - 只能查看和编辑自己的信息
  - 不能修改会员状态和借阅限制

- **管理员**：
  - 可以查看和编辑所有用户的信息
  - 可以修改所有字段，包括状态和借阅限制
  - 可以管理所有用户的借阅权限

## 6. 前端开发建议

### 6.1 编辑表单设计
1. 根据用户角色动态显示可编辑字段
2. 对必填字段添加前端验证
3. 实现用户名和邮箱的唯一性检查（可通过API预检查）
4. 日期字段使用日期选择器组件
5. 状态字段使用下拉选择器（仅管理员可见）
6. 借阅限制使用数字输入框（仅管理员可见）

### 6.2 API调用流程
1. 编辑前先获取用户当前信息（GET /api/members/{member_id}）
2. 填充表单后提交更新（PUT /api/members/{member_id}）
3. 处理可能的错误响应，显示友好的错误提示
4. 更新成功后刷新页面或用户信息

### 6.3 权限控制实现
1. 在前端存储用户角色信息
2. 根据角色决定显示哪些字段和操作按钮
3. 所有API请求都需要携带有效的JWT token

## 7. 测试账号

- **管理员账号**：
  - 用户名：starlight
  - 密码：88888888

- **普通用户账号**：
  - 用户名：李四
  - 密码：123456

## 8. 完整测试示例

### 8.1 管理员编辑用户流程
```javascript
// 1. 管理员登录
const loginResponse = await fetch('/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ name: 'starlight', password: '88888888' })
});

const loginData = await loginResponse.json();
const token = loginData.access_token;

// 2. 获取用户信息
const userResponse = await fetch('/api/members/2', {
  headers: { 'Authorization': `Bearer ${token}` }
});

const userData = await userResponse.json();

// 3. 更新用户信息
const updateResponse = await fetch('/api/members/2', {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    name: `${userData.name}（管理员编辑）`,
    status: userData.status === 'active' ? 'inactive' : 'active',
    max_borrow_limit: userData.max_borrow_limit === 5 ? 10 : 5
  })
});

const updateData = await updateResponse.json();
console.log('更新成功:', updateData);
```

### 8.2 普通用户编辑自己流程
```javascript
// 1. 普通用户登录
const loginResponse = await fetch('/api/auth/login', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ name: '李四', password: '123456' })
});

const loginData = await loginResponse.json();
const token = loginData.access_token;

// 2. 获取自己的信息
const profileResponse = await fetch('/api/auth/profile', {
  headers: { 'Authorization': `Bearer ${token}` }
});

const profileData = await profileResponse.json();

// 3. 更新个人信息
const updateResponse = await fetch(`/api/members/${profileData.id}`, {
  method: 'PUT',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${token}`
  },
  body: JSON.stringify({
    phone: '13888888888',
    address: '北京市海淀区'
  })
});

const updateData = await updateResponse.json();
console.log('更新成功:', updateData);
```

## 9. 注意事项

1. 所有API请求都需要在请求头中包含有效的JWT token
2. 用户名和邮箱的唯一性验证由后端负责，前端可做预检查优化体验
3. 普通用户无法修改自己的角色和权限
4. 入会日期如果不提供，将保持原有值
5. 更新成功后，API会返回完整的更新后的用户信息

## 10. 技术支持

如有任何问题或需要进一步的API支持，请联系后端开发人员。