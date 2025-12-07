# OpenDevin Windows 中文使用指南

这是OpenDevin项目的中文使用指南，专门为Windows用户和DeepSeek API用户优化。

## 🎯 项目简介

OpenDevin是一个基于AI的自主软件工程师平台，可以帮助你：
- 自动编写代码
- 分析和重构项目
- 生成文档
- 修复bug
- 创建完整的应用程序

## 🚀 快速开始（Windows）

### 1. 环境准备
- Python 3.11+
- Git
- DeepSeek API密钥

### 2. 克隆项目
```bash
git clone https://github.com/frank8572888/devin.git
cd devin
```

### 3. 安装依赖
```bash
# 最小依赖安装（推荐）
pip install litellm fastapi python-dotenv

# 或完整安装
pip install poetry
poetry install
```

### 4. 配置API
```powershell
# 设置DeepSeek API密钥
$env:LLM_API_KEY = "your-deepseek-api-key-here"
```

### 5. 开始使用
```bash
# 简化运行器（推荐）
python run_simple.py -t "创建一个Python计算器"

# PowerShell脚本
.\run_windows.ps1 -Task "创建一个Web应用"

# 完整版本
poetry run python opendevin/core/main.py -t "分析这个项目"
```

## 📁 文件说明

### 核心文件
- `opendevin/core/main.py` - 主程序入口
- `run_simple.py` - 简化运行器（推荐Windows用户使用）
- `run_windows.ps1` - PowerShell运行脚本
- `run_windows.bat` - 批处理运行脚本

### 配置文件
- `config.deepseek.toml` - DeepSeek配置模板
- `config.template.toml` - 通用配置模板

### 文档
- `QUICKSTART_WINDOWS.md` - 5分钟快速开始
- `WINDOWS_SETUP_GUIDE.md` - 详细Windows设置指南
- `README_CHINESE.md` - 本文件

## 🛠️ 运行方式对比

| 方式 | 优点 | 缺点 | 适用场景 |
|------|------|------|----------|
| `run_simple.py` | 依赖少，启动快 | 功能相对简单 | 日常使用，快速测试 |
| `run_windows.ps1` | 功能丰富，用户友好 | 需要PowerShell | Windows用户推荐 |
| `main.py` | 功能完整 | 依赖复杂 | 高级用户，完整功能 |

## 🎨 使用示例

### 代码生成
```bash
python run_simple.py -t "创建一个待办事项管理应用，包含添加、删除、标记完成功能"
```

### 代码分析
```bash
python run_simple.py -t "分析当前目录的Python代码，找出可以优化的地方"
```

### 文档生成
```bash
python run_simple.py -t "为这个项目生成详细的README文档"
```

### Bug修复
```bash
python run_simple.py -t "检查并修复代码中的潜在bug和安全问题"
```

## ⚙️ 配置选项

### 环境变量
```bash
LLM_API_KEY=your-deepseek-api-key    # DeepSeek API密钥
LLM_MODEL=deepseek-chat              # 使用的模型
LLM_BASE_URL=https://api.deepseek.com # API地址
DEBUG=1                              # 启用调试模式
```

### 配置文件
复制 `config.deepseek.toml` 为 `config.toml` 并修改：
```toml
[llm]
model = "deepseek-chat"
api_key = "your-api-key-here"
base_url = "https://api.deepseek.com"
temperature = 0.1
max_output_tokens = 4000
```

## 🔧 故障排除

### 常见问题

1. **"模块未找到"错误**
   ```bash
   pip install litellm fastapi python-dotenv
   ```

2. **"API密钥错误"**
   - 检查DeepSeek API密钥是否正确
   - 确认环境变量已设置

3. **"权限错误"**
   - 以管理员身份运行PowerShell
   - 检查文件权限

4. **"网络连接错误"**
   - 检查网络连接
   - 确认能访问 https://api.deepseek.com

### 获取帮助
```bash
# 查看帮助
python run_simple.py --help
.\run_windows.ps1 -Help

# 启用调试模式
python run_simple.py -t "你的任务" --debug
```

## 💡 最佳实践

1. **任务描述要具体**
   - ❌ "写个程序"
   - ✅ "创建一个Python计算器，支持加减乘除和括号运算"

2. **合理设置工作目录**
   ```bash
   python run_simple.py -t "任务" -d "C:\my_projects\calculator"
   ```

3. **使用调试模式排查问题**
   ```bash
   python run_simple.py -t "任务" --debug
   ```

4. **定期备份重要代码**
   - 生成的代码保存在workspace目录
   - 重要项目建议使用Git管理

## 🌟 高级功能

### 批量处理
```bash
# 创建任务文件
echo "任务1: 创建登录页面" > tasks.txt
echo "任务2: 创建用户管理" >> tasks.txt

# 批量执行（需要自己编写脚本）
```

### 自定义配置
```bash
# 使用自定义配置文件
python run_simple.py -t "任务" --config my_config.toml
```

## 📞 支持与反馈

- GitHub Issues: [项目Issues页面]
- 文档问题: 在本仓库提交Issue
- 功能建议: 欢迎提交Pull Request

## 📄 许可证

本项目基于MIT许可证开源。

---

**开始你的AI编程之旅吧！** 🚀

如果这个指南对你有帮助，请给项目一个⭐️！