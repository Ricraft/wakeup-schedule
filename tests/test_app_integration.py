"""
应用程序集成测试

测试完整的用户流程
"""

import sys
from pathlib import Path
from datetime import date

# 添加src目录到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from models.course_base import CourseBase
from models.course_detail import CourseDetail
from models.week_type import WeekType


def test_app_startup():
    """测试应用程序启动"""
    print("\n测试应用程序启动...")
    
    # 创建应用程序
    app = QApplication(sys.argv)
    
    # 创建主窗口
    window = MainWindow()
    
    # 验证窗口创建成功
    assert window is not None
    assert window.windowTitle() == "WakeUp 课表"
    print("✓ 应用程序启动成功")
    
    # 验证核心组件
    assert window.schedule is not None
    assert window.config is not None
    assert window.schedule_manager is not None
    assert window.course_manager is not None
    assert window.week_calculator is not None
    print("✓ 核心组件初始化成功")
    
    # 验证UI组件
    assert window.schedule_view is not None
    assert window.week_selector is not None
    assert window.statusBar is not None
    print("✓ UI组件创建成功")
    
    print("\n应用程序启动测试通过！✓")


def test_course_management():
    """测试课程管理功能"""
    print("\n测试课程管理功能...")
    
    # 创建应用程序
    app = QApplication(sys.argv)
    
    # 创建主窗口
    window = MainWindow()
    
    # 获取初始课程数量
    initial_count = len(window.schedule.course_bases)
    print(f"  初始课程数量: {initial_count}")
    
    # 添加课程
    course_base = CourseBase(
        course_id="test-course-1",
        name="测试课程",
        color="#FF5722",
        note="这是一个测试课程"
    )
    
    course_detail = CourseDetail(
        course_id="test-course-1",
        teacher="测试老师",
        location="测试教室",
        day_of_week=1,
        start_section=1,
        step=2,
        start_week=1,
        end_week=16,
        week_type=WeekType.EVERY_WEEK
    )
    
    success, msg = window.course_manager.add_course_base(course_base)
    assert success, f"添加课程基础信息失败: {msg}"
    
    success, msg = window.course_manager.add_course_detail(course_detail)
    assert success, f"添加课程详细信息失败: {msg}"
    
    print("✓ 添加课程成功")
    
    # 验证课程已添加
    new_count = len(window.schedule.course_bases)
    assert new_count == initial_count + 1
    print(f"✓ 课程数量增加: {initial_count} -> {new_count}")
    
    # 获取课程
    retrieved_base = window.course_manager.get_course_base("test-course-1")
    assert retrieved_base is not None
    assert retrieved_base.name == "测试课程"
    print("✓ 获取课程成功")
    
    # 删除课程
    success, msg = window.course_manager.delete_course_base("test-course-1")
    assert success, f"删除课程失败: {msg}"
    print("✓ 删除课程成功")
    
    # 验证课程已删除
    final_count = len(window.schedule.course_bases)
    assert final_count == initial_count
    print(f"✓ 课程数量恢复: {new_count} -> {final_count}")
    
    print("\n课程管理功能测试通过！✓")


def test_week_navigation():
    """测试周次导航功能"""
    print("\n测试周次导航功能...")
    
    # 创建应用程序
    app = QApplication(sys.argv)
    
    # 创建主窗口
    window = MainWindow()
    
    # 获取当前周次
    current_week = window.display_week
    print(f"  当前显示周次: 第 {current_week} 周")
    
    # 测试切换到下一周
    if current_week < 30:
        window._on_next_week()
        assert window.display_week == current_week + 1
        print(f"✓ 切换到下一周: 第 {window.display_week} 周")
        
        # 切换回上一周
        window._on_prev_week()
        assert window.display_week == current_week
        print(f"✓ 切换回上一周: 第 {window.display_week} 周")
    else:
        print("  (当前已是最后一周，跳过下一周测试)")
    
    # 测试周次选择器
    test_week = 5
    # 直接调用主窗口的周次改变处理方法
    window._on_week_selector_changed(test_week)
    assert window.display_week == test_week
    print(f"✓ 周次选择器工作正常: 第 {test_week} 周")
    
    print("\n周次导航功能测试通过！✓")


def test_schedule_view():
    """测试课表视图功能"""
    print("\n测试课表视图功能...")
    
    # 创建应用程序
    app = QApplication(sys.argv)
    
    # 创建主窗口
    window = MainWindow()
    
    # 验证课表视图 (ScheduleView itself is the table)
    assert window.schedule_view is not None
    print("✓ 课表表格创建成功")
    
    # 验证表格结构
    assert window.schedule_view.columnCount() == 8  # 时间 + 7天
    assert window.schedule_view.rowCount() == len(window.config.time_slots)
    print(f"✓ 表格结构正确: {window.schedule_view.rowCount()} 行 x {window.schedule_view.columnCount()} 列")
    
    # 获取当前周的课程
    courses = window.schedule_manager.get_courses_for_week(window.display_week)
    print(f"  当前周课程数量: {len(courses)}")
    
    # 更新课表视图
    window.schedule_view.update_courses(courses)
    print("✓ 课表视图更新成功")
    
    print("\n课表视图功能测试通过！✓")


def test_conflict_detection():
    """测试冲突检测功能"""
    print("\n测试冲突检测功能...")
    
    # 创建应用程序
    app = QApplication(sys.argv)
    
    # 创建主窗口
    window = MainWindow()
    
    # 创建两个冲突的课程
    course1 = CourseDetail(
        course_id="conflict-test-1",
        teacher="老师A",
        location="教室A",
        day_of_week=1,
        start_section=1,
        step=2,
        start_week=1,
        end_week=16,
        week_type=WeekType.EVERY_WEEK
    )
    
    course2 = CourseDetail(
        course_id="conflict-test-2",
        teacher="老师B",
        location="教室B",
        day_of_week=1,
        start_section=2,  # 与course1的第2节重叠
        step=2,
        start_week=1,
        end_week=16,
        week_type=WeekType.EVERY_WEEK
    )
    
    # 添加第一个课程
    from core.conflict_detector import ConflictDetector
    detector = ConflictDetector(window.schedule)
    
    # 先添加course1到schedule
    window.course_manager.add_course_base(CourseBase(
        course_id="conflict-test-1",
        name="课程A",
        color="#FF0000",
        note=""
    ))
    window.course_manager.add_course_detail(course1)
    
    # 检测course2是否与course1冲突
    conflicts = detector.detect_conflicts(course2)
    
    # 应该检测到冲突
    assert len(conflicts) > 0, "应该检测到时间冲突"
    print(f"✓ 检测到 {len(conflicts)} 个冲突")
    
    # 清理测试数据
    window.course_manager.delete_course_base("conflict-test-1")
    
    print("\n冲突检测功能测试通过！✓")


if __name__ == "__main__":
    try:
        test_app_startup()
        test_course_management()
        test_week_navigation()
        test_schedule_view()
        test_conflict_detection()
        
        print("\n" + "="*50)
        print("所有集成测试通过！✓")
        print("="*50)
        print("\n应用程序功能完整，可以正常使用！")
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
