# OpenDevin Windows 自动安装脚本
# 使用方法: .\install_windows.ps1

param(
    [Parameter(HelpMessage="跳过依赖检查")]
    [switch]$SkipCheck,
    
    [Parameter(HelpMessage="只安装最小依赖")]
    [switch]$MinimalInstall,
    
    [Parameter(HelpMessage="DeepSeek API密钥")]
    [string]$ApiKey
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

# 显示欢迎信息
Write-Host "🚀 OpenDevin Windows 安装脚本" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# 检查Python
if (-not $SkipCheck) {
    Write-Info "检查Python安装..."
    try {
        $pythonVersion = python --version 2>&1
        if ($pythonVersion -match "Python 3\.1[1-9]") {
            Write-Success "Python版本: $pythonVersion"
        } else {
            Write-Warning "Python版本: $pythonVersion (推荐Python 3.11+)"
        }
    } catch {
        Write-Error "Python未安装，请先安装Python 3.11+"
        Write-Info "下载地址: https://www.python.org/downloads/"
        exit 1
    }
}

# 安装依赖
Write-Info "安装Python依赖..."

if ($MinimalInstall) {
    Write-Info "安装最小依赖包..."
    $packages = @("litellm", "fastapi", "python-dotenv", "uvicorn", "toml")
} else {
    Write-Info "安装完整依赖包..."
    $packages = @(
        "litellm", "fastapi", "python-dotenv", "uvicorn", "toml",
        "pandas", "datasets", "docker", "json-repair", "tenacity",
        "termcolor", "seaborn", "python-docx", "PyPDF2", "pylatexenc",
        "python-pptx", "pexpect"
    )
}

foreach ($package in $packages) {
    try {
        Write-Host "  安装 $package..." -NoNewline
        pip install $package --quiet
        Write-Host " ✅" -ForegroundColor Green
    } catch {
        Write-Host " ❌" -ForegroundColor Red
        Write-Warning "安装 $package 失败，但可以继续"
    }
}

# 检查Poetry（可选）
if (-not $MinimalInstall) {
    Write-Info "检查Poetry..."
    try {
        $poetryVersion = poetry --version 2>&1
        Write-Success "Poetry已安装: $poetryVersion"
        
        Write-Info "使用Poetry安装项目依赖..."
        poetry install --quiet
        Write-Success "Poetry依赖安装完成"
    } catch {
        Write-Warning "Poetry未安装，跳过Poetry依赖安装"
        Write-Info "如需安装Poetry: pip install poetry"
    }
}

# 创建工作目录
Write-Info "创建工作目录..."
if (-not (Test-Path "workspace")) {
    New-Item -ItemType Directory -Path "workspace" -Force | Out-Null
    Write-Success "已创建workspace目录"
}

# 设置API密钥
if ($ApiKey) {
    Write-Info "设置API密钥..."
    [Environment]::SetEnvironmentVariable("LLM_API_KEY", $ApiKey, "User")
    $env:LLM_API_KEY = $ApiKey
    Write-Success "API密钥已设置"
} else {
    Write-Info "设置环境变量..."
    Write-Host "请设置你的DeepSeek API密钥:" -ForegroundColor Yellow
    Write-Host '  $env:LLM_API_KEY = "your-api-key-here"' -ForegroundColor Gray
    Write-Host "或者运行:" -ForegroundColor Yellow
    Write-Host '  .\install_windows.ps1 -ApiKey "your-api-key"' -ForegroundColor Gray
}

# 测试安装
Write-Info "测试安装..."
try {
    $testResult = python run_simple.py --help 2>&1
    if ($testResult -match "简化的OpenDevin运行器") {
        Write-Success "安装测试通过！"
    } else {
        Write-Warning "安装可能有问题，但基本功能应该可用"
    }
} catch {
    Write-Warning "无法测试安装，但基本依赖已安装"
}

# 显示使用说明
Write-Host ""
Write-Host "🎉 安装完成！" -ForegroundColor Green
Write-Host "===============" -ForegroundColor Green
Write-Host ""
Write-Info "快速开始:"
Write-Host '  python run_simple.py -t "创建一个Python计算器"' -ForegroundColor Gray
Write-Host ""
Write-Info "查看帮助:"
Write-Host '  python run_simple.py --help' -ForegroundColor Gray
Write-Host ""
Write-Info "更多信息:"
Write-Host "  - 快速指南: QUICKSTART_WINDOWS.md" -ForegroundColor Gray
Write-Host "  - 详细指南: WINDOWS_SETUP_GUIDE.md" -ForegroundColor Gray
Write-Host "  - 中文说明: README_CHINESE.md" -ForegroundColor Gray
Write-Host ""

if (-not $ApiKey) {
    Write-Warning "别忘了设置你的DeepSeek API密钥！"
}

Write-Host "开始你的AI编程之旅吧！🚀" -ForegroundColor Cyan