"""
测试设置对话框
"""

import sys
from pathlib import Path
from datetime import date

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from PyQt6.QtWidgets import QApplication
from ui.settings_dialog import SettingsDialog
from models.config import Config


def test_settings_dialog():
    """测试设置对话框"""
    print("\n测试设置对话框...")
    
    # 创建应用程序
    app = QApplication(sys.argv)
    
    # 创建配置
    config = Config()
    semester_start_date = date(2024, 9, 2)
    
    # 创建对话框
    dialog = SettingsDialog(config=config, semester_start_date=semester_start_date)
    
    # 验证对话框创建成功
    assert dialog is not None
    assert dialog.windowTitle() == "设置"
    print("✓ 设置对话框创建成功")
    
    # 验证选项卡
    assert dialog.tab_widget.count() == 3
    assert dialog.tab_widget.tabText(0) == "常规"
    assert dialog.tab_widget.tabText(1) == "时间段"
    assert dialog.tab_widget.tabText(2) == "学期"
    print("✓ 选项卡创建正确")
    
    # 验证常规设置选项卡
    assert dialog.general_tab is not None
    assert dialog.general_tab.show_widget_checkbox is not None
    print("✓ 常规设置选项卡正确")
    
    # 验证时间段设置选项卡
    assert dialog.time_slots_tab is not None
    assert dialog.time_slots_tab.table is not None
    assert dialog.time_slots_tab.table.rowCount() == 12  # 默认12节课
    print("✓ 时间段设置选项卡正确")
    
    # 验证学期设置选项卡
    assert dialog.semester_tab is not None
    assert dialog.semester_tab.start_date_edit is not None
    print("✓ 学期设置选项卡正确")
    
    print("\n设置对话框测试通过！✓")


def test_time_slots_operations():
    """测试时间段操作"""
    print("\n测试时间段操作...")
    
    # 创建应用程序
    app = QApplication(sys.argv)
    
    # 创建配置
    config = Config()
    
    # 创建对话框
    dialog = SettingsDialog(config=config)
    
    # 测试添加节次
    initial_count = dialog.time_slots_tab.table.rowCount()
    dialog.time_slots_tab._on_add_slot()
    assert dialog.time_slots_tab.table.rowCount() == initial_count + 1
    print("✓ 添加节次成功")
    
    # 测试删除节次
    dialog.time_slots_tab._on_remove_slot()
    assert dialog.time_slots_tab.table.rowCount() == initial_count
    print("✓ 删除节次成功")
    
    print("\n时间段操作测试通过！✓")


def test_semester_settings():
    """测试学期设置"""
    print("\n测试学期设置...")
    
    # 创建应用程序
    app = QApplication(sys.argv)
    
    # 创建配置
    config = Config()
    semester_start_date = date(2024, 9, 2)
    
    # 创建对话框
    dialog = SettingsDialog(config=config, semester_start_date=semester_start_date)
    
    # 验证学期开始日期
    retrieved_date = dialog.semester_tab.get_semester_start_date()
    assert retrieved_date == semester_start_date
    print("✓ 学期开始日期正确")
    
    # 验证当前周次显示
    assert dialog.semester_tab.current_week_label.text().startswith("第")
    assert dialog.semester_tab.current_week_label.text().endswith("周")
    print("✓ 当前周次显示正确")
    
    print("\n学期设置测试通过！✓")


if __name__ == "__main__":
    try:
        test_settings_dialog()
        test_time_slots_operations()
        test_semester_settings()
        print("\n" + "="*50)
        print("所有测试通过！✓")
        print("="*50)
    except AssertionError as e:
        print(f"\n✗ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ 发生错误: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
