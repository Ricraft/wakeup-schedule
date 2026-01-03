# 添加新学校支持指南

本指南介绍如何为 WakeUp Schedule 添加新学校的教务系统支持。

## 概述

WakeUp Schedule 使用模块化的导入器架构，支持多种教务系统。如果你的学校使用的是强智教务系统，通常只需要简单配置即可支持。

## 方式一：配置强智系统参数

如果你的学校使用强智教务系统（URL 通常包含 `/jsxsd/`），可以通过继承 `QiangZhiImporter` 快速添加支持。

### 步骤

1. 在 `src/importers/` 目录下创建新文件，如 `your_school_importer.py`

2. 继承 `QiangZhiImporter` 并配置参数：

```python
from .qiangzhi_importer import QiangZhiImporter

class YourSchoolImporter(QiangZhiImporter):
    def __init__(self):
        super().__init__(
            school_name="你的学校名称",
            sunday_first=False,      # 课表是否以周日开头
            first_col_is_header=True # 第一列是否为节次列
        )
    
    def get_importer_name(self) -> str:
        return "你的学校教务系统"
```

3. 在 `src/importers/html_importer.py` 中注册新导入器

### 关键参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `sunday_first` | 课表第一列是否为周日 | `False` |
| `first_col_is_header` | 第一列是否为节次标题列 | `False` |
| `table_id` | 课表表格的 HTML ID | `kbtable` |
| `cell_class` | 课程单元格的 CSS 类名 | `kbcontent` |

## 方式二：创建自定义导入器

如果学校使用非强智系统，需要创建自定义导入器。

### 步骤

1. 继承 `BaseImporter` 基类：

```python
from .base_importer import BaseImporter
from ..models.course_base import CourseBase
from ..models.course_detail import CourseDetail

class CustomImporter(BaseImporter):
    
    def get_supported_formats(self):
        return ['.html', '.htm']
    
    def get_importer_name(self):
        return "自定义教务系统"
    
    def validate(self, content: str):
        # 验证内容是否为该系统的课表
        # 返回 (True, "") 或 (False, "错误信息")
        pass
    
    def parse(self, content: str):
        # 解析课表内容
        # 返回 (List[CourseBase], List[CourseDetail])
        pass
```

2. 实现 `validate` 方法检测 HTML 特征

3. 实现 `parse` 方法解析课程数据

## 测试新导入器

1. 从教务系统保存课表页面为 HTML 文件

2. 创建测试文件 `tests/test_your_school_importer.py`

3. 运行测试：
```bash
pytest tests/test_your_school_importer.py -v
```

## 提交贡献

1. Fork 本仓库
2. 创建分支 `git checkout -b feature/add-your-school`
3. 提交更改并创建 Pull Request

欢迎为更多学校添加支持！
