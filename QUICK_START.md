# 🚀 快速启动指南

## 问题解决

### 1. Swagger文档已配置 ✅

项目已经集成了Swagger文档，启动后可以访问：
- **Swagger UI**: http://localhost:8001/docs
- **ReDoc**: http://localhost:8001/redoc

### 2. 解决依赖安装问题 ✅

如果遇到 `ModuleNotFoundError: No module named 'fastapi'` 错误，说明依赖包未安装。

## 启动方式

### 方式一：使用Python启动脚本（推荐）

```bash
# 自动安装依赖并启动
python3 start.py

# 或者给予执行权限后直接运行
./start.py
```

**启动参数：**
```bash
python3 start.py --help                    # 查看帮助
python3 start.py --port 8080              # 指定端口
python3 start.py --host 127.0.0.1         # 指定主机
python3 start.py --no-reload              # 禁用自动重载
python3 start.py --workers 4              # 生产模式，4个工作进程
python3 start.py --skip-install           # 跳过依赖安装
python3 start.py --skip-checks            # 跳过环境检查
```

### 方式二：使用Bash脚本

```bash
# 给予执行权限
chmod +x start.sh

# 启动应用
./start.sh
```

### 方式三：手动启动

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 复制环境配置文件
cp .env.example .env

# 3. 编辑环境配置（配置数据库连接等）
nano .env

# 4. 启动应用
python3 main.py
# 或使用uvicorn
uvicorn main:app --host 0.0.0.0 --port 8001 --reload
```

## 环境准备

### 1. Python环境要求
- Python 3.8+
- 建议使用虚拟环境

### 2. 创建虚拟环境（推荐）
```bash
# 创建虚拟环境
python3 -m venv venv

# 激活虚拟环境
source venv/bin/activate      # Linux/Mac
# venv\Scripts\activate       # Windows
```

### 3. 数据库准备
```bash
# 创建MySQL数据库
mysql -u root -p -e "CREATE DATABASE fastapi_admin CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;"

# 初始化数据库迁移
alembic init migrations
alembic revision --autogenerate -m "Initial migration"
alembic upgrade head
```

## 访问地址

启动成功后，可以访问以下地址：

| 服务 | 地址 | 说明 |
|------|------|------|
| 主页 | http://localhost:8001 | 应用首页 |
| **Swagger文档** | http://localhost:8001/docs | **API接口文档和调试界面** |
| ReDoc文档 | http://localhost:8001/redoc | API文档（ReDoc样式） |
| 健康检查 | http://localhost:8001/health | 服务健康状态 |

## API接口测试

### 使用Swagger UI（推荐）

1. 访问 http://localhost:8001/docs
2. 展开接口分组（如"用户管理"）
3. 点击要测试的接口
4. 点击"Try it out"按钮
5. 填写请求参数
6. 点击"Execute"执行

### 示例：用户注册

**POST** `/api/users/register`

```json
{
  "username": "testuser",
  "email": "test@example.com",
  "password": "123456",
  "confirm_password": "123456"
}
```

### 示例：用户登录

**POST** `/api/users/login`

```json
{
  "username": "testuser",
  "password": "123456"
}
```

## 常见问题

### Q1: 依赖安装失败怎么办？
```bash
# 升级pip
pip install --upgrade pip

# 使用清华源安装
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple/
```

### Q2: 数据库连接失败怎么办？
1. 检查MySQL服务是否启动
2. 检查 `.env` 文件中的数据库配置
3. 确认数据库已创建
4. 确认用户权限

### Q3: 端口被占用怎么办？
```bash
# 查看端口占用
lsof -i :8001

# 或者使用其他端口启动
python3 start.py --port 8080
```

### Q4: 如何停止服务？
按 `Ctrl+C` 停止服务

## 项目结构

```
python-study-demo/
├── start.py              # Python启动脚本
├── start.sh              # Bash启动脚本
├── main.py               # FastAPI应用入口
├── config.py             # 配置文件
├── requirements.txt      # 依赖文件
├── .env.example          # 环境变量示例
├── README.md             # 项目文档
├── QUICK_START.md        # 快速启动指南
└── app/                  # 应用代码
    ├── models/           # 数据库模型
    ├── schemas/          # 数据验证
    ├── services/         # 业务逻辑
    ├── routes/           # API路由
    └── utils/            # 工具类
```

---

🎉 **现在您可以愉快地使用Swagger文档调试API接口了！**