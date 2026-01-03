"""
测试文本导入器
"""

import sys
from pathlib import Path

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from importers.text_importer import TextImporter
from models.week_type import WeekType


def test_validate():
    """测试验证功能"""
    print("测试验证功能...")
    
    importer = TextImporter()
    
    # 测试空内容
    valid, msg = importer.validate("")
    assert not valid, "应该拒绝空内容"
    
    # 测试无效格式
    valid, msg = importer.validate("这是无效的内容")
    assert not valid, "应该拒绝无效格式"
    
    # 测试有效格式
    valid_text = "周一 1-2节 高等数学 张老师 A101 1-16周"
    valid, msg = importer.validate(valid_text)
    assert valid, f"应该接受有效格式: {msg}"
    
    print("✓ 验证功能测试通过")


def test_parse_simple():
    """测试解析简单文本"""
    print("测试解析简单文本...")
    
    importer = TextImporter()
    
    text = """周一 1-2节 高等数学 张老师 A101 1-16周
周二 3-4节 线性代数 李老师 B202 1-16周"""
    
    course_bases, course_details = importer.parse(text)
    
    # 验证课程数量
    assert len(course_bases) == 2, f"应该有2门课程，实际有{len(course_bases)}门"
    assert len(course_details) == 2, f"应该有2个课程详情，实际有{len(course_details)}个"
    
    # 验证第一门课程
    course1 = course_bases[0]
    assert course1.name == "高等数学"
    
    detail1 = course_details[0]
    assert detail1.teacher == "张老师"
    assert detail1.location == "A101"
    assert detail1.day_of_week == 1, f"应该是周一(1)，实际是{detail1.day_of_week}"
    assert detail1.start_section == 1
    assert detail1.step == 2
    assert detail1.start_week == 1
    assert detail1.end_week == 16
    assert detail1.week_type == WeekType.EVERY_WEEK
    
    # 验证第二门课程
    course2 = course_bases[1]
    assert course2.name == "线性代数"
    
    detail2 = course_details[1]
    assert detail2.teacher == "李老师"
    assert detail2.location == "B202"
    assert detail2.day_of_week == 2, f"应该是周二(2)，实际是{detail2.day_of_week}"
    assert detail2.start_section == 3
    assert detail2.step == 2
    
    print("✓ 解析简单文本测试通过")


def test_parse_week_types():
    """测试解析单双周"""
    print("测试解析单双周...")
    
    importer = TextImporter()
    
    text = """周一 1-2节 课程A 老师A 地点A 1-16周
周二 1-2节 课程B 老师B 地点B 1-16周(单)
周三 1-2节 课程C 老师C 地点C 1-16周(双)"""
    
    course_bases, course_details = importer.parse(text)
    
    assert len(course_details) == 3
    
    # 验证周类型
    assert course_details[0].week_type == WeekType.EVERY_WEEK, "课程A应该是每周"
    assert course_details[1].week_type == WeekType.ODD_WEEK, "课程B应该是单周"
    assert course_details[2].week_type == WeekType.EVEN_WEEK, "课程C应该是双周"
    
    print("✓ 解析单双周测试通过")


def test_parse_all_days():
    """测试解析所有星期"""
    print("测试解析所有星期...")
    
    importer = TextImporter()
    
    text = """周一 1-2节 课程1 老师1 地点1 1-16周
周二 1-2节 课程2 老师2 地点2 1-16周
周三 1-2节 课程3 老师3 地点3 1-16周
周四 1-2节 课程4 老师4 地点4 1-16周
周五 1-2节 课程5 老师5 地点5 1-16周
周六 1-2节 课程6 老师6 地点6 1-16周
周日 1-2节 课程7 老师7 地点7 1-16周"""
    
    course_bases, course_details = importer.parse(text)
    
    assert len(course_details) == 7
    
    # 验证星期
    for i, detail in enumerate(course_details):
        expected_day = i + 1
        assert detail.day_of_week == expected_day, f"课程{i+1}应该是周{expected_day}，实际是周{detail.day_of_week}"
    
    print("✓ 解析所有星期测试通过")


def test_parse_same_course_different_times():
    """测试同一门课程在不同时间"""
    print("测试同一门课程在不同时间...")
    
    importer = TextImporter()
    
    text = """周一 1-2节 高等数学 张老师 A101 1-16周
周三 3-4节 高等数学 张老师 A101 1-16周"""
    
    course_bases, course_details = importer.parse(text)
    
    # 同一门课程应该只有一个 CourseBase
    assert len(course_bases) == 1, f"同一门课程应该只有1个CourseBase，实际有{len(course_bases)}个"
    assert course_bases[0].name == "高等数学"
    
    # 但应该有两个 CourseDetail（不同时间）
    assert len(course_details) == 2, f"应该有2个CourseDetail，实际有{len(course_details)}个"
    
    # 验证两个详情关联到同一个课程
    assert course_details[0].course_id == course_details[1].course_id
    
    print("✓ 同一门课程在不同时间测试通过")


def test_parse_with_empty_lines():
    """测试包含空行的文本"""
    print("测试包含空行的文本...")
    
    importer = TextImporter()
    
    text = """周一 1-2节 高等数学 张老师 A101 1-16周

周二 3-4节 线性代数 李老师 B202 1-16周

"""
    
    course_bases, course_details = importer.parse(text)
    
    # 应该忽略空行
    assert len(course_bases) == 2
    assert len(course_details) == 2
    
    print("✓ 包含空行的文本测试通过")


def test_get_supported_formats():
    """测试获取支持的格式"""
    print("测试获取支持的格式...")
    
    importer = TextImporter()
    formats = importer.get_supported_formats()
    
    assert '.txt' in formats
    
    print("✓ 获取支持的格式测试通过")


if __name__ == "__main__":
    print("=" * 50)
    print("开始测试文本导入器")
    print("=" * 50)
    
    test_validate()
    test_parse_simple()
    test_parse_week_types()
    test_parse_all_days()
    test_parse_same_course_different_times()
    test_parse_with_empty_lines()
    test_get_supported_formats()
    
    print("=" * 50)
    print("✓ 所有文本导入器测试通过！")
    print("=" * 50)
