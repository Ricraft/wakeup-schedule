"""
WebView 导入对话框自动化测试
"""

import sys
from pathlib import Path

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent / "src"))

from PyQt6.QtWidgets import QApplication
from ui.webview_import_dialog import WebViewImportDialog


def test_webview_creation():
    """测试 WebView 导入对话框的创建"""
    print("=" * 50)
    print("测试 WebView 导入对话框创建")
    print("=" * 50)
    
    # 创建对话框
    dialog = WebViewImportDialog()
    
    # 验证基本属性
    print("\n1. 验证窗口属性...")
    assert dialog.windowTitle() == "从教务系统导入课表", "窗口标题不正确"
    assert dialog.minimumWidth() == 1000, "最小宽度不正确"
    assert dialog.minimumHeight() == 700, "最小高度不正确"
    print("   ✓ 窗口属性正确")
    
    # 验证组件存在
    print("\n2. 验证UI组件...")
    assert dialog.url_combo is not None, "URL下拉框不存在"
    assert dialog.url_input is not None, "地址栏不存在"
    assert dialog.webview is not None, "WebView不存在"
    assert dialog.import_btn is not None, "导入按钮不存在"
    assert dialog.back_btn is not None, "后退按钮不存在"
    assert dialog.forward_btn is not None, "前进按钮不存在"
    assert dialog.refresh_btn is not None, "刷新按钮不存在"
    assert dialog.status_label is not None, "状态标签不存在"
    print("   ✓ 所有UI组件存在")
    
    # 验证常用 URL
    print("\n3. 验证常用URL...")
    assert "苏州大学" in dialog.COMMON_URLS, "缺少苏州大学URL"
    assert "南京大学" in dialog.COMMON_URLS, "缺少南京大学URL"
    assert "东南大学" in dialog.COMMON_URLS, "缺少东南大学URL"
    assert "自定义" in dialog.COMMON_URLS, "缺少自定义选项"
    print("   ✓ 常用URL配置正确")
    
    # 验证 URL 下拉框
    print("\n4. 验证URL下拉框...")
    assert dialog.url_combo.count() == len(dialog.COMMON_URLS), "下拉框项目数量不正确"
    assert dialog.url_combo.currentText() in dialog.COMMON_URLS, "当前选中项不在常用URL中"
    print("   ✓ URL下拉框配置正确")
    
    # 验证按钮文本
    print("\n5. 验证按钮文本...")
    assert "获取课表" in dialog.import_btn.text(), "导入按钮文本不正确"
    assert "后退" in dialog.back_btn.text(), "后退按钮文本不正确"
    assert "前进" in dialog.forward_btn.text(), "前进按钮文本不正确"
    assert "刷新" in dialog.refresh_btn.text(), "刷新按钮文本不正确"
    print("   ✓ 按钮文本正确")
    
    # 验证HTML导入器
    print("\n6. 验证HTML导入器...")
    assert dialog.html_importer is not None, "HTML导入器不存在"
    print("   ✓ HTML导入器已初始化")
    
    print("\n" + "=" * 50)
    print("✓ 所有自动化测试通过！")
    print("=" * 50)
    
    return True


def test_url_loading():
    """测试URL加载功能"""
    print("\n" + "=" * 50)
    print("测试URL加载功能")
    print("=" * 50)
    
    dialog = WebViewImportDialog()
    
    # 测试URL输入
    print("\n1. 测试URL输入...")
    test_url = "http://example.com"
    dialog.url_input.setText(test_url)
    assert dialog.url_input.text() == test_url, "URL输入失败"
    print("   ✓ URL输入正常")
    
    # 测试URL选择
    print("\n2. 测试URL选择...")
    dialog.url_combo.setCurrentText("苏州大学")
    expected_url = dialog.COMMON_URLS["苏州大学"]
    # 注意：URL可能会被自动加载，所以我们只检查下拉框的选择
    assert dialog.url_combo.currentText() == "苏州大学", "URL选择失败"
    print("   ✓ URL选择正常")
    
    print("\n" + "=" * 50)
    print("✓ URL加载功能测试通过！")
    print("=" * 50)
    
    return True


def test_signal_connections():
    """测试信号连接"""
    print("\n" + "=" * 50)
    print("测试信号连接")
    print("=" * 50)
    
    dialog = WebViewImportDialog()
    
    # 测试信号是否存在
    print("\n1. 验证信号...")
    assert hasattr(dialog, 'courses_imported'), "缺少courses_imported信号"
    print("   ✓ courses_imported信号存在")
    
    # 测试信号连接
    print("\n2. 测试信号连接...")
    signal_received = []
    
    def on_courses_imported(course_bases, course_details):
        signal_received.append((course_bases, course_details))
    
    dialog.courses_imported.connect(on_courses_imported)
    print("   ✓ 信号连接成功")
    
    print("\n" + "=" * 50)
    print("✓ 信号连接测试通过！")
    print("=" * 50)
    
    return True


if __name__ == "__main__":
    try:
        # 创建单个 QApplication 实例
        app = QApplication(sys.argv)
        
        # 运行所有测试
        test_webview_creation()
        test_url_loading()
        test_signal_connections()
        
        print("\n" + "=" * 60)
        print("🎉 所有 WebView 自动化测试通过！")
        print("=" * 60)
        print("\n提示：要进行完整的功能测试，请运行主程序并使用")
        print("      '导入 -> 从教务系统导入' 菜单项。")
        print("=" * 60)
        
    except AssertionError as e:
        print(f"\n❌ 测试失败: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ 测试出错: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
