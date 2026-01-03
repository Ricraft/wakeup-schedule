"""
测试课程对话框
"""

import sys
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from PyQt6.QtWidgets import QApplication
from ui.course_dialog import CourseDialog
from models.course_base import CourseBase
from models.course_detail import CourseDetail
from models.week_type import WeekType


def test_course_dialog_add_mode():
    """测试添加模式"""
    print("\n测试课程对话框（添加模式）...")
    
    # 创建应用程序
    app = QApplication(sys.argv)
    
    # 创建对话框（添加模式）
    dialog = CourseDialog()
    
    # 验证对话框创建成功
    assert dialog is not None
    assert dialog.windowTitle() == "添加课程"
    assert not dialog.edit_mode
    print("✓ 添加模式对话框创建成功")
    
    # 验证所有输入字段都已创建
    assert dialog.name_edit is not None
    assert dialog.teacher_edit is not None
    assert dialog.location_edit is not None
    assert dialog.day_combo is not None
    assert dialog.start_section_spin is not None
    assert dialog.end_section_spin is not None
    assert dialog.start_week_spin is not None
    assert dialog.end_week_spin is not None
    assert dialog.week_type_combo is not None
    assert dialog.note_edit is not None
    print("✓ 所有输入字段已创建")
    
    # 验证默认值
    assert dialog.name_edit.text() == ""
    assert dialog.teacher_edit.text() == ""
    assert dialog.location_edit.text() == ""
    assert dialog.day_combo.currentIndex() == 0  # 周一
    assert dialog.start_section_spin.value() == 1
    assert dialog.end_section_spin.value() == 2
    assert dialog.start_week_spin.value() == 1
    assert dialog.end_week_spin.value() == 16
    assert dialog.week_type_combo.currentData() == WeekType.EVERY_WEEK
    assert dialog.note_edit.toPlainText() == ""
    print("✓ 默认值正确")
    
    print("\n添加模式测试通过！✓")


def test_course_dialog_edit_mode():
    """测试编辑模式"""
    print("\n测试课程对话框（编辑模式）...")
    
    # 创建应用程序
    app = QApplication(sys.argv)
    
    # 创建测试数据
    course_base = CourseBase(
        course_id="test-id",
        name="高等数学",
        color="#FF5722",
        note="重要课程"
    )
    
    course_detail = CourseDetail(
        course_id="test-id",
        teacher="张老师",
        location="教学楼A101",
        day_of_week=1,
        start_section=3,
        step=2,
        start_week=1,
        end_week=16,
        week_type=WeekType.EVERY_WEEK
    )
    
    # 创建对话框（编辑模式）
    dialog = CourseDialog(course_base=course_base, course_detail=course_detail)
    
    # 验证对话框创建成功
    assert dialog is not None
    assert dialog.windowTitle() == "编辑课程"
    assert dialog.edit_mode
    print("✓ 编辑模式对话框创建成功")
    
    # 验证数据已正确加载
    assert dialog.name_edit.text() == "高等数学"
    assert dialog.teacher_edit.text() == "张老师"
    assert dialog.location_edit.text() == "教学楼A101"
    assert dialog.day_combo.currentIndex() == 0  # 周一
    assert dialog.start_section_spin.value() == 3
    assert dialog.end_section_spin.value() == 4  # start_section + step - 1 = 3 + 2 - 1 = 4
    assert dialog.start_week_spin.value() == 1
    assert dialog.end_week_spin.value() == 16
    assert dialog.week_type_combo.currentData() == WeekType.EVERY_WEEK
    assert dialog.note_edit.toPlainText() == "重要课程"
    print("✓ 课程数据已正确加载")
    
    print("\n编辑模式测试通过！✓")


def test_validation():
    """测试数据验证"""
    print("\n测试数据验证...")
    
    # 创建应用程序
    app = QApplication(sys.argv)
    
    # 创建对话框
    dialog = CourseDialog()
    dialog.show()  # 显示对话框
    app.processEvents()  # 处理事件
    
    # 测试空课程名称验证
    dialog.name_edit.clear()  # 确保字段为空
    app.processEvents()
    result = dialog._validate_name()
    assert not result, "空课程名称应该验证失败"
    assert dialog.name_error_label.isVisible(), "错误标签应该可见"
    print("✓ 空课程名称验证正确")
    
    # 测试有效课程名称
    dialog.name_edit.setText("高等数学")
    app.processEvents()
    result = dialog._validate_name()
    assert result
    assert not dialog.name_error_label.isVisible()
    print("✓ 有效课程名称验证正确")
    
    # 测试节次范围验证
    dialog.start_section_spin.setValue(5)
    dialog.end_section_spin.setValue(3)
    app.processEvents()
    result = dialog._validate_sections()
    assert not result
    assert dialog.section_error_label.isVisible()
    print("✓ 无效节次范围验证正确")
    
    # 测试有效节次范围
    dialog.start_section_spin.setValue(3)
    dialog.end_section_spin.setValue(5)
    app.processEvents()
    result = dialog._validate_sections()
    assert result
    assert not dialog.section_error_label.isVisible()
    print("✓ 有效节次范围验证正确")
    
    # 测试周次范围验证
    dialog.start_week_spin.setValue(10)
    dialog.end_week_spin.setValue(5)
    app.processEvents()
    result = dialog._validate_weeks()
    assert not result
    assert dialog.week_error_label.isVisible()
    print("✓ 无效周次范围验证正确")
    
    # 测试有效周次范围
    dialog.start_week_spin.setValue(5)
    dialog.end_week_spin.setValue(10)
    app.processEvents()
    result = dialog._validate_weeks()
    assert result
    assert not dialog.week_error_label.isVisible()
    print("✓ 有效周次范围验证正确")
    
    print("\n数据验证测试通过！✓")


if __name__ == "__main__":
    try:
        test_course_dialog_add_mode()
        test_course_dialog_edit_mode()
        test_validation()
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
