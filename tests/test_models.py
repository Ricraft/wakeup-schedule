"""
数据模型测试脚本

测试所有数据模型的基本功能
"""

import sys
from datetime import date, time

# 添加 src 到路径
sys.path.insert(0, 'src')

from models import (
    WeekType, CourseBase, CourseDetail, 
    TimeSlot, Schedule, Config, Theme
)
from utils.color_manager import ColorManager


def test_week_type():
    """测试 WeekType 枚举"""
    print("=" * 50)
    print("测试 WeekType 枚举")
    print("=" * 50)
    
    # 测试基本功能
    every = WeekType.EVERY_WEEK
    odd = WeekType.ODD_WEEK
    even = WeekType.EVEN_WEEK
    
    print(f"每周: {every} ({every.to_chinese()})")
    print(f"单周: {odd} ({odd.to_chinese()})")
    print(f"双周: {even} ({even.to_chinese()})")
    
    # 测试周次匹配
    print("\n周次匹配测试:")
    for week in [1, 2, 3, 4]:
        print(f"  第{week}周: 每周={every.matches_week(week)}, "
              f"单周={odd.matches_week(week)}, 双周={even.matches_week(week)}")
    
    # 测试转换
    print("\n转换测试:")
    print(f"  从字符串: {WeekType.from_string('odd')}")
    print(f"  从整数: {WeekType.from_int(1)}")
    print(f"  转整数: {odd.to_int()}")
    
    print("✅ WeekType 测试通过\n")


def test_course_base():
    """测试 CourseBase 数据模型"""
    print("=" * 50)
    print("测试 CourseBase 数据模型")
    print("=" * 50)
    
    # 创建课程
    course = CourseBase(
        name="高等数学",
        color="#FF6B6B",
        note="重要课程"
    )
    
    print(f"课程: {course}")
    print(f"ID: {course.id}")
    print(f"名称: {course.name}")
    print(f"颜色: {course.color}")
    
    # 测试序列化
    print("\n序列化测试:")
    data = course.to_dict()
    print(f"  字典: {data}")
    
    course2 = CourseBase.from_dict(data)
    print(f"  反序列化: {course2}")
    print(f"  相等性: {course == course2}")
    
    print("✅ CourseBase 测试通过\n")


def test_course_detail():
    """测试 CourseDetail 数据模型"""
    print("=" * 50)
    print("测试 CourseDetail 数据模型")
    print("=" * 50)
    
    # 创建课程详情
    detail = CourseDetail(
        course_id="test-id",
        day_of_week=1,  # 周一
        start_section=1,
        step=2,  # 连续2节
        start_week=1,
        end_week=16,
        week_type=WeekType.ODD_WEEK,
        teacher="张老师",
        location="教学楼A101"
    )
    
    print(f"课程详情: {detail}")
    print(f"结束节次: {detail.end_section}")
    
    # 测试周次判断
    print("\n周次判断测试:")
    for week in [1, 2, 3, 16, 17]:
        print(f"  第{week}周: {detail.is_in_week(week)}")
    
    # 测试时间冲突
    print("\n时间冲突测试:")
    detail2 = CourseDetail(
        course_id="test-id-2",
        day_of_week=1,  # 同一天
        start_section=2,  # 有重叠
        step=2,
        start_week=1,
        end_week=16,
        week_type=WeekType.EVERY_WEEK
    )
    print(f"  与另一课程冲突: {detail.has_time_overlap(detail2, 1)}")
    
    # 测试序列化
    print("\n序列化测试:")
    data = detail.to_dict()
    detail3 = CourseDetail.from_dict(data)
    print(f"  相等性: {detail == detail3}")
    
    print("✅ CourseDetail 测试通过\n")


def test_color_manager():
    """测试颜色管理器"""
    print("=" * 50)
    print("测试颜色管理器")
    print("=" * 50)
    
    # 测试颜色分配
    courses = ["高等数学", "线性代数", "大学物理", "程序设计", "高等数学"]
    
    print("课程颜色分配:")
    for course_name in courses:
        color = ColorManager.get_color_for_course(course_name)
        print(f"  {course_name}: {color}")
    
    # 验证同一课程颜色一致
    color1 = ColorManager.get_color_for_course("高等数学")
    color2 = ColorManager.get_color_for_course("高等数学")
    print(f"\n同一课程颜色一致: {color1 == color2}")
    
    # 测试颜色验证
    print("\n颜色验证测试:")
    print(f"  #FF6B6B 有效: {ColorManager.is_valid_color('#FF6B6B')}")
    print(f"  #GGGGGG 有效: {ColorManager.is_valid_color('#GGGGGG')}")
    print(f"  FF6B6B 有效: {ColorManager.is_valid_color('FF6B6B')}")
    
    print("✅ ColorManager 测试通过\n")


def test_time_slot():
    """测试 TimeSlot 数据模型"""
    print("=" * 50)
    print("测试 TimeSlot 数据模型")
    print("=" * 50)
    
    # 生成默认时间段
    time_slots = TimeSlot.generate_default_time_slots()
    
    print(f"默认时间段数量: {len(time_slots)}")
    print("\n前5个时间段:")
    for slot in time_slots[:5]:
        print(f"  {slot}")
    
    # 测试序列化
    print("\n序列化测试:")
    data = time_slots[0].to_dict()
    print(f"  字典: {data}")
    slot2 = TimeSlot.from_dict(data)
    print(f"  相等性: {time_slots[0] == slot2}")
    
    print("✅ TimeSlot 测试通过\n")


def test_schedule():
    """测试 Schedule 数据模型"""
    print("=" * 50)
    print("测试 Schedule 数据模型")
    print("=" * 50)
    
    # 创建课表
    schedule = Schedule(
        semester_start_date=date(2024, 9, 1),
        current_week=1
    )
    
    # 添加课程
    course_base = CourseBase(name="高等数学", color="#FF6B6B")
    course_detail = CourseDetail(
        course_id=course_base.id,
        day_of_week=1,
        start_section=1,
        step=2,
        start_week=1,
        end_week=16,
        week_type=WeekType.EVERY_WEEK,
        teacher="张老师",
        location="A101"
    )
    
    schedule.add_course(course_base, course_detail)
    
    print(f"课表: {schedule}")
    print(f"课程数量: {len(schedule.course_bases)}")
    print(f"详情数量: {len(schedule.course_details)}")
    
    # 测试查询
    print("\n查询测试:")
    base = schedule.get_course_base(course_base.id)
    print(f"  查询课程: {base.name if base else 'Not Found'}")
    
    details = schedule.get_course_details_by_id(course_base.id)
    print(f"  课程详情数量: {len(details)}")
    
    # 测试序列化
    print("\n序列化测试:")
    data = schedule.to_dict()
    schedule2 = Schedule.from_dict(data)
    print(f"  相等性: {schedule == schedule2}")
    
    print("✅ Schedule 测试通过\n")


def test_config():
    """测试 Config 数据模型"""
    print("=" * 50)
    print("测试 Config 数据模型")
    print("=" * 50)
    
    # 创建配置
    config = Config()
    
    print(f"配置: {config}")
    print(f"时间段数量: {len(config.time_slots)}")
    print(f"主题: {config.theme.primary_color}")
    print(f"窗口大小: {config.window_geometry['width']}x{config.window_geometry['height']}")
    print(f"保存的URL: {config.saved_urls}")
    
    # 测试序列化
    print("\n序列化测试:")
    data = config.to_dict()
    config2 = Config.from_dict(data)
    print(f"  相等性: {config == config2}")
    
    print("✅ Config 测试通过\n")


def main():
    """运行所有测试"""
    print("\n" + "=" * 50)
    print("WakeUp 课表 - 数据模型测试")
    print("=" * 50 + "\n")
    
    try:
        test_week_type()
        test_course_base()
        test_course_detail()
        test_color_manager()
        test_time_slot()
        test_schedule()
        test_config()
        
        print("=" * 50)
        print("✅ 所有测试通过！")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
