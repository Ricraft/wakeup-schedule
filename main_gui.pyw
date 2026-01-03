"""
WakeUp Schedule - GUI 启动入口（无控制台窗口）

使用 .pyw 扩展名或 pythonw.exe 运行时不会显示控制台
"""
import sys
import os

# 重定向 stdout/stderr 防止无控制台时报错
if sys.stdout is None:
    sys.stdout = open(os.devnull, 'w')
if sys.stderr is None:
    sys.stderr = open(os.devnull, 'w')

# 导入并运行主程序
from main import main

if __name__ == "__main__":
    main()
