@echo off
chcp 65001 >nul
echo ========================================
echo    OpenDevin AI Agent 一键启动脚本
echo ========================================
echo.

REM 检查是否设置了API密钥
if "%LLM_API_KEY%"=="" (
    echo ❌ 错误: 未设置DeepSeek API密钥
    echo.
    echo 请先设置环境变量:
    echo set LLM_API_KEY=your-deepseek-api-key-here
    echo.
    echo 或者编辑这个脚本文件，在下面设置你的API密钥:
    pause
    exit /b 1
)

REM 如果你想直接在脚本中设置API密钥，取消下面这行的注释并填入你的密钥
REM set LLM_API_KEY=your-deepseek-api-key-here

REM 设置其他环境变量
set LLM_MODEL=deepseek-chat
set LLM_BASE_URL=https://api.deepseek.com

REM 检查Docker是否运行
echo 🔍 检查Docker状态...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker未安装或未运行
    echo 请先安装并启动Docker Desktop
    pause
    exit /b 1
)

echo ✅ Docker已就绪

REM 创建工作目录
if not exist "workspace" mkdir workspace

REM 获取当前目录的workspace路径
for %%i in ("%cd%") do set "CURRENT_DIR=%%i"
set "WORKSPACE_BASE=%CURRENT_DIR%\workspace"

echo 📁 工作目录: %WORKSPACE_BASE%
echo 🤖 模型: %LLM_MODEL%
echo 🌐 API地址: %LLM_BASE_URL%
echo.

echo 🚀 正在启动OpenDevin...
echo 请稍等，首次运行需要下载Docker镜像...
echo.

REM 运行OpenDevin Docker容器
docker run -it ^
    --pull=always ^
    -e LLM_API_KEY=%LLM_API_KEY% ^
    -e LLM_MODEL=%LLM_MODEL% ^
    -e LLM_BASE_URL=%LLM_BASE_URL% ^
    -e WORKSPACE_MOUNT_PATH=%WORKSPACE_BASE% ^
    -v "%WORKSPACE_BASE%:/opt/workspace_base" ^
    -v /var/run/docker.sock:/var/run/docker.sock ^
    -p 3000:3000 ^
    --add-host host.docker.internal:host-gateway ^
    --name opendevin-app-%date:~0,4%%date:~5,2%%date:~8,2%-%time:~0,2%%time:~3,2%%time:~6,2% ^
    ghcr.io/opendevin/opendevin

echo.
echo 🎉 OpenDevin已启动！
echo 📱 请在浏览器中访问: http://localhost:3000
echo 📁 AI生成的文件将保存在: %WORKSPACE_BASE%
echo.
pause