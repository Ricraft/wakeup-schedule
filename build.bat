@echo off
chcp 65001 >nul
echo ========================================
echo   WakeUp Schedule 打包脚本
echo   版本: v2.5.0
echo ========================================
echo.

:: 检查 PyInstaller
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo [!] 正在安装 PyInstaller...
    pip install pyinstaller
)

:: 清理旧的构建文件
echo [1/3] 清理旧文件...
if exist "dist" rmdir /s /q dist
if exist "build" rmdir /s /q build

:: 开始打包
echo [2/3] 开始打包...
pyinstaller build.spec --noconfirm

:: 复制必要文件到输出目录
echo [3/3] 复制配置文件...
if exist "dist\WakeUpSchedule.exe" (
    :: 创建 logs 目录
    if not exist "dist\logs" mkdir "dist\logs"
    
    :: 复制配置文件（如果存在）
    if exist "config.json" copy /y "config.json" "dist\" >nul
    
    echo.
    echo ========================================
    echo   打包完成！
    echo   输出文件: dist\WakeUpSchedule.exe
    echo ========================================
) else (
    echo.
    echo [错误] 打包失败，请检查错误信息
)

pause
