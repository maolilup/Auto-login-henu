@echo off
REM 安装Windows任务计划程序 - 开机自动登录
REM 需要管理员权限运行

setlocal enabledelayedexpansion

REM 检查管理员权限
net session >nul 2>&1
if errorlevel 1 (
    echo 错误: 需要管理员权限运行此脚本
    echo 请右键点击此脚本，选择"以管理员身份运行"
    pause
    exit /b 1
)

echo ========================================
echo 河南大学校园网自动登录 - 服务安装
echo ========================================
echo.

REM 获取当前目录
cd /d "%~dp0"
cd ..\..
set SCRIPT_DIR=%CD%

REM 设置任务名称
set TASK_NAME=HENUAutoLogin

REM 检查任务是否已存在
schtasks /query /tn "%TASK_NAME%" >nul 2>&1
if not errorlevel 1 (
    echo 任务 "%TASK_NAME%" 已存在
    set /p CHOICE="是否删除并重新创建？(Y/N): "
    if /i "!CHOICE!"=="Y" (
        schtasks /delete /tn "%TASK_NAME%" /f >nul 2>&1
        echo 已删除旧任务
    ) else (
        echo 安装取消
        pause
        exit /b 0
    )
)

REM 创建任务计划XML
set TASK_XML=%TEMP%\henu_login_task.xml

echo ^<?xml version="1.0" encoding="UTF-16"?^> > "%TASK_XML%"
echo ^<Task version="1.2" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task"^> >> "%TASK_XML%"
echo   ^<RegistrationInfo^> >> "%TASK_XML%"
echo     ^<Description^>河南大学校园网自动登录服务^</Description^> >> "%TASK_XML%"
echo   ^</RegistrationInfo^> >> "%TASK_XML%"
echo   ^<Triggers^> >> "%TASK_XML%"
echo     ^<LogonTrigger^> >> "%TASK_XML%"
echo       ^<Enabled^>true^</Enabled^> >> "%TASK_XML%"
echo     ^</LogonTrigger^> >> "%TASK_XML%"
echo     ^<TimeTrigger^> >> "%TASK_XML%"
echo       ^<Repetition^> >> "%TASK_XML%"
echo         ^<Interval^>PT5M^</Interval^> >> "%TASK_XML%"
echo       ^</Repetition^> >> "%TASK_XML%"
echo       ^<Enabled^>true^</Enabled^> >> "%TASK_XML%"
echo     ^</TimeTrigger^> >> "%TASK_XML%"
echo   ^</Triggers^> >> "%TASK_XML%"
echo   ^<Principals^> >> "%TASK_XML%"
echo     ^<Principal^> >> "%TASK_XML%"
echo       ^<LogonType^>InteractiveToken^</LogonType^> >> "%TASK_XML%"
echo       ^<RunLevel^>LeastPrivilege^</RunLevel^> >> "%TASK_XML%"
echo     ^</Principal^> >> "%TASK_XML%"
echo   ^</Principals^> >> "%TASK_XML%"
echo   ^<Settings^> >> "%TASK_XML%"
echo     ^<MultipleInstancesPolicy^>IgnoreNew^</MultipleInstancesPolicy^> >> "%TASK_XML%"
echo     ^<DisallowStartIfOnBatteries^>false^</DisallowStartIfOnBatteries^> >> "%TASK_XML%"
echo     ^<StopIfGoingOnBatteries^>false^</StopIfGoingOnBatteries^> >> "%TASK_XML%"
echo     ^<AllowHardTerminate^>true^</AllowHardTerminate^> >> "%TASK_XML%"
echo     ^<StartWhenAvailable^>true^</StartWhenAvailable^> >> "%TASK_XML%"
echo     ^<RunOnlyIfNetworkAvailable^>false^</RunOnlyIfNetworkAvailable^> >> "%TASK_XML%"
echo     ^<AllowStartOnDemand^>true^</AllowStartOnDemand^> >> "%TASK_XML%"
echo     ^<Enabled^>true^</Enabled^> >> "%TASK_XML%"
echo     ^<Hidden^>false^</Hidden^> >> "%TASK_XML%"
echo     ^<ExecutionTimeLimit^>PT1H^</ExecutionTimeLimit^> >> "%TASK_XML%"
echo   ^</Settings^> >> "%TASK_XML%"
echo   ^<Actions^> >> "%TASK_XML%"
echo     ^<Exec^> >> "%TASK_XML%"
echo       ^<Command^>python^</Command^> >> "%TASK_XML%"
echo       ^<Arguments^>auto_login_enhanced.py^</Arguments^> >> "%TASK_XML%"
echo       ^<WorkingDirectory^>%SCRIPT_DIR%^</WorkingDirectory^> >> "%TASK_XML%"
echo     ^</Exec^> >> "%TASK_XML%"
echo   ^</Actions^> >> "%TASK_XML%"
echo ^</Task^> >> "%TASK_XML%"

REM 创建任务
echo 正在创建任务计划...
schtasks /create /tn "%TASK_NAME%" /xml "%TASK_XML%" /f

if errorlevel 1 (
    echo.
    echo 错误: 任务创建失败
    del "%TASK_XML%" >nul 2>&1
    pause
    exit /b 1
)

REM 清理临时文件
del "%TASK_XML%" >nul 2>&1

echo.
echo ========================================
echo 安装成功！
echo ========================================
echo.
echo 任务名称: %TASK_NAME%
echo 触发条件: 
echo   - 用户登录时
echo   - 每5分钟检查一次
echo.
echo 您可以在"任务计划程序"中查看和管理此任务
echo.
echo 立即运行任务测试：
schtasks /run /tn "%TASK_NAME%"
echo.

pause
endlocal
