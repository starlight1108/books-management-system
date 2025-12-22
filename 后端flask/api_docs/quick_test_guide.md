# 快速测试指南

## 1. 环境准备

### 1.1 启动服务
```bash
# 进入项目目录
cd c:\Users\starlight\Documents\项目\pbl5\后端flask

# 安装依赖
pip install -r requirements.txt

# 启动服务
python run.py
```

### 1.2 服务信息
- 服务地址：`http://localhost:5000`
- 默认端口：5000

## 2. 快速测试流程

### 2.1 测试账号

| 角色 | 用户名 | 密码 | 权限 |
|------|--------|------|------|
| 管理员 | starlight | 88888888 | 所有权限 |
| 普通用户 | 李四 | 123456 | 个人权限 |

### 2.2 基础测试步骤

#### 步骤1：获取Token
```bash
# 管理员登录
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"name": "starlight", "password": "88888888"}'

# 普通用户登录  
curl -X POST http://localhost:5000/auth/login \
  -H "Content-Type: application/json" \
  -d '{"name": "李四", "password": "123456"}'
```

#### 步骤2：测试认证接口
```bash
# 获取用户信息
curl -X GET http://localhost:5000/auth/profile \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 修改密码
curl -X POST http://localhost:5000/auth/change-password \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"old_password": "123456", "new_password": "654321"}'
```

#### 步骤3：测试图书管理
```bash
# 获取图书列表
curl -X GET "http://localhost:5000/books?page=1&per_page=5" \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 添加图书（需要管理员权限）
curl -X POST http://localhost:5000/books \
  -H "Authorization: Bearer ADMIN_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "测试图书",
    "author": "测试作者", 
    "isbn": "9781234567890",
    "category": "测试分类",
    "total_copies": 5
  }'
```

#### 步骤4：测试借阅功能
```bash
# 借阅图书
curl -X POST http://localhost:5000/borrows \
  -H "Authorization: Bearer YOUR_TOKEN_HERE" \
  -H "Content-Type: application/json" \
  -d '{"book_id": 1}'

# 查看借阅记录
curl -X GET http://localhost:5000/borrows \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"

# 归还图书
curl -X PUT http://localhost:5000/borrows/1/return \
  -H "Authorization: Bearer YOUR_TOKEN_HERE"
```

#### 步骤5：测试统计功能
```bash
# 获取系统统计
curl -X GET http://localhost:5000/statistics

# 获取概览统计
curl -X GET http://localhost:5000/statistics/overview
```

## 3. Postman测试集合

### 3.1 导入Postman集合
1. 打开Postman
2. 点击"Import"按钮
3. 选择"Raw text"
4. 粘贴以下JSON：

```json
{
  "info": {
    "name": "图书馆管理系统API测试",
    "description": "完整的API测试集合",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
  },
  "item": [
    {
      "name": "认证接口",
      "item": [
        {
          "name": "用户登录",
          "request": {
            "method": "POST",
            "header": [
              {
                "key": "Content-Type",
                "value": "application/json"
              }
            ],
            "body": {
              "mode": "raw",
              "raw": "{\n  \"name\": \"starlight\",\n  \"password\": \"88888888\"\n}"
            },
            "url": {
              "raw": "{{base_url}}/auth/login",
              "host": ["{{base_url}}"],
              "path": ["auth", "login"]
            }
          }
        },
        {
          "name": "获取用户信息",
          "request": {
            "method": "GET",
            "header": [
              {
                "key": "Authorization",
                "value": "Bearer {{token}}"
              }
            ],
            "url": {
              "raw": "{{base_url}}/auth/profile",
              "host": ["{{base_url}}"],
              "path": ["auth", "profile"]
            }
          }
        }
      ]
    }
  ],
  "variable": [
    {
      "key": "base_url",
      "value": "http://localhost:5000",
      "type": "string"
    },
    {
      "key": "token",
      "value": "",
      "type": "string"
    }
  ]
}
```

### 3.2 设置环境变量
在Postman中设置以下环境变量：
- `base_url`: `http://localhost:5000`
- `token`: 登录后获取的token

## 4. 常见测试场景

### 4.1 用户注册和登录
1. 测试用户注册功能
2. 测试登录功能
3. 验证Token有效性
4. 测试密码修改

### 4.2 图书管理测试
1. 测试图书列表查询（分页、搜索、分类）
2. 测试图书添加（管理员权限）
3. 测试图书信息更新
4. 测试图书删除（有借阅记录的图书不能删除）

### 4.3 借阅流程测试
1. 测试借阅图书
2. 测试归还图书
3. 测试借阅记录查询
4. 测试逾期处理

### 4.4 权限控制测试
1. 测试普通用户权限限制
2. 测试管理员权限
3. 测试跨用户数据访问限制

### 4.5 数据验证测试
1. 测试必填字段验证
2. 测试唯一性验证（用户名、邮箱、ISBN）
3. 测试数据格式验证
4. 测试边界值测试

## 5. 错误场景测试

### 5.1 认证相关错误
- 未提供Token
- Token过期
- Token格式错误

### 5.2 权限相关错误
- 普通用户尝试管理员操作
- 用户尝试访问他人数据

### 5.3 数据验证错误
- 必填字段为空
- 数据格式错误
- 唯一性冲突

### 5.4 业务逻辑错误
- 借阅已借出的图书
- 删除有借阅记录的图书
- 超过借阅限制

## 6. 性能测试建议

### 6.1 基础性能测试
- 并发用户登录测试
- 大数据量图书查询测试
- 高并发借阅操作测试

### 6.2 压力测试
- 模拟大量用户同时操作
- 测试数据库连接池性能
- 测试内存使用情况

## 7. 测试报告模板

### 7.1 测试结果记录
```
测试日期: ______________
测试人员: ______________
测试环境: ______________

接口测试结果:
- 认证接口: □ 通过 □ 失败
- 图书管理接口: □ 通过 □ 失败  
- 借阅管理接口: □ 通过 □ 失败
- 统计接口: □ 通过 □ 失败

发现的问题:
1. _________________________
2. _________________________
3. _________________________

建议:
1. _________________________
2. _________________________
3. _________________________
```

## 8. 联系方式

如有问题请联系开发团队。

---

*文档版本：v1.0*  
*最后更新：2024-12-18*