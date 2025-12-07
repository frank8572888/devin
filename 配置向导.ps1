# OpenDevin 配置向导
# 帮助用户快速配置OpenDevin环境

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
function Write-Title($message) { Write-ColorOutput Magenta "🎯 $message" }

# 显示欢迎信息
Clear-Host
Write-Host ""
Write-Title "OpenDevin AI Agent 配置向导"
Write-Host "================================" -ForegroundColor Magenta
Write-Host ""
Write-Host "这个向导将帮助你快速配置OpenDevin环境" -ForegroundColor Gray
Write-Host ""

# 步骤1: 检查系统要求
Write-Title "步骤 1/4: 检查系统要求"
Write-Host ""

# 检查PowerShell版本
$psVersion = $PSVersionTable.PSVersion
if ($psVersion.Major -ge 5) {
    Write-Success "PowerShell版本: $psVersion"
} else {
    Write-Warning "PowerShell版本较低: $psVersion (建议5.0+)"
}

# 检查Docker
Write-Info "检查Docker..."
try {
    $dockerVersion = docker --version 2>&1
    Write-Success "Docker已安装: $dockerVersion"
    
    # 检查Docker是否运行
    try {
        docker info | Out-Null
        Write-Success "Docker服务正在运行"
    } catch {
        Write-Warning "Docker已安装但未运行，请启动Docker Desktop"
    }
} catch {
    Write-Error "Docker未安装"
    Write-Host ""
    Write-Host "请先安装Docker Desktop:" -ForegroundColor Yellow
    Write-Host "https://www.docker.com/products/docker-desktop/" -ForegroundColor Blue
    Write-Host ""
    $continue = Read-Host "是否继续配置其他选项? (y/N)"
    if ($continue -notmatch '^[Yy]') {
        exit 1
    }
}

Write-Host ""
Read-Host "按回车继续到下一步"

# 步骤2: 配置API密钥
Clear-Host
Write-Title "步骤 2/4: 配置DeepSeek API"
Write-Host ""

Write-Host "OpenDevin需要DeepSeek API来运行AI功能" -ForegroundColor Gray
Write-Host ""

# 检查现有API密钥
if ($env:LLM_API_KEY) {
    Write-Success "检测到现有API密钥: $($env:LLM_API_KEY.Substring(0, [Math]::Min(10, $env:LLM_API_KEY.Length)))..."
    $useExisting = Read-Host "是否使用现有密钥? (Y/n)"
    if ($useExisting -match '^[Nn]') {
        $env:LLM_API_KEY = $null
    }
}

if (-not $env:LLM_API_KEY) {
    Write-Host "请输入你的DeepSeek API密钥:" -ForegroundColor Yellow
    Write-Host "如果没有API密钥，请访问: https://platform.deepseek.com/" -ForegroundColor Blue
    Write-Host ""
    
    $apiKey = Read-Host "API密钥"
    
    if ($apiKey) {
        $env:LLM_API_KEY = $apiKey
        
        # 询问是否永久保存
        $savePermanent = Read-Host "是否将API密钥保存到系统环境变量? (Y/n)"
        if ($savePermanent -notmatch '^[Nn]') {
            try {
                [Environment]::SetEnvironmentVariable("LLM_API_KEY", $apiKey, "User")
                Write-Success "API密钥已保存到系统环境变量"
            } catch {
                Write-Warning "无法保存到系统环境变量，仅在当前会话有效"
            }
        }
        
        Write-Success "API密钥配置完成"
    } else {
        Write-Warning "未设置API密钥，稍后可以手动设置"
    }
}

Write-Host ""
Read-Host "按回车继续到下一步"

# 步骤3: 选择运行模式
Clear-Host
Write-Title "步骤 3/4: 选择运行模式"
Write-Host ""

Write-Host "OpenDevin支持多种运行模式:" -ForegroundColor Gray
Write-Host ""
Write-Host "1. Docker模式 (推荐)" -ForegroundColor Green
Write-Host "   - 最简单，开箱即用" -ForegroundColor Gray
Write-Host "   - 自动隔离，安全可靠" -ForegroundColor Gray
Write-Host "   - 需要Docker Desktop" -ForegroundColor Gray
Write-Host ""
Write-Host "2. 本地开发模式" -ForegroundColor Yellow
Write-Host "   - 可以修改源代码" -ForegroundColor Gray
Write-Host "   - 需要安装更多依赖" -ForegroundColor Gray
Write-Host "   - 适合开发者" -ForegroundColor Gray
Write-Host ""

$mode = Read-Host "请选择运行模式 (1/2)"

$selectedMode = "docker"
if ($mode -eq "2") {
    $selectedMode = "local"
    Write-Info "已选择本地开发模式"
    Write-Warning "本地模式需要安装Python 3.11+, Node.js 18+, Poetry等依赖"
} else {
    Write-Info "已选择Docker模式"
}

Write-Host ""
Read-Host "按回车继续到下一步"

# 步骤4: 创建启动脚本
Clear-Host
Write-Title "步骤 4/4: 创建启动脚本"
Write-Host ""

Write-Info "正在创建个性化启动脚本..."

# 创建工作目录
$workspaceDir = Join-Path $PWD "workspace"
if (-not (Test-Path $workspaceDir)) {
    New-Item -ItemType Directory -Path $workspaceDir -Force | Out-Null
    Write-Success "已创建工作目录: $workspaceDir"
}

if ($selectedMode -eq "docker") {
    # 创建Docker启动脚本
    $scriptContent = @"
# 个性化OpenDevin启动脚本
# 由配置向导自动生成

`$env:LLM_API_KEY = "$env:LLM_API_KEY"
`$env:LLM_MODEL = "deepseek-chat"
`$env:LLM_BASE_URL = "https://api.deepseek.com"

Write-Host "🚀 启动OpenDevin..." -ForegroundColor Cyan

`$workspaceDir = Join-Path `$PWD "workspace"
`$timestamp = Get-Date -Format "yyyyMMddHHmmss"

docker run -it ``
    --pull=always ``
    -e LLM_API_KEY=`$env:LLM_API_KEY ``
    -e LLM_MODEL=`$env:LLM_MODEL ``
    -e LLM_BASE_URL=`$env:LLM_BASE_URL ``
    -e WORKSPACE_MOUNT_PATH=`$workspaceDir ``
    -v "`${workspaceDir}:/opt/workspace_base" ``
    -v /var/run/docker.sock:/var/run/docker.sock ``
    -p 3000:3000 ``
    --add-host host.docker.internal:host-gateway ``
    --name opendevin-app-`$timestamp ``
    ghcr.io/opendevin/opendevin

Write-Host ""
Write-Host "🎉 OpenDevin已启动！访问: http://localhost:3000" -ForegroundColor Green
"@
    
    $scriptPath = "我的OpenDevin.ps1"
    $scriptContent | Out-File -FilePath $scriptPath -Encoding UTF8
    Write-Success "已创建启动脚本: $scriptPath"
    
} else {
    # 创建本地开发启动脚本
    $scriptContent = @"
# 本地开发模式启动脚本
# 由配置向导自动生成

`$env:LLM_API_KEY = "$env:LLM_API_KEY"
`$env:LLM_MODEL = "deepseek-chat"
`$env:LLM_BASE_URL = "https://api.deepseek.com"

Write-Host "🚀 启动OpenDevin (本地开发模式)..." -ForegroundColor Cyan

# 检查依赖
if (-not (Get-Command poetry -ErrorAction SilentlyContinue)) {
    Write-Error "Poetry未安装，请先安装: pip install poetry"
    exit 1
}

# 安装依赖
Write-Host "安装Python依赖..." -ForegroundColor Yellow
poetry install

# 安装前端依赖
Write-Host "安装前端依赖..." -ForegroundColor Yellow
Set-Location frontend
npm install
Set-Location ..

# 启动应用
Write-Host "启动应用..." -ForegroundColor Yellow
make run

Write-Host ""
Write-Host "🎉 OpenDevin已启动！访问: http://localhost:3000" -ForegroundColor Green
"@
    
    $scriptPath = "我的OpenDevin-本地.ps1"
    $scriptContent | Out-File -FilePath $scriptPath -Encoding UTF8
    Write-Success "已创建启动脚本: $scriptPath"
}

# 创建配置文件
if ($env:LLM_API_KEY) {
    $configContent = @"
[llm]
model = "deepseek-chat"
api_key = "$env:LLM_API_KEY"
base_url = "https://api.deepseek.com"
temperature = 0.1
max_output_tokens = 4000

[core]
workspace_base = "./workspace"
sandbox_type = "docker"

[agent]
default_agent = "CodeActAgent"
"@
    
    $configContent | Out-File -FilePath "config.toml" -Encoding UTF8
    Write-Success "已创建配置文件: config.toml"
}

Write-Host ""
Write-Success "配置完成！"
Write-Host ""
Write-Info "下一步:"
Write-Host "1. 运行启动脚本: .\$scriptPath" -ForegroundColor Gray
Write-Host "2. 在浏览器中访问: http://localhost:3000" -ForegroundColor Gray
Write-Host "3. 开始与AI助手对话！" -ForegroundColor Gray
Write-Host ""

# 询问是否立即启动
$startNow = Read-Host "是否现在就启动OpenDevin? (Y/n)"
if ($startNow -notmatch '^[Nn]') {
    Write-Host ""
    Write-Info "正在启动OpenDevin..."
    & ".\$scriptPath"
}

Write-Host ""
Write-Host "感谢使用OpenDevin配置向导！" -ForegroundColor Cyan
Write-Host "如有问题，请查看: 本地运行指南.md" -ForegroundColor Gray