"""
测试 Excel 导入器
"""

import sys
from pathlib import Path

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from importers.excel_importer import ExcelImporter
from models.week_type import WeekType


def test_validate():
    """测试验证功能"""
    print("测试验证功能...")
    
    importer = ExcelImporter()
    
    # 测试空路径
    valid, msg = importer.validate("")
    assert not valid, "应该拒绝空路径"
    
    # 测试不存在的文件
    valid, msg = importer.validate("nonexistent.xlsx")
    assert not valid, "应该拒绝不存在的文件"
    
    # 测试有效文件
    test_file = Path(__file__).parent / "test_schedule.xlsx"
    if test_file.exists():
        valid, msg = importer.validate(str(test_file))
        assert valid, f"应该接受有效文件: {msg}"
    else:
        print("  警告: 测试文件不存在，跳过有效文件测试")
    
    print("✓ 验证功能测试通过")


def test_parse():
    """测试解析 Excel 文件"""
    print("测试解析 Excel 文件...")
    
    test_file = Path(__file__).parent / "test_schedule.xlsx"
    
    if not test_file.exists():
        print("  警告: 测试文件不存在，跳过解析测试")
        return
    
    importer = ExcelImporter()
    
    try:
        course_bases, course_details = importer.parse(str(test_file))
        
        print(f"  解析成功: {len(course_bases)} 门课程, {len(course_details)} 个详情")
        
        # 验证课程数量
        assert len(course_bases) >= 1, f"应该至少有1门课程，实际有{len(course_bases)}门"
        assert len(course_details) >= 1, f"应该至少有1个课程详情，实际有{len(course_details)}个"
        
        # 打印解析结果
        for base in course_bases:
            print(f"  课程: {base.name}, 颜色: {base.color}")
        
        for detail in course_details:
            print(f"  详情: 周{detail.day_of_week} 第{detail.start_section}节, "
                  f"{detail.teacher}, {detail.location}, "
                  f"第{detail.start_week}-{detail.end_week}周, {detail.week_type.to_chinese()}")
        
        print("✓ 解析 Excel 文件测试通过")
    except Exception as e:
        print(f"  解析失败: {e}")
        import traceback
        traceback.print_exc()
        raise


def test_get_supported_formats():
    """测试获取支持的格式"""
    print("测试获取支持的格式...")
    
    importer = ExcelImporter()
    formats = importer.get_supported_formats()
    
    assert '.xlsx' in formats
    assert '.xls' in formats
    
    print("✓ 获取支持的格式测试通过")


if __name__ == "__main__":
    print("=" * 50)
    print("开始测试 Excel 导入器")
    print("=" * 50)
    
    test_validate()
    test_parse()
    test_get_supported_formats()
    
    print("=" * 50)
    print("✓ 所有 Excel 导入器测试通过！")
    print("=" * 50)
