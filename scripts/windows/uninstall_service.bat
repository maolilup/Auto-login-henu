@echo off
REM 卸载Windows任务计划程序
REM 需要管理员权限运行

setlocal

REM 检查管理员权限
net session >nul 2>&1
if errorlevel 1 (
    echo 错误: 需要管理员权限运行此脚本
    echo 请右键点击此脚本，选择"以管理员身份运行"
    pause
    exit /b 1
)

echo ========================================
echo 河南大学校园网自动登录 - 服务卸载
echo ========================================
echo.

set TASK_NAME=HENUAutoLogin

REM 检查任务是否存在
schtasks /query /tn "%TASK_NAME%" >nul 2>&1
if errorlevel 1 (
    echo 任务 "%TASK_NAME%" 不存在
    pause
    exit /b 0
)

REM 删除任务
echo 正在删除任务 "%TASK_NAME%"...
schtasks /delete /tn "%TASK_NAME%" /f

if errorlevel 1 (
    echo 错误: 任务删除失败
    pause
    exit /b 1
)

echo.
echo 任务已成功删除！
echo.
pause

endlocal
