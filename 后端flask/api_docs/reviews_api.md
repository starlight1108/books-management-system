# 评论功能 API 文档

## 概述
评论功能允许普通用户对书籍进行评价，包括评分和评论内容，同时支持查看他人评价和删除自己的评价。

## API 端点

### 1. 获取书籍评论列表
**GET** `/api/books/<int:book_id>/reviews`

获取指定书籍的所有评论，包括平均评分和星级分布统计。

**参数：**
- `page` (可选): 页码，默认为1
- `per_page` (可选): 每页数量，默认为10

**响应示例：**
```json
{
    "book": {
        "id": 1,
        "title": "示例书籍",
        "author": "作者名",
        "...": "其他书籍信息"
    },
    "reviews": [
        {
            "id": 1,
            "book_id": 1,
            "member_id": 1,
            "member_name": "用户名",
            "rating": 5,
            "content": "很好的书籍！",
            "created_at": "2024-01-01T10:00:00",
            "updated_at": "2024-01-01T10:00:00"
        }
    ],
    "total": 15,
    "pages": 2,
    "current_page": 1,
    "average_rating": 4.3,
    "rating_counts": {
        "1": 1,
        "2": 2,
        "3": 3,
        "4": 4,
        "5": 5
    }
}
```

### 2. 添加评论
**POST** `/api/books/<int:book_id>/reviews`

为指定书籍添加评论。需要用户登录。

**请求头：**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**请求体：**
```json
{
    "rating": 5,
    "content": "这本书非常棒！"
}
```

**响应示例：**
```json
{
    "id": 1,
    "book_id": 1,
    "member_id": 1,
    "member_name": "用户名",
    "rating": 5,
    "content": "这本书非常棒！",
    "created_at": "2024-01-01T10:00:00",
    "updated_at": "2024-01-01T10:00:00"
}
```

### 3. 修改评论
**PUT** `/api/reviews/<int:review_id>`

修改指定评论。只能修改自己的评论，管理员可以修改任何评论。

**请求头：**
```
Authorization: Bearer <jwt_token>
Content-Type: application/json
```

**请求体：**
```json
{
    "rating": 4,
    "content": "修改后的评论内容"
}
```

### 4. 删除评论
**DELETE** `/api/reviews/<int:review_id>`

删除指定评论。只能删除自己的评论，管理员可以删除任何评论。

**请求头：**
```
Authorization: Bearer <jwt_token>
```

**响应示例：**
```json
{
    "message": "评论删除成功"
}
```

### 5. 获取会员评论列表
**GET** `/api/members/<int:member_id>/reviews`

获取指定会员的所有评论。需要登录且只能查看自己的评论或管理员权限。

**请求头：**
```
Authorization: Bearer <jwt_token>
```

**参数：**
- `page` (可选): 页码，默认为1
- `per_page` (可选): 每页数量，默认为10

### 6. 获取当前用户评论列表
**GET** `/api/reviews/my-reviews`

获取当前登录用户的所有评论。

**请求头：**
```
Authorization: Bearer <jwt_token>
```

**参数：**
- `page` (可选): 页码，默认为1
- `per_page` (可选): 每页数量，默认为10

## 错误码说明

- `400`: 请求参数错误（如评分不在1-5之间，评论内容为空等）
- `401`: 未授权访问（需要登录）
- `403`: 权限不足（如修改/删除他人评论）
- `404`: 资源不存在（书籍或评论不存在）
- `500`: 服务器内部错误

## 使用示例

### 前端实现建议

1. **书籍详情页**：显示书籍信息和评论列表
2. **评论组件**：包含评分选择（1-5星）和评论输入框
3. **评论列表**：显示所有评论，支持分页
4. **我的评论**：用户个人中心显示自己的评论，支持编辑和删除

### JavaScript 示例代码

```javascript
// 获取书籍评论
async function getBookReviews(bookId) {
    const response = await fetch(`/api/books/${bookId}/reviews`);
    return await response.json();
}

// 添加评论
async function addReview(bookId, rating, content, token) {
    const response = await fetch(`/api/books/${bookId}/reviews`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ rating, content })
    });
    return await response.json();
}

// 删除评论
async function deleteReview(reviewId, token) {
    const response = await fetch(`/api/reviews/${reviewId}`, {
        method: 'DELETE',
        headers: {
            'Authorization': `Bearer ${token}`
        }
    });
    return await response.json();
}
```

## 数据库表结构

```sql
CREATE TABLE reviews (
    id INTEGER PRIMARY KEY,
    book_id INTEGER NOT NULL,
    member_id INTEGER NOT NULL,
    rating INTEGER NOT NULL,
    content TEXT NOT NULL,
    created_at DATETIME,
    updated_at DATETIME,
    FOREIGN KEY (book_id) REFERENCES books (id),
    FOREIGN KEY (member_id) REFERENCES members (id)
);
```