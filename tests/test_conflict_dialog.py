"""
测试冲突提示对话框
"""

import sys
from pathlib import Path

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from PyQt6.QtWidgets import QApplication
from ui.conflict_dialog import ConflictDialog
from models.course_base import CourseBase
from models.course_detail import CourseDetail
from models.week_type import WeekType


def test_conflict_dialog():
    """测试冲突对话框"""
    print("\n测试冲突提示对话框...")
    
    # 创建应用程序
    app = QApplication(sys.argv)
    
    # 创建测试数据 - 冲突的课程
    conflicts = [
        (
            CourseBase(
                course_id="course-1",
                name="高等数学",
                color="#FF5722",
                note=""
            ),
            CourseDetail(
                course_id="course-1",
                teacher="张老师",
                location="教学楼A101",
                day_of_week=1,
                start_section=1,
                step=2,
                start_week=1,
                end_week=16,
                week_type=WeekType.EVERY_WEEK
            ),
            "周一 第1-2节 时间冲突"
        ),
        (
            CourseBase(
                course_id="course-2",
                name="线性代数",
                color="#2196F3",
                note=""
            ),
            CourseDetail(
                course_id="course-2",
                teacher="李老师",
                location="教学楼B202",
                day_of_week=1,
                start_section=2,
                step=2,
                start_week=1,
                end_week=16,
                week_type=WeekType.EVERY_WEEK
            ),
            "周一 第2-3节 部分时间冲突"
        )
    ]
    
    # 创建对话框
    dialog = ConflictDialog(
        new_course_name="大学物理",
        conflicts=conflicts
    )
    
    # 验证对话框创建成功
    assert dialog is not None
    assert dialog.windowTitle() == "课程冲突提示"
    print("✓ 冲突对话框创建成功")
    
    # 验证冲突列表
    assert dialog.conflict_table.rowCount() == 2
    print("✓ 冲突列表行数正确")
    
    # 验证第一行数据
    assert dialog.conflict_table.item(0, 0).text() == "高等数学"
    assert dialog.conflict_table.item(0, 1).text() == "张老师"
    assert dialog.conflict_table.item(0, 2).text() == "教学楼A101"
    assert dialog.conflict_table.item(0, 3).text() == "周一 第1-2节"
    assert dialog.conflict_table.item(0, 4).text() == "周一 第1-2节 时间冲突"
    print("✓ 第一行冲突数据正确")
    
    # 验证第二行数据
    assert dialog.conflict_table.item(1, 0).text() == "线性代数"
    assert dialog.conflict_table.item(1, 1).text() == "李老师"
    assert dialog.conflict_table.item(1, 2).text() == "教学楼B202"
    assert dialog.conflict_table.item(1, 3).text() == "周一 第2-3节"
    assert dialog.conflict_table.item(1, 4).text() == "周一 第2-3节 部分时间冲突"
    print("✓ 第二行冲突数据正确")
    
    # 验证颜色
    assert dialog.conflict_table.item(0, 0).background().color().name() == "#ff5722"
    assert dialog.conflict_table.item(1, 0).background().color().name() == "#2196f3"
    print("✓ 课程颜色显示正确")
    
    print("\n冲突对话框测试通过！✓")


def test_empty_conflicts():
    """测试空冲突列表"""
    print("\n测试空冲突列表...")
    
    # 创建应用程序
    app = QApplication(sys.argv)
    
    # 创建对话框（无冲突）
    dialog = ConflictDialog(
        new_course_name="大学物理",
        conflicts=[]
    )
    
    # 验证表格为空
    assert dialog.conflict_table.rowCount() == 0
    print("✓ 空冲突列表处理正确")
    
    print("\n空冲突列表测试通过！✓")


if __name__ == "__main__":
    try:
        test_conflict_dialog()
        test_empty_conflicts()
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
