"""
WakeUp Schedule - 唤醒你的校园时光
主入口文件

一款专为大学生打造的高颜值、现代化桌面课表管理工具
"""
import sys
import os
from pathlib import Path

# ========================================================
# 1. 核心路径配置
# ========================================================
if getattr(sys, 'frozen', False):
    # 打包后的 exe 运行
    project_root = Path(sys.executable).parent
else:
    # 开发环境运行
    project_root = Path(__file__).resolve().parent

if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

src_path = project_root / "src"
if str(src_path) not in sys.path:
    sys.path.insert(0, str(src_path))

# ========================================================
# 2. 初始化日志系统
# ========================================================
from src.utils.logger import logger, log_exception

# 设置全局异常处理
sys.excepthook = log_exception

logger.info("=" * 50)
logger.info("WakeUp Schedule 启动中...")
logger.info(f"运行目录: {project_root}")

# ========================================================
# 3. 导入主窗口
# ========================================================
try:
    from PyQt6.QtWidgets import QApplication
    from PyQt6.QtGui import QFont
    from src.ui.main_window import MainWindow
    logger.info("模块导入成功")
except ImportError as e:
    logger.critical(f"模块导入失败: {e}")
    sys.exit(1)


def main():
    """主函数"""
    try:
        # 创建应用程序实例
        app = QApplication(sys.argv)
        logger.info("QApplication 创建成功")

        # 设置全局字体
        font = QFont("Microsoft YaHei, Segoe UI, sans-serif")
        font.setPixelSize(13)
        app.setFont(font)

        # 初始化并显示主窗口
        window = MainWindow()
        window.show()
        logger.info("主窗口已显示")

        # 进入事件循环
        exit_code = app.exec()
        logger.info(f"程序正常退出，退出码: {exit_code}")
        sys.exit(exit_code)
        
    except Exception as e:
        logger.critical(f"程序运行异常: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
