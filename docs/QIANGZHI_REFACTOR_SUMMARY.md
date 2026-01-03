# 强智教务系统导入器重构总结

## 重构目标

将原本耦合在 `USCImporter` 中的强智教务系统通用逻辑剥离，创建通用基类 `QiangZhiImporter`，使系统能够轻松适配其他使用强智教务系统的学校。

## 架构设计

```
BaseImporter (抽象接口)
    ↓
QiangZhiImporter (强智系统通用实现)
    ↓
USCImporter (南华大学配置)
```

## 重构成果

### 1. 新增文件

#### `src/importers/qiangzhi_importer.py`
- **作用**: 强智教务系统通用导入器
- **特点**: 
  - 零硬编码，所有学校特有逻辑通过参数配置
  - 支持真实 HTML 格式（`<font title="...">` 标签）
  - 支持简化文本格式（`|` 分隔）
  - 完整的配置参数系统

#### 配置参数列表

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `school_name` | str | "通用强智系统" | 学校名称（用于显示） |
| `sunday_first` | bool | False | 是否星期日开头 |
| `first_col_is_header` | bool | False | 第一列是否为表头（节次列） |
| `split_pattern` | str | `r'-{10,}'` | 课程块分隔符正则 |
| `table_id` | str | 'kbtable' | 课表 table 的 id 属性 |
| `cell_class` | str | 'kbcontent' | 课程内容 div 的 class 属性 |
| `week_pattern` | str | `r'([\d\-,]+)\(周\)'` | 周次提取正则 |
| `section_pattern` | str | `r'\[(\d+)-(\d+)节\]'` | 节次提取正则 |
| `teacher_title` | str | '老师' | 教师字段的 font title 属性值 |
| `location_title` | str | '教室' | 教室字段的 font title 属性值 |
| `week_section_title` | str | '周次(节次)' | 周次节次字段的 font title 属性值 |
| `odd_week_keyword` | str | '单周' | 单周标识关键字 |
| `even_week_keyword` | str | '双周' | 双周标识关键字 |
| `exclude_courses` | List[str] | `["教学资料", ""]` | 需要排除的课程名称列表 |

### 2. 重构文件

#### `src/importers/usc_importer.py`
- **重构前**: 300+ 行，包含所有解析逻辑
- **重构后**: 30 行，仅包含南华大学特有配置
- **代码减少**: 约 90%

#### 重构后的 USCImporter

```python
class USCImporter(QiangZhiImporter):
    def __init__(self):
        super().__init__(
            school_name="南华大学",
            sunday_first=False,             # 第一列（节次列后）是周一
            first_col_is_header=True,       # 第一列是节次表头
            split_pattern=r'-{10,}',        # 南华特有：长横线分隔
            exclude_courses=["教学资料", ""]  # 过滤杂质
        )
    
    def get_importer_name(self) -> str:
        return "南华大学教务系统"
```

## 核心特性

### 1. 双格式支持

#### 真实强智系统格式
```html
<font title="老师">张三</font>
<font title="教室">A101</font>
<font title="周次(节次)">1-16(周)[01-02节]</font>
```

#### 简化文本格式
```
高等数学|老师|张三|周次(节次)|1-16(周)[01-02节]|教室|A101
```

### 2. 灵活的星期计算

- **`sunday_first=True`**: 第0列是周日，映射为 day_of_week=7
- **`sunday_first=False`**: 第0列是周一，映射为 day_of_week=1
- **`first_col_is_header=True`**: 第一列是表头，自动跳过

### 3. 智能字段提取

1. 优先使用 `<font title="...">` 标签（真实格式）
2. 回退到文本解析（简化格式）
3. 自动处理多种周次格式（如 "1-8,10-12(周)"）

## 测试验证

### 测试结果
```
✅ test_basic_parsing - 基本解析功能
✅ test_multiple_courses_in_cell - 多课程单元格
✅ test_sunday_offset - 周日课程偏移
✅ test_invalid_content - 无效内容验证
```

### 真实 HTML 测试
```
✅ 成功解析 7 门课程
✅ 所有字段提取正确
✅ 颜色自动分配正常
✅ 周次范围解析准确
```

## 扩展性

### 如何适配其他学校

只需创建新的子类并传入学校特有参数：

```python
class OtherSchoolImporter(QiangZhiImporter):
    def __init__(self):
        super().__init__(
            school_name="其他学校",
            sunday_first=True,              # 根据实际情况调整
            first_col_is_header=False,      # 根据实际情况调整
            split_pattern=r'-{5,}',         # 根据实际情况调整
            # ... 其他参数
        )
    
    def get_importer_name(self) -> str:
        return "其他学校教务系统"
```

### 常见变体处理

| 学校特征 | 配置方案 |
|---------|---------|
| 星期日在第一列 | `sunday_first=True, first_col_is_header=False` |
| 星期一在第一列 | `sunday_first=False, first_col_is_header=False` |
| 第一列是节次 | `first_col_is_header=True` |
| 不同的分隔符 | 修改 `split_pattern` |
| 不同的字段名 | 修改 `teacher_title`, `location_title` 等 |
| 不同的周次格式 | 修改 `week_pattern` |

## 向后兼容性

- ✅ 所有现有测试通过
- ✅ UI 层无需修改（`get_importer_name()` 返回值不变）
- ✅ 现有功能完全保留
- ✅ 性能无影响

## 代码质量

### 优点
1. **高内聚低耦合**: 通用逻辑与学校配置完全分离
2. **易于维护**: 南华大学代码从 300+ 行减少到 30 行
3. **易于扩展**: 新增学校只需 20-30 行代码
4. **零重复**: 所有学校共享通用解析逻辑
5. **类型安全**: 完整的类型注解

### 设计模式
- **模板方法模式**: 通用流程在基类，具体配置在子类
- **策略模式**: 通过参数配置不同的解析策略
- **工厂模式**: 通过配置创建不同的导入器实例

## 总结

这次重构成功实现了：

1. ✅ **通用性**: 可适配所有强智系统学校
2. ✅ **简洁性**: 南华大学代码减少 90%
3. ✅ **可维护性**: 配置与逻辑分离
4. ✅ **可扩展性**: 新增学校成本极低
5. ✅ **向后兼容**: 现有功能完全保留
6. ✅ **测试覆盖**: 所有测试通过

重构后的架构为项目的长期发展奠定了坚实基础，使系统能够轻松支持更多学校的教务系统。
