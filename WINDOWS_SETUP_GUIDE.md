# Windows 运行指南 - 直接运行 core/main.py

本指南将帮助你在Windows上直接运行OpenDevin的core/main.py，使用DeepSeek API。

## 前置要求

### 1. 安装必要软件
- **Python 3.11**: 从 [python.org](https://www.python.org/downloads/) 下载安装
- **Docker Desktop**: 从 [docker.com](https://www.docker.com/products/docker-desktop/) 下载安装
- **Git**: 从 [git-scm.com](https://git-scm.com/download/win) 下载安装
- **Poetry**: 安装Python包管理器

### 2. 安装Poetry
在PowerShell或命令提示符中运行：
```powershell
# 使用pip安装Poetry
pip install poetry

# 或者使用官方安装脚本
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

## 环境设置

### 1. 克隆并进入项目目录
```bash
git clone https://github.com/frank8572888/devin.git
cd devin
```

### 2. 安装Python依赖
```bash
# 安装项目依赖
poetry install

# 如果需要额外的功能，也可以安装可选依赖
poetry install --with llama-index,test,evaluation
```

### 3. 拉取Docker镜像
```bash
docker pull ghcr.io/opendevin/sandbox:main
```

## 配置DeepSeek API

### 方法1: 使用环境变量（推荐）
在PowerShell中设置环境变量：
```powershell
# 设置DeepSeek API配置
$env:LLM_MODEL = "deepseek-chat"
$env:LLM_API_KEY = "your-deepseek-api-key-here"
$env:LLM_BASE_URL = "https://api.deepseek.com"

# 可选：设置其他配置
$env:LLM_TEMPERATURE = "0.1"
$env:LLM_MAX_OUTPUT_TOKENS = "4000"
```

### 方法2: 创建config.toml文件
在项目根目录创建`config.toml`文件：
```toml
[llm]
model = "deepseek-chat"
api_key = "your-deepseek-api-key-here"
base_url = "https://api.deepseek.com"
temperature = 0.1
max_output_tokens = 4000

[core]
workspace_base = "./workspace"
max_iterations = 50

[sandbox]
box_type = "ssh"
timeout = 120
```

### 方法3: 使用命令行参数
直接在运行时指定模型：
```bash
poetry run python opendevin/core/main.py -m deepseek-chat -t "你的任务描述"
```

## 运行方式

### 🚀 方法1: 简化运行器（推荐，适合Windows）

我们提供了一个简化的运行脚本`run_simple.py`，避免了复杂的依赖问题：

```bash
# 基本运行
python run_simple.py -t "请帮我创建一个简单的Python计算器"

# 指定API密钥
python run_simple.py -t "创建一个Web应用" --api-key "your-deepseek-api-key"

# 指定工作目录
python run_simple.py -t "分析这个项目" -d "C:\your\project\path"

# 启用调试模式
python run_simple.py -t "修复代码bug" --debug
```

### 🔧 方法2: 完整版本（需要完整依赖）

如果你已经安装了所有依赖，可以使用完整版本：

```bash
# 激活Poetry环境并运行
poetry run python opendevin/core/main.py -t "请帮我创建一个简单的Python计算器"

# 从文件读取任务
echo "请帮我分析这个Python项目的结构，并生成一个README文件" > task.txt
poetry run python opendevin/core/main.py -f task.txt

# 完整参数示例
poetry run python opendevin/core/main.py \
  -t "创建一个Web应用" \
  -m "deepseek-chat" \
  -i 30 \
  -d "./workspace" \
  -c "CodeActAgent"
```

### 🎯 方法3: 使用批处理脚本

使用提供的Windows脚本：

```bash
# PowerShell脚本（推荐）
.\run_windows.ps1 -Task "创建一个Python计算器" -ApiKey "your-api-key"

# 批处理脚本
.\run_windows.bat "创建一个Python计算器"
```

## 参数说明

- `-t, --task`: 要执行的任务描述
- `-f, --file`: 包含任务的文件路径
- `-m, --model-name`: 使用的模型名称（如：deepseek-chat）
- `-d, --directory`: 工作目录路径
- `-c, --agent-cls`: 使用的代理类（默认：CodeActAgent）
- `-i, --max-iterations`: 最大迭代次数（默认：100）
- `-b, --max-budget-per-task`: 每个任务的最大预算
- `-l, --llm-config`: LLM配置组名

## 常见问题解决

### 1. Docker相关问题
如果遇到Docker权限问题：
```bash
# 确保Docker Desktop正在运行
# 在Docker Desktop设置中启用"Expose daemon on tcp://localhost:2375 without TLS"
```

### 2. 网络连接问题
如果无法连接到DeepSeek API：
```bash
# 检查网络连接
curl -I https://api.deepseek.com

# 如果需要代理，设置环境变量
$env:HTTP_PROXY = "http://your-proxy:port"
$env:HTTPS_PROXY = "http://your-proxy:port"
```

### 3. 依赖安装问题
如果Poetry安装依赖失败：
```bash
# 清理缓存重新安装
poetry cache clear pypi --all
poetry install --no-cache
```

### 4. 路径问题
Windows路径使用反斜杠，在命令行中可能需要转义：
```bash
# 使用正斜杠或双反斜杠
poetry run python opendevin/core/main.py -d "C:/workspace" -t "任务"
# 或
poetry run python opendevin/core/main.py -d "C:\\workspace" -t "任务"
```

## 调试模式

启用调试模式查看详细日志：
```bash
# 设置调试环境变量
$env:DEBUG = "1"
$env:LLM_DEBUG = "1"

# 运行程序
poetry run python opendevin/core/main.py -t "你的任务"
```

调试日志将保存在`logs/llm/`目录下。

## 示例使用场景

### 1. 代码分析
```bash
poetry run python opendevin/core/main.py -t "分析当前目录下的Python代码，找出潜在的bug和改进建议"
```

### 2. 文档生成
```bash
poetry run python opendevin/core/main.py -t "为这个项目生成完整的API文档"
```

### 3. 代码重构
```bash
poetry run python opendevin/core/main.py -t "重构main.py文件，提高代码可读性和性能"
```

## 注意事项

1. **API密钥安全**: 不要将API密钥提交到版本控制系统
2. **工作目录**: 确保指定的工作目录存在且有写入权限
3. **Docker要求**: 某些功能需要Docker运行，确保Docker Desktop已启动
4. **网络访问**: 确保能够访问DeepSeek API服务
5. **资源使用**: 长时间运行可能消耗较多API配额，注意监控使用量

## 获取帮助

如果遇到问题，可以：
1. 查看项目的GitHub Issues
2. 检查OpenDevin官方文档
3. 在项目目录运行 `poetry run python opendevin/core/main.py --help` 查看所有可用参数