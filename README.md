# 🎓 WakeUp 课表 Windows 版

<div align="center">

![Python Version](https://img.shields.io/badge/python-3.10+-blue.svg)
![PyQt6](https://img.shields.io/badge/PyQt6-6.6+-green.svg)
![License](https://img.shields.io/badge/license-MIT-orange.svg)
![Tests](https://img.shields.io/badge/tests-91%20passing-brightgreen.svg)
![Coverage](https://img.shields.io/badge/coverage-60%25-yellow.svg)

一个功能完整、界面现代化的桌面课程表管理应用程序，基于 Python 和 PyQt6 开发。  
支持多种导入方式、智能冲突检测、现代化 UI 设计和主题系统。

[功能特点](#-功能特点) • [快速开始](#-快速开始) • [使用指南](#-使用指南) • [开发文档](#-开发文档)

</div>

---

## ✨ 功能特点

### 🎨 现代化 UI 设计

#### 毛玻璃效果
- **半透明表头**: 表头和时间列采用 40% 透明度白色背景，创造层次感
- **智能文字颜色**: 根据背景亮度自动选择黑色或白色文字，确保最佳可读性
  - 使用标准亮度公式: `L = 0.299*R + 0.587*G + 0.114*B`
  - 亮度 > 128 使用黑色文字，≤ 128 使用白色文字
- **圆角设计**: 课程块采用 8px 圆角，现代感十足
- **透明网格**: 完全透明的背景，让自定义背景图片清晰可见

#### 主题系统
- **浅色模式**: 明亮清爽的界面，适合白天使用
- **深色模式**: 护眼的深色界面，适合夜间使用  
- **自动模式**: 跟随系统主题自动切换（需要 darkdetect）
- **透明度调节**: 可调节窗口透明度 (0.0-1.0)

#### 背景定制
- **自定义背景**: 支持静态图片和 GIF 动图作为背景
- **背景透明度**: 独立调节背景图片透明度
- **课程透明度**: 独立调节课程块透明度，平衡美观与可读性

### 📚 强大的课程管理

#### 基础功能
- ✅ **添加课程**: 直观的对话框，支持完整的课程信息录入
- ✅ **编辑课程**: 点击课程块即可快速编辑
- ✅ **删除课程**: 一键删除不需要的课程
- ✅ **批量管理**: 支持同时管理多个上课时间
- ✅ **颜色管理**: 自动为课程分配颜色，同名课程颜色一致

#### 智能特性
- 🔍 **冲突检测**: 实时检测课程时间冲突，避免排课错误
- 📊 **周次管理**: 完整支持每周/单周/双周课程
- 🎯 **精确定位**: 自动计算当前周次，快速定位当前课程
- 🔄 **数据同步**: 自动保存，支持备份和恢复

### 📥 多样化导入方式

#### 1. WebView 自动化导入 🆕
- **内嵌浏览器**: 无需手动下载文件，直接在程序内操作
- **支持系统**: 正方教务系统、强智教务系统
- **常用高校**: 内置常用高校教务系统 URL
- **智能识别**: 自动识别课表页面，一键提取课程信息
- **便捷高效**: 登录一次即可导入，省时省力

#### 2. HTML 文件导入
- 支持从教务系统导出的 HTML 文件导入
- 智能解析课表结构，自动识别课程信息
- 支持多种 HTML 格式

#### 3. Excel 文件导入
- 支持标准 Excel 格式 (.xlsx, .xls)
- 灵活的表格结构识别
- 批量导入课程，快速建立课表

#### 4. 文本文件导入
- 支持简单的文本格式
- 适合快速录入少量课程
- 自定义格式解析

### ⚙️ 灵活的设置选项

#### 学期设置
- 自定义学期开始日期
- 自动计算当前周次
- 支持多学期管理

#### 时间段设置
- 完全自定义每节课的时间
- 支持不同作息时间
- 灵活适配各种课表
- 默认提供标准时间段模板

#### 外观设置
- **背景图片**: 设置静态图片或 GIF 动图
- **背景透明度**: 调节背景图片透明度
- **课程透明度**: 调节课程块透明度
- **主题模式**: 浅色/深色/自动切换
- **窗口透明度**: 调节整体窗口透明度

#### 常规设置
- 启动选项配置
- 桌面小部件开关（预留）
- 其他个性化设置

### 🔒 数据安全

- **自动保存**: 程序关闭时自动保存所有数据
- **备份机制**: 每次保存前自动创建备份文件
- **错误恢复**: 支持从备份恢复数据
- **数据加密**: 可选的数据加密功能（开发中）

---

## 🚀 快速开始

### 系统要求

- **操作系统**: Windows 10/11
- **Python 版本**: 3.10 或更高版本
- **内存**: 2GB 可用内存
- **磁盘空间**: 100MB 可用空间

### 安装步骤

#### 1. 克隆或下载项目

```bash
git clone https://github.com/Ricraft/wakeup-schedule.git
cd wakeup-schedule
```

#### 2. 创建虚拟环境（推荐）

```bash
python -m venv venv
venv\Scripts\activate
```

#### 3. 安装依赖

```bash
pip install -r requirements.txt
```

**依赖包列表**:
- PyQt6 >= 6.6.0 - GUI 框架
- PyQt6-WebEngine >= 6.6.0 - WebView 支持
- beautifulsoup4 >= 4.12.0 - HTML 解析
- lxml >= 4.9.0 - XML/HTML 解析
- openpyxl >= 3.1.0 - Excel 读取
- python-dateutil >= 2.8.0 - 日期处理
- darkdetect >= 0.8.0 - 系统主题检测
- requests >= 2.31.0 - HTTP 请求

**开发依赖**:
- pytest >= 7.4.0 - 测试框架
- pytest-cov >= 4.1.0 - 代码覆盖率
- hypothesis >= 6.92.0 - 属性测试

#### 4. 运行程序

```bash
python main.py
```

### 快速导入课表

#### 方法一：WebView 自动导入（推荐）✨

1. 启动程序后，点击菜单 **导入 > 从教务系统导入**
2. 在下拉框中选择你的学校，或输入自定义 URL
3. 在内嵌浏览器中登录教务系统
4. 导航到课表页面
5. 点击 **📥 获取课表** 按钮
6. 确认导入的课程信息

**支持的教务系统**:
- 正方教务系统
- 强智教务系统
- 其他兼容系统

#### 方法二：HTML 文件导入

1. 从教务系统导出课表为 HTML 文件
2. 点击菜单 **导入 > 从 HTML 导入**
3. 选择下载的 HTML 文件
4. 确认导入的课程信息

#### 方法三：Excel 文件导入

1. 准备 Excel 格式的课表文件
2. 点击菜单 **导入 > 从 Excel 导入**
3. 选择 Excel 文件
4. 确认导入的课程信息

**Excel 模板**: 可以使用 `scripts/create_excel_template.py` 生成标准模板

---

## 📖 使用指南

### 基本操作

#### 添加课程

1. 点击工具栏的 **➕ 添加课程** 按钮
2. 填写课程信息：
   - 课程名称（必填）
   - 教师姓名
   - 上课地点
   - 星期几
   - 第几节课（支持连续多节）
   - 周次范围（如 1-16 周）
   - 单双周类型
3. 点击 **保存** 按钮

#### 编辑课程

1. 点击课表中的课程块
2. 在弹出的详情对话框中点击 **✏️ 编辑** 按钮
3. 修改课程信息
4. 点击 **保存** 按钮

#### 删除课程

1. 点击课表中的课程块
2. 在弹出的详情对话框中点击 **🗑️ 删除** 按钮
3. 确认删除操作

### 周次管理

#### 切换周次

- 使用工具栏的 **◀ 上一周** / **下一周 ▶** 按钮
- 在周次选择器中直接输入周次数字
- 点击 **📍 回到当前周** 按钮快速回到当前周

#### 设置学期开始日期

1. 点击菜单 **设置 > 学期设置**
2. 选择学期开始日期
3. 程序会自动计算当前周次

### 外观定制

#### 设置背景图片

1. 点击菜单 **设置 > 外观设置**(
2. 点击 **选择背景图片** 按钮
3. 选择图片文件（支持 PNG, JPG, GIF）
4. 调节 **背景透明度** 滑块
5. 点击 **确定** 保存

**提示**: GIF 动图会自动播放，创造动态背景效果

#### 调节课程透明度

1. 点击菜单 **设置 > 外观设置**
2. 调节 **课程块透明度** 滑块
3. 实时预览效果
4. 点击 **确定** 保存

**建议值**: 0.85-0.95 之间可以平衡美观和可读性

#### 切换主题模式

1. 点击菜单 **设置 > 主题设置**（或工具栏的主题按钮）
2. 主题将按照 **浅色 → 深色 → 自动** 的顺序循环切换
3. 状态栏会显示当前主题模式

**主题说明**:
- **浅色模式**: 白色背景，深色文字，适合白天
- **深色模式**: 深色背景，浅色文字，适合夜间
- **自动模式**: 跟随系统主题（需要安装 darkdetect）

#### 调节窗口透明度

在配置文件中设置 `opacity` 值 (0.0-1.0):

```json
{
  "opacity": 0.95
}
```

### 高级功能

#### 冲突检测

程序会自动检测课程时间冲突：
- 添加课程时自动检测
- 编辑课程时实时检测
- 显示详细的冲突信息
- 提供解决建议

#### 数据备份与恢复

**自动备份**:
- 每次保存时自动创建 `.bak` 备份文件
- 保留最近的备份

**手动恢复**:
1. 关闭程序
2. 找到数据目录: `%APPDATA%\WakeupSchedule\`
3. 将 `schedule.json.bak` 重命名为 `schedule.json`
4. 重新启动程序

---

## 🏗️ 项目结构

```
wakeup-schedule/
├── src/                          # 源代码目录
│   ├── models/                   # 数据模型 (7个文件)
│   │   ├── course_base.py       # 课程基础信息
│   │   ├── course_detail.py     # 课程详细信息
│   │   ├── schedule.py          # 课表模型
│   │   ├── config.py            # 配置模型
│   │   ├── time_slot.py         # 时间段模型
│   │   └── week_type.py         # 周次类型枚举
│   ├── core/                     # 核心业务逻辑 (4个文件)
│   │   ├── course_manager.py    # 课程管理器
│   │   ├── schedule_manager.py  # 课表管理器
│   │   ├── conflict_detector.py # 冲突检测器
│   │   └── week_calculator.py   # 周次计算器
│   ├── ui/                       # 用户界面 (10+个文件)
│   │   ├── main_window.py       # 主窗口
│   │   ├── schedule_view.py     # 课表视图（现代化 UI）
│   │   ├── course_dialog.py     # 单课程对话框
│   │   ├── course_dialog_multi.py # 多课程对话框
│   │   ├── conflict_dialog.py   # 冲突对话框
│   │   ├── settings_dialog.py   # 设置对话框
│   │   ├── webview_import_dialog.py  # WebView 导入对话框
│   │   ├── week_selector.py     # 周次选择器
│   │   ├── appearance_settings_tab.py # 外观设置标签
│   │   ├── general_settings_tab.py    # 常规设置标签
│   │   ├── semester_settings_tab.py   # 学期设置标签
│   │   └── time_slots_settings_tab.py # 时间段设置标签
│   ├── storage/                  # 数据存储 (1个文件)
│   │   └── json_storage.py      # JSON 存储实现
│   ├── importers/                # 导入器 (6个文件)
│   │   ├── base_importer.py     # 导入器基类
│   │   ├── qiangzhi_importer.py # 强智系统导入器
│   │   ├── usc_importer.py      # 南华大学导入器
│   │   ├── html_importer.py     # HTML 导入器
│   │   ├── excel_importer.py    # Excel 导入器
│   │   └── text_importer.py     # 文本导入器
│   └── utils/                    # 工具函数 (4个文件)
│       ├── validators.py         # 数据验证
│       ├── time_utils.py         # 时间工具
│       ├── color_manager.py      # 颜色管理
│       └── theme_manager.py      # 主题管理
├── tests/                        # 测试文件 (16个文件)
│   ├── test_models.py           # 数据模型测试
│   ├── test_course_manager.py   # 课程管理测试
│   ├── test_conflict_detector.py # 冲突检测测试
│   ├── test_modern_ui_integration.py  # 现代化 UI 集成测试
│   ├── test_*_importer.py       # 各导入器测试
│   └── ...
├── docs/                         # 文档目录
│   ├── QUICKSTART.md            # 快速开始指南
│   ├── IMPORT_GUIDE.md          # 导入功能详细指南
│   ├── WEBVIEW_IMPORT_GUIDE.md  # WebView 导入指南
│   ├── THEME_SYSTEM.md          # 主题系统文档
│   ├── ADD_NEW_SCHOOL_GUIDE.md  # 添加新学校支持指南
│   ├── PROJECT_SUMMARY.md       # 项目总结
│   └── ...
├── examples/                     # 示例文件
│   ├── test_schedule.xlsx       # Excel 示例
│   ├── test_usc_sample.html     # HTML 示例
│   └── schedule_template.xlsx   # Excel 模板
├── scripts/                      # 脚本工具
│   └── create_excel_template.py # 创建 Excel 模板
├── .kiro/                        # 开发规范
│   └── specs/                    # 功能规范
│       ├── modern-ui-enhancement/  # 现代化 UI 规范
│       ├── class-schedule/         # 课表功能规范
│       └── schedule-sync/          # 同步功能规范
├── main.py                       # 程序入口
├── requirements.txt              # 依赖列表
├── setup.py                      # 安装配置
├── pytest.ini                    # 测试配置
├── clean_and_run.bat            # 清理并运行脚本
└── README.md                     # 本文件
```

**代码统计**:
- Python 文件: 40+ 个
- 代码行数: 约 8,000+ 行
- 测试文件: 16 个
- 文档文件: 15+ 个

---

## 🛠️ 技术栈

### 核心技术

- **Python 3.10+**: 现代化的 Python 特性，类型注解支持
- **PyQt6 6.6+**: 强大的跨平台 GUI 框架
- **PyQt6-WebEngine**: WebView 支持，用于教务系统登录
- **JSON**: 轻量级数据存储格式

### 数据处理

- **BeautifulSoup4**: HTML 解析，用于课表导入
- **lxml**: 高性能 XML/HTML 解析器
- **openpyxl**: Excel 文件读写
- **python-dateutil**: 日期时间处理

### UI 增强

- **darkdetect**: 系统主题检测，用于自动主题切换
- **requests**: HTTP 请求，用于教务系统交互

### 开发工具

- **pytest**: 测试框架，支持单元测试和集成测试
- **pytest-qt**: Qt 应用测试插件
- **pytest-cov**: 代码覆盖率统计
- **hypothesis**: 属性测试框架（开发中）

### 架构模式

- **MVC 模式**: 清晰的模型-视图-控制器分离
- **模块化设计**: 高内聚低耦合
- **面向对象**: 充分利用 Python 的 OOP 特性

---

## 🧪 测试

项目包含完整的单元测试和集成测试，确保代码质量和功能正确性。

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_models.py

# 运行现代化 UI 测试
pytest tests/test_modern_ui_integration.py

# 查看详细输出
pytest -v

# 生成覆盖率报告
pytest --cov=src --cov-report=html

# 查看覆盖率报告
# 打开 htmlcov/index.html
```

### 测试统计

- ✅ **91 个测试通过**
- 📊 **60% 代码覆盖率**
- 🎯 **核心功能 100% 覆盖**
- ⚡ **现代化 UI 测试: 10/12 通过**

### 测试文件列表

**模型测试**:
- `test_models.py` - 数据模型测试
- `test_storage.py` - 存储层测试
- `test_validators.py` - 验证器测试
- `test_time_utils.py` - 时间工具测试

**核心逻辑测试**:
- `test_course_manager.py` - 课程管理测试
- `test_schedule_manager.py` - 课表管理测试
- `test_conflict_detector.py` - 冲突检测测试

**导入器测试**:
- `test_html_importer.py` - HTML 导入测试
- `test_excel_importer.py` - Excel 导入测试
- `test_text_importer.py` - 文本导入测试
- `test_usc_importer.py` - USC 导入器测试

**UI 测试**:
- `test_main_window.py` - 主窗口测试
- `test_course_dialog.py` - 课程对话框测试
- `test_conflict_dialog.py` - 冲突对话框测试
- `test_settings_dialog.py` - 设置对话框测试
- `test_modern_ui_integration.py` - 现代化 UI 集成测试

**集成测试**:
- `test_app_integration.py` - 完整应用流程测试

---

## 📚 开发文档

### 用户文档

- [快速开始指南](docs/QUICKSTART.md) - 5分钟快速上手教程
- [导入指南](docs/IMPORT_GUIDE.md) - 详细的导入功能说明
- [WebView 导入指南](docs/WEBVIEW_IMPORT_GUIDE.md) - WebView 功能详解
- [主题系统文档](docs/THEME_SYSTEM.md) - 主题系统使用和定制

### 开发者文档

- [项目总结](docs/PROJECT_SUMMARY.md) - 完整的项目概述和功能清单
- [项目结构](docs/PROJECT_STRUCTURE.md) - 详细的代码结构说明
- [添加新学校指南](docs/ADD_NEW_SCHOOL_GUIDE.md) - 为你的学校添加教务系统支持
- [强智系统架构](docs/QIANGZHI_REFACTOR_SUMMARY.md) - 强智系统设计说明
- [导入器增强](docs/IMPORTER_IMPROVEMENTS_2026.md) - 导入器改进文档

### 规范文档

- [现代化 UI 需求](.kiro/specs/modern-ui-enhancement/requirements.md) - UI 功能需求
- [现代化 UI 设计](.kiro/specs/modern-ui-enhancement/design.md) - UI 设计规范
- [现代化 UI 任务](.kiro/specs/modern-ui-enhancement/tasks.md) - UI 实现任务列表

### 测试文档

- [测试 README](tests/README.md) - 测试说明和指南

---

## 🎯 设计特点

### 1. 分离式课程设计

**CourseBase + CourseDetail 架构**:
- **CourseBase**: 存储课程基础信息（名称、颜色、备注）
- **CourseDetail**: 存储课程详细信息（时间、地点、教师）
- 一个课程可以有多个上课时间

**优势**:
- 避免数据冗余
- 便于批量管理
- 支持复杂排课

### 2. 智能颜色管理

**基于哈希的颜色分配**:
- 使用课程名称的哈希值自动分配颜色
- 同一课程始终使用相同颜色
- 预设 15 种高对比度颜色

**智能文字颜色**:
- 根据背景亮度自动选择文字颜色
- 使用标准亮度公式: L = 0.299*R + 0.587*G + 0.114*B
- 确保最佳可读性

### 3. 现代化 UI 设计

**毛玻璃效果**:
- 表头和时间列采用 40% 透明度白色背景
- 创造层次感和深度感
- 保持背景图片可见性

**Widget 渲染**:
- 使用 QWidget 而非 QTableWidgetItem
- 确保背景色正确渲染
- 支持复杂交互

**响应式设计**:
- 自适应窗口大小
- 流畅的动画效果
- 优秀的性能表现

### 4. 完整的周次支持

**三种周次类型**:
- 每周: 每周都上课
- 单周: 仅单周上课（1, 3, 5...）
- 双周: 仅双周上课（2, 4, 6...）

**智能过滤**:
- 自动根据当前周次过滤课程
- 准确计算周次范围
- 支持跨学期管理

### 5. 智能冲突检测

**多维度检测**:
- 星期冲突检测
- 节次冲突检测
- 周次范围冲突检测
- 单双周冲突检测

**详细提示**:
- 显示冲突的具体信息
- 提供解决建议
- 支持强制保存

---

## 💾 数据存储

### 存储位置

- **Windows**: `%APPDATA%\WakeupSchedule\`
- **课表数据**: `schedule.json`
- **配置数据**: `config.json`
- **备份文件**: `*.json.bak`

### 数据格式

```json
{
  "course_bases": [
    {
      "id": "uuid-string",
      "name": "高等数学",
      "color": "#4CAF50",
      "note": "重要课程"
    }
  ],
  "course_details": [
    {
      "course_id": "uuid-string",
      "teacher": "张教授",
      "location": "教学楼A101",
      "day_of_week": 1,
      "start_section": 1,
      "step": 2,
      "start_week": 1,
      "end_week": 16,
      "week_type": "every"
    }
  ],
  "semester_start_date": "2024-09-01",
  "time_slots": [...],
  "config": {...}
}
```

---

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议！

### 报告问题

1. 在 [Issues](https://github.com/Ricraft/wakeup-schedule/issues) 页面创建新问题
2. 描述问题的详细情况
3. 提供复现步骤
4. 附上截图或日志（如果可能）

### 贡献代码

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 添加新学校支持

请参考 [添加新学校指南](docs/ADD_NEW_SCHOOL_GUIDE.md)

---

## 📝 更新日志

### v1.0.0 (2024-12-31) - 首次发布 🎉

#### ✨ 核心功能
- ✅ 完整的课程管理系统（添加、编辑、删除）
- ✅ 智能冲突检测
- ✅ 周次管理（每周/单周/双周）
- ✅ 自动颜色分配
- ✅ 数据持久化和备份

#### 🎨 现代化 UI
- ✅ 毛玻璃效果表头和时间列
- ✅ 智能文字颜色自动选择
- ✅ 课程块圆角设计（8px）
- ✅ 完全透明的网格背景
- ✅ 自定义背景图片支持（静态/GIF）
- ✅ 主题系统（浅色/深色/自动）
- ✅ 透明度可调节

#### 📥 导入功能
- ✅ WebView 自动化导入
- ✅ HTML 文件导入
- ✅ Excel 文件导入
- ✅ 文本文件导入
- ✅ 支持正方和强智教务系统

#### ⚙️ 设置功能
- ✅ 学期设置
- ✅ 时间段自定义
- ✅ 外观设置
- ✅ 常规设置

#### 🧪 测试和文档
- ✅ 91 个测试通过
- ✅ 60% 代码覆盖率
- ✅ 完整的用户和开发文档

---

## 🤝 贡献指南

欢迎贡献代码、报告问题或提出建议！

### 报告问题

1. 在 [Issues](https://github.com/Ricraft/wakeup-schedule/issues) 页面创建新问题
2. 描述问题的详细情况
3. 提供复现步骤
4. 附上截图或日志（如果可能）

### 贡献代码

1. Fork 本仓库
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

### 代码规范

- 遵循 PEP 8 代码规范
- 添加必要的注释和文档字符串
- 编写单元测试
- 确保所有测试通过

### 添加新学校支持

请参考 [添加新学校指南](docs/ADD_NEW_SCHOOL_GUIDE.md)

---

## 📄 许可证

本项目采用 MIT 许可证 - 详见 [LICENSE](LICENSE) 文件

---

## 🤖 AI 辅助开发声明

本项目在开发过程中使用了 AI 辅助工具（Kiro / Claude）进行：
- 代码编写与优化
- 文档撰写
- 测试用例生成
- Bug 修复与调试

所有 AI 生成的代码均经过人工审核和测试。

---

## 🙏 致谢

- 感谢 [WakeUp 课表 Kotlin 版](https://github.com/YZune/WakeupSchedule_Kotlin) 提供的设计灵感和课程表解析逻辑参考
- 感谢 PyQt6 团队提供优秀的 GUI 框架
- 感谢 AI 工具在开发过程中的辅助
- 感谢所有贡献者的付出
- 感谢开源社区的支持

---

## 📧 联系方式

- **项目主页**: [GitHub](https://github.com/Ricraft/wakeup-schedule)
- **问题反馈**: [Issues](https://github.com/Ricraft/wakeup-schedule/issues)

---

## 🚀 未来计划

### 近期计划
- [ ] 系统托盘支持
- [ ] 课程提醒功能
- [ ] 更多主题预设
- [ ] 导出功能（PDF/图片）

### 中期计划
- [ ] 桌面小部件
- [ ] 云同步功能
- [ ] 多语言支持

### 长期计划
- [ ] 移动端同步
- [ ] 课程笔记功能
- [ ] 成绩管理
- [ ] 社区分享功能

---

<div align="center">

**如果这个项目对你有帮助，请给一个 ⭐️ Star！**

Made with ❤️ by WakeUp Schedule Team

</div>
