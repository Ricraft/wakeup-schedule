"""
测试冲突检测器
"""

import sys
from pathlib import Path

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from models.course_base import CourseBase
from models.course_detail import CourseDetail
from models.week_type import WeekType
from core.conflict_detector import ConflictDetector


def test_no_conflict_different_days():
    """测试不同星期的课程不冲突"""
    print("测试不同星期的课程不冲突...")
    
    # 周一的课程
    detail1 = CourseDetail(
        course_id="course1",
        day_of_week=1,
        start_section=1,
        step=2,
        start_week=1,
        end_week=16
    )
    
    # 周二的课程
    detail2 = CourseDetail(
        course_id="course2",
        day_of_week=2,
        start_section=1,
        step=2,
        start_week=1,
        end_week=16
    )
    
    conflicts = ConflictDetector.check_conflict(detail1, [detail2])
    assert len(conflicts) == 0, "不同星期的课程不应该冲突"
    
    print("✓ 不同星期的课程不冲突测试通过")


def test_no_conflict_different_sections():
    """测试不同节次的课程不冲突"""
    print("测试不同节次的课程不冲突...")
    
    # 第1-2节
    detail1 = CourseDetail(
        course_id="course1",
        day_of_week=1,
        start_section=1,
        step=2,
        start_week=1,
        end_week=16
    )
    
    # 第3-4节
    detail2 = CourseDetail(
        course_id="course2",
        day_of_week=1,
        start_section=3,
        step=2,
        start_week=1,
        end_week=16
    )
    
    conflicts = ConflictDetector.check_conflict(detail1, [detail2])
    assert len(conflicts) == 0, "不同节次的课程不应该冲突"
    
    print("✓ 不同节次的课程不冲突测试通过")


def test_no_conflict_different_weeks():
    """测试不同周次的课程不冲突"""
    print("测试不同周次的课程不冲突...")
    
    # 第1-8周
    detail1 = CourseDetail(
        course_id="course1",
        day_of_week=1,
        start_section=1,
        step=2,
        start_week=1,
        end_week=8
    )
    
    # 第9-16周
    detail2 = CourseDetail(
        course_id="course2",
        day_of_week=1,
        start_section=1,
        step=2,
        start_week=9,
        end_week=16
    )
    
    conflicts = ConflictDetector.check_conflict(detail1, [detail2])
    assert len(conflicts) == 0, "不同周次的课程不应该冲突"
    
    print("✓ 不同周次的课程不冲突测试通过")


def test_conflict_same_time():
    """测试相同时间的课程冲突"""
    print("测试相同时间的课程冲突...")
    
    # 周一第1-2节，第1-16周
    detail1 = CourseDetail(
        course_id="course1",
        day_of_week=1,
        start_section=1,
        step=2,
        start_week=1,
        end_week=16
    )
    
    # 周一第1-2节，第1-16周
    detail2 = CourseDetail(
        course_id="course2",
        day_of_week=1,
        start_section=1,
        step=2,
        start_week=1,
        end_week=16
    )
    
    conflicts = ConflictDetector.check_conflict(detail1, [detail2])
    assert len(conflicts) == 1, "相同时间的课程应该冲突"
    assert conflicts[0] == detail2
    
    print("✓ 相同时间的课程冲突测试通过")


def test_conflict_overlapping_sections():
    """测试节次重叠的课程冲突"""
    print("测试节次重叠的课程冲突...")
    
    # 第1-3节
    detail1 = CourseDetail(
        course_id="course1",
        day_of_week=1,
        start_section=1,
        step=3,
        start_week=1,
        end_week=16
    )
    
    # 第2-4节（与第1-3节重叠）
    detail2 = CourseDetail(
        course_id="course2",
        day_of_week=1,
        start_section=2,
        step=3,
        start_week=1,
        end_week=16
    )
    
    conflicts = ConflictDetector.check_conflict(detail1, [detail2])
    assert len(conflicts) == 1, "节次重叠的课程应该冲突"
    
    print("✓ 节次重叠的课程冲突测试通过")


def test_no_conflict_odd_even_weeks():
    """测试单双周课程不冲突"""
    print("测试单双周课程不冲突...")
    
    # 单周课程
    detail1 = CourseDetail(
        course_id="course1",
        day_of_week=1,
        start_section=1,
        step=2,
        start_week=1,
        end_week=16,
        week_type=WeekType.ODD_WEEK
    )
    
    # 双周课程
    detail2 = CourseDetail(
        course_id="course2",
        day_of_week=1,
        start_section=1,
        step=2,
        start_week=1,
        end_week=16,
        week_type=WeekType.EVEN_WEEK
    )
    
    conflicts = ConflictDetector.check_conflict(detail1, [detail2])
    assert len(conflicts) == 0, "单双周课程不应该冲突"
    
    print("✓ 单双周课程不冲突测试通过")


def test_conflict_odd_weeks_with_every_week():
    """测试单周课程与每周课程冲突"""
    print("测试单周课程与每周课程冲突...")
    
    # 单周课程
    detail1 = CourseDetail(
        course_id="course1",
        day_of_week=1,
        start_section=1,
        step=2,
        start_week=1,
        end_week=16,
        week_type=WeekType.ODD_WEEK
    )
    
    # 每周课程
    detail2 = CourseDetail(
        course_id="course2",
        day_of_week=1,
        start_section=1,
        step=2,
        start_week=1,
        end_week=16,
        week_type=WeekType.EVERY_WEEK
    )
    
    conflicts = ConflictDetector.check_conflict(detail1, [detail2])
    assert len(conflicts) == 1, "单周课程与每周课程应该冲突"
    
    print("✓ 单周课程与每周课程冲突测试通过")


def test_has_time_overlap_specific_week():
    """测试指定周次的时间重叠检测"""
    print("测试指定周次的时间重叠检测...")
    
    # 单周课程
    detail1 = CourseDetail(
        course_id="course1",
        day_of_week=1,
        start_section=1,
        step=2,
        start_week=1,
        end_week=16,
        week_type=WeekType.ODD_WEEK
    )
    
    # 每周课程
    detail2 = CourseDetail(
        course_id="course2",
        day_of_week=1,
        start_section=1,
        step=2,
        start_week=1,
        end_week=16,
        week_type=WeekType.EVERY_WEEK
    )
    
    # 第1周（单周）：应该冲突
    assert ConflictDetector.has_time_overlap(detail1, detail2, 1), "第1周应该冲突"
    
    # 第2周（双周）：不应该冲突（单周课程不上课）
    assert not ConflictDetector.has_time_overlap(detail1, detail2, 2), "第2周不应该冲突"
    
    # 第3周（单周）：应该冲突
    assert ConflictDetector.has_time_overlap(detail1, detail2, 3), "第3周应该冲突"
    
    print("✓ 指定周次的时间重叠检测测试通过")


def test_conflict_partial_week_overlap():
    """测试部分周次重叠的冲突"""
    print("测试部分周次重叠的冲突...")
    
    # 第1-10周
    detail1 = CourseDetail(
        course_id="course1",
        day_of_week=1,
        start_section=1,
        step=2,
        start_week=1,
        end_week=10
    )
    
    # 第5-16周（与第1-10周有重叠）
    detail2 = CourseDetail(
        course_id="course2",
        day_of_week=1,
        start_section=1,
        step=2,
        start_week=5,
        end_week=16
    )
    
    conflicts = ConflictDetector.check_conflict(detail1, [detail2])
    assert len(conflicts) == 1, "部分周次重叠的课程应该冲突"
    
    print("✓ 部分周次重叠的冲突测试通过")


def test_multiple_conflicts():
    """测试检测多个冲突"""
    print("测试检测多个冲突...")
    
    # 要检查的课程
    detail1 = CourseDetail(
        course_id="course1",
        day_of_week=1,
        start_section=1,
        step=2,
        start_week=1,
        end_week=16
    )
    
    # 冲突课程1
    detail2 = CourseDetail(
        course_id="course2",
        day_of_week=1,
        start_section=1,
        step=2,
        start_week=1,
        end_week=16
    )
    
    # 冲突课程2
    detail3 = CourseDetail(
        course_id="course3",
        day_of_week=1,
        start_section=2,
        step=2,
        start_week=1,
        end_week=16
    )
    
    # 不冲突的课程
    detail4 = CourseDetail(
        course_id="course4",
        day_of_week=2,
        start_section=1,
        step=2,
        start_week=1,
        end_week=16
    )
    
    conflicts = ConflictDetector.check_conflict(detail1, [detail2, detail3, detail4])
    assert len(conflicts) == 2, f"应该检测到2个冲突，实际检测到{len(conflicts)}个"
    
    print("✓ 检测多个冲突测试通过")


def test_get_conflict_description():
    """测试获取冲突描述"""
    print("测试获取冲突描述...")
    
    detail1 = CourseDetail(
        course_id="course1",
        day_of_week=1,
        start_section=1,
        step=2,
        start_week=1,
        end_week=16
    )
    
    detail2 = CourseDetail(
        course_id="course2",
        day_of_week=1,
        start_section=1,
        step=2,
        start_week=1,
        end_week=16
    )
    
    detector = ConflictDetector()
    description = detector.get_conflict_description(detail1, detail2)
    
    assert "周一" in description
    assert "第1-2节" in description
    assert "冲突" in description
    
    print(f"  冲突描述: {description}")
    print("✓ 获取冲突描述测试通过")


if __name__ == "__main__":
    print("=" * 50)
    print("开始测试冲突检测器")
    print("=" * 50)
    
    test_no_conflict_different_days()
    test_no_conflict_different_sections()
    test_no_conflict_different_weeks()
    test_conflict_same_time()
    test_conflict_overlapping_sections()
    test_no_conflict_odd_even_weeks()
    test_conflict_odd_weeks_with_every_week()
    test_has_time_overlap_specific_week()
    test_conflict_partial_week_overlap()
    test_multiple_conflicts()
    test_get_conflict_description()
    
    print("=" * 50)
    print("✓ 所有冲突检测器测试通过！")
    print("=" * 50)
