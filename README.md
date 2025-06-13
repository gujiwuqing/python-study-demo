# FastAPI 后端管理系统

基于 FastAPI 的现代化后端管理系统，包含用户管理、角色管理、菜单管理等功能，支持权限控制和JWT认证。

## 🚀 特性

- ✅ **现代化框架**: 基于 FastAPI，高性能异步API
- ✅ **数据库支持**: MySQL + SQLAlchemy ORM
- ✅ **认证授权**: JWT Token + RBAC权限控制
- ✅ **统一响应**: 标准化API响应格式
- ✅ **分页查询**: 完整的分页支持
- ✅ **数据迁移**: Alembic数据库迁移工具
- ✅ **类型提示**: 完整的Python类型注解
- ✅ **API文档**: 自动生成OpenAPI文档
- ✅ **异常处理**: 统一的异常处理机制

## 📋 功能模块

### 用户管理
- 用户注册/登录
- 用户信息CRUD
- 密码修改
- 用户角色分配

### 角色管理
- 角色CRUD
- 角色权限分配
- 用户角色管理

### 菜单管理
- 菜单CRUD
- 树形菜单结构
- 权限控制
- 用户菜单获取

## 🛠️ 技术栈

- **后端框架**: FastAPI 0.104.1
- **数据库**: MySQL 8.0+
- **ORM**: SQLAlchemy 2.0
- **认证**: JWT + Passlib
- **数据验证**: Pydantic
- **数据迁移**: Alembic
- **API文档**: OpenAPI (Swagger)

## 📦 项目结构

```
python-study-demo/
├── app/                    # 应用核心代码
│   ├── models/            # 数据库模型
│   │   ├── __init__.py
│   │   ├── base.py        # 基础模型
│   │   ├── user.py        # 用户和角色模型
│   │   └── menu.py        # 菜单模型
│   ├── schemas/           # 数据验证和序列化
│   │   ├── __init__.py
│   │   ├── user.py        # 用户相关schemas
│   │   ├── role.py        # 角色相关schemas
│   │   └── menu.py        # 菜单相关schemas
│   ├── services/          # 业务逻辑层
│   │   ├── __init__.py
│   │   ├── user_service.py    # 用户业务逻辑
│   │   ├── role_service.py    # 角色业务逻辑
│   │   └── menu_service.py    # 菜单业务逻辑
│   ├── routes/            # 路由和视图
│   │   ├── __init__.py
│   │   ├── user_routes.py     # 用户路由
│   │   ├── role_routes.py     # 角色路由
│   │   └── menu_routes.py     # 菜单路由
│   ├── utils/             # 工具类
│   │   ├── __init__.py
│   │   ├── database.py        # 数据库连接
│   │   ├── auth.py           # JWT认证工具
│   │   ├── response.py       # 统一响应工具
│   │   └── dependencies.py   # FastAPI依赖注入
│   └── __init__.py
├── migrations/            # 数据库迁移文件
├── tests/                # 单元测试
├── config.py             # 配置文件
├── main.py              # 应用入口
├── alembic.ini          # Alembic配置
├── requirements.txt     # Python依赖
└── README.md           # 项目文档
```

## 🚀 快速开始

### 1. 环境要求

- Python 3.8+
- MySQL 8.0+
- pip

### 2. 安装依赖

```bash
# 克隆项目
git clone <your-repo-url>
cd python-study-demo

# 创建虚拟环境（推荐）
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows

# 安装依赖
pip install -r requirements.txt
```

### 3. 环境配置

创建 `.env` 文件并配置环境变量：

```bash
# 数据库配置
MYSQL_HOST=localhost
MYSQL_PORT=3306
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=fastapi_admin

# JWT配置
JWT_SECRET_KEY=your-secret-key-here
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=30

# 应用配置
DEBUG=True
ENVIRONMENT=development
```

### 4. 数据库初始化

```bash
# 创建数据库
mysql -u root -p -e "CREATE DATABASE fastapi_admin CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 初始化Alembic
alembic init migrations

# 生成迁移文件
alembic revision --autogenerate -m "Initial migration"

# 执行迁移
alembic upgrade head
```

### 5. 启动应用

```bash
# 开发模式启动
python main.py

# 或使用uvicorn
uvicorn main:app --reload --host 0.0.0.0 --port 8001
```

应用启动后，可以访问：
- API文档: http://localhost:8001/docs
- ReDoc文档: http://localhost:8001/redoc
- 健康检查: http://localhost:8001/health

## 📚 API文档

### 统一响应格式

所有API都遵循统一的响应格式：

```json
{
    "code": 200,
    "message": "操作成功",
    "data": {},
    "timestamp": 1704096000000
}
```

### 分页响应格式

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

### 主要接口

#### 用户管理

- `POST /api/users/register` - 用户注册
- `POST /api/users/login` - 用户登录
- `GET /api/users/me` - 获取当前用户信息
- `PUT /api/users/me` - 更新当前用户信息
- `PUT /api/users/me/password` - 修改密码
- `GET /api/users` - 分页获取用户列表（管理员）
- `POST /api/users` - 创建用户（管理员）
- `GET /api/users/{user_id}` - 获取指定用户（管理员）
- `PUT /api/users/{user_id}` - 更新指定用户（管理员）
- `DELETE /api/users/{user_id}` - 删除用户（管理员）
- `POST /api/users/{user_id}/roles` - 分配角色（管理员）

#### 角色管理

- `GET /api/roles` - 分页获取角色列表
- `POST /api/roles` - 创建角色
- `GET /api/roles/{role_id}` - 获取指定角色
- `PUT /api/roles/{role_id}` - 更新角色
- `DELETE /api/roles/{role_id}` - 删除角色
- `POST /api/roles/{role_id}/users` - 分配用户
- `POST /api/roles/{role_id}/menus` - 分配菜单权限

#### 菜单管理

- `GET /api/menus` - 分页获取菜单列表
- `GET /api/menus/tree` - 获取菜单树
- `GET /api/menus/user-menus` - 获取用户菜单
- `POST /api/menus` - 创建菜单
- `GET /api/menus/{menu_id}` - 获取指定菜单
- `PUT /api/menus/{menu_id}` - 更新菜单
- `DELETE /api/menus/{menu_id}` - 删除菜单

## 🔐 认证授权

### JWT Token

系统使用JWT进行身份认证，登录后会返回：

```json
{
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "token_type": "bearer"
}
```

在请求头中携带Token：
```
Authorization: Bearer your_access_token
```

### 权限控制

系统基于RBAC（基于角色的访问控制）模型：

1. **用户(User)** - 系统用户
2. **角色(Role)** - 权限的集合
3. **菜单(Menu)** - 具体的权限资源
4. **用户角色关联** - 用户可以拥有多个角色
5. **角色菜单关联** - 角色可以访问多个菜单

## 🗄️ 数据库设计

### 主要数据表

#### users (用户表)
- id: 主键
- username: 用户名
- email: 邮箱
- phone: 手机号
- hashed_password: 加密密码
- real_name: 真实姓名
- avatar: 头像URL
- is_active: 是否激活
- is_superuser: 是否超级管理员
- created_at: 创建时间
- updated_at: 更新时间
- is_deleted: 是否删除

#### roles (角色表)
- id: 主键
- name: 角色名称
- code: 角色代码
- description: 角色描述
- is_active: 是否启用
- created_at: 创建时间
- updated_at: 更新时间
- is_deleted: 是否删除

#### menus (菜单表)
- id: 主键
- name: 菜单名称
- path: 菜单路径
- component: 组件路径
- icon: 菜单图标
- order_num: 排序号
- parent_id: 父菜单ID
- menu_type: 菜单类型
- permission: 权限标识
- is_visible: 是否显示
- is_active: 是否启用
- created_at: 创建时间
- updated_at: 更新时间
- is_deleted: 是否删除

#### 关联表
- user_roles: 用户角色关联表
- role_menu_association: 角色菜单关联表

## 🧪 测试

```bash
# 运行测试
pytest

# 运行测试并生成覆盖率报告
pytest --cov=app tests/
```

## 📝 开发规范

### 代码风格
- 遵循 PEP 8 编码规范
- 使用类型提示
- 添加必要的注释和文档字符串

### Git提交
- 使用语义化提交信息
- feat: 新功能
- fix: 修复bug
- docs: 文档更新
- style: 代码格式调整
- refactor: 代码重构
- test: 测试相关
- chore: 构建工具或辅助工具的变动

## 🤝 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 📄 许可证

本项目采用 MIT 许可证 - 查看 [LICENSE](LICENSE) 文件了解详情。

## 📞 联系方式

如有问题或建议，请通过以下方式联系：

- 项目Issues: [GitHub Issues](https://github.com/your-username/python-study-demo/issues)
- 邮箱: your-email@example.com

## 🙏 致谢

感谢以下开源项目的支持：

- [FastAPI](https://fastapi.tiangolo.com/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [Pydantic](https://pydantic-docs.helpmanual.io/)
- [Alembic](https://alembic.sqlalchemy.org/)