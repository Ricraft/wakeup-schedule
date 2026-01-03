好的！以下是完整的添加新教务系统操作文档：

---

# 如何为新学校添加强智教务系统支持

## 📋 目录

1. [前置准备](#前置准备)
2. [快速开始](#快速开始)
3. [详细步骤](#详细步骤)
4. [配置参数详解](#配置参数详解)
5. [常见场景配置](#常见场景配置)
6. [测试验证](#测试验证)
7. [集成到主程序](#集成到主程序)
8. [故障排查](#故障排查)

---

## 前置准备

### 1. 获取课表 HTML 文件

从你学校的教务系统导出课表 HTML 文件：

1. 登录教务系统
2. 进入"我的课表"或"个人课表"页面
3. 右键 → "另存为" → 保存为 `.html` 文件
4. 将文件保存到项目根目录，命名为 `your_school_sample.html`

### 2. 分析 HTML 结构

使用浏览器开发者工具（F12）或文本编辑器打开 HTML 文件，查看关键信息：

```html
<!-- 查找课表的 table 标签 -->
<table id="kbtable">  <!-- 记录 id 属性 -->
  <tr>
    <td>节次</td>  <!-- 第一列是否为表头？ -->
    <td>周一</td>  <!-- 还是周日？ -->
    ...
  </tr>
  <tr>
    <td>1-2节</td>
    <td>
      <div class="kbcontent">  <!-- 记录 class 属性 -->
        <!-- 课程信息格式 -->
      </div>
    </td>
  </tr>
</table>
```

### 3. 确定关键特征

记录以下信息：

- ✅ 表格 ID（通常是 `kbtable`）
- ✅ 课程容器 class（通常是 `kbcontent`）
- ✅ 第一列是"节次"还是"周一"？
- ✅ 如果第一列是"周一"，那是周一还是周日？
- ✅ 课程块之间的分隔符（如 `----` 或 `====`）
- ✅ 字段标识方式（`<font title="老师">` 还是 `老师|张三`）

---

## 快速开始

### 最简单的情况（与南华大学相同）

如果你的学校教务系统与南华大学完全相同，只需修改学校名称：

```python
# 文件: src/importers/your_school_importer.py

from .qiangzhi_importer import QiangZhiImporter

class YourSchoolImporter(QiangZhiImporter):
    def __init__(self):
        super().__init__(
            school_name="你的学校名称",
            sunday_first=False,
            first_col_is_header=True,
            split_pattern=r'-{10,}',
            exclude_courses=["教学资料", ""]
        )
    
    def get_importer_name(self) -> str:
        return "你的学校教务系统"
```

---

## 详细步骤

### 步骤 1: 创建导入器文件

在 `src/importers/` 目录下创建新文件，命名规则：`学校简称_importer.py`

例如：
- 湖南大学 → `hnu_importer.py`
- 中南大学 → `csu_importer.py`
- 湘潭大学 → `xtu_importer.py`

### 步骤 2: 编写导入器类

```python
"""
你的学校教务系统导入器

针对你的学校强智教务系统的专用解析器
"""

try:
    from .qiangzhi_importer import QiangZhiImporter
except ImportError:
    from importers.qiangzhi_importer import QiangZhiImporter


class YourSchoolImporter(QiangZhiImporter):
    """
    你的学校教务系统导入器
    
    解析你的学校强智教务系统导出的 HTML 课表文件
    """
    
    def __init__(self):
        """初始化导入器"""
        super().__init__(
            school_name="你的学校名称",
            
            # === 核心配置（必须根据实际情况调整） ===
            sunday_first=False,              # 是否星期日开头
            first_col_is_header=True,        # 第一列是否为表头
            split_pattern=r'-{10,}',         # 课程块分隔符
            
            # === 标准配置（通常不需要修改） ===
            table_id='kbtable',
            cell_class='kbcontent',
            week_pattern=r'([\d\-,]+)\(周\)',
            section_pattern=r'\[(\d+)-(\d+)节\]',
            teacher_title='老师',
            location_title='教室',
            week_section_title='周次(节次)',
            odd_week_keyword='单周',
            even_week_keyword='双周',
            exclude_courses=["教学资料", ""]
        )
    
    def get_importer_name(self) -> str:
        """获取导入器名称"""
        return "你的学校教务系统"
```

### 步骤 3: 创建测试文件

在项目根目录创建 `test_your_school_importer.py`：

```python
"""
你的学校教务系统导入器测试
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from importers.your_school_importer import YourSchoolImporter


def test_real_html():
    """测试真实 HTML 文件"""
    
    html_file = "your_school_sample.html"
    
    if not os.path.exists(html_file):
        print(f"❌ 文件不存在: {html_file}")
        print("请将你的课表 HTML 文件保存为此文件名")
        return
    
    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    print("=" * 60)
    print("测试你的学校教务系统导入器")
    print("=" * 60)
    
    importer = YourSchoolImporter()
    
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
        print("-" * 60)
        
        for course in course_bases:
            print(f"\n📚 {course.name}")
            print(f"   ID: {course.id[:8]}...")
            print(f"   颜色: {course.color}")
            
            details = [d for d in course_details if d.course_id == course.id]
            print(f"   上课时间: {len(details)} 个")
            
            for detail in details:
                week_type = detail.week_type.to_chinese()
                print(f"   • 周{detail.day_of_week} 第{detail.start_section}-{detail.end_section}节")
                print(f"     {detail.start_week}-{detail.end_week}周 ({week_type})")
                print(f"     教师: {detail.teacher}, 地点: {detail.location}")
        
        print("\n" + "=" * 60)
        print("✅ 测试完成!")
        
    except Exception as e:
        print(f"\n❌ 解析失败: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    test_real_html()
```

### 步骤 4: 运行测试

```bash
python test_your_school_importer.py
```

如果解析成功，你会看到：
```
✅ 成功解析 X 门课程
✅ 共 X 个上课时间
📚 课程名称
   • 周X 第X-X节
   ...
```

---

## 配置参数详解

### 核心参数（必须配置）

#### 1. `sunday_first` - 星期日是否在第一列

**如何判断？**

查看 HTML 表格的表头行：

```html
<!-- 情况 A: 周一在第一列 -->
<tr>
  <td>节次</td>
  <td>周一</td>  <!-- 第一列（索引1）是周一 -->
  <td>周二</td>
  ...
</tr>
<!-- 配置: sunday_first=False -->

<!-- 情况 B: 周日在第一列 -->
<tr>
  <td>节次</td>
  <td>周日</td>  <!-- 第一列（索引1）是周日 -->
  <td>周一</td>
  ...
</tr>
<!-- 配置: sunday_first=True -->
```

#### 2. `first_col_is_header` - 第一列是否为表头

**如何判断？**

查看表格第一列的内容：

```html
<!-- 情况 A: 第一列是节次（表头） -->
<tr>
  <td>1-2节</td>  <!-- 这是节次描述，不是课程 -->
  <td>课程内容</td>
  ...
</tr>
<!-- 配置: first_col_is_header=True -->

<!-- 情况 B: 第一列就是周一/周日的课程 -->
<tr>
  <td>课程内容</td>  <!-- 这是第一天的课程 -->
  <td>课程内容</td>
  ...
</tr>
<!-- 配置: first_col_is_header=False -->
```

#### 3. `split_pattern` - 课程块分隔符

**如何判断？**

查看同一单元格内多门课程的分隔方式：

```html
<!-- 情况 A: 长横线分隔（10个以上） -->
<div class="kbcontent">
  课程A信息
  --------------------
  课程B信息
</div>
<!-- 配置: split_pattern=r'-{10,}' -->

<!-- 情况 B: 短横线分隔（5个以上） -->
<div class="kbcontent">
  课程A信息
  -----
  课程B信息
</div>
<!-- 配置: split_pattern=r'-{5,}' -->

<!-- 情况 C: 等号分隔 -->
<div class="kbcontent">
  课程A信息
  ==========
  课程B信息
</div>
<!-- 配置: split_pattern=r'={5,}' -->
```

### 标准参数（通常不需要修改）

#### 4. `table_id` - 课表 table 的 id

```html
<table id="kbtable">  <!-- 默认值 -->
<!-- 如果你的系统使用不同的 id，如: -->
<table id="coursetable">
<!-- 则配置: table_id='coursetable' -->
```

#### 5. `cell_class` - 课程容器的 class

```html
<div class="kbcontent">  <!-- 默认值 -->
<!-- 如果你的系统使用不同的 class，如: -->
<div class="course-cell">
<!-- 则配置: cell_class='course-cell' -->
```

#### 6. `week_pattern` - 周次提取正则

```python
# 默认格式: "1-8(周)" 或 "1-8,10-12(周)"
week_pattern=r'([\d\-,]+)\(周\)'

# 如果格式是 "第1-8周"
week_pattern=r'第([\d\-,]+)周'

# 如果格式是 "wk1-8"
week_pattern=r'wk([\d\-,]+)'
```

#### 7. `section_pattern` - 节次提取正则

```python
# 默认格式: "[01-02节]"
section_pattern=r'\[(\d+)-(\d+)节\]'

# 如果格式是 "第1-2节"
section_pattern=r'第(\d+)-(\d+)节'

# 如果格式是 "1-2"
section_pattern=r'(\d+)-(\d+)'
```

#### 8. 字段标题参数

```python
# 如果你的系统使用 <font title="..."> 标签
teacher_title='老师'        # <font title="老师">张三</font>
location_title='教室'       # <font title="教室">A101</font>
week_section_title='周次(节次)'  # <font title="周次(节次)">...</font>

# 如果你的系统使用不同的标题
teacher_title='教师'
location_title='上课地点'
week_section_title='时间'
```

#### 9. 周类型关键字

```python
# 默认值
odd_week_keyword='单周'
even_week_keyword='双周'

# 如果你的系统使用不同的关键字
odd_week_keyword='奇数周'
even_week_keyword='偶数周'
```

#### 10. `exclude_courses` - 排除课程列表

```python
# 默认排除
exclude_courses=["教学资料", ""]

# 根据你的系统添加需要排除的内容
exclude_courses=["教学资料", "选课说明", "备注", ""]
```

---

## 常见场景配置

### 场景 1: 标准强智系统（与南华大学相同）

```python
super().__init__(
    school_name="你的学校",
    sunday_first=False,
    first_col_is_header=True,
    split_pattern=r'-{10,}'
)
```

### 场景 2: 周日在第一列

```python
super().__init__(
    school_name="你的学校",
    sunday_first=True,          # ← 改为 True
    first_col_is_header=True,
    split_pattern=r'-{10,}'
)
```

### 场景 3: 第一列直接是课程（无节次列）

```python
super().__init__(
    school_name="你的学校",
    sunday_first=False,
    first_col_is_header=False,  # ← 改为 False
    split_pattern=r'-{10,}'
)
```

### 场景 4: 使用短横线分隔

```python
super().__init__(
    school_name="你的学校",
    sunday_first=False,
    first_col_is_header=True,
    split_pattern=r'-{5,}'      # ← 改为 5 个以上
)
```

### 场景 5: 使用等号分隔

```python
super().__init__(
    school_name="你的学校",
    sunday_first=False,
    first_col_is_header=True,
    split_pattern=r'={5,}'      # ← 改为等号
)
```

### 场景 6: 不同的表格 ID

```python
super().__init__(
    school_name="你的学校",
    sunday_first=False,
    first_col_is_header=True,
    split_pattern=r'-{10,}',
    table_id='coursetable'      # ← 修改 table id
)
```

### 场景 7: 不同的字段标题

```python
super().__init__(
    school_name="你的学校",
    sunday_first=False,
    first_col_is_header=True,
    split_pattern=r'-{10,}',
    teacher_title='教师',       # ← 修改字段标题
    location_title='上课地点',
    week_section_title='时间'
)
```

---

## 测试验证

### 1. 基本验证

```bash
python test_your_school_importer.py
```

检查输出：
- ✅ 验证结果应该为 `True`
- ✅ 应该解析出正确数量的课程
- ✅ 每门课程的信息应该完整（教师、地点、时间）

### 2. 详细检查

验证以下内容：

#### 课程名称
- ✅ 课程名称是否正确？
- ✅ 是否去除了班级括号（如 "(机械15)"）？
- ✅ 是否过滤了干扰项（如 "教学资料"）？

#### 时间信息
- ✅ 星期几是否正确？（周一=1, 周日=7）
- ✅ 节次是否正确？
- ✅ 周次范围是否正确？

#### 教师和地点
- ✅ 教师姓名是否正确？
- ✅ 教室地点是否正确？

#### 周类型
- ✅ 单周课程是否标记为"单周"？
- ✅ 双周课程是否标记为"双周"？
- ✅ 每周课程是否标记为"每周"？

### 3. 边界情况测试

测试以下特殊情况：

- ✅ 同一单元格多门课程
- ✅ 跨多周的课程（如 1-8,10-16周）
- ✅ 单周/双周课程
- ✅ 周日的课程
- ✅ 空单元格

---

## 集成到主程序

### 步骤 1: 注册导入器

编辑 `src/ui/main_window.py`，在导入器列表中添加你的导入器：

```python
# 找到这一段代码
from importers.html_importer import HTMLImporter
from importers.text_importer import TextImporter
from importers.excel_importer import ExcelImporter
from importers.usc_importer import USCImporter
from importers.your_school_importer import YourSchoolImporter  # ← 添加这行

# 找到导入器列表
self.importers = [
    HTMLImporter(),
    TextImporter(),
    ExcelImporter(),
    USCImporter(),
    YourSchoolImporter()  # ← 添加这行
]
```

### 步骤 2: 测试集成

1. 运行主程序：
```bash
python main.py
```

2. 点击"导入课程" → "从文件导入"

3. 在导入器下拉列表中应该能看到"你的学校教务系统"

4. 选择你的 HTML 文件进行导入

5. 验证导入结果

---

## 故障排查

### 问题 1: 验证失败 - "未找到课表"

**原因**: `table_id` 配置错误

**解决方案**:
1. 打开 HTML 文件，搜索 `<table`
2. 查看 `id` 属性的值
3. 修改配置中的 `table_id` 参数

### 问题 2: 解析到 0 门课程

**可能原因**:
- `cell_class` 配置错误
- `split_pattern` 配置错误
- 课程内容格式不符合预期

**解决方案**:
1. 检查 `<div class="...">` 的 class 值
2. 检查课程块之间的分隔符
3. 添加调试输出查看原始 HTML

### 问题 3: 星期几错误

**原因**: `sunday_first` 或 `first_col_is_header` 配置错误

**解决方案**:
1. 检查表头第一列是"节次"还是"周一/周日"
2. 如果是"节次"，设置 `first_col_is_header=True`
3. 如果第一列是"周日"，设置 `sunday_first=True`

### 问题 4: 教师/地点信息缺失

**原因**: 字段标题配置错误

**解决方案**:
1. 检查 HTML 中 `<font title="...">` 的 title 值
2. 修改 `teacher_title`、`location_title` 等参数
3. 如果没有 `<font>` 标签，检查是否使用 `|` 分隔的文本格式

### 问题 5: 周次解析错误

**原因**: `week_pattern` 配置错误

**解决方案**:
1. 查看 HTML 中周次的格式（如 "1-8(周)" 或 "第1-8周"）
2. 修改 `week_pattern` 正则表达式
3. 确保正则表达式能捕获数字部分

---

## 完整示例

以下是一个完整的示例，假设为"湖南大学"添加支持：

```python
"""
湖南大学教务系统导入器
"""

try:
    from .qiangzhi_importer import QiangZhiImporter
except ImportError:
    from importers.qiangzhi_importer import QiangZhiImporter


class HNUImporter(QiangZhiImporter):
    """
    湖南大学教务系统导入器
    """
    
    def __init__(self):
        super().__init__(
            school_name="湖南大学",
            sunday_first=False,
            first_col_is_header=True,
            split_pattern=r'-{10,}',
            table_id='kbtable',
            cell_class='kbcontent',
            week_pattern=r'([\d\-,]+)\(周\)',
            section_pattern=r'\[(\d+)-(\d+)节\]',
            teacher_title='老师',
            location_title='教室',
            week_section_title='周次(节次)',
            odd_week_keyword='单周',
            even_week_keyword='双周',
            exclude_courses=["教学资料", ""]
        )
    
    def get_importer_name(self) -> str:
        return "湖南大学教务系统"
```

---

## 总结

添加新学校支持只需要：

1. ✅ 获取课表 HTML 样本
2. ✅ 分析 HTML 结构
3. ✅ 创建导入器类（20-30 行代码）
4. ✅ 配置参数（主要是 3 个核心参数）
5. ✅ 测试验证
6. ✅ 集成到主程序

整个过程通常只需要 **15-30 分钟**！

如果遇到问题，请参考故障排查部分，或查看 `USCImporter` 的实现作为参考。

---

**祝你成功！** 🎉