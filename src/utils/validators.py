"""
数据验证工具
src/utils/validators.py
"""

from typing import Tuple

def validate_course_name(name: str) -> Tuple[bool, str]:
    if not name or not name.strip():
        return False, "课程名称不能为空"
    if len(name) > 50:
        return False, "课程名称过长"
    return True, ""

def validate_teacher_name(name: str) -> Tuple[bool, str]:
    if name and len(name) > 20:
        return False, "教师姓名过长"
    return True, ""

def validate_location(location: str) -> Tuple[bool, str]:
    if location and len(location) > 30:
        return False, "地点名称过长"
    return True, ""

def validate_section_range(start: int, end: int) -> Tuple[bool, str]:
    if start < 1 or end > 12:
        return False, "节次必须在 1-12 之间"
    if start > end:
        return False, "开始节次不能大于结束节次"
    return True, ""

def validate_week_range(start: int, end: int) -> Tuple[bool, str]:
    if start < 1 or end > 30:
        return False, "周次必须在 1-30 之间"
    if start > end:
        return False, "开始周次不能大于结束周次"
    return True, ""

def validate_note(note: str) -> Tuple[bool, str]:
    if note and len(note) > 200:
        return False, "备注不能超过 200 字"
    return True, ""

def validate_day_of_week(day: int) -> Tuple[bool, str]:
    if day < 1 or day > 7:
        return False, "无效的星期"
    return True, ""