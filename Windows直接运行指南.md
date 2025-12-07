# OpenDevin Windows 直接运行指南

## 🎯 问题解决

你想直接运行 `opendevin/core/main.py`，但遇到了依赖问题。我已经为你创建了解决方案！

## 🚀 解决方案

### 方法1: 使用简化版main.py（推荐）

我创建了 `main_simple.py`，这是一个简化版本，跳过了复杂的运行时依赖，专注于核心LLM功能。

#### 快速开始

1. **安装基础依赖**：
   ```bash
   pip install litellm python-dotenv toml tenacity termcolor
   ```

2. **设置API密钥**：
   ```bash
   # Windows CMD
   set LLM_API_KEY=your-deepseek-api-key

   # Windows PowerShell
   $env:LLM_API_KEY = "your-deepseek-api-key"
   ```

3. **运行任务**：
   ```bash
   # 基本使用
   python main_simple.py -t "创建一个Python计算器"

   # 指定API密钥
   python main_simple.py -t "创建一个Web应用" --api-key "your-api-key"

   # 指定工作目录
   python main_simple.py -t "分析这个项目" -d "C:\my_project"

   # 从文件读取任务
   echo "创建一个待办事项应用" > task.txt
   python main_simple.py -f task.txt
   ```

#### 完整参数说明

```bash
python main_simple.py [选项]

选项:
  -t, --task           任务描述
  -f, --file           从文件读取任务
  -m, --model-name     模型名称 (默认: deepseek-chat)
  --api-key            API密钥
  --base-url           API地址 (默认: https://api.deepseek.com)
  -d, --directory      工作目录 (默认: ./workspace)
  --temperature        温度参数 (默认: 0.1)
  --debug              启用调试模式
```

### 方法2: 修复原版main.py的依赖

如果你坚持要运行原版的 `opendevin/core/main.py`，可以使用我创建的修复脚本：

1. **运行依赖修复脚本**：
   ```bash
   python 修复依赖.py
   ```

2. **手动安装缺失的依赖**：
   ```bash
   pip install e2b pexpect fastapi uvicorn websockets
   ```

3. **尝试运行原版**：
   ```bash
   python opendevin/core/main.py -t "你的任务"
   ```

## 📋 使用示例

### 代码生成
```bash
python main_simple.py -t "创建一个Python文件管理器，支持文件复制、移动、删除功能"
```

### 项目分析
```bash
python main_simple.py -t "分析当前目录的Python代码，找出可以优化的地方" -d "."
```

### Web应用开发
```bash
python main_simple.py -t "创建一个Flask Web应用，包含用户注册、登录、个人资料管理功能"
```

### 数据处理
```bash
python main_simple.py -t "创建一个数据分析脚本，读取CSV文件并生成可视化图表"
```

## 🔧 配置选项

### 环境变量配置
```bash
# Windows CMD
set LLM_API_KEY=your-deepseek-api-key
set LLM_MODEL=deepseek-chat
set LLM_BASE_URL=https://api.deepseek.com

# Windows PowerShell
$env:LLM_API_KEY = "your-deepseek-api-key"
$env:LLM_MODEL = "deepseek-chat"
$env:LLM_BASE_URL = "https://api.deepseek.com"
```

### 配置文件
创建 `config.toml` 文件：
```toml
[llm]
model = "deepseek-chat"
api_key = "your-api-key-here"
base_url = "https://api.deepseek.com"
temperature = 0.1
max_output_tokens = 4000
```

## 🛠️ 故障排除

### 常见问题

1. **"模块未找到"错误**
   ```bash
   # 安装缺失的模块
   pip install 模块名
   
   # 或运行修复脚本
   python 修复依赖.py
   ```

2. **"API密钥错误"**
   - 检查DeepSeek API密钥是否正确
   - 确认环境变量已设置
   - 尝试使用 `--api-key` 参数直接指定

3. **"网络连接错误"**
   - 检查网络连接
   - 确认能访问 https://api.deepseek.com
   - 检查防火墙设置

4. **"权限错误"**
   - 确保有写入工作目录的权限
   - 尝试使用管理员权限运行

### 调试模式
```bash
# 启用调试模式查看详细错误信息
python main_simple.py -t "你的任务" --debug
```

## 💡 优势对比

| 特性 | main_simple.py | 原版main.py |
|------|----------------|-------------|
| 依赖复杂度 | 低 | 高 |
| 启动速度 | 快 | 慢 |
| Windows兼容性 | 优秀 | 一般 |
| 功能完整性 | 核心功能 | 完整功能 |
| 适用场景 | 日常使用 | 高级开发 |

## 🎉 开始使用

现在你可以直接在Windows上运行OpenDevin的核心功能了！

```bash
# 第一次使用
python main_simple.py -t "创建一个Hello World程序" --api-key "your-api-key"

# 后续使用（已设置环境变量）
python main_simple.py -t "帮我写一个数据库连接工具"
```

AI会自动：
- 分析你的需求
- 生成完整的代码
- 创建必要的文件
- 提供使用说明

就像有一个专业的程序员在帮你工作一样！🚀