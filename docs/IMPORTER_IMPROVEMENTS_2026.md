# 导入器改进总结 (2026-01)

## 改进概述

本次改进重点优化了 HTML 和 Excel 导入器，实现了智能格式检测和多格式支持，大幅提升了用户体验和兼容性。

## 主要改进

### 1. HTML 导入器增强

#### 1.1 智能路由机制

**改进前**：
- 只支持特定格式（`id='Table1'`）
- 无法识别强智教务系统格式
- 解析逻辑固定，缺乏灵活性

**改进后**：
- ✅ 自动检测强智教务系统格式
- ✅ 智能路由到专用解析器
- ✅ 支持通用 HTML 表格格式
- ✅ 多层次回退机制

**技术实现**：
```python
def parse(self, content: str):
    soup = BeautifulSoup(content, 'html.parser')
    
    # 智能检测格式
    if self._is_qiangzhi_format(soup):
        return self._parse_qiangzhi_format(content)
    
    # 回退到通用格式
    return self._parse_generic_format(soup)
```

**检测特征**：
- `<table id="kbtable">` - 强智系统特征表格
- `<div class="kbcontent">` - 强智系统课程容器
- `<font title="...">` - 强智系统元数据标签
- 至少满足 2 个特征即判定为强智格式

#### 1.2 验证逻辑优化

**改进前**：
```python
# 硬编码检查特定 ID
table = soup.find('table', id='Table1')
if not table:
    return False, "未找到课表"
```

**改进后**：
```python
# 灵活检测多种格式
if self._is_qiangzhi_format(soup):
    return True, ""

tables = soup.find_all('table')
if not tables:
    return False, "未找到表格"

# 检查课表相关信息
has_weekday = any(day in text for day in ["星期一", "星期二", ...])
has_section = any(sec in text for sec in ["第1节", "第2节", ...])
```

### 2. Excel 导入器增强

#### 2.1 多格式支持

**改进前**：
- 格式假设固定（第一列=周一）
- 无法处理强智系统导出的 Excel
- 缺少表头自动检测

**改进后**：
- ✅ 自动检测强智系统格式
- ✅ 智能识别表头位置
- ✅ 支持多种星期格式（中英文）
- ✅ 支持简化格式（课程名 教师 地点）

**格式检测**：
```python
def _detect_format(self, sheet: Worksheet) -> str:
    rows = list(sheet.iter_rows(values_only=True, max_row=10))
    
    for row in rows:
        for cell in row:
            if cell and isinstance(cell, str):
                # 检测强智系统特征
                if '{第' in cell and '周' in cell:
                    return "qiangzhi"
    
    return "standard"
```

#### 2.2 表头智能识别

**支持的星期格式**：
- 中文：周一、星期一
- 英文：Monday、Mon
- 其他：Tuesday、Tue、Wednesday、Wed 等

**自动定位**：
```python
# 查找表头行
for idx, row in enumerate(rows):
    for col_idx, cell in enumerate(row):
        if cell and isinstance(cell, str):
            for weekday_name, weekday_num in self.weekday_names.items():
                if weekday_name in cell:
                    header_row_idx = idx
                    weekday_col_map[col_idx] = weekday_num
```

#### 2.3 单元格解析增强

**支持的格式**：

1. **完整格式**（强智系统）：
   ```
   高等数学 {第1-16周 张老师 A101
   ```

2. **简化格式**：
   ```
   高等数学 张老师 A101
   ```
   （默认周次为 1-16 周）

3. **单双周标记**：
   ```
   线性代数 {第1-16周(单) 李老师 B202
   大学物理 {第1-16周(双) 王老师 C303
   ```

### 3. 标准模板创建

#### 3.1 Excel 模板

**文件位置**：`examples/schedule_template.xlsx`

**特点**：
- ✅ 标准化格式
- ✅ 示例数据
- ✅ 详细使用说明
- ✅ 美观的样式设计

**工作表**：
1. **课表** - 主要数据表
   - 表头：节次、周一~周日
   - 12 个节次行
   - 预填充示例数据
   - 专业的样式设计

2. **使用说明** - 详细指南
   - 填写格式说明
   - 注意事项
   - 导入步骤
   - 常见问题解答

#### 3.2 生成脚本

**文件位置**：`scripts/create_excel_template.py`

**功能**：
- 自动生成标准模板
- 可自定义样式
- 可批量生成

**使用方法**：
```bash
python scripts/create_excel_template.py
```

### 4. 文档完善

#### 4.1 导入指南

**文件位置**：`docs/IMPORT_GUIDE.md`

**内容**：
- 支持的导入格式详解
- HTML 格式导入指南
- Excel 格式导入指南
- 文本格式导入指南
- 常见问题解答
- 高级功能说明

#### 4.2 项目结构文档

**更新内容**：
- 新增 `docs/` 目录说明
- 新增 `examples/` 目录说明
- 新增 `scripts/` 目录说明

## 技术架构

### 导入器层次结构

```
BaseImporter (抽象基类)
├── HTMLImporter (智能路由)
│   ├── QiangZhiImporter (强智系统)
│   └── 通用 HTML 解析
├── ExcelImporter (智能检测)
│   ├── 强智格式解析
│   └── 标准格式解析
└── TextImporter (文本格式)
```

### 解析流程

```
用户上传文件
    ↓
格式验证 (validate)
    ↓
格式检测 (detect_format)
    ↓
选择解析器
    ├── 强智系统 → QiangZhiImporter
    ├── 通用格式 → 通用解析器
    └── 标准格式 → 标准解析器
    ↓
数据转换 (convert_to_courses)
    ↓
返回课程数据
```

## 测试验证

### HTML 导入器测试

**测试文件**：`tests/test_html_importer.py`

**测试用例**：
- ✅ 验证功能测试
- ✅ 解析简单课表
- ✅ 解析多节次课程
- ✅ 同一门课程在不同时间
- ✅ 解析单双周
- ✅ 获取支持的格式

**测试结果**：6/6 通过 ✓

### Excel 导入器测试

**测试文件**：`tests/test_excel_importer.py`

**测试用例**：
- ✅ 验证功能测试
- ✅ 解析 Excel 文件
- ✅ 获取支持的格式

## 兼容性

### 支持的教务系统

1. **强智教务系统** ⭐⭐⭐⭐⭐
   - 自动识别
   - 专用解析器
   - 完整支持

2. **通用 HTML 系统** ⭐⭐⭐⭐
   - 表格格式
   - 基本信息提取

3. **自定义 Excel** ⭐⭐⭐⭐⭐
   - 标准模板
   - 灵活格式

### 支持的文件格式

| 格式 | 扩展名 | 支持程度 | 备注 |
|------|--------|----------|------|
| HTML | .html, .htm | ⭐⭐⭐⭐⭐ | 强智系统优先 |
| Excel | .xlsx, .xls | ⭐⭐⭐⭐⭐ | 多格式支持 |
| 文本 | .txt | ⭐⭐⭐ | 简单格式 |

## 性能优化

### 解析性能

- **HTML 解析**：使用 BeautifulSoup4，高效稳定
- **Excel 解析**：使用 openpyxl，支持大文件
- **延迟初始化**：QiangZhiImporter 延迟加载，减少内存占用

### 内存优化

- 使用生成器读取大文件
- 及时关闭文件句柄
- 避免重复数据存储

## 用户体验改进

### 改进前

1. 用户需要了解具体格式要求
2. 导入失败时缺少明确提示
3. 不支持多种格式
4. 缺少标准模板

### 改进后

1. ✅ 自动识别格式，无需用户判断
2. ✅ 详细的错误提示和建议
3. ✅ 支持多种格式，兼容性强
4. ✅ 提供标准模板和详细文档
5. ✅ 智能回退机制，提高成功率

## 未来规划

### 短期计划

1. **UI 集成**
   - 在主窗口添加"下载模板"按钮
   - 导入时显示格式检测结果
   - 提供导入预览功能

2. **错误处理**
   - 更详细的错误提示
   - 导入失败时的修复建议
   - 部分导入成功的处理

3. **格式扩展**
   - 支持 CSV 格式
   - 支持 JSON 格式
   - 支持 iCal 格式

### 长期计划

1. **智能识别**
   - 使用机器学习识别课表格式
   - 自动修正常见错误
   - 智能推断缺失信息

2. **批量导入**
   - 支持多文件批量导入
   - 支持文件夹导入
   - 支持在线导入（URL）

3. **导入历史**
   - 记录导入历史
   - 支持撤销导入
   - 导入数据对比

## 贡献者

- 主要开发：AI Assistant
- 架构设计：基于用户需求和最佳实践
- 测试验证：自动化测试 + 手动验证

## 更新日志

### 2026-01-01
- ✅ HTML 导入器智能路由实现
- ✅ Excel 导入器多格式支持
- ✅ 创建标准 Excel 模板
- ✅ 完善导入指南文档
- ✅ 修复测试文件导入路径
- ✅ 所有测试通过验证

## 参考资料

- [导入指南](IMPORT_GUIDE.md)
- [项目结构](PROJECT_STRUCTURE.md)
- [强智系统重构总结](QIANGZHI_REFACTOR_SUMMARY.md)
- [添加新学校指南](ADD_NEW_SCHOOL_GUIDE.md)
