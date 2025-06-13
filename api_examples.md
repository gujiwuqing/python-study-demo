# API使用示例文档

本文档提供了FastAPI后端管理系统的完整API使用示例，包括请求格式、响应格式、认证方式等。

## 📋 目录

- [API使用示例文档](#api使用示例文档)
  - [📋 目录](#-目录)
  - [🔐 认证说明](#-认证说明)
    - [JWT Token认证](#jwt-token认证)
    - [权限级别](#权限级别)
  - [📊 统一响应格式](#-统一响应格式)
    - [成功响应](#成功响应)
    - [错误响应](#错误响应)
    - [分页响应](#分页响应)
  - [👤 用户管理API](#-用户管理api)
    - [用户注册](#用户注册)
    - [用户登录](#用户登录)
    - [获取当前用户信息](#获取当前用户信息)
    - [更新当前用户信息](#更新当前用户信息)
    - [修改密码](#修改密码)
    - [分页获取用户列表](#分页获取用户列表)
    - [创建用户](#创建用户)
    - [获取指定用户信息](#获取指定用户信息)
    - [更新指定用户信息](#更新指定用户信息)
    - [删除用户](#删除用户)
    - [为用户分配角色](#为用户分配角色)
  - [🎭 角色管理API](#-角色管理api)
    - [创建角色](#创建角色)
    - [分页获取角色列表](#分页获取角色列表)
    - [获取指定角色信息](#获取指定角色信息)
    - [更新角色信息](#更新角色信息)
    - [删除角色](#删除角色)
    - [为角色分配用户](#为角色分配用户)
    - [为角色分配菜单](#为角色分配菜单)
  - [🍔 菜单管理API](#-菜单管理api)
    - [创建菜单](#创建菜单)
    - [分页获取菜单列表](#分页获取菜单列表)
    - [获取菜单树形结构](#获取菜单树形结构)
    - [获取当前用户菜单](#获取当前用户菜单)
    - [获取指定用户菜单](#获取指定用户菜单)
    - [获取指定菜单信息](#获取指定菜单信息)
    - [更新菜单信息](#更新菜单信息)
    - [删除菜单](#删除菜单)

## 🔐 认证说明

### JWT Token认证

大多数API需要在请求头中携带JWT Token：

```http
Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...
```

### 权限级别

- **公开接口**：无需认证
- **用户接口**：需要登录用户Token
- **管理员接口**：需要超级管理员权限

## 📊 统一响应格式

所有API都遵循统一的响应格式：

### 成功响应
```json
{
    "code": 200,
    "message": "操作成功",
    "data": {
        // 具体数据
    },
    "timestamp": 1704096000000
}
```

### 错误响应
```json
{
    "code": 400,
    "message": "请求参数错误",
    "data": {
        "errors": {
            "field": ["错误信息"]
        }
    },
    "timestamp": 1704096000000
}
```

### 分页响应
```json
{
    "code": 200,
    "message": "查询成功",
    "data": {
        "items": [...],
        "pagination": {
            "page": 1,
            "per_page": 10,
            "total": 100,
            "pages": 10,
            "has_next": true,
            "has_prev": false
        }
    },
    "timestamp": 1704096000000
}
```

## 👤 用户管理API

### 用户注册

**接口地址**：`POST /api/users/register`

**权限要求**：无需认证

**请求示例**：

```bash
curl -X POST "http://localhost:8001/api/users/register" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "email": "test@example.com",
    "password": "123456",
    "confirm_password": "123456"
  }'
```

**请求参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| username | string | 是 | 用户名（3-50字符） |
| email | string | 是 | 邮箱地址 |
| password | string | 是 | 密码（6-20字符） |
| confirm_password | string | 是 | 确认密码 |

**成功响应**：

```json
{
    "code": 200,
    "message": "注册成功",
    "data": {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "real_name": null,
        "avatar": null,
        "is_active": true,
        "is_superuser": false,
        "created_at": "2024-01-01T10:00:00Z",
        "updated_at": "2024-01-01T10:00:00Z"
    },
    "timestamp": 1704096000000
}
```

**错误响应示例**：

```json
{
    "code": 400,
    "message": "两次密码输入不一致",
    "data": null,
    "timestamp": 1704096000000
}
```

### 用户登录

**接口地址**：`POST /api/users/login`

**权限要求**：无需认证

**请求示例**：

```bash
curl -X POST "http://localhost:8001/api/users/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "testuser",
    "password": "123456"
  }'
```

**请求参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| username | string | 是 | 用户名或邮箱 |
| password | string | 是 | 密码 |

**成功响应**：

```json
{
    "code": 200,
    "message": "登录成功",
    "data": {
        "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
        "token_type": "bearer",
        "user": {
            "id": 1,
            "username": "testuser",
            "email": "test@example.com",
            "real_name": null,
            "avatar": null,
            "is_active": true,
            "is_superuser": false
        }
    },
    "timestamp": 1704096000000
}
```

### 获取当前用户信息

**接口地址**：`GET /api/users/me`

**权限要求**：需要用户Token

**请求示例**：

```bash
curl -X GET "http://localhost:8001/api/users/me" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

**成功响应**：

```json
{
    "code": 200,
    "message": "获取成功",
    "data": {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "phone": null,
        "real_name": "张三",
        "avatar": "https://example.com/avatar.jpg",
        "is_active": true,
        "is_superuser": false,
        "created_at": "2024-01-01T10:00:00Z",
        "updated_at": "2024-01-01T10:00:00Z"
    },
    "timestamp": 1704096000000
}
```

### 更新当前用户信息

**接口地址**：`PUT /api/users/me`

**权限要求**：需要用户Token

**请求示例**：

```bash
curl -X PUT "http://localhost:8001/api/users/me" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "real_name": "张三",
    "phone": "13888888888",
    "avatar": "https://example.com/new-avatar.jpg"
  }'
```

**请求参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| username | string | 否 | 用户名（3-50字符） |
| email | string | 否 | 邮箱地址 |
| phone | string | 否 | 手机号 |
| real_name | string | 否 | 真实姓名 |
| avatar | string | 否 | 头像URL |
| is_active | boolean | 否 | 是否激活 |

**成功响应**：

```json
{
    "code": 200,
    "message": "更新成功",
    "data": {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "phone": "13888888888",
        "real_name": "张三",
        "avatar": "https://example.com/new-avatar.jpg",
        "is_active": true,
        "is_superuser": false,
        "created_at": "2024-01-01T10:00:00Z",
        "updated_at": "2024-01-01T12:00:00Z"
    },
    "timestamp": 1704096000000
}
```

### 修改密码

**接口地址**：`PUT /api/users/me/password`

**权限要求**：需要用户Token

**请求示例**：

```bash
curl -X PUT "http://localhost:8001/api/users/me/password" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "old_password": "123456",
    "new_password": "newpassword123"
  }'
```

**请求参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| old_password | string | 是 | 原密码 |
| new_password | string | 是 | 新密码（6-20字符） |

**成功响应**：

```json
{
    "code": 200,
    "message": "密码修改成功",
    "data": null,
    "timestamp": 1704096000000
}
```

### 分页获取用户列表

**接口地址**：`GET /api/users`

**权限要求**：需要超级管理员权限

**请求示例**：

```bash
curl -X GET "http://localhost:8001/api/users?page=1&per_page=10&search=test" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

**查询参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| page | integer | 否 | 页码（默认1） |
| per_page | integer | 否 | 每页数量（默认10，最大100） |
| search | string | 否 | 搜索关键词 |

**成功响应**：

```json
{
    "code": 200,
    "message": "查询成功",
    "data": {
        "items": [
            {
                "id": 1,
                "username": "testuser1",
                "email": "test1@example.com",
                "phone": null,
                "real_name": "张三",
                "avatar": null,
                "is_active": true,
                "is_superuser": false,
                "created_at": "2024-01-01T10:00:00Z",
                "updated_at": "2024-01-01T10:00:00Z"
            },
            {
                "id": 2,
                "username": "testuser2",
                "email": "test2@example.com",
                "phone": null,
                "real_name": "李四",
                "avatar": null,
                "is_active": true,
                "is_superuser": false,
                "created_at": "2024-01-01T11:00:00Z",
                "updated_at": "2024-01-01T11:00:00Z"
            }
        ],
        "pagination": {
            "page": 1,
            "per_page": 10,
            "total": 2,
            "pages": 1,
            "has_next": false,
            "has_prev": false
        }
    },
    "timestamp": 1704096000000
}
```

### 创建用户

**接口地址**：`POST /api/users`

**权限要求**：需要超级管理员权限

**请求示例**：

```bash
curl -X POST "http://localhost:8001/api/users" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "username": "newuser",
    "email": "newuser@example.com",
    "password": "123456",
    "real_name": "新用户",
    "is_active": true
  }'
```

**请求参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| username | string | 是 | 用户名（3-50字符） |
| email | string | 是 | 邮箱地址 |
| password | string | 是 | 密码（6-20字符） |
| phone | string | 否 | 手机号 |
| real_name | string | 否 | 真实姓名 |
| avatar | string | 否 | 头像URL |
| is_active | boolean | 否 | 是否激活（默认true） |

**成功响应**：

```json
{
    "code": 200,
    "message": "创建成功",
    "data": {
        "id": 3,
        "username": "newuser",
        "email": "newuser@example.com",
        "phone": null,
        "real_name": "新用户",
        "avatar": null,
        "is_active": true,
        "is_superuser": false,
        "created_at": "2024-01-01T10:00:00Z",
        "updated_at": "2024-01-01T10:00:00Z"
    },
    "timestamp": 1704096000000
}
```

### 获取指定用户信息

**接口地址**：`GET /api/users/{user_id}`

**权限要求**：需要超级管理员权限

**请求示例**：

```bash
curl -X GET "http://localhost:8001/api/users/1" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

**路径参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| user_id | integer | 是 | 用户ID |

**成功响应**：

```json
{
    "code": 200,
    "message": "查询成功",
    "data": {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "phone": "13888888888",
        "real_name": "张三",
        "avatar": "https://example.com/avatar.jpg",
        "is_active": true,
        "is_superuser": false,
        "created_at": "2024-01-01T10:00:00Z",
        "updated_at": "2024-01-01T12:00:00Z"
    },
    "timestamp": 1704096000000
}
```

### 更新指定用户信息

**接口地址**：`PUT /api/users/{user_id}`

**权限要求**：需要超级管理员权限

**请求示例**：

```bash
curl -X PUT "http://localhost:8001/api/users/1" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "real_name": "张三丰",
    "is_active": false
  }'
```

**路径参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| user_id | integer | 是 | 用户ID |

**请求参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| username | string | 否 | 用户名（3-50字符） |
| email | string | 否 | 邮箱地址 |
| phone | string | 否 | 手机号 |
| real_name | string | 否 | 真实姓名 |
| avatar | string | 否 | 头像URL |
| is_active | boolean | 否 | 是否激活 |

**成功响应**：

```json
{
    "code": 200,
    "message": "更新成功",
    "data": {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "phone": "13888888888",
        "real_name": "张三丰",
        "avatar": "https://example.com/avatar.jpg",
        "is_active": false,
        "is_superuser": false,
        "created_at": "2024-01-01T10:00:00Z",
        "updated_at": "2024-01-01T14:00:00Z"
    },
    "timestamp": 1704096000000
}
```

### 删除用户

**接口地址**：`DELETE /api/users/{user_id}`

**权限要求**：需要超级管理员权限

**请求示例**：

```bash
curl -X DELETE "http://localhost:8001/api/users/1" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

**路径参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| user_id | integer | 是 | 用户ID |

**成功响应**：

```json
{
    "code": 200,
    "message": "删除成功",
    "data": {
        "id": 1,
        "deleted": true
    },
    "timestamp": 1704096000000
}
```

### 为用户分配角色

**接口地址**：`POST /api/users/{user_id}/roles`

**权限要求**：需要超级管理员权限

**请求示例**：

```bash
curl -X POST "http://localhost:8001/api/users/1/roles" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "role_ids": [1, 2, 3]
  }'
```

**路径参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| user_id | integer | 是 | 用户ID |

**请求参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| role_ids | array | 是 | 角色ID列表 |

**成功响应**：

```json
{
    "code": 200,
    "message": "角色分配成功",
    "data": null,
    "timestamp": 1704096000000
}
```

## 🎭 角色管理API

### 创建角色

**接口地址**：`POST /api/roles`

**权限要求**：需要超级管理员权限

**请求示例**：

```bash
curl -X POST "http://localhost:8001/api/roles" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "name": "管理员",
    "code": "admin",
    "description": "系统管理员，拥有所有权限",
    "is_active": true
  }'
```

**请求参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| name | string | 是 | 角色名称（1-50字符） |
| code | string | 是 | 角色代码（1-50字符） |
| description | string | 否 | 角色描述（最大255字符） |
| is_active | boolean | 否 | 是否启用（默认true） |

**成功响应**：

```json
{
    "code": 200,
    "message": "角色创建成功",
    "data": {
        "id": 1,
        "name": "管理员",
        "code": "admin",
        "description": "系统管理员，拥有所有权限",
        "is_active": true,
        "created_at": "2024-01-01T10:00:00Z",
        "updated_at": "2024-01-01T10:00:00Z"
    },
    "timestamp": 1704096000000
}
```

### 分页获取角色列表

**接口地址**：`GET /api/roles`

**权限要求**：需要用户Token

**请求示例**：

```bash
curl -X GET "http://localhost:8001/api/roles?page=1&per_page=10&search=管理" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

**查询参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| page | integer | 否 | 页码（默认1） |
| per_page | integer | 否 | 每页数量（默认10，最大100） |
| search | string | 否 | 搜索关键词 |

**成功响应**：

```json
{
    "code": 200,
    "message": "查询成功",
    "data": {
        "items": [
            {
                "id": 1,
                "name": "管理员",
                "code": "admin",
                "description": "系统管理员，拥有所有权限",
                "is_active": true,
                "created_at": "2024-01-01T10:00:00Z",
                "updated_at": "2024-01-01T10:00:00Z"
            },
            {
                "id": 2,
                "name": "普通用户",
                "code": "user",
                "description": "普通用户权限",
                "is_active": true,
                "created_at": "2024-01-01T11:00:00Z",
                "updated_at": "2024-01-01T11:00:00Z"
            }
        ],
        "pagination": {
            "page": 1,
            "per_page": 10,
            "total": 2,
            "pages": 1,
            "has_next": false,
            "has_prev": false
        }
    },
    "timestamp": 1704096000000
}
```

### 获取指定角色信息

**接口地址**：`GET /api/roles/{role_id}`

**权限要求**：需要用户Token

**请求示例**：

```bash
curl -X GET "http://localhost:8001/api/roles/1" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

**路径参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| role_id | integer | 是 | 角色ID |

**成功响应**：

```json
{
    "code": 200,
    "message": "查询成功",
    "data": {
        "id": 1,
        "name": "管理员",
        "code": "admin",
        "description": "系统管理员，拥有所有权限",
        "is_active": true,
        "created_at": "2024-01-01T10:00:00Z",
        "updated_at": "2024-01-01T10:00:00Z"
    },
    "timestamp": 1704096000000
}
```

### 更新角色信息

**接口地址**：`PUT /api/roles/{role_id}`

**权限要求**：需要超级管理员权限

**请求示例**：

```bash
curl -X PUT "http://localhost:8001/api/roles/1" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "name": "高级管理员",
    "description": "高级管理员，拥有更多权限"
  }'
```

**路径参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| role_id | integer | 是 | 角色ID |

**请求参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| name | string | 否 | 角色名称（1-50字符） |
| code | string | 否 | 角色代码（1-50字符） |
| description | string | 否 | 角色描述（最大255字符） |
| is_active | boolean | 否 | 是否启用 |

**成功响应**：

```json
{
    "code": 200,
    "message": "更新成功",
    "data": {
        "id": 1,
        "name": "高级管理员",
        "code": "admin",
        "description": "高级管理员，拥有更多权限",
        "is_active": true,
        "created_at": "2024-01-01T10:00:00Z",
        "updated_at": "2024-01-01T14:00:00Z"
    },
    "timestamp": 1704096000000
}
```

### 删除角色

**接口地址**：`DELETE /api/roles/{role_id}`

**权限要求**：需要超级管理员权限

**请求示例**：

```bash
curl -X DELETE "http://localhost:8001/api/roles/1" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

**路径参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| role_id | integer | 是 | 角色ID |

**成功响应**：

```json
{
    "code": 200,
    "message": "删除成功",
    "data": {
        "id": 1,
        "deleted": true
    },
    "timestamp": 1704096000000
}
```

### 为角色分配用户

**接口地址**：`POST /api/roles/{role_id}/users`

**权限要求**：需要超级管理员权限

**请求示例**：

```bash
curl -X POST "http://localhost:8001/api/roles/1/users" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "user_ids": [1, 2, 3]
  }'
```

**路径参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| role_id | integer | 是 | 角色ID |

**请求参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| user_ids | array | 是 | 用户ID列表 |

**成功响应**：

```json
{
    "code": 200,
    "message": "用户分配成功",
    "data": null,
    "timestamp": 1704096000000
}
```

### 为角色分配菜单

**接口地址**：`POST /api/roles/{role_id}/menus`

**权限要求**：需要超级管理员权限

**请求示例**：

```bash
curl -X POST "http://localhost:8001/api/roles/1/menus" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "menu_ids": [1, 2, 3, 4]
  }'
```

**路径参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| role_id | integer | 是 | 角色ID |

**请求参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| menu_ids | array | 是 | 菜单ID列表 |

**成功响应**：

```json
{
    "code": 200,
    "message": "菜单分配成功",
    "data": null,
    "timestamp": 1704096000000
}
```

## 🍔 菜单管理API

### 创建菜单

**接口地址**：`POST /api/menus`

**权限要求**：需要超级管理员权限

**请求示例**：

```bash
curl -X POST "http://localhost:8001/api/menus" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "name": "用户管理",
    "path": "/users",
    "component": "UserManagement",
    "icon": "user",
    "order_num": 1,
    "parent_id": null,
    "menu_type": "menu",
    "permission": "user:list",
    "is_visible": true,
    "is_active": true
  }'
```

**请求参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| name | string | 是 | 菜单名称（1-50字符） |
| path | string | 否 | 菜单路径（最大255字符） |
| component | string | 否 | 组件路径（最大255字符） |
| icon | string | 否 | 菜单图标（最大100字符） |
| order_num | integer | 否 | 排序号（默认0） |
| parent_id | integer | 否 | 父菜单ID |
| menu_type | string | 否 | 菜单类型：menu菜单，button按钮（默认menu） |
| permission | string | 否 | 权限标识（最大100字符） |
| is_visible | boolean | 否 | 是否显示（默认true） |
| is_active | boolean | 否 | 是否启用（默认true） |

**成功响应**：

```json
{
    "code": 200,
    "message": "菜单创建成功",
    "data": {
        "id": 1,
        "name": "用户管理",
        "path": "/users",
        "component": "UserManagement",
        "icon": "user",
        "order_num": 1,
        "parent_id": null,
        "menu_type": "menu",
        "permission": "user:list",
        "is_visible": true,
        "is_active": true,
        "created_at": "2024-01-01T10:00:00Z",
        "updated_at": "2024-01-01T10:00:00Z"
    },
    "timestamp": 1704096000000
}
```

### 分页获取菜单列表

**接口地址**：`GET /api/menus`

**权限要求**：需要用户Token

**请求示例**：

```bash
curl -X GET "http://localhost:8001/api/menus?page=1&per_page=10&search=用户" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

**查询参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| page | integer | 否 | 页码（默认1） |
| per_page | integer | 否 | 每页数量（默认10，最大100） |
| search | string | 否 | 搜索关键词 |

**成功响应**：

```json
{
    "code": 200,
    "message": "查询成功",
    "data": {
        "items": [
            {
                "id": 1,
                "name": "用户管理",
                "path": "/users",
                "component": "UserManagement",
                "icon": "user",
                "order_num": 1,
                "parent_id": null,
                "menu_type": "menu",
                "permission": "user:list",
                "is_visible": true,
                "is_active": true,
                "created_at": "2024-01-01T10:00:00Z",
                "updated_at": "2024-01-01T10:00:00Z"
            }
        ],
        "pagination": {
            "page": 1,
            "per_page": 10,
            "total": 1,
            "pages": 1,
            "has_next": false,
            "has_prev": false
        }
    },
    "timestamp": 1704096000000
}
```

### 获取菜单树形结构

**接口地址**：`GET /api/menus/tree`

**权限要求**：需要用户Token

**请求示例**：

```bash
curl -X GET "http://localhost:8001/api/menus/tree" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

**成功响应**：

```json
{
    "code": 200,
    "message": "查询成功",
    "data": [
        {
            "id": 1,
            "name": "系统管理",
            "path": "/system",
            "component": "Layout",
            "icon": "setting",
            "order_num": 1,
            "parent_id": null,
            "menu_type": "menu",
            "permission": null,
            "is_visible": true,
            "is_active": true,
            "children": [
                {
                    "id": 2,
                    "name": "用户管理",
                    "path": "/system/users",
                    "component": "UserManagement",
                    "icon": "user",
                    "order_num": 1,
                    "parent_id": 1,
                    "menu_type": "menu",
                    "permission": "user:list",
                    "is_visible": true,
                    "is_active": true,
                    "children": []
                }
            ]
        }
    ],
    "timestamp": 1704096000000
}
```

### 获取当前用户菜单

**接口地址**：`GET /api/menus/me`

**权限要求**：需要用户Token

**请求示例**：

```bash
curl -X GET "http://localhost:8001/api/menus/me" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

**成功响应**：

```json
{
    "code": 200,
    "message": "查询成功",
    "data": [
        {
            "id": 1,
            "name": "系统管理",
            "path": "/system",
            "component": "Layout",
            "icon": "setting",
            "order_num": 1,
            "parent_id": null,
            "menu_type": "menu",
            "permission": null,
            "is_visible": true,
            "is_active": true,
            "children": [
                {
                    "id": 2,
                    "name": "用户管理",
                    "path": "/system/users",
                    "component": "UserManagement",
                    "icon": "user",
                    "order_num": 1,
                    "parent_id": 1,
                    "menu_type": "menu",
                    "permission": "user:list",
                    "is_visible": true,
                    "is_active": true,
                    "children": []
                }
            ]
        }
    ],
    "timestamp": 1704096000000
}
```

### 获取指定用户菜单

**接口地址**：`GET /api/menus/user/{user_id}`

**权限要求**：需要用户Token（只能查看自己的菜单或超级管理员查看任何人的菜单）

**请求示例**：

```bash
curl -X GET "http://localhost:8001/api/menus/user/1" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

**路径参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| user_id | integer | 是 | 用户ID |

**成功响应**：

```json
{
    "code": 200,
    "message": "查询成功",
    "data": [
        {
            "id": 1,
            "name": "系统管理",
            "path": "/system",
            "component": "Layout",
            "icon": "setting",
            "order_num": 1,
            "parent_id": null,
            "menu_type": "menu",
            "permission": null,
            "is_visible": true,
            "is_active": true,
            "children": []
        }
    ],
    "timestamp": 1704096000000
}
```

### 获取指定菜单信息

**接口地址**：`GET /api/menus/{menu_id}`

**权限要求**：需要用户Token

**请求示例**：

```bash
curl -X GET "http://localhost:8001/api/menus/1" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

**路径参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| menu_id | integer | 是 | 菜单ID |

**成功响应**：

```json
{
    "code": 200,
    "message": "查询成功",
    "data": {
        "id": 1,
        "name": "用户管理",
        "path": "/users",
        "component": "UserManagement",
        "icon": "user",
        "order_num": 1,
        "parent_id": null,
        "menu_type": "menu",
        "permission": "user:list",
        "is_visible": true,
        "is_active": true,
        "created_at": "2024-01-01T10:00:00Z",
        "updated_at": "2024-01-01T10:00:00Z"
    },
    "timestamp": 1704096000000
}
```

### 更新菜单信息

**接口地址**：`PUT /api/menus/{menu_id}`

**权限要求**：需要超级管理员权限

**请求示例**：

```bash
curl -X PUT "http://localhost:8001/api/menus/1" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  -H "Content-Type: application/json" \
  -d '{
    "name": "高级用户管理",
    "path": "/advanced-users",
    "icon": "user-plus"
  }'
```

**路径参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| menu_id | integer | 是 | 菜单ID |

**请求参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| name | string | 否 | 菜单名称（1-50字符） |
| path | string | 否 | 菜单路径（最大255字符） |
| component | string | 否 | 组件路径（最大255字符） |
| icon | string | 否 | 菜单图标（最大100字符） |
| order_num | integer | 否 | 排序号（默认0） |
| parent_id | integer | 否 | 父菜单ID |
| menu_type | string | 否 | 菜单类型：menu菜单，button按钮（默认menu） |
| permission | string | 否 | 权限标识（最大100字符） |
| is_visible | boolean | 否 | 是否显示（默认true） |
| is_active | boolean | 否 | 是否启用（默认true） |

**成功响应**：

```json
{
    "code": 200,
    "message": "更新成功",
    "data": {
        "id": 1,
        "name": "高级用户管理",
        "path": "/advanced-users",
        "component": "AdvancedUserManagement",
        "icon": "user-plus",
        "order_num": 5,
        "parent_id": null,
        "menu_type": "menu",
        "permission": "user:advanced",
        "is_visible": true,
        "is_active": true,
        "created_at": "2024-01-01T10:00:00Z",
        "updated_at": "2024-01-01T15:00:00Z"
    },
    "timestamp": 1704096000000
}
```

### 删除菜单

**接口地址**：`DELETE /api/menus/{menu_id}`

**权限要求**：需要超级管理员权限

**请求示例**：

```bash
curl -X DELETE "http://localhost:8001/api/menus/1" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

**路径参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| menu_id | integer | 是 | 菜单ID |

**成功响应**：

```json
{
    "code": 200,
    "message": "删除成功",
    "data": {
        "id": 1,
        "deleted": true
    },
    "timestamp": 1704096000000
}
```

**错误响应示例**：

```json
{
    "code": 400,
    "message": "存在子菜单，不能删除",
    "data": null,
    "timestamp": 1704096000000
}
```