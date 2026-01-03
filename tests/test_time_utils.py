"""
测试时间工具函数
"""

import sys
from pathlib import Path
from datetime import date, timedelta

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from utils.time_utils import (
    calculate_week_number,
    is_odd_week,
    is_even_week,
    get_week_start_date,
    get_week_end_date,
    get_current_week
)


def test_calculate_week_number():
    """测试周次计算"""
    print("测试周次计算...")
    
    # 学期开始日期: 2024年9月1日（周日）
    semester_start = date(2024, 9, 1)
    
    # 第 1 周（9月1日-9月7日）
    assert calculate_week_number(semester_start, date(2024, 9, 1)) == 1
    assert calculate_week_number(semester_start, date(2024, 9, 2)) == 1
    assert calculate_week_number(semester_start, date(2024, 9, 7)) == 1
    
    # 第 2 周（9月8日-9月14日）
    assert calculate_week_number(semester_start, date(2024, 9, 8)) == 2
    assert calculate_week_number(semester_start, date(2024, 9, 14)) == 2
    
    # 第 3 周
    assert calculate_week_number(semester_start, date(2024, 9, 15)) == 3
    
    # 第 10 周（11月3日）
    assert calculate_week_number(semester_start, date(2024, 11, 3)) == 10
    
    # 学期开始前
    assert calculate_week_number(semester_start, date(2024, 8, 31)) == 0
    
    print("✓ 周次计算测试通过")


def test_calculate_week_number_monday_start():
    """测试学期从周一开始的情况"""
    print("测试学期从周一开始的周次计算...")
    
    # 学期开始日期: 2024年9月2日（周一）
    semester_start = date(2024, 9, 2)
    
    # 第 1 周
    assert calculate_week_number(semester_start, date(2024, 9, 2)) == 1
    assert calculate_week_number(semester_start, date(2024, 9, 8)) == 1
    
    # 第 2 周
    assert calculate_week_number(semester_start, date(2024, 9, 9)) == 2
    assert calculate_week_number(semester_start, date(2024, 9, 15)) == 2
    
    print("✓ 周一开始的周次计算测试通过")


def test_is_odd_week():
    """测试单周判断"""
    print("测试单周判断...")
    
    assert is_odd_week(1) == True
    assert is_odd_week(3) == True
    assert is_odd_week(5) == True
    assert is_odd_week(15) == True
    
    assert is_odd_week(2) == False
    assert is_odd_week(4) == False
    assert is_odd_week(16) == False
    
    print("✓ 单周判断测试通过")


def test_is_even_week():
    """测试双周判断"""
    print("测试双周判断...")
    
    assert is_even_week(2) == True
    assert is_even_week(4) == True
    assert is_even_week(6) == True
    assert is_even_week(16) == True
    
    assert is_even_week(1) == False
    assert is_even_week(3) == False
    assert is_even_week(15) == False
    
    print("✓ 双周判断测试通过")


def test_get_week_start_date():
    """测试获取周开始日期"""
    print("测试获取周开始日期...")
    
    # 学期开始日期: 2024年9月1日（周日）
    semester_start = date(2024, 9, 1)
    
    # 第 1 周的开始日期就是学期开始日期
    week1_start = get_week_start_date(semester_start, 1)
    assert week1_start == date(2024, 9, 1), f"第1周开始应该是9月1日，实际是{week1_start}"
    
    # 第 2 周的开始日期应该是 9月8日（第1周 + 7天）
    week2_start = get_week_start_date(semester_start, 2)
    assert week2_start == date(2024, 9, 8), f"第2周开始应该是9月8日，实际是{week2_start}"
    
    # 第 3 周的开始日期应该是 9月15日
    week3_start = get_week_start_date(semester_start, 3)
    assert week3_start == date(2024, 9, 15), f"第3周开始应该是9月15日，实际是{week3_start}"
    
    print("✓ 获取周开始日期测试通过")


def test_get_week_start_date_monday_start():
    """测试学期从周一开始时获取周开始日期"""
    print("测试学期从周一开始时获取周开始日期...")
    
    # 学期开始日期: 2024年9月2日（周一）
    semester_start = date(2024, 9, 2)
    
    # 第 1 周的开始日期就是学期开始日期
    week1_start = get_week_start_date(semester_start, 1)
    assert week1_start == date(2024, 9, 2), f"第1周开始应该是9月2日，实际是{week1_start}"
    
    # 第 2 周的开始日期应该是 9月9日
    week2_start = get_week_start_date(semester_start, 2)
    assert week2_start == date(2024, 9, 9), f"第2周开始应该是9月9日，实际是{week2_start}"
    
    print("✓ 周一开始时获取周开始日期测试通过")


def test_get_week_end_date():
    """测试获取周结束日期"""
    print("测试获取周结束日期...")
    
    # 学期开始日期: 2024年9月1日（周日）
    semester_start = date(2024, 9, 1)
    
    # 第 1 周的结束日期应该是 9月7日（9月1日 + 6天）
    week1_end = get_week_end_date(semester_start, 1)
    assert week1_end == date(2024, 9, 7), f"第1周结束应该是9月7日，实际是{week1_end}"
    
    # 第 2 周的结束日期应该是 9月14日
    week2_end = get_week_end_date(semester_start, 2)
    assert week2_end == date(2024, 9, 14), f"第2周结束应该是9月14日，实际是{week2_end}"
    
    print("✓ 获取周结束日期测试通过")


def test_get_current_week():
    """测试获取当前周次"""
    print("测试获取当前周次...")
    
    # 使用一个过去的日期作为学期开始
    semester_start = date(2024, 9, 1)
    current_week = get_current_week(semester_start)
    
    # 验证返回的是一个正整数
    assert isinstance(current_week, int)
    assert current_week > 0
    
    # 手动计算验证
    today = date.today()
    expected_week = calculate_week_number(semester_start, today)
    assert current_week == expected_week
    
    print(f"✓ 获取当前周次测试通过（当前是第 {current_week} 周）")


def test_week_number_consistency():
    """测试周次计算的一致性"""
    print("测试周次计算的一致性...")
    
    semester_start = date(2024, 9, 1)
    
    # 同一周内的所有日期应该返回相同的周次
    for week in range(1, 5):
        week_start = get_week_start_date(semester_start, week)
        week_end = get_week_end_date(semester_start, week)
        
        # 检查这一周的每一天
        current_date = week_start
        while current_date <= week_end:
            calculated_week = calculate_week_number(semester_start, current_date)
            assert calculated_week == week, \
                f"日期 {current_date} 应该在第 {week} 周，但计算结果是第 {calculated_week} 周"
            current_date += timedelta(days=1)
    
    print("✓ 周次计算一致性测试通过")


if __name__ == "__main__":
    print("=" * 50)
    print("开始测试时间工具函数")
    print("=" * 50)
    
    test_calculate_week_number()
    test_calculate_week_number_monday_start()
    test_is_odd_week()
    test_is_even_week()
    test_get_week_start_date()
    test_get_week_start_date_monday_start()
    test_get_week_end_date()
    test_get_current_week()
    test_week_number_consistency()
    
    print("=" * 50)
    print("✓ 所有时间工具函数测试通过！")
    print("=" * 50)
