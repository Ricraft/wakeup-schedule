"""
测试南华大学导入器 - 使用真实 HTML 文件
"""

import sys
import os

# 添加 src 目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from importers.usc_importer import USCImporter


def test_sample_html():
    """测试示例 HTML 文件"""
    
    # 读取示例 HTML 文件
    html_file = "test_usc_sample.html"
    
    if not os.path.exists(html_file):
        print(f"❌ 文件不存在: {html_file}")
        return
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print("=" * 60)
    print("测试南华大学教务系统导入器 - 真实 HTML")
    print("=" * 60)
    
    importer = USCImporter()
    
    # 验证
    valid, msg = importer.validate(html_content)
    print(f"\n验证结果: {valid}")
    if msg:
        print(f"消息: {msg}")
    
    if not valid:
        print("❌ 验证失败")
        return
    
    # 解析
    try:
        course_bases, course_details = importer.parse(html_content)
        
        print(f"\n✅ 成功解析 {len(course_bases)} 门课程:")
        print("-" * 60)
        
        for course in course_bases:
            print(f"\n📚 {course.name}")
            print(f"   ID: {course.id[:8]}...")
            print(f"   颜色: {course.color}")
            
            # 找到该课程的所有详情
            details = [d for d in course_details if d.course_id == course.id]
            print(f"   上课时间: {len(details)} 个")
            
            for detail in details:
                week_type = detail.week_type.to_chinese()
                print(f"   • 周{detail.day_of_week} 第{detail.start_section}-{detail.end_section}节")
                print(f"     {detail.start_week}-{detail.end_week}周 ({week_type})")
                print(f"     教师: {detail.teacher}, 地点: {detail.location}")
        
        print("\n" + "=" * 60)
        print("✅ 测试完成!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ 解析失败: {str(e)}")
        import traceback
        traceback.print_exc()


def test_user_html():
    """测试用户提供的 HTML 文件"""
    
    print("\n" + "=" * 60)
    print("测试用户 HTML 文件")
    print("=" * 60)
    
    # 让用户输入文件路径
    print("\n请将你的教务系统课表 HTML 文件放在当前目录")
    print("或输入完整路径:")
    
    file_path = input("HTML 文件路径 (直接回车跳过): ").strip()
    
    if not file_path:
        print("跳过用户 HTML 测试")
        return
    
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        return
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
    except Exception as e:
        print(f"❌ 读取文件失败: {str(e)}")
        return
    
    importer = USCImporter()
    
    # 验证
    valid, msg = importer.validate(html_content)
    print(f"\n验证结果: {valid}")
    if msg:
        print(f"消息: {msg}")
    
    if not valid:
        print("❌ 验证失败")
        return
    
    # 解析
    try:
        course_bases, course_details = importer.parse(html_content)
        
        print(f"\n✅ 成功解析 {len(course_bases)} 门课程")
        print(f"✅ 共 {len(course_details)} 个上课时间")
        
        # 显示详细信息
        for course in course_bases:
            print(f"\n📚 {course.name}")
            details = [d for d in course_details if d.course_id == course.id]
            for detail in details:
                print(f"   • 周{detail.day_of_week} 第{detail.start_section}-{detail.end_section}节")
                print(f"     {detail.teacher} @ {detail.location}")
        
        print("\n✅ 用户 HTML 测试完成!")
        
    except Exception as e:
        print(f"\n❌ 解析失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    # 测试示例 HTML
    test_sample_html()
    
    # 测试用户 HTML
    test_user_html()
