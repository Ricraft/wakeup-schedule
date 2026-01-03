"""
南华大学教务系统导入器测试
"""

import sys
import os

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from importers.usc_importer import USCImporter


def test_basic_parsing():
    """测试基本解析功能"""
    
    # 模拟南华大学教务系统的 HTML 格式（使用 id='kbtable'）
    # 表头顺序：节次、周一、周二、周三、周四、周五、周六、周日
    html_content = """
    <html>
    <body>
        <table id="kbtable">
            <tr>
                <td>节次</td>
                <td>周一</td>
                <td>周二</td>
                <td>周三</td>
            </tr>
            <tr>
                <td>1-2节</td>
                <td>
                    <div class="kbcontent">
                        高等数学(机械15)|老师|张三|周次(节次)|1-16(周)[01-02节]|教室|A101
                    </div>
                </td>
                <td>
                    <div class="kbcontent">
                        线性代数|老师|李四|周次(节次)|1-16(周)[03-04节]|教室|B202
                    </div>
                </td>
                <td></td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    importer = USCImporter()
    
    # 验证
    valid, msg = importer.validate(html_content)
    print(f"验证结果: {valid}, 消息: {msg}")
    assert valid, f"验证失败: {msg}"
    
    # 解析
    course_bases, course_details = importer.parse(html_content)
    
    print(f"\n解析到 {len(course_bases)} 门课程:")
    for course in course_bases:
        print(f"  - {course.name} (ID: {course.id[:8]}...)")
    
    print(f"\n解析到 {len(course_details)} 个课程详情:")
    for detail in course_details:
        print(f"  - 周{detail.day_of_week} 第{detail.start_section}-{detail.end_section}节")
        print(f"    教师: {detail.teacher}, 地点: {detail.location}")
        print(f"    周次: {detail.start_week}-{detail.end_week} ({detail.week_type.to_chinese()})")
    
    # 断言
    assert len(course_bases) == 2, f"应该有 2 门课程，实际: {len(course_bases)}"
    assert len(course_details) == 2, f"应该有 2 个课程详情，实际: {len(course_details)}"
    
    # 检查第一门课程（周一的课，col_idx=1 应该对应 day_of_week=1）
    assert course_bases[0].name == "高等数学", f"课程名称错误: {course_bases[0].name}"
    assert course_details[0].teacher == "张三", f"教师错误: {course_details[0].teacher}"
    assert course_details[0].location == "A101", f"地点错误: {course_details[0].location}"
    assert course_details[0].start_section == 1, f"开始节次错误: {course_details[0].start_section}"
    assert course_details[0].step == 2, f"持续节数错误: {course_details[0].step}"
    assert course_details[0].day_of_week == 1, f"星期几错误（应该是周一=1）: {course_details[0].day_of_week}"
    
    # 检查第二门课程（周二的课，col_idx=2 应该对应 day_of_week=2）
    assert course_details[1].day_of_week == 2, f"星期几错误（应该是周二=2）: {course_details[1].day_of_week}"
    
    print("\n✓ 所有测试通过!")


def test_multiple_courses_in_cell():
    """测试一个单元格内多门课程的情况"""
    
    html_content = """
    <html>
    <body>
        <table id="kbtable">
            <tr>
                <td>节次</td>
                <td>周一</td>
                <td>周二</td>
            </tr>
            <tr>
                <td>1-2节</td>
                <td>
                    <div class="kbcontent">
                        高等数学|老师|张三|周次(节次)|1-8(周)[01-02节]|教室|A101
                        --------------------
                        物理学|老师|王五|周次(节次)|9-16(周)[01-02节]|教室|C303
                    </div>
                </td>
                <td></td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    importer = USCImporter()
    course_bases, course_details = importer.parse(html_content)
    
    print(f"\n测试多课程单元格:")
    print(f"解析到 {len(course_bases)} 门课程")
    print(f"解析到 {len(course_details)} 个课程详情")
    
    assert len(course_bases) == 2, f"应该有 2 门课程，实际: {len(course_bases)}"
    assert len(course_details) == 2, f"应该有 2 个课程详情，实际: {len(course_details)}"
    
    print("✓ 多课程单元格测试通过!")


def test_sunday_offset():
    """测试周日课程（col_idx=7 应该对应 day_of_week=7）"""
    
    html_content = """
    <html>
    <body>
        <table id="kbtable">
            <tr>
                <td>节次</td>
                <td>周一</td>
                <td>周二</td>
                <td>周三</td>
                <td>周四</td>
                <td>周五</td>
                <td>周六</td>
                <td>周日</td>
            </tr>
            <tr>
                <td>1-2节</td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td></td>
                <td>
                    <div class="kbcontent">
                        体育课|老师|赵六|周次(节次)|1-16(周)[01-02节]|教室|操场
                    </div>
                </td>
            </tr>
        </table>
    </body>
    </html>
    """
    
    importer = USCImporter()
    course_bases, course_details = importer.parse(html_content)
    
    print(f"\n测试周日课程:")
    print(f"解析到 {len(course_bases)} 门课程")
    print(f"解析到 {len(course_details)} 个课程详情")
    
    assert len(course_bases) == 1, f"应该有 1 门课程，实际: {len(course_bases)}"
    assert len(course_details) == 1, f"应该有 1 个课程详情，实际: {len(course_details)}"
    
    # 核心测试：周日（col_idx=7）应该对应 day_of_week=7
    assert course_details[0].day_of_week == 7, f"周日应该是 7，实际: {course_details[0].day_of_week}"
    
    print(f"✓ 周日课程测试通过！周日正确对应 day_of_week=7")


def test_invalid_content():
    """测试无效内容"""
    
    importer = USCImporter()
    
    # 空内容
    valid, msg = importer.validate("")
    assert not valid, "空内容应该验证失败"
    print(f"✓ 空内容验证失败: {msg}")
    
    # 无效 HTML
    valid, msg = importer.validate("<html><body>没有课表</body></html>")
    assert not valid, "无效 HTML 应该验证失败"
    print(f"✓ 无效 HTML 验证失败: {msg}")


if __name__ == '__main__':
    print("=" * 60)
    print("南华大学教务系统导入器测试")
    print("=" * 60)
    
    test_basic_parsing()
    print("\n" + "=" * 60)
    test_multiple_courses_in_cell()
    print("\n" + "=" * 60)
    test_sunday_offset()
    print("\n" + "=" * 60)
    test_invalid_content()
    print("\n" + "=" * 60)
    print("所有测试完成!")
