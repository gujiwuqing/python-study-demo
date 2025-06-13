#!/bin/bash

# FastAPI 后端管理系统启动脚本

echo "🚀 启动 FastAPI 后端管理系统..."

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: Python3 未找到，请先安装 Python3"
    exit 1
fi

# 检查是否在虚拟环境中
if [[ "$VIRTUAL_ENV" != "" ]]; then
    echo "✅ 检测到虚拟环境: $VIRTUAL_ENV"
else
    echo "⚠️  警告: 建议使用虚拟环境"
    echo "创建虚拟环境: python3 -m venv venv"
    echo "激活虚拟环境: source venv/bin/activate"
fi

# 检查依赖文件
if [ ! -f "requirements.txt" ]; then
    echo "❌ Error: requirements.txt 文件不存在"
    exit 1
fi

# 安装依赖包
echo "📦 安装依赖包..."
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "❌ Error: 依赖包安装失败"
    exit 1
fi

# 检查环境配置文件
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        echo "⚠️  .env 文件不存在，请复制 .env.example 为 .env 并配置相关参数"
        echo "cp .env.example .env"
        echo "然后编辑 .env 文件配置数据库连接等信息"
    else
        echo "⚠️  请创建 .env 文件并配置环境变量"
    fi
fi

# 检查主程序文件
if [ ! -f "main.py" ]; then
    echo "❌ Error: main.py 文件不存在"
    exit 1
fi

# 启动应用
echo "🎯 启动应用..."
echo "访问地址："
echo "  - 主页: http://localhost:8000"
echo "  - API文档: http://localhost:8000/docs"
echo "  - ReDoc文档: http://localhost:8000/redoc"
echo "  - 健康检查: http://localhost:8000/health"
echo ""

# 使用uvicorn启动
python3 -m uvicorn main:app --host 0.0.0.0 --port 8000 --reload