# 示例文件目录

本目录包含用于测试和演示的示例文件。

## 📁 文件列表

### HTML 示例
- `test_usc_sample.html` - 南华大学课表 HTML 示例
  - 用途：测试 USC 导入器
  - 格式：强智教务系统标准格式
  - 包含：多门课程、多周次、单双周等复杂场景

- `debug_captured.html` - 调试捕获的 HTML
  - 用途：调试和故障排查
  - 来源：实际教务系统导出

### Excel 示例
- `schedule_template.xlsx` - **标准 Excel 模板** ⭐ 新增
  - 用途：用户填写课表的标准模板
  - 格式：标准化的课表格式
  - 包含：示例数据和详细使用说明
  - 推荐：所有用户使用此模板导入课表

- `test_schedule.xlsx` - Excel 课表示例
  - 用途：测试 Excel 导入器
  - 格式：标准 Excel 课表格式
  - 包含：课程名称、教师、地点、时间等信息

## 🎯 使用方法

### 测试导入器

#### 测试 USC 导入器
```python
from importers.usc_importer import USCImporter

with open('examples/test_usc_sample.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

importer = USCImporter()
course_bases, course_details = importer.parse(html_content)

print(f"解析到 {len(course_bases)} 门课程")
```

#### 测试 Excel 导入器
```python
from importers.excel_importer import ExcelImporter

importer = ExcelImporter()
course_bases, course_details = importer.parse('examples/test_schedule.xlsx')

print(f"解析到 {len(course_bases)} 门课程")
```

### 在应用中使用

1. 启动应用：`python main.py`
2. 点击"导入课程" → "从文件导入"
3. 选择 `examples/` 目录中的示例文件
4. 查看导入结果

## 📝 创建自己的示例

### HTML 格式
如果你想为你的学校创建示例文件：

1. 登录教务系统
2. 进入课表页面
3. 右键 → "另存为" → 保存为 `.html`
4. 将文件放入 `examples/` 目录
5. 命名格式：`your_school_sample.html`

### Excel 格式
Excel 文件应包含以下列：

| 课程名称 | 教师 | 地点 | 星期 | 开始节次 | 结束节次 | 开始周 | 结束周 | 周类型 |
|---------|------|------|------|---------|---------|--------|--------|--------|
| 高等数学 | 张三 | A101 | 1 | 1 | 2 | 1 | 16 | 每周 |

## 🔍 示例文件说明

### test_usc_sample.html

这是一个完整的南华大学课表示例，包含：

- ✅ 7 门不同课程
- ✅ 多种时间段（1-2节、3-4节）
- ✅ 不同周次范围（1-16周、1-8周、9-16周）
- ✅ 单周/双周课程
- ✅ 同一单元格多门课程
- ✅ 不同教师和地点

### test_schedule.xlsx

这是一个标准的 Excel 课表示例，适合：

- ✅ 测试 Excel 导入功能
- ✅ 演示 Excel 格式要求
- ✅ 作为创建自己课表的模板

### debug_captured.html

这是从实际教务系统捕获的 HTML，用于：

- ✅ 调试解析问题
- ✅ 测试边界情况
- ✅ 验证兼容性

## ⚠️ 注意事项

1. **隐私保护**：示例文件中的个人信息（姓名、学号等）已脱敏处理
2. **格式标准**：示例文件遵循各自格式的标准规范
3. **测试用途**：这些文件仅用于测试，不代表真实课表
4. **版本兼容**：示例文件会随着系统更新而更新

## 🤝 贡献示例

如果你想贡献新的示例文件：

1. 确保文件已脱敏（移除个人信息）
2. 添加清晰的文件说明
3. 测试文件可以正常导入
4. 提交 Pull Request

---

**最后更新**: 2026-01-01
