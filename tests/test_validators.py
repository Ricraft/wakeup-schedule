"""
测试数据验证器
"""

import sys
from pathlib import Path

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from utils.validators import (
    validate_course_name,
    validate_teacher_name,
    validate_location,
    validate_day_of_week,
    validate_section_range,
    validate_week_range,
    validate_color,
    validate_note
)


def test_course_name():
    """测试课程名称验证"""
    print("测试课程名称验证...")
    
    # 有效的课程名称
    valid, msg = validate_course_name("高等数学")
    assert valid, f"应该接受有效的课程名称: {msg}"
    
    valid, msg = validate_course_name("A" * 50)
    assert valid, f"应该接受 50 字符的课程名称: {msg}"
    
    # 无效的课程名称
    valid, msg = validate_course_name("")
    assert not valid, "应该拒绝空字符串"
    assert "不能为空" in msg
    
    valid, msg = validate_course_name("   ")
    assert not valid, "应该拒绝纯空白字符串"
    assert "不能为空" in msg
    
    valid, msg = validate_course_name("A" * 51)
    assert not valid, "应该拒绝超过 50 字符的课程名称"
    assert "不能超过 50 个字符" in msg
    
    print("✓ 课程名称验证测试通过")


def test_teacher_name():
    """测试教师姓名验证"""
    print("测试教师姓名验证...")
    
    # 有效的教师姓名
    valid, msg = validate_teacher_name("张老师")
    assert valid, f"应该接受有效的教师姓名: {msg}"
    
    valid, msg = validate_teacher_name("")
    assert valid, "应该接受空教师姓名"
    
    valid, msg = validate_teacher_name("A" * 30)
    assert valid, f"应该接受 30 字符的教师姓名: {msg}"
    
    # 无效的教师姓名
    valid, msg = validate_teacher_name("A" * 31)
    assert not valid, "应该拒绝超过 30 字符的教师姓名"
    assert "不能超过 30 个字符" in msg
    
    print("✓ 教师姓名验证测试通过")


def test_location():
    """测试上课地点验证"""
    print("测试上课地点验证...")
    
    # 有效的地点
    valid, msg = validate_location("教学楼A101")
    assert valid, f"应该接受有效的地点: {msg}"
    
    valid, msg = validate_location("")
    assert valid, "应该接受空地点"
    
    valid, msg = validate_location("A" * 50)
    assert valid, f"应该接受 50 字符的地点: {msg}"
    
    # 无效的地点
    valid, msg = validate_location("A" * 51)
    assert not valid, "应该拒绝超过 50 字符的地点"
    assert "不能超过 50 个字符" in msg
    
    print("✓ 上课地点验证测试通过")


def test_day_of_week():
    """测试星期验证"""
    print("测试星期验证...")
    
    # 有效的星期
    for day in range(1, 8):
        valid, msg = validate_day_of_week(day)
        assert valid, f"应该接受星期 {day}: {msg}"
    
    # 无效的星期
    valid, msg = validate_day_of_week(0)
    assert not valid, "应该拒绝星期 0"
    assert "1-7 之间" in msg
    
    valid, msg = validate_day_of_week(8)
    assert not valid, "应该拒绝星期 8"
    assert "1-7 之间" in msg
    
    valid, msg = validate_day_of_week("1")
    assert not valid, "应该拒绝字符串类型"
    assert "必须是整数" in msg
    
    print("✓ 星期验证测试通过")


def test_section_range():
    """测试节次范围验证"""
    print("测试节次范围验证...")
    
    # 有效的节次范围
    valid, msg = validate_section_range(1, 2)
    assert valid, f"应该接受有效的节次范围: {msg}"
    
    valid, msg = validate_section_range(1, 1)
    assert valid, f"应该接受相同的开始和结束节次: {msg}"
    
    valid, msg = validate_section_range(1, 12)
    assert valid, f"应该接受 1-12 的节次范围: {msg}"
    
    # 无效的节次范围
    valid, msg = validate_section_range(2, 1)
    assert not valid, "应该拒绝开始节次大于结束节次"
    assert "不能大于" in msg
    
    valid, msg = validate_section_range(0, 2)
    assert not valid, "应该拒绝节次 0"
    assert "1-12 之间" in msg
    
    valid, msg = validate_section_range(1, 13)
    assert not valid, "应该拒绝节次 13"
    assert "1-12 之间" in msg
    
    valid, msg = validate_section_range("1", 2)
    assert not valid, "应该拒绝字符串类型"
    assert "必须是整数" in msg
    
    print("✓ 节次范围验证测试通过")


def test_week_range():
    """测试周次范围验证"""
    print("测试周次范围验证...")
    
    # 有效的周次范围
    valid, msg = validate_week_range(1, 16)
    assert valid, f"应该接受有效的周次范围: {msg}"
    
    valid, msg = validate_week_range(1, 1)
    assert valid, f"应该接受相同的开始和结束周次: {msg}"
    
    valid, msg = validate_week_range(1, 30)
    assert valid, f"应该接受 1-30 的周次范围: {msg}"
    
    # 无效的周次范围
    valid, msg = validate_week_range(16, 1)
    assert not valid, "应该拒绝开始周次大于结束周次"
    assert "不能大于" in msg
    
    valid, msg = validate_week_range(0, 16)
    assert not valid, "应该拒绝周次 0"
    assert "1-30 之间" in msg
    
    valid, msg = validate_week_range(1, 31)
    assert not valid, "应该拒绝周次 31"
    assert "1-30 之间" in msg
    
    valid, msg = validate_week_range("1", 16)
    assert not valid, "应该拒绝字符串类型"
    assert "必须是整数" in msg
    
    print("✓ 周次范围验证测试通过")


def test_color():
    """测试颜色代码验证"""
    print("测试颜色代码验证...")
    
    # 有效的颜色代码
    valid_colors = [
        "#000000",
        "#FFFFFF",
        "#4CAF50",
        "#2196F3",
        "#FF5722",
        "#abcdef",
        "#ABCDEF"
    ]
    
    for color in valid_colors:
        valid, msg = validate_color(color)
        assert valid, f"应该接受有效的颜色代码 {color}: {msg}"
    
    # 无效的颜色代码
    invalid_colors = [
        "",
        "#",
        "#12345",
        "#1234567",
        "123456",
        "#GGGGGG",
        "#12-456"
    ]
    
    for color in invalid_colors:
        valid, msg = validate_color(color)
        assert not valid, f"应该拒绝无效的颜色代码 {color}"
        if color:
            assert "十六进制" in msg or "不能为空" in msg
    
    print("✓ 颜色代码验证测试通过")


def test_note():
    """测试备注验证"""
    print("测试备注验证...")
    
    # 有效的备注
    valid, msg = validate_note("这是一个备注")
    assert valid, f"应该接受有效的备注: {msg}"
    
    valid, msg = validate_note("")
    assert valid, "应该接受空备注"
    
    valid, msg = validate_note("A" * 200)
    assert valid, f"应该接受 200 字符的备注: {msg}"
    
    # 无效的备注
    valid, msg = validate_note("A" * 201)
    assert not valid, "应该拒绝超过 200 字符的备注"
    assert "不能超过 200 个字符" in msg
    
    print("✓ 备注验证测试通过")


if __name__ == "__main__":
    print("=" * 50)
    print("开始测试数据验证器")
    print("=" * 50)
    
    test_course_name()
    test_teacher_name()
    test_location()
    test_day_of_week()
    test_section_range()
    test_week_range()
    test_color()
    test_note()
    
    print("=" * 50)
    print("✓ 所有验证器测试通过！")
    print("=" * 50)
