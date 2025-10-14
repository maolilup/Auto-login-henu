@echo off
REM 河南大学校园网自动登录脚本 - Windows版本
REM 使用方法：双击运行或通过命令行运行

setlocal enabledelayedexpansion

REM 获取脚本所在目录
cd /d "%~dp0"
cd ..\..

REM 设置Python可执行文件路径
set PYTHON=python

REM 检查Python是否安装
%PYTHON% --version >nul 2>&1
if errorlevel 1 (
    echo 错误: 未找到Python，请先安装Python 3.7或更高版本
    pause
    exit /b 1
)

REM 检查依赖是否安装
echo 检查依赖...
%PYTHON% -c "import requests" >nul 2>&1
if errorlevel 1 (
    echo 正在安装依赖...
    %PYTHON% -m pip install -r requirements.txt
    if errorlevel 1 (
        echo 错误: 依赖安装失败
        pause
        exit /b 1
    )
)

REM 检查配置文件
if not exist "config.json" (
    if exist "config.json.example" (
        echo 警告: 未找到config.json，请从config.json.example复制并配置
        echo 正在复制config.json.example到config.json...
        copy config.json.example config.json >nul
        echo 请编辑config.json文件，填入您的账号信息
        notepad config.json
        echo 配置完成后按任意键继续...
        pause >nul
    ) else (
        echo 错误: 未找到配置文件
        pause
        exit /b 1
    )
)

REM 运行自动登录程序
echo 正在启动自动登录...
%PYTHON% auto_login_enhanced.py %*

REM 如果是双击运行，等待用户查看结果
if "%~1"=="" (
    echo.
    echo 按任意键退出...
    pause >nul
)

endlocal
