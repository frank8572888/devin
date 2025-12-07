# OpenDevin AI Agent 一键启动脚本 (PowerShell版本)

param(
    [Parameter(HelpMessage="DeepSeek API密钥")]
    [string]$ApiKey,
    
    [Parameter(HelpMessage="使用的模型")]
    [string]$Model = "deepseek-chat",
    
    [Parameter(HelpMessage="端口号")]
    [int]$Port = 3000,
    
    [Parameter(HelpMessage="显示帮助")]
    [switch]$Help
)

# 颜色输出函数
function Write-ColorOutput($ForegroundColor) {
    $fc = $host.UI.RawUI.ForegroundColor
    $host.UI.RawUI.ForegroundColor = $ForegroundColor
    if ($args) {
        Write-Output $args
    } else {
        $input | Write-Output
    }
    $host.UI.RawUI.ForegroundColor = $fc
}

function Write-Info($message) { Write-ColorOutput Cyan "ℹ️ $message" }
function Write-Success($message) { Write-ColorOutput Green "✅ $message" }
function Write-Warning($message) { Write-ColorOutput Yellow "⚠️ $message" }
function Write-Error($message) { Write-ColorOutput Red "❌ $message" }

# 显示帮助
if ($Help) {
    Write-Host "OpenDevin AI Agent 启动脚本" -ForegroundColor Cyan
    Write-Host "================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "用法:"
    Write-Host "  .\启动OpenDevin.ps1 -ApiKey 'your-api-key'"
    Write-Host ""
    Write-Host "参数:"
    Write-Host "  -ApiKey    DeepSeek API密钥"
    Write-Host "  -Model     使用的模型 (默认: deepseek-chat)"
    Write-Host "  -Port      端口号 (默认: 3000)"
    Write-Host "  -Help      显示此帮助信息"
    Write-Host ""
    Write-Host "示例:"
    Write-Host "  .\启动OpenDevin.ps1 -ApiKey 'sk-xxx' -Port 3001"
    exit 0
}

# 显示欢迎信息
Write-Host ""
Write-Host "🤖 OpenDevin AI Agent 一键启动" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# 检查API密钥
if ($ApiKey) {
    $env:LLM_API_KEY = $ApiKey
    Write-Success "API密钥已设置"
} elseif ($env:LLM_API_KEY) {
    Write-Success "使用环境变量中的API密钥"
} else {
    Write-Error "未设置DeepSeek API密钥"
    Write-Host ""
    Write-Host "请使用以下方式之一设置API密钥:" -ForegroundColor Yellow
    Write-Host "1. 命令行参数: .\启动OpenDevin.ps1 -ApiKey 'your-api-key'" -ForegroundColor Gray
    Write-Host "2. 环境变量: `$env:LLM_API_KEY = 'your-api-key'" -ForegroundColor Gray
    Write-Host ""
    exit 1
}

# 设置环境变量
$env:LLM_MODEL = $Model
$env:LLM_BASE_URL = "https://api.deepseek.com"

# 检查Docker
Write-Info "检查Docker状态..."
try {
    $dockerVersion = docker --version 2>&1
    Write-Success "Docker已就绪: $dockerVersion"
} catch {
    Write-Error "Docker未安装或未运行"
    Write-Host ""
    Write-Host "请先安装并启动Docker Desktop:" -ForegroundColor Yellow
    Write-Host "https://www.docker.com/products/docker-desktop/" -ForegroundColor Gray
    Write-Host ""
    exit 1
}

# 创建工作目录
$workspaceDir = Join-Path $PWD "workspace"
if (-not (Test-Path $workspaceDir)) {
    New-Item -ItemType Directory -Path $workspaceDir -Force | Out-Null
    Write-Success "已创建工作目录: $workspaceDir"
} else {
    Write-Info "工作目录: $workspaceDir"
}

# 显示配置信息
Write-Host ""
Write-Info "启动配置:"
Write-Host "  🤖 模型: $Model" -ForegroundColor Gray
Write-Host "  🌐 API地址: https://api.deepseek.com" -ForegroundColor Gray
Write-Host "  📁 工作目录: $workspaceDir" -ForegroundColor Gray
Write-Host "  🌐 访问地址: http://localhost:$Port" -ForegroundColor Gray
Write-Host ""

# 检查端口是否被占用
$portInUse = Get-NetTCPConnection -LocalPort $Port -ErrorAction SilentlyContinue
if ($portInUse) {
    Write-Warning "端口 $Port 已被占用，将尝试使用其他端口"
    $Port = $Port + 1
    Write-Info "新端口: $Port"
}

# 生成容器名称
$timestamp = Get-Date -Format "yyyyMMddHHmmss"
$containerName = "opendevin-app-$timestamp"

Write-Info "正在启动OpenDevin..."
Write-Host "首次运行需要下载Docker镜像，请耐心等待..." -ForegroundColor Yellow
Write-Host ""

# 运行Docker容器
try {
    $dockerArgs = @(
        "run", "-it",
        "--pull=always",
        "-e", "LLM_API_KEY=$env:LLM_API_KEY",
        "-e", "LLM_MODEL=$env:LLM_MODEL", 
        "-e", "LLM_BASE_URL=$env:LLM_BASE_URL",
        "-e", "WORKSPACE_MOUNT_PATH=$workspaceDir",
        "-v", "${workspaceDir}:/opt/workspace_base",
        "-v", "/var/run/docker.sock:/var/run/docker.sock",
        "-p", "${Port}:3000",
        "--add-host", "host.docker.internal:host-gateway",
        "--name", $containerName,
        "ghcr.io/opendevin/opendevin"
    )
    
    & docker @dockerArgs
    
} catch {
    Write-Error "启动失败: $_"
    Write-Host ""
    Write-Host "可能的解决方案:" -ForegroundColor Yellow
    Write-Host "1. 确保Docker Desktop正在运行" -ForegroundColor Gray
    Write-Host "2. 检查网络连接" -ForegroundColor Gray
    Write-Host "3. 尝试重启Docker Desktop" -ForegroundColor Gray
    Write-Host ""
    exit 1
}

Write-Host ""
Write-Success "OpenDevin已启动！"
Write-Host ""
Write-Info "下一步:"
Write-Host "1. 在浏览器中访问: http://localhost:$Port" -ForegroundColor Gray
Write-Host "2. 开始与AI助手对话" -ForegroundColor Gray
Write-Host "3. AI生成的文件将保存在: $workspaceDir" -ForegroundColor Gray
Write-Host ""
Write-Host "按任意键退出..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")