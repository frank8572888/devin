#!/usr/bin/env python3
"""
OpenDevin 依赖修复脚本
解决Windows上运行opendevin/core/main.py的依赖问题
"""

import subprocess
import sys
import os

def install_package(package):
    """安装Python包"""
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ 成功安装: {package}")
        return True
    except subprocess.CalledProcessError:
        print(f"❌ 安装失败: {package}")
        return False

def check_import(module_name, package_name=None):
    """检查模块是否可以导入"""
    try:
        __import__(module_name)
        print(f"✅ {module_name} 可以导入")
        return True
    except ImportError:
        print(f"❌ {module_name} 无法导入")
        if package_name:
            print(f"   正在安装 {package_name}...")
            return install_package(package_name)
        return False

def main():
    print("🔧 OpenDevin 依赖修复工具")
    print("=" * 50)
    
    # 必需的依赖列表
    dependencies = [
        ("dotenv", "python-dotenv"),
        ("litellm", "litellm"),
        ("tenacity", "tenacity"),
        ("toml", "toml"),
        ("termcolor", "termcolor"),
        ("pandas", "pandas"),
        ("datasets", "datasets"),
        ("docker", "docker"),
        ("json_repair", "json-repair"),
        ("seaborn", "seaborn"),
        ("docx", "python-docx"),
        ("PyPDF2", "PyPDF2"),
        ("pylatexenc", "pylatexenc"),
        ("pptx", "python-pptx"),
    ]
    
    # Windows特殊处理的依赖
    windows_dependencies = [
        ("pexpect", "pexpect"),  # 在Windows上可能有问题
    ]
    
    print("检查基础依赖...")
    failed_deps = []
    
    for module, package in dependencies:
        if not check_import(module, package):
            failed_deps.append((module, package))
    
    # 特殊处理pexpect（Windows上可能有问题）
    print("\n检查Windows特殊依赖...")
    if os.name == 'nt':  # Windows
        print("检测到Windows系统，尝试安装Windows兼容的pexpect...")
        try:
            # 先尝试安装pexpect
            install_package("pexpect")
            # 如果还是有问题，尝试安装wexpect作为替代
            if not check_import("pexpect"):
                print("pexpect在Windows上有问题，尝试安装wexpect...")
                install_package("wexpect")
        except:
            print("⚠️ pexpect安装有问题，但可能不影响基本功能")
    else:
        check_import("pexpect", "pexpect")
    
    # 检查其他可能需要的依赖
    optional_deps = [
        ("fastapi", "fastapi"),
        ("uvicorn", "uvicorn"),
        ("websockets", "websockets"),
    ]
    
    print("\n检查可选依赖...")
    for module, package in optional_deps:
        check_import(module, package)
    
    print("\n" + "=" * 50)
    if failed_deps:
        print("❌ 以下依赖安装失败:")
        for module, package in failed_deps:
            print(f"   - {module} ({package})")
        print("\n请手动安装这些依赖:")
        for module, package in failed_deps:
            print(f"   pip install {package}")
    else:
        print("✅ 所有依赖检查完成！")
    
    print("\n🚀 现在尝试运行 opendevin/core/main.py --help")
    
    # 尝试运行main.py
    try:
        result = subprocess.run([
            sys.executable, "opendevin/core/main.py", "--help"
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ opendevin/core/main.py 可以正常运行！")
            print("\n使用方法:")
            print(result.stdout)
        else:
            print("❌ opendevin/core/main.py 运行失败")
            print("错误信息:")
            print(result.stderr)
            
            # 尝试提供解决方案
            if "pexpect" in result.stderr:
                print("\n💡 解决方案:")
                print("pexpect在Windows上有兼容性问题，你可以:")
                print("1. 使用我们提供的简化运行器: python run_simple.py")
                print("2. 或者使用Docker模式运行OpenDevin")
            
    except subprocess.TimeoutExpired:
        print("⚠️ 运行超时，可能还有其他问题")
    except Exception as e:
        print(f"❌ 运行出错: {e}")

if __name__ == "__main__":
    main()