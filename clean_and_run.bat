@echo off
echo ========================================
echo 清理 Python 缓存并启动程序
echo ========================================
echo.

echo 正在清理 __pycache__ 目录...
for /d /r . %%d in (__pycache__) do @if exist "%%d" rd /s /q "%%d"

echo 正在清理 .pyc 文件...
del /s /q *.pyc 2>nul

echo.
echo 缓存清理完成！
echo.
echo 正在启动程序（使用修复版）...
echo.

python main.py

pause
