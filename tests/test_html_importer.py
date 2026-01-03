"""
测试 HTML 导入器
"""

import sys
from pathlib import Path

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from importers.html_importer import HTMLImporter
from models.week_type import WeekType


def test_validate():
    """测试验证功能"""
    print("测试验证功能...")
    
    importer = HTMLImporter()
    
    # 测试空内容
    valid, msg = importer.validate("")
    assert not valid, "应该拒绝空内容"
    assert "空" in msg
    
    # 测试无效 HTML
    valid, msg = importer.validate("<html><body>无效内容</body></html>")
    assert not valid, "应该拒绝无效 HTML"
    
    # 测试有效 HTML
    valid_html = """
    <html>
    <body>
        <table id="Table1">
            <tr>
                <td>星期一</td>
                <td>星期二</td>
            </tr>
        </table>
    </body>
    </html>
    """
    valid, msg = importer.validate(valid_html)
    assert valid, f"应该接受有效 HTML: {msg}"
    
    print("✓ 验证功能测试通过")


def test_parse_simple():
    """测试解析简单课表"""
    print("测试解析简单课表...")
    
    importer = HTMLImporter()
    
    # 构造简单的课表 HTML（更符合实际格式）
    html = """
    <html>
    <body>
        <table id="Table1">
            <tr>
                <td>时间</td>
                <td>星期一</td>
                <td>星期二</td>
            </tr>
            <tr>
                <td>第1节</td>
                <td>高等数学 周一{第1-16周 张老师 A101</td>
                <td>线性代数 周二{第1-16周(单) 李老师 B202</td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    course_bases, course_details = importer.parse(html)
    
    # 验证课程数量
    assert len(course_bases) == 2, f"应该有2门课程，实际有{len(course_bases)}门"
    assert len(course_details) == 2, f"应该有2个课程详情，实际有{len(course_details)}个"
    
    # 验证第一门课程
    course1 = course_bases[0]
    assert course1.name == "高等数学"
    assert course1.color.startswith('#')
    
    detail1 = course_details[0]
    assert detail1.teacher == "张老师"
    assert detail1.location == "A101"
    assert detail1.start_section == 1
    assert detail1.day_of_week == 1, f"应该是周一(1)，实际是{detail1.day_of_week}"
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
    assert detail2.week_type == WeekType.ODD_WEEK
    
    print("✓ 解析简单课表测试通过")


def test_parse_multiple_sections():
    """测试解析多节次课程"""
    print("测试解析多节次课程...")
    
    importer = HTMLImporter()
    
    html = """
    <html>
    <body>
        <table id="Table1">
            <tr>
                <td>时间</td>
                <td>星期一</td>
            </tr>
            <tr>
                <td>第1节</td>
                <td>高等数学 周一{第1-16周 张老师 A101</td>
            </tr>
            <tr>
                <td>第3节</td>
                <td>线性代数 周一{第1-16周 李老师 B202</td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    course_bases, course_details = importer.parse(html)
    
    assert len(course_bases) == 2
    assert len(course_details) == 2
    
    # 验证节次
    assert course_details[0].start_section == 1
    assert course_details[1].start_section == 3
    
    print("✓ 解析多节次课程测试通过")


def test_parse_same_course_different_times():
    """测试同一门课程在不同时间"""
    print("测试同一门课程在不同时间...")
    
    importer = HTMLImporter()
    
    html = """
    <html>
    <body>
        <table id="Table1">
            <tr>
                <td>时间</td>
                <td>星期一</td>
                <td>星期三</td>
            </tr>
            <tr>
                <td>第1节</td>
                <td>高等数学 周一{第1-16周 张老师 A101</td>
                <td>高等数学 周三{第1-16周 张老师 A101</td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    course_bases, course_details = importer.parse(html)
    
    # 同一门课程应该只有一个 CourseBase
    assert len(course_bases) == 1, f"同一门课程应该只有1个CourseBase，实际有{len(course_bases)}个"
    assert course_bases[0].name == "高等数学"
    
    # 但应该有两个 CourseDetail（不同时间）
    assert len(course_details) == 2, f"应该有2个CourseDetail，实际有{len(course_details)}个"
    
    # 验证两个详情关联到同一个课程
    assert course_details[0].course_id == course_details[1].course_id
    
    print("✓ 同一门课程在不同时间测试通过")


def test_parse_week_types():
    """测试解析单双周"""
    print("测试解析单双周...")
    
    importer = HTMLImporter()
    
    html = """
    <html>
    <body>
        <table id="Table1">
            <tr>
                <td>时间</td>
                <td>星期一</td>
                <td>星期二</td>
                <td>星期三</td>
            </tr>
            <tr>
                <td>第1节</td>
                <td>课程A 周一{第1-16周 老师A 地点A</td>
                <td>课程B 周二{第1-16周(单) 老师B 地点B</td>
                <td>课程C 周三{第1-16周(双) 老师C 地点C</td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    course_bases, course_details = importer.parse(html)
    
    assert len(course_details) == 3
    
    # 验证周类型
    assert course_details[0].week_type == WeekType.EVERY_WEEK, "课程A应该是每周"
    assert course_details[1].week_type == WeekType.ODD_WEEK, "课程B应该是单周"
    assert course_details[2].week_type == WeekType.EVEN_WEEK, "课程C应该是双周"
    
    print("✓ 解析单双周测试通过")


def test_get_supported_formats():
    """测试获取支持的格式"""
    print("测试获取支持的格式...")
    
    importer = HTMLImporter()
    formats = importer.get_supported_formats()
    
    assert '.html' in formats
    assert '.htm' in formats
    
    print("✓ 获取支持的格式测试通过")


if __name__ == "__main__":
    print("=" * 50)
    print("开始测试 HTML 导入器")
    print("=" * 50)
    
    test_validate()
    test_parse_simple()
    test_parse_multiple_sections()
    test_parse_same_course_different_times()
    test_parse_week_types()
    test_get_supported_formats()
    
    print("=" * 50)
    print("✓ 所有 HTML 导入器测试通过！")
    print("=" * 50)
