"""
测试主窗口

验证主窗口可以正常创建和初始化
"""

import sys
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from models import Schedule, Config
from storage.json_storage import JSONStorage
from ui.main_window import MainWindow
from PyQt6.QtWidgets import QApplication


def test_main_window_creation():
    """测试主窗口创建"""
    print("测试主窗口创建...")
    
    # 创建应用程序（必须先创建）
    app = QApplication(sys.argv)
    
    # 创建主窗口
    window = MainWindow()
    
    # 验证窗口属性
    assert window.windowTitle() == "WakeUp 课表"
    assert window.schedule is not None
    assert window.config is not None
    assert window.schedule_manager is not None
    assert window.course_manager is not None
    assert window.week_calculator is not None
    
    print("✓ 主窗口创建成功")
    print(f"  - 窗口标题: {window.windowTitle()}")
    print(f"  - 课表对象: {window.schedule}")
    print(f"  - 配置对象: {window.config}")
    print(f"  - 课程数量: {len(window.schedule.course_bases)}")
    
    # 验证菜单栏
    menubar = window.menuBar()
    assert menubar is not None
    menus = menubar.actions()
    assert len(menus) >= 5  # 文件、编辑、导入、设置、帮助
    print(f"  - 菜单数量: {len(menus)}")
    
    # 验证工具栏
    toolbars = window.findChildren(type(window.addToolBar("test")))
    assert len(toolbars) >= 1
    print(f"  - 工具栏数量: {len(toolbars)}")
    
    # 验证状态栏
    statusbar = window.statusBar
    assert statusbar is not None
    print(f"  - 状态栏: 已创建")
    
    # 验证课表视图
    assert window.schedule_view is not None
    print(f"  - 课表视图: 已创建")
    print(f"  - 显示周次: 第 {window.display_week} 周")
    
    # 验证周次选择器
    assert hasattr(window, 'week_selector'), "周次选择器未创建"
    assert window.week_selector is not None
    print(f"  - 周次选择器: 已创建")
    print(f"  - 选择器周次: 第 {window.week_selector.get_week()} 周")
    
    # 验证课表视图的表格 (ScheduleView itself is the table)
    assert window.schedule_view.columnCount() == 8  # 时间 + 7天
    assert window.schedule_view.rowCount() == len(window.config.time_slots)
    print(f"  - 表格大小: {window.schedule_view.rowCount()} 行 x {window.schedule_view.columnCount()} 列")
    
    print("\n所有测试通过！✓")
    
    # 不显示窗口，直接退出
    return True


if __name__ == "__main__":
    try:
        test_main_window_creation()
    except Exception as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)