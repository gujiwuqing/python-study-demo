#!/usr/bin/env python3
"""
FastAPI 后端管理系统启动脚本
"""
import os
import sys
import subprocess
import argparse


def check_python_version():
    """检查Python版本"""
    if sys.version_info < (3, 8):
        print("❌ Error: 需要 Python 3.8 或更高版本")
        print(f"当前版本: {sys.version}")
        sys.exit(1)
    print(f"✅ Python版本: {sys.version}")


def check_virtual_env():
    """检查虚拟环境"""
    if hasattr(sys, 'real_prefix') or (hasattr(sys, 'base_prefix') and sys.base_prefix != sys.prefix):
        print(f"✅ 检测到虚拟环境: {sys.prefix}")
        return True
    else:
        print("⚠️  警告: 建议使用虚拟环境")
        print("创建虚拟环境: python3 -m venv venv")
        print("激活虚拟环境: source venv/bin/activate  (Linux/Mac)")
        print("               venv\\Scripts\\activate     (Windows)")
        return False


def install_dependencies():
    """安装依赖包"""
    if not os.path.exists("requirements.txt"):
        print("❌ Error: requirements.txt 文件不存在")
        sys.exit(1)
    
    print("📦 安装依赖包...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True)
        print("✅ 依赖包安装成功")
    except subprocess.CalledProcessError:
        print("❌ Error: 依赖包安装失败")
        print("请手动执行: pip install -r requirements.txt")
        sys.exit(1)


def check_env_file():
    """检查环境配置文件"""
    if not os.path.exists(".env"):
        if os.path.exists(".env.example"):
            print("⚠️  .env 文件不存在")
            print("请复制 .env.example 为 .env 并配置相关参数:")
            print("cp .env.example .env")
            print("然后编辑 .env 文件配置数据库连接等信息")
        else:
            print("⚠️  请创建 .env 文件并配置环境变量")
        return False
    return True


def check_main_file():
    """检查主程序文件"""
    if not os.path.exists("main.py"):
        print("❌ Error: main.py 文件不存在")
        sys.exit(1)


def start_application(host="0.0.0.0", port=8000, reload=True, workers=1):
    """启动应用"""
    print("🎯 启动应用...")
    print("访问地址：")
    print(f"  - 主页: http://localhost:{port}")
    print(f"  - API文档 (Swagger): http://localhost:{port}/docs")
    print(f"  - ReDoc文档: http://localhost:{port}/redoc")
    print(f"  - 健康检查: http://localhost:{port}/health")
    print("")
    print("按 Ctrl+C 停止服务")
    print("-" * 50)
    
    try:
        if workers > 1:
            # 生产模式，使用多进程
            subprocess.run([
                sys.executable, "-m", "uvicorn", "main:app",
                "--host", host,
                "--port", str(port),
                "--workers", str(workers)
            ])
        else:
            # 开发模式
            subprocess.run([
                sys.executable, "-m", "uvicorn", "main:app",
                "--host", host,
                "--port", str(port),
                "--reload" if reload else "--no-reload"
            ])
    except KeyboardInterrupt:
        print("\n👋 应用已停止")
    except FileNotFoundError:
        print("❌ Error: uvicorn 未找到，请确保已安装 FastAPI 和 uvicorn")
        print("安装命令: pip install fastapi uvicorn")


def main():
    """主函数"""
    parser = argparse.ArgumentParser(description="FastAPI 后端管理系统启动脚本")
    parser.add_argument("--host", default="0.0.0.0", help="绑定主机地址 (默认: 0.0.0.0)")
    parser.add_argument("--port", type=int, default=8000, help="绑定端口 (默认: 8000)")
    parser.add_argument("--no-reload", action="store_true", help="禁用自动重载")
    parser.add_argument("--workers", type=int, default=1, help="工作进程数 (生产模式)")
    parser.add_argument("--skip-install", action="store_true", help="跳过依赖安装")
    parser.add_argument("--skip-checks", action="store_true", help="跳过环境检查")
    
    args = parser.parse_args()
    
    print("🚀 FastAPI 后端管理系统启动脚本")
    print("=" * 50)
    
    if not args.skip_checks:
        # 环境检查
        check_python_version()
        check_virtual_env()
        check_main_file()
        check_env_file()
    
    if not args.skip_install:
        # 安装依赖
        install_dependencies()
    
    # 启动应用
    start_application(
        host=args.host,
        port=args.port,
        reload=not args.no_reload,
        workers=args.workers
    )


if __name__ == "__main__":
    main()