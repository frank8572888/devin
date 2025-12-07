# OpenDevin Windows PowerShell 运行脚本
# 使用方法: .\run_windows.ps1 -Task "你的任务描述"

param(
    [Parameter(Mandatory=$true, HelpMessage="要执行的任务描述")]
    [string]$Task,
    
    [Parameter(HelpMessage="DeepSeek API密钥")]
    [string]$ApiKey = $env:LLM_API_KEY,
    
    [Parameter(HelpMessage="使用的模型名称")]
    [string]$Model = "deepseek-chat",
    
    [Parameter(HelpMessage="工作目录路径")]
    [string]$WorkspaceDir = "./workspace",
    
    [Parameter(HelpMessage="最大迭代次数")]
    [int]$MaxIterations = 50,
    
    [Parameter(HelpMessage="启用调试模式")]
    [switch]$Debug
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

function Write-Info($message) {
    Write-ColorOutput Cyan "ℹ️ $message"
}

function Write-Success($message) {
    Write-ColorOutput Green "✅ $message"
}

function Write-Warning($message) {
    Write-ColorOutput Yellow "⚠️ $message"
}

function Write-Error($message) {
    Write-ColorOutput Red "❌ $message"
}

# 显示标题
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "    OpenDevin Windows 运行脚本" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# 检查API密钥
if (-not $ApiKey) {
    Write-Error "未设置DeepSeek API密钥"
    Write-Info "请使用以下方式之一设置API密钥:"
    Write-Host "  1. 环境变量: `$env:LLM_API_KEY = 'your-api-key'" -ForegroundColor Gray
    Write-Host "  2. 参数传递: .\run_windows.ps1 -Task '任务' -ApiKey 'your-api-key'" -ForegroundColor Gray
    exit 1
}

# 设置环境变量
$env:LLM_MODEL = $Model
$env:LLM_API_KEY = $ApiKey
$env:LLM_BASE_URL = "https://api.deepseek.com"

if ($Debug) {
    $env:DEBUG = "1"
    $env:LLM_DEBUG = "1"
    Write-Info "调试模式已启用"
}

# 检查依赖
Write-Info "检查系统依赖..."

# 检查Python
try {
    $pythonVersion = python --version 2>&1
    if ($pythonVersion -match "Python 3\.11") {
        Write-Success "Python版本: $pythonVersion"
    } else {
        Write-Warning "Python版本: $pythonVersion (推荐使用Python 3.11)"
    }
} catch {
    Write-Error "Python未安装或不在PATH中"
    exit 1
}

# 检查Poetry
try {
    $poetryVersion = poetry --version 2>&1
    Write-Success "Poetry版本: $poetryVersion"
} catch {
    Write-Error "Poetry未安装或不在PATH中"
    Write-Info "请安装Poetry: pip install poetry"
    exit 1
}

# 检查Docker
try {
    $dockerVersion = docker --version 2>&1
    Write-Success "Docker版本: $dockerVersion"
} catch {
    Write-Warning "Docker未安装或未运行"
    Write-Info "某些功能可能无法正常工作，请确保Docker Desktop已启动"
}

# 创建工作目录
if (-not (Test-Path $WorkspaceDir)) {
    New-Item -ItemType Directory -Path $WorkspaceDir -Force | Out-Null
    Write-Info "已创建工作目录: $WorkspaceDir"
}

# 显示配置信息
Write-Host ""
Write-Info "运行配置:"
Write-Host "  模型: $Model" -ForegroundColor Gray
Write-Host "  API地址: https://api.deepseek.com" -ForegroundColor Gray
Write-Host "  任务: $Task" -ForegroundColor Gray
Write-Host "  工作目录: $(Resolve-Path $WorkspaceDir)" -ForegroundColor Gray
Write-Host "  最大迭代: $MaxIterations" -ForegroundColor Gray
Write-Host ""

# 确认运行
$confirmation = Read-Host "是否继续运行? (y/N)"
if ($confirmation -ne 'y' -and $confirmation -ne 'Y') {
    Write-Info "已取消运行"
    exit 0
}

Write-Info "正在启动OpenDevin..."
Write-Host "========================================" -ForegroundColor Cyan

# 构建命令
$command = "poetry run python opendevin/core/main.py"
$arguments = @(
    "-t", "`"$Task`""
    "-m", $Model
    "-d", $WorkspaceDir
    "-i", $MaxIterations
)

try {
    # 运行OpenDevin
    & $command @arguments
    
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Success "运行完成"
    
    # 显示工作目录内容
    if (Test-Path $WorkspaceDir) {
        Write-Info "工作目录内容:"
        Get-ChildItem $WorkspaceDir | Format-Table Name, Length, LastWriteTime -AutoSize
    }
    
} catch {
    Write-Error "运行失败: $($_.Exception.Message)"
    exit 1
}

# 询问是否查看日志
if ($Debug -and (Test-Path "logs")) {
    $viewLogs = Read-Host "是否查看调试日志? (y/N)"
    if ($viewLogs -eq 'y' -or $viewLogs -eq 'Y') {
        $latestLog = Get-ChildItem "logs" -Recurse -File | Sort-Object LastWriteTime -Descending | Select-Object -First 1
        if ($latestLog) {
            Write-Info "最新日志文件: $($latestLog.FullName)"
            Get-Content $latestLog.FullName | Select-Object -Last 50
        }
    }
}

Write-Host ""
Write-Info "感谢使用OpenDevin!"