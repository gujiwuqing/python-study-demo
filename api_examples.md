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
  - [🚨 常见错误处理](#-常见错误处理)
    - [401 未授权](#401-未授权)
    - [403 权限不足](#403-权限不足)
    - [404 资源不存在](#404-资源不存在)
    - [422 参数验证错误](#422-参数验证错误)
  - [🔧 SDK使用示例](#-sdk使用示例)
    - [JavaScript/TypeScript](#javascripttypescript)
    - [Python SDK](#python-sdk)
  - [🔍 测试工具](#-测试工具)
    - [Postman集合导入](#postman集合导入)
    - [环境变量设置](#环境变量设置)
    - [HTTPie命令示例](#httpie命令示例)
  - [📚 API状态码说明](#-api状态码说明)
  - [📋 API版本控制](#-api版本控制)
  - [🔗 相关链接](#-相关链接)
  - [📝 更新日志](#-更新日志)
    - [v1.0.0 (2024-01-01)](#v100-2024-01-01)
    - [未来版本计划](#未来版本计划)
  - [💡 使用建议](#-使用建议)

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
curl -X POST "http://localhost:8000/api/users/register" \
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
curl -X POST "http://localhost:8000/api/users/login" \
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
curl -X GET "http://localhost:8000/api/users/me" \
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
curl -X PUT "http://localhost:8000/api/users/me" \
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
curl -X PUT "http://localhost:8000/api/users/me/password" \
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
curl -X GET "http://localhost:8000/api/users?page=1&per_page=10&search=test" \
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
curl -X POST "http://localhost:8000/api/users" \
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
curl -X GET "http://localhost:8000/api/users/1" \
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
curl -X PUT "http://localhost:8000/api/users/1" \
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
curl -X DELETE "http://localhost:8000/api/users/1" \
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
curl -X POST "http://localhost:8000/api/users/1/roles" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..." \
  -H "Content-Type: application/json" \
  -d '[1, 2, 3]'
```

**路径参数**：

| 参数 | 类型 | 必填 | 描述 |
|------|------|------|------|
| user_id | integer | 是 | 用户ID |

**请求参数**：

传递角色ID数组，例如：`[1, 2, 3]`

**成功响应**：

```json
{
    "code": 200,
    "message": "角色分配成功",
    "data": null,
    "timestamp": 1704096000000
}
```

## 🚨 常见错误处理

### 401 未授权

```json
{
    "code": 401,
    "message": "未授权访问",
    "data": null,
    "timestamp": 1704096000000
}
```

### 403 权限不足

```json
{
    "code": 403,
    "message": "权限不足",
    "data": null,
    "timestamp": 1704096000000
}
```

### 404 资源不存在

```json
{
    "code": 404,
    "message": "用户不存在",
    "data": null,
    "timestamp": 1704096000000
}
```

### 422 参数验证错误

```json
{
    "code": 400,
    "message": "参数验证失败",
    "data": {
        "errors": {
            "email": ["邮箱格式不正确"],
            "password": ["密码长度至少6位"]
        }
    },
    "timestamp": 1704096000000
}
```

## 🔧 SDK使用示例

### JavaScript/TypeScript

```javascript
// API客户端封装
class ApiClient {
    constructor(baseURL = 'http://localhost:8000', token = null) {
        this.baseURL = baseURL;
        this.token = token;
    }

    setToken(token) {
        this.token = token;
    }

    async request(method, endpoint, data = null) {
        const headers = {
            'Content-Type': 'application/json',
        };

        if (this.token) {
            headers['Authorization'] = `Bearer ${this.token}`;
        }

        const config = {
            method,
            headers,
        };

        if (data) {
            config.body = JSON.stringify(data);
        }

        const response = await fetch(`${this.baseURL}${endpoint}`, config);
        return await response.json();
    }

    // 用户注册
    async register(userData) {
        return await this.request('POST', '/api/users/register', userData);
    }

    // 用户登录
    async login(credentials) {
        const result = await this.request('POST', '/api/users/login', credentials);
        if (result.code === 200) {
            this.setToken(result.data.access_token);
        }
        return result;
    }

    // 获取当前用户信息
    async getCurrentUser() {
        return await this.request('GET', '/api/users/me');
    }

    // 更新当前用户信息
    async updateCurrentUser(userData) {
        return await this.request('PUT', '/api/users/me', userData);
    }

    // 修改密码
    async changePassword(passwordData) {
        return await this.request('PUT', '/api/users/me/password', passwordData);
    }

    // 获取用户列表
    async getUsers(page = 1, perPage = 10, search = '') {
        const params = new URLSearchParams({
            page: page.toString(),
            per_page: perPage.toString(),
        });
        
        if (search) {
            params.append('search', search);
        }

        return await this.request('GET', `/api/users?${params}`);
    }
}

// 使用示例
const api = new ApiClient();

// 用户注册
async function registerUser() {
    try {
        const result = await api.register({
            username: 'testuser',
            email: 'test@example.com',
            password: '123456',
            confirm_password: '123456'
        });
        
        if (result.code === 200) {
            console.log('注册成功:', result.data);
        } else {
            console.error('注册失败:', result.message);
        }
    } catch (error) {
        console.error('请求错误:', error);
    }
}

// 用户登录
async function loginUser() {
    try {
        const result = await api.login({
            username: 'testuser',
            password: '123456'
        });
        
        if (result.code === 200) {
            console.log('登录成功:', result.data);
            localStorage.setItem('access_token', result.data.access_token);
        } else {
            console.error('登录失败:', result.message);
        }
    } catch (error) {
        console.error('请求错误:', error);
    }
}
```

### Python SDK

```python
import requests
import json
from typing import Optional, Dict, Any

class ApiClient:
    def __init__(self, base_url: str = "http://localhost:8000", token: Optional[str] = None):
        self.base_url = base_url
        self.token = token
        self.session = requests.Session()
    
    def set_token(self, token: str):
        """设置认证令牌"""
        self.token = token
        self.session.headers.update({'Authorization': f'Bearer {token}'})
    
    def request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict[str, Any]:
        """发送HTTP请求"""
        url = f"{self.base_url}{endpoint}"
        headers = {'Content-Type': 'application/json'}
        
        if self.token:
            headers['Authorization'] = f'Bearer {self.token}'
        
        response = self.session.request(
            method=method,
            url=url,
            headers=headers,
            json=data if data else None
        )
        
        return response.json()
    
    def register(self, user_data: Dict) -> Dict[str, Any]:
        """用户注册"""
        return self.request('POST', '/api/users/register', user_data)
    
    def login(self, credentials: Dict) -> Dict[str, Any]:
        """用户登录"""
        result = self.request('POST', '/api/users/login', credentials)
        if result.get('code') == 200:
            self.set_token(result['data']['access_token'])
        return result
    
    def get_current_user(self) -> Dict[str, Any]:
        """获取当前用户信息"""
        return self.request('GET', '/api/users/me')
    
    def update_current_user(self, user_data: Dict) -> Dict[str, Any]:
        """更新当前用户信息"""
        return self.request('PUT', '/api/users/me', user_data)
    
    def change_password(self, password_data: Dict) -> Dict[str, Any]:
        """修改密码"""
        return self.request('PUT', '/api/users/me/password', password_data)
    
    def get_users(self, page: int = 1, per_page: int = 10, search: str = '') -> Dict[str, Any]:
        """获取用户列表"""
        params = f"?page={page}&per_page={per_page}"
        if search:
            params += f"&search={search}"
        return self.request('GET', f'/api/users{params}')

# 使用示例
def main():
    api = ApiClient()
    
    # 用户注册
    try:
        result = api.register({
            'username': 'testuser',
            'email': 'test@example.com',
            'password': '123456',
            'confirm_password': '123456'
        })
        
        if result['code'] == 200:
            print('注册成功:', result['data'])
        else:
            print('注册失败:', result['message'])
    except Exception as e:
        print('请求错误:', e)
    
    # 用户登录
    try:
        result = api.login({
            'username': 'testuser',
            'password': '123456'
        })
        
        if result['code'] == 200:
            print('登录成功:', result['data'])
        else:
            print('登录失败:', result['message'])
    except Exception as e:
        print('请求错误:', e)

if __name__ == '__main__':
    main()
```

## 🔍 测试工具

### Postman集合导入

您可以创建Postman集合来测试API：

```json
{
    "info": {
        "name": "FastAPI 后端管理系统",
        "description": "用户管理API测试集合",
        "version": "1.0.0"
    },
    "item": [
        {
            "name": "用户注册",
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
                    "raw": "{\n  \"username\": \"testuser\",\n  \"email\": \"test@example.com\",\n  \"password\": \"123456\",\n  \"confirm_password\": \"123456\"\n}"
                },
                "url": {
                    "raw": "{{baseUrl}}/api/users/register",
                    "host": ["{{baseUrl}}"],
                    "path": ["api", "users", "register"]
                }
            }
        },
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
                    "raw": "{\n  \"username\": \"testuser\",\n  \"password\": \"123456\"\n}"
                },
                "url": {
                    "raw": "{{baseUrl}}/api/users/login",
                    "host": ["{{baseUrl}}"],
                    "path": ["api", "users", "login"]
                }
            }
        }
    ],
    "variable": [
        {
            "key": "baseUrl",
            "value": "http://localhost:8000"
        },
        {
            "key": "accessToken",
            "value": ""
        }
    ]
}
```

### 环境变量设置

在Postman中设置以下环境变量：

| 变量名 | 值 | 描述 |
|--------|----|----|
| baseUrl | http://localhost:8000 | API基础地址 |
| accessToken | (登录后设置) | JWT访问令牌 |

### HTTPie命令示例

使用HTTPie工具测试API：

```bash
# 用户注册
http POST localhost:8000/api/users/register \
  username=testuser \
  email=test@example.com \
  password=123456 \
  confirm_password=123456

# 用户登录
http POST localhost:8000/api/users/login \
  username=testuser \
  password=123456

# 获取当前用户信息（需要先登录获取token）
http GET localhost:8000/api/users/me \
  Authorization:"Bearer YOUR_ACCESS_TOKEN"

# 分页获取用户列表
http GET localhost:8000/api/users \
  Authorization:"Bearer YOUR_ACCESS_TOKEN" \
  page==1 \
  per_page==10 \
  search=="test"
```

## 📚 API状态码说明

| 状态码 | 说明 | 场景 |
|--------|------|------|
| 200 | 成功 | 请求成功处理 |
| 400 | 请求错误 | 参数验证失败、业务逻辑错误 |
| 401 | 未授权 | 未提供认证信息或认证失败 |
| 403 | 禁止访问 | 权限不足 |
| 404 | 资源不存在 | 请求的资源未找到 |
| 422 | 参数验证失败 | 请求参数格式错误 |
| 500 | 服务器错误 | 服务器内部错误 |

## 📋 API版本控制

当前API版本：`v1.0.0`

版本控制策略：
- **主版本号**：不兼容的API修改
- **次版本号**：向下兼容的功能新增
- **修订号**：向下兼容的问题修正

## 🔗 相关链接

- **项目仓库**：[GitHub Repository](https://github.com/your-username/fastapi-admin)
- **在线文档**：[API Documentation](http://localhost:8000/docs)
- **问题反馈**：[Issue Tracker](https://github.com/your-username/fastapi-admin/issues)

## 📝 更新日志

### v1.0.0 (2024-01-01)
- ✅ 用户管理API
- ✅ JWT认证
- ✅ 统一响应格式
- ✅ 分页查询支持
- ✅ 完整的错误处理

### 未来版本计划
- 🔄 角色管理API
- 🔄 菜单管理API
- 🔄 文件上传API
- 🔄 消息通知API

---

## 💡 使用建议

1. **开发环境**：使用Swagger UI进行接口调试
2. **生产环境**：使用SDK进行API调用
3. **测试**：使用Postman或HTTPie进行集成测试
4. **监控**：关注API响应时间和错误率

希望这份API使用示例文档能帮助您快速上手FastAPI后端管理系统！如有问题，请参考项目文档或提交Issue。