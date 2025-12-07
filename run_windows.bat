@echo off
REM Windows批处理脚本 - 运行OpenDevin core/main.py
REM 使用方法: run_windows.bat "你的任务描述"

echo ========================================
echo OpenDevin Windows 运行脚本
echo ========================================

REM 检查是否提供了任务参数
if "%~1"=="" (
    echo 错误: 请提供任务描述
    echo 使用方法: run_windows.bat "你的任务描述"
    echo 示例: run_windows.bat "创建一个Python计算器"
    pause
    exit /b 1
)

REM 设置DeepSeek API配置（如果环境变量未设置）
if "%LLM_MODEL%"=="" set LLM_MODEL=deepseek-chat
if "%LLM_BASE_URL%"=="" set LLM_BASE_URL=https://api.deepseek.com

REM 检查API密钥
if "%LLM_API_KEY%"=="" (
    echo 警告: 未设置LLM_API_KEY环境变量
    echo 请设置你的DeepSeek API密钥:
    echo set LLM_API_KEY=your-api-key-here
    pause
    exit /b 1
)

REM 检查Poetry是否安装
poetry --version >nul 2>&1
if errorlevel 1 (
    echo 错误: Poetry未安装或不在PATH中
    echo 请先安装Poetry: pip install poetry
    pause
    exit /b 1
)

REM 检查Docker是否运行
docker version >nul 2>&1
if errorlevel 1 (
    echo 警告: Docker未运行或未安装
    echo 某些功能可能无法正常工作
    echo 请确保Docker Desktop已启动
)

REM 创建workspace目录（如果不存在）
if not exist "workspace" mkdir workspace

echo 配置信息:
echo - 模型: %LLM_MODEL%
echo - API地址: %LLM_BASE_URL%
echo - 任务: %~1
echo - 工作目录: %cd%\workspace
echo.

echo 正在启动OpenDevin...
echo ========================================

REM 运行OpenDevin
poetry run python opendevin/core/main.py -t "%~1" -m "%LLM_MODEL%" -d "./workspace"

echo ========================================
echo 运行完成
pause