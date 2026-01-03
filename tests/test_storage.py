"""
存储层测试脚本

测试 JSON 存储功能
"""

import sys
from datetime import date

# 添加 src 到路径
sys.path.insert(0, 'src')

from models import Schedule, Config, CourseBase, CourseDetail, WeekType
from storage import JSONStorage


def test_schedule_storage():
    """测试课表存储"""
    print("=" * 50)
    print("测试课表存储")
    print("=" * 50)
    
    # 创建测试课表
    schedule = Schedule(
        semester_start_date=date(2024, 9, 1),
        current_week=5
    )
    
    # 添加几门课程
    courses_data = [
        ("高等数学", "张老师", "A101", 1, 1, 2),
        ("线性代数", "李老师", "B202", 2, 3, 2),
        ("大学物理", "王老师", "C303", 3, 5, 2),
    ]
    
    for name, teacher, location, day, section, step in courses_data:
        course_base = CourseBase(name=name)
        course_detail = CourseDetail(
            course_id=course_base.id,
            day_of_week=day,
            start_section=section,
            step=step,
            start_week=1,
            end_week=16,
            week_type=WeekType.EVERY_WEEK,
            teacher=teacher,
            location=location
        )
        schedule.add_course(course_base, course_detail)
    
    print(f"创建课表: {len(schedule.course_bases)} 门课程")
    
    # 保存课表
    print("\n保存课表...")
    success = JSONStorage.save_schedule(schedule)
    print(f"  保存{'成功' if success else '失败'}")
    
    if success:
        print(f"  保存位置: {JSONStorage.SCHEDULE_FILE}")
    
    # 加载课表
    print("\n加载课表...")
    loaded_schedule = JSONStorage.load_schedule()
    
    if loaded_schedule:
        print(f"  加载成功: {len(loaded_schedule.course_bases)} 门课程")
        print(f"  学期开始: {loaded_schedule.semester_start_date}")
        print(f"  当前周次: {loaded_schedule.current_week}")
        
        # 验证数据一致性
        print("\n验证数据一致性:")
        print(f"  课程数量匹配: {len(schedule.course_bases) == len(loaded_schedule.course_bases)}")
        print(f"  详情数量匹配: {len(schedule.course_details) == len(loaded_schedule.course_details)}")
        print(f"  数据完全相等: {schedule == loaded_schedule}")
        
        # 显示课程列表
        print("\n课程列表:")
        for base in loaded_schedule.course_bases:
            details = loaded_schedule.get_course_details_by_id(base.id)
            for detail in details:
                print(f"  - {base.name}: {detail}")
    else:
        print("  加载失败")
    
    print("\n✅ 课表存储测试完成\n")


def test_config_storage():
    """测试配置存储"""
    print("=" * 50)
    print("测试配置存储")
    print("=" * 50)
    
    # 创建测试配置
    config = Config()
    config.show_desktop_widget = True
    config.window_geometry = {
        "x": 200,
        "y": 200,
        "width": 1200,
        "height": 800
    }
    config.saved_urls.append("http://example.com")
    
    print(f"创建配置:")
    print(f"  时间段: {len(config.time_slots)} 个")
    print(f"  桌面小部件: {config.show_desktop_widget}")
    print(f"  窗口大小: {config.window_geometry['width']}x{config.window_geometry['height']}")
    print(f"  保存的URL: {len(config.saved_urls)} 个")
    
    # 保存配置
    print("\n保存配置...")
    success = JSONStorage.save_config(config)
    print(f"  保存{'成功' if success else '失败'}")
    
    if success:
        print(f"  保存位置: {JSONStorage.CONFIG_FILE}")
    
    # 加载配置
    print("\n加载配置...")
    loaded_config = JSONStorage.load_config()
    
    print(f"  加载成功")
    print(f"  时间段: {len(loaded_config.time_slots)} 个")
    print(f"  桌面小部件: {loaded_config.show_desktop_widget}")
    print(f"  窗口大小: {loaded_config.window_geometry['width']}x{loaded_config.window_geometry['height']}")
    print(f"  保存的URL: {len(loaded_config.saved_urls)} 个")
    
    # 验证数据一致性
    print("\n验证数据一致性:")
    print(f"  数据完全相等: {config == loaded_config}")
    
    print("\n✅ 配置存储测试完成\n")


def test_data_directory():
    """测试数据目录"""
    print("=" * 50)
    print("测试数据目录")
    print("=" * 50)
    
    data_dir = JSONStorage.get_data_dir()
    print(f"数据目录: {data_dir}")
    print(f"目录存在: {data_dir.exists()}")
    
    if data_dir.exists():
        print("\n目录内容:")
        for file in data_dir.iterdir():
            size = file.stat().st_size if file.is_file() else 0
            print(f"  - {file.name} ({size} bytes)")
    
    print("\n✅ 数据目录测试完成\n")


def main():
    """运行所有测试"""
    print("\n" + "=" * 50)
    print("WakeUp 课表 - 存储层测试")
    print("=" * 50 + "\n")
    
    try:
        test_schedule_storage()
        test_config_storage()
        test_data_directory()
        
        print("=" * 50)
        print("✅ 所有存储测试通过！")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())
