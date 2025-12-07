# 🚀 Windows 快速开始指南

这是在Windows上快速运行OpenDevin core/main.py的最简指南。

## ⚡ 5分钟快速开始

### 1. 准备环境
```powershell
# 确保已安装Python 3.11和Poetry
python --version  # 应该显示Python 3.11.x
poetry --version  # 确认Poetry已安装
```

### 2. 安装基础依赖
```powershell
# 安装必要的Python包
pip install litellm fastapi python-dotenv

# 可选：如果要使用完整功能，安装所有依赖
poetry install
```

### 3. 配置DeepSeek API
```powershell
# 设置环境变量
$env:LLM_API_KEY = "your-deepseek-api-key-here"
```

### 4. 运行
```powershell
# 方式1: 简化运行器 (推荐，依赖最少)
python run_simple.py -t "创建一个Python计算器"

# 方式2: 使用PowerShell脚本
.\run_windows.ps1 -Task "创建一个Python计算器"

# 方式3: 完整版本 (需要所有依赖)
poetry run python opendevin/core/main.py -t "创建一个Python计算器"
```

## 📋 常用命令

### 基本使用
```powershell
# 简化运行器 (推荐)
python run_simple.py -t "分析当前目录的Python代码"
python run_simple.py -t "创建Web应用" -d "C:\my_project"
python run_simple.py -t "修复bug" --debug

# PowerShell脚本
.\run_windows.ps1 -Task "分析当前目录的Python代码"
.\run_windows.ps1 -Task "创建Web应用" -WorkspaceDir "C:\my_project"
.\run_windows.ps1 -Task "修复bug" -Debug
```

### 高级使用
```powershell
# 使用配置文件
copy config.deepseek.toml config.toml
# 编辑config.toml，填入你的API密钥
poetry run python opendevin/core/main.py -t "你的任务"

# 从文件读取任务
echo "创建一个待办事项应用" > task.txt
poetry run python opendevin/core/main.py -f task.txt
```

## 🔧 故障排除

### 常见问题
1. **"Poetry未找到"** → 运行 `pip install poetry`
2. **"Docker错误"** → 启动Docker Desktop
3. **"API密钥错误"** → 检查DeepSeek API密钥是否正确
4. **"权限错误"** → 以管理员身份运行PowerShell

### 获取帮助
```powershell
# 查看所有可用参数
poetry run python opendevin/core/main.py --help

# 查看PowerShell脚本帮助
Get-Help .\run_windows.ps1 -Full
```

## 📁 文件说明

- `run_windows.ps1` - PowerShell运行脚本 (推荐)
- `run_windows.bat` - 批处理运行脚本
- `config.deepseek.toml` - DeepSeek配置模板
- `WINDOWS_SETUP_GUIDE.md` - 详细设置指南

## 🎯 示例任务

```powershell
# 代码分析
.\run_windows.ps1 -Task "分析这个Python项目，找出可以改进的地方"

# 文档生成
.\run_windows.ps1 -Task "为这个项目生成README文档"

# 代码重构
.\run_windows.ps1 -Task "重构main.py，提高代码质量"

# 测试编写
.\run_windows.ps1 -Task "为现有代码编写单元测试"

# Bug修复
.\run_windows.ps1 -Task "修复代码中的潜在bug"
```

## 💡 提示

- 首次运行会下载Docker镜像，可能需要几分钟
- 工作目录默认为`./workspace`，所有生成的文件都在这里
- 使用`-Debug`参数可以查看详细的运行日志
- API调用会产生费用，注意监控使用量

开始你的AI编程之旅吧！🎉