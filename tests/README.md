# 测试目录

本目录包含项目的所有单元测试。

## 🧪 测试文件

### 核心功能测试
- `test_models.py` - 数据模型测试
- `test_course_manager.py` - 课程管理器测试
- `test_schedule_manager.py` - 课表管理器测试
- `test_conflict_detector.py` - 冲突检测器测试
- `test_storage.py` - 存储功能测试

### 工具类测试
- `test_time_utils.py` - 时间工具测试
- `test_validators.py` - 验证器测试

### 导入器测试
- `test_html_importer.py` - HTML 导入器测试
- `test_text_importer.py` - 文本导入器测试
- `test_excel_importer.py` - Excel 导入器测试
- `test_usc_importer.py` - USC 导入器测试
- `test_usc_real_html.py` - USC 真实 HTML 测试

### UI 测试
- `test_main_window.py` - 主窗口测试
- `test_course_dialog.py` - 课程对话框测试
- `test_conflict_dialog.py` - 冲突对话框测试
- `test_settings_dialog.py` - 设置对话框测试
- `test_webview_auto.py` - WebView 自动化测试

### 集成测试
- `test_app_integration.py` - 应用集成测试

## 🚀 运行测试

### 运行所有测试
```bash
pytest
```

### 运行特定测试文件
```bash
pytest tests/test_models.py
```

### 运行特定测试函数
```bash
pytest tests/test_models.py::test_course_base_creation
```

### 查看测试覆盖率
```bash
pytest --cov=src --cov-report=html
```

### 详细输出
```bash
pytest -v
```

### 显示打印输出
```bash
pytest -s
```

## 📊 测试覆盖率

运行测试后，可以在 `htmlcov/index.html` 查看详细的覆盖率报告。

## ✅ 测试规范

### 测试文件命名
- 测试文件以 `test_` 开头
- 测试函数以 `test_` 开头
- 测试类以 `Test` 开头

### 测试结构
```python
def test_function_name():
    """测试描述"""
    # 准备 (Arrange)
    # 执行 (Act)
    # 断言 (Assert)
```

### 测试原则
1. 每个测试只测试一个功能点
2. 测试应该独立，不依赖其他测试
3. 测试应该可重复运行
4. 使用清晰的断言消息
5. 保持测试简单易懂

## 🔧 测试工具

- **pytest** - 测试框架
- **pytest-cov** - 覆盖率插件
- **pytest-qt** - Qt 应用测试

## 📝 添加新测试

1. 在 `tests/` 目录创建 `test_*.py` 文件
2. 导入需要测试的模块
3. 编写测试函数
4. 运行测试验证

示例：
```python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from models.course_base import CourseBase

def test_course_creation():
    """测试课程创建"""
    course = CourseBase(
        name="测试课程",
        course_id="test-123",
        color="#FF0000"
    )
    assert course.name == "测试课程"
    assert course.id == "test-123"
    assert course.color == "#FF0000"
```

---

**最后更新**: 2026-01-01
