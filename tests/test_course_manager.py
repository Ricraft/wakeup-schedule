"""
测试课程管理器
"""

import sys
from pathlib import Path
from datetime import date

# Path is now handled by conftest.py

from models.course_base import CourseBase
from models.course_detail import CourseDetail
from models.schedule import Schedule
from models.week_type import WeekType
from core.course_manager import CourseManager


def test_add_course_base():
    """测试添加课程基础信息"""
    print("测试添加课程基础信息...")
    
    schedule = Schedule(semester_start_date=date(2024, 9, 1))
    manager = CourseManager(schedule)
    
    # 添加有效的课程
    course = CourseBase(name="高等数学", color="#4CAF50")
    success, msg = manager.add_course_base(course)
    assert success, f"应该成功添加课程: {msg}"
    assert len(schedule.course_bases) == 1
    
    # 尝试添加空名称的课程
    invalid_course = CourseBase(name="", color="#4CAF50")
    success, msg = manager.add_course_base(invalid_course)
    assert not success, "应该拒绝空名称的课程"
    assert "不能为空" in msg
    assert len(schedule.course_bases) == 1  # 数量不应该增加
    
    # 尝试添加无效颜色的课程
    invalid_course = CourseBase(name="线性代数", color="invalid")
    success, msg = manager.add_course_base(invalid_course)
    assert not success, "应该拒绝无效颜色的课程"
    assert "十六进制" in msg
    
    print("✓ 添加课程基础信息测试通过")


def test_add_course_detail():
    """测试添加课程详细信息"""
    print("测试添加课程详细信息...")
    
    schedule = Schedule(semester_start_date=date(2024, 9, 1))
    manager = CourseManager(schedule)
    
    # 先添加课程基础信息
    course_base = CourseBase(name="高等数学", color="#4CAF50")
    manager.add_course_base(course_base)
    
    # 添加有效的课程详细信息
    detail = CourseDetail(
        course_id=course_base.id,
        day_of_week=1,
        start_section=1,
        step=2,
        start_week=1,
        end_week=16,
        teacher="张老师",
        location="A101"
    )
    success, msg = manager.add_course_detail(detail)
    assert success, f"应该成功添加课程详细信息: {msg}"
    assert len(schedule.course_details) == 1
    
    # 尝试添加不存在的课程ID
    invalid_detail = CourseDetail(
        course_id="non-existent-id",
        day_of_week=1,
        start_section=1,
        step=2,
        start_week=1,
        end_week=16
    )
    success, msg = manager.add_course_detail(invalid_detail)
    assert not success, "应该拒绝不存在的课程ID"
    assert "不存在" in msg
    
    # 尝试添加无效星期的课程
    invalid_detail = CourseDetail(
        course_id=course_base.id,
        day_of_week=8,  # 无效
        start_section=1,
        step=2,
        start_week=1,
        end_week=16
    )
    success, msg = manager.add_course_detail(invalid_detail)
    assert not success, "应该拒绝无效星期"
    assert "1-7 之间" in msg
    
    print("✓ 添加课程详细信息测试通过")


def test_update_course_base():
    """测试更新课程基础信息"""
    print("测试更新课程基础信息...")
    
    schedule = Schedule(semester_start_date=date(2024, 9, 1))
    manager = CourseManager(schedule)
    
    # 添加课程
    course = CourseBase(name="高等数学", color="#4CAF50")
    manager.add_course_base(course)
    original_id = course.id
    
    # 更新课程
    updated_course = CourseBase(name="高等数学A", color="#2196F3", note="更新后的备注")
    success, msg = manager.update_course_base(original_id, updated_course)
    assert success, f"应该成功更新课程: {msg}"
    
    # 验证更新后的数据
    retrieved = manager.get_course_base(original_id)
    assert retrieved is not None
    assert retrieved.id == original_id, "ID应该保持不变"
    assert retrieved.name == "高等数学A"
    assert retrieved.color == "#2196F3"
    assert retrieved.note == "更新后的备注"
    
    # 尝试更新不存在的课程
    success, msg = manager.update_course_base("non-existent-id", updated_course)
    assert not success, "应该拒绝更新不存在的课程"
    assert "不存在" in msg
    
    print("✓ 更新课程基础信息测试通过")


def test_delete_course_base():
    """测试删除课程基础信息"""
    print("测试删除课程基础信息...")
    
    schedule = Schedule(semester_start_date=date(2024, 9, 1))
    manager = CourseManager(schedule)
    
    # 添加课程和详细信息
    course = CourseBase(name="高等数学", color="#4CAF50")
    manager.add_course_base(course)
    
    detail1 = CourseDetail(
        course_id=course.id,
        day_of_week=1,
        start_section=1,
        step=2,
        start_week=1,
        end_week=16
    )
    detail2 = CourseDetail(
        course_id=course.id,
        day_of_week=3,
        start_section=3,
        step=2,
        start_week=1,
        end_week=16
    )
    manager.add_course_detail(detail1)
    manager.add_course_detail(detail2)
    
    assert len(schedule.course_bases) == 1
    assert len(schedule.course_details) == 2
    
    # 删除课程
    success, msg = manager.delete_course_base(course.id)
    assert success, f"应该成功删除课程: {msg}"
    assert len(schedule.course_bases) == 0
    assert len(schedule.course_details) == 0, "关联的详细信息也应该被删除"
    
    # 尝试删除不存在的课程
    success, msg = manager.delete_course_base("non-existent-id")
    assert not success, "应该拒绝删除不存在的课程"
    assert "不存在" in msg
    
    print("✓ 删除课程基础信息测试通过")


def test_get_course_base():
    """测试获取课程基础信息"""
    print("测试获取课程基础信息...")
    
    schedule = Schedule(semester_start_date=date(2024, 9, 1))
    manager = CourseManager(schedule)
    
    # 添加课程
    course1 = CourseBase(name="高等数学", color="#4CAF50")
    course2 = CourseBase(name="线性代数", color="#2196F3")
    manager.add_course_base(course1)
    manager.add_course_base(course2)
    
    # 获取单个课程
    retrieved = manager.get_course_base(course1.id)
    assert retrieved is not None
    assert retrieved.id == course1.id
    assert retrieved.name == "高等数学"
    
    # 获取不存在的课程
    retrieved = manager.get_course_base("non-existent-id")
    assert retrieved is None
    
    # 获取所有课程
    all_courses = manager.get_all_course_bases()
    assert len(all_courses) == 2
    
    print("✓ 获取课程基础信息测试通过")


def test_get_course_details():
    """测试获取课程详细信息"""
    print("测试获取课程详细信息...")
    
    schedule = Schedule(semester_start_date=date(2024, 9, 1))
    manager = CourseManager(schedule)
    
    # 添加两门课程
    course1 = CourseBase(name="高等数学", color="#4CAF50")
    course2 = CourseBase(name="线性代数", color="#2196F3")
    manager.add_course_base(course1)
    manager.add_course_base(course2)
    
    # 为第一门课程添加两个详细信息
    detail1 = CourseDetail(
        course_id=course1.id,
        day_of_week=1,
        start_section=1,
        step=2,
        start_week=1,
        end_week=16
    )
    detail2 = CourseDetail(
        course_id=course1.id,
        day_of_week=3,
        start_section=3,
        step=2,
        start_week=1,
        end_week=16
    )
    # 为第二门课程添加一个详细信息
    detail3 = CourseDetail(
        course_id=course2.id,
        day_of_week=2,
        start_section=1,
        step=2,
        start_week=1,
        end_week=16
    )
    
    manager.add_course_detail(detail1)
    manager.add_course_detail(detail2)
    manager.add_course_detail(detail3)
    
    # 获取第一门课程的详细信息
    details = manager.get_course_details_by_course_id(course1.id)
    assert len(details) == 2
    
    # 获取第二门课程的详细信息
    details = manager.get_course_details_by_course_id(course2.id)
    assert len(details) == 1
    
    # 获取所有详细信息
    all_details = manager.get_all_course_details()
    assert len(all_details) == 3
    
    print("✓ 获取课程详细信息测试通过")


def test_validate_course():
    """测试课程验证"""
    print("测试课程验证...")
    
    schedule = Schedule(semester_start_date=date(2024, 9, 1))
    manager = CourseManager(schedule)
    
    # 验证有效的课程基础信息
    valid_course = CourseBase(name="高等数学", color="#4CAF50")
    valid, msg = manager.validate_course_base(valid_course)
    assert valid, f"应该接受有效的课程: {msg}"
    
    # 验证无效的课程基础信息
    invalid_course = CourseBase(name="", color="#4CAF50")
    valid, msg = manager.validate_course_base(invalid_course)
    assert not valid, "应该拒绝无效的课程"
    
    # 验证有效的课程详细信息
    valid_detail = CourseDetail(
        course_id="test-id",
        day_of_week=1,
        start_section=1,
        step=2,
        start_week=1,
        end_week=16
    )
    valid, msg = manager.validate_course_detail(valid_detail)
    assert valid, f"应该接受有效的课程详细信息: {msg}"
    
    # 验证无效的课程详细信息
    invalid_detail = CourseDetail(
        course_id="test-id",
        day_of_week=8,  # 无效
        start_section=1,
        step=2,
        start_week=1,
        end_week=16
    )
    valid, msg = manager.validate_course_detail(invalid_detail)
    assert not valid, "应该拒绝无效的课程详细信息"
    
    print("✓ 课程验证测试通过")


if __name__ == "__main__":
    print("=" * 50)
    print("开始测试课程管理器")
    print("=" * 50)
    
    test_add_course_base()
    test_add_course_detail()
    test_update_course_base()
    test_delete_course_base()
    test_get_course_base()
    test_get_course_details()
    test_validate_course()
    
    print("=" * 50)
    print("✓ 所有课程管理器测试通过！")
    print("=" * 50)
