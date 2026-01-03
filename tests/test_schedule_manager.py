"""
测试课表管理器和周次计算器
"""

import sys
from pathlib import Path
from datetime import date

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from models.course_base import CourseBase
from models.course_detail import CourseDetail
from models.schedule import Schedule
from models.week_type import WeekType
from core.week_calculator import WeekCalculator
from core.schedule_manager import ScheduleManager


def test_week_calculator():
    """测试周次计算器"""
    print("测试周次计算器...")
    
    semester_start = date(2024, 9, 1)
    calculator = WeekCalculator(semester_start)
    
    # 测试计算周次
    week1 = calculator.calculate_week(date(2024, 9, 1))
    assert week1 == 1, f"9月1日应该是第1周，实际是第{week1}周"
    
    week2 = calculator.calculate_week(date(2024, 9, 8))
    assert week2 == 2, f"9月8日应该是第2周，实际是第{week2}周"
    
    # 测试单双周判断
    assert calculator.is_odd_week(1) == True
    assert calculator.is_odd_week(2) == False
    assert calculator.is_even_week(2) == True
    assert calculator.is_even_week(1) == False
    
    # 测试设置学期开始日期
    calculator.set_semester_start_date(date(2024, 9, 2))
    week1_new = calculator.calculate_week(date(2024, 9, 2))
    assert week1_new == 1
    
    print("✓ 周次计算器测试通过")


def test_get_courses_for_week():
    """测试获取指定周次的课程"""
    print("测试获取指定周次的课程...")
    
    schedule = Schedule(semester_start_date=date(2024, 9, 1))
    manager = ScheduleManager(schedule)
    
    # 添加课程
    course1 = CourseBase(name="高等数学", color="#4CAF50")
    course2 = CourseBase(name="线性代数", color="#2196F3")
    schedule.course_bases.extend([course1, course2])
    
    # 课程1: 第1-16周，每周
    detail1 = CourseDetail(
        course_id=course1.id,
        day_of_week=1,
        start_section=1,
        step=2,
        start_week=1,
        end_week=16,
        week_type=WeekType.EVERY_WEEK
    )
    
    # 课程2: 第1-16周，单周
    detail2 = CourseDetail(
        course_id=course2.id,
        day_of_week=2,
        start_section=3,
        step=2,
        start_week=1,
        end_week=16,
        week_type=WeekType.ODD_WEEK
    )
    
    schedule.course_details.extend([detail1, detail2])
    
    # 第1周（单周）：应该有两门课
    week1_courses = manager.get_courses_for_week(1)
    assert len(week1_courses) == 2, f"第1周应该有2门课，实际有{len(week1_courses)}门"
    
    # 第2周（双周）：应该只有课程1
    week2_courses = manager.get_courses_for_week(2)
    assert len(week2_courses) == 1, f"第2周应该有1门课，实际有{len(week2_courses)}门"
    assert week2_courses[0][0].name == "高等数学"
    
    # 第3周（单周）：应该有两门课
    week3_courses = manager.get_courses_for_week(3)
    assert len(week3_courses) == 2, f"第3周应该有2门课，实际有{len(week3_courses)}门"
    
    # 第17周（超出范围）：应该没有课
    week17_courses = manager.get_courses_for_week(17)
    assert len(week17_courses) == 0, f"第17周应该没有课，实际有{len(week17_courses)}门"
    
    print("✓ 获取指定周次的课程测试通过")


def test_get_courses_for_day():
    """测试获取指定日期的课程"""
    print("测试获取指定日期的课程...")
    
    schedule = Schedule(semester_start_date=date(2024, 9, 1))
    manager = ScheduleManager(schedule)
    
    # 添加课程
    course1 = CourseBase(name="高等数学", color="#4CAF50")
    course2 = CourseBase(name="线性代数", color="#2196F3")
    course3 = CourseBase(name="大学物理", color="#FF5722")
    schedule.course_bases.extend([course1, course2, course3])
    
    # 周一的课程（第3-4节）
    detail1 = CourseDetail(
        course_id=course1.id,
        day_of_week=1,
        start_section=3,
        step=2,
        start_week=1,
        end_week=16
    )
    
    # 周一的课程（第1-2节）
    detail2 = CourseDetail(
        course_id=course2.id,
        day_of_week=1,
        start_section=1,
        step=2,
        start_week=1,
        end_week=16
    )
    
    # 周二的课程
    detail3 = CourseDetail(
        course_id=course3.id,
        day_of_week=2,
        start_section=1,
        step=2,
        start_week=1,
        end_week=16
    )
    
    schedule.course_details.extend([detail1, detail2, detail3])
    
    # 获取第1周周一的课程
    monday_courses = manager.get_courses_for_day(1, 1)
    assert len(monday_courses) == 2, f"周一应该有2门课，实际有{len(monday_courses)}门"
    
    # 验证排序（应该按节次排序）
    assert monday_courses[0][0].name == "线性代数", "第一门课应该是线性代数（第1-2节）"
    assert monday_courses[1][0].name == "高等数学", "第二门课应该是高等数学（第3-4节）"
    
    # 获取第1周周二的课程
    tuesday_courses = manager.get_courses_for_day(1, 2)
    assert len(tuesday_courses) == 1, f"周二应该有1门课，实际有{len(tuesday_courses)}门"
    assert tuesday_courses[0][0].name == "大学物理"
    
    # 获取第1周周三的课程（没有课）
    wednesday_courses = manager.get_courses_for_day(1, 3)
    assert len(wednesday_courses) == 0, f"周三应该没有课，实际有{len(wednesday_courses)}门"
    
    print("✓ 获取指定日期的课程测试通过")


def test_week_type_filtering():
    """测试单双周过滤"""
    print("测试单双周过滤...")
    
    schedule = Schedule(semester_start_date=date(2024, 9, 1))
    manager = ScheduleManager(schedule)
    
    # 添加课程
    course_every = CourseBase(name="每周课程", color="#4CAF50")
    course_odd = CourseBase(name="单周课程", color="#2196F3")
    course_even = CourseBase(name="双周课程", color="#FF5722")
    schedule.course_bases.extend([course_every, course_odd, course_even])
    
    # 每周课程
    detail_every = CourseDetail(
        course_id=course_every.id,
        day_of_week=1,
        start_section=1,
        step=2,
        start_week=1,
        end_week=10,
        week_type=WeekType.EVERY_WEEK
    )
    
    # 单周课程
    detail_odd = CourseDetail(
        course_id=course_odd.id,
        day_of_week=1,
        start_section=3,
        step=2,
        start_week=1,
        end_week=10,
        week_type=WeekType.ODD_WEEK
    )
    
    # 双周课程
    detail_even = CourseDetail(
        course_id=course_even.id,
        day_of_week=1,
        start_section=5,
        step=2,
        start_week=1,
        end_week=10,
        week_type=WeekType.EVEN_WEEK
    )
    
    schedule.course_details.extend([detail_every, detail_odd, detail_even])
    
    # 第1周（单周）：应该有每周课程和单周课程
    week1_courses = manager.get_courses_for_week(1)
    assert len(week1_courses) == 2
    course_names = {base.name for base, _ in week1_courses}
    assert "每周课程" in course_names
    assert "单周课程" in course_names
    assert "双周课程" not in course_names
    
    # 第2周（双周）：应该有每周课程和双周课程
    week2_courses = manager.get_courses_for_week(2)
    assert len(week2_courses) == 2
    course_names = {base.name for base, _ in week2_courses}
    assert "每周课程" in course_names
    assert "双周课程" in course_names
    assert "单周课程" not in course_names
    
    # 第3周（单周）：应该有每周课程和单周课程
    week3_courses = manager.get_courses_for_week(3)
    assert len(week3_courses) == 2
    course_names = {base.name for base, _ in week3_courses}
    assert "每周课程" in course_names
    assert "单周课程" in course_names
    
    print("✓ 单双周过滤测试通过")


def test_set_semester_start_date():
    """测试设置学期开始日期"""
    print("测试设置学期开始日期...")
    
    schedule = Schedule(semester_start_date=date(2024, 9, 1))
    manager = ScheduleManager(schedule)
    
    # 验证初始日期
    assert schedule.semester_start_date == date(2024, 9, 1)
    
    # 设置新的学期开始日期
    new_date = date(2024, 9, 2)
    manager.set_semester_start_date(new_date)
    
    # 验证更新后的日期
    assert schedule.semester_start_date == new_date
    assert manager.week_calculator.semester_start_date == new_date
    
    print("✓ 设置学期开始日期测试通过")


def test_get_all_courses_sorted():
    """测试获取所有课程并排序"""
    print("测试获取所有课程并排序...")
    
    schedule = Schedule(semester_start_date=date(2024, 9, 1))
    manager = ScheduleManager(schedule)
    
    # 添加课程（故意打乱顺序）
    course1 = CourseBase(name="课程1", color="#4CAF50")
    course2 = CourseBase(name="课程2", color="#2196F3")
    course3 = CourseBase(name="课程3", color="#FF5722")
    schedule.course_bases.extend([course1, course2, course3])
    
    # 周三第1节
    detail1 = CourseDetail(
        course_id=course1.id,
        day_of_week=3,
        start_section=1,
        step=2,
        start_week=1,
        end_week=16
    )
    
    # 周一第3节
    detail2 = CourseDetail(
        course_id=course2.id,
        day_of_week=1,
        start_section=3,
        step=2,
        start_week=1,
        end_week=16
    )
    
    # 周一第1节
    detail3 = CourseDetail(
        course_id=course3.id,
        day_of_week=1,
        start_section=1,
        step=2,
        start_week=1,
        end_week=16
    )
    
    schedule.course_details.extend([detail1, detail2, detail3])
    
    # 获取排序后的课程
    sorted_courses = manager.get_all_courses_sorted()
    assert len(sorted_courses) == 3
    
    # 验证排序顺序
    assert sorted_courses[0][0].name == "课程3", "第一个应该是周一第1节"
    assert sorted_courses[1][0].name == "课程2", "第二个应该是周一第3节"
    assert sorted_courses[2][0].name == "课程1", "第三个应该是周三第1节"
    
    print("✓ 获取所有课程并排序测试通过")


if __name__ == "__main__":
    print("=" * 50)
    print("开始测试课表管理器和周次计算器")
    print("=" * 50)
    
    test_week_calculator()
    test_get_courses_for_week()
    test_get_courses_for_day()
    test_week_type_filtering()
    test_set_semester_start_date()
    test_get_all_courses_sorted()
    
    print("=" * 50)
    print("✓ 所有测试通过！")
    print("=" * 50)
