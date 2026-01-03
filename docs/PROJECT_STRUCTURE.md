# 项目结构说明

## 📁 目录结构

```
wakeup-schedule/
├── src/                          # 源代码
│   ├── core/                     # 核心业务逻辑
│   │   ├── course_manager.py     # 课程管理器
│   │   ├── schedule_manager.py   # 课表管理器
│   │   ├── conflict_detector.py  # 冲突检测器
│   │   └── week_calculator.py    # 周次计算器
│   │
│   ├── models/                   # 数据模型
│   │   ├── course_base.py        # 课程基础信息
│   │   ├── course_detail.py      # 课程详细信息
│   │   ├── schedule.py           # 课表模型
│   │   ├── time_slot.py          # 时间段模型
│   │   ├── week_type.py          # 周类型枚举
│   │   └── config.py             # 配置模型
│   │
│   ├── ui/                       # 用户界面
│   │   ├── main_window.py        # 主窗口
│   │   ├── schedule_view.py      # 课表视图
│   │   ├── course_dialog.py      # 课程对话框
│   │   ├── course_dialog_multi.py # 多课程对话框
│   │   ├── conflict_dialog.py    # 冲突对话框
│   │   ├── settings_dialog.py    # 设置对话框
│   │   ├── webview_import_dialog.py # WebView导入对话框
│   │   ├── week_selector.py      # 周次选择器
│   │   ├── general_settings_tab.py # 常规设置标签
│   │   ├── semester_settings_tab.py # 学期设置标签
│   │   └── time_slots_settings_tab.py # 时间段设置标签
│   │
│   ├── importers/                # 导入器
│   │   ├── base_importer.py      # 导入器基类
│   │   ├── qiangzhi_importer.py  # 强智系统通用导入器
│   │   ├── usc_importer.py       # 南华大学导入器
│   │   ├── html_importer.py      # HTML导入器
│   │   ├── text_importer.py      # 文本导入器
│   │   └── excel_importer.py     # Excel导入器
│   │
│   ├── storage/                  # 数据存储
│   │   └── json_storage.py       # JSON存储实现
│   │
│   └── utils/                    # 工具类
│       ├── validators.py         # 验证器
│       ├── time_utils.py         # 时间工具
│       └── color_manager.py      # 颜色管理器
│
├── tests/                        # 测试文件
│   ├── test_models.py            # 模型测试
│   ├── test_course_manager.py    # 课程管理器测试
│   ├── test_schedule_manager.py  # 课表管理器测试
│   ├── test_conflict_detector.py # 冲突检测器测试
│   ├── test_storage.py           # 存储测试
│   ├── test_validators.py        # 验证器测试
│   ├── test_time_utils.py        # 时间工具测试
│   ├── test_html_importer.py     # HTML导入器测试
│   ├── test_text_importer.py     # 文本导入器测试
│   ├── test_excel_importer.py    # Excel导入器测试
│   ├── test_usc_importer.py      # USC导入器测试
│   ├── test_usc_real_html.py     # USC真实HTML测试
│   ├── test_main_window.py       # 主窗口测试
│   ├── test_course_dialog.py     # 课程对话框测试
│   ├── test_conflict_dialog.py   # 冲突对话框测试
│   ├── test_settings_dialog.py   # 设置对话框测试
│   ├── test_webview_auto.py      # WebView自动化测试
│   ├── test_app_integration.py   # 应用集成测试
│   └── README.md                 # 测试说明
│
├── docs/                         # 文档
│   ├── QUICKSTART.md             # 快速开始
│   ├── PROJECT_SUMMARY.md        # 项目总结
│   ├── FINAL_STATUS.md           # 最终状态
│   ├── ADD_NEW_SCHOOL_GUIDE.md   # 添加学校指南
│   ├── QIANGZHI_REFACTOR_SUMMARY.md # 强智重构总结
│   ├── USC_IMPORTER_GUIDE.md     # USC导入器指南
│   ├── USC_TROUBLESHOOTING.md    # USC故障排查
│   ├── WEBVIEW_IMPORT_GUIDE.md   # WebView导入指南
│   ├── PROJECT_CLEANUP_2026.md   # 项目清理总结
│   ├── PROJECT_STRUCTURE.md      # 本文件
│   └── README.md                 # 文档索引
│
├── examples/                     # 示例文件
│   ├── test_usc_sample.html      # USC HTML示例
│   ├── test_schedule.xlsx        # Excel示例
│   ├── debug_captured.html       # 调试HTML
│   └── README.md                 # 示例说明
│
├── main.py                       # 程序入口
├── setup.py                      # 安装配置
├── requirements.txt              # 依赖列表
├── pytest.ini                    # 测试配置
├── .gitignore                    # Git忽略配置
└── README.md                     # 项目主文档
```

## 📦 核心模块说明

### src/core/ - 核心业务逻辑

#### CourseManager
- 管理课程的增删改查
- 处理课程ID映射
- 维护课程列表

#### ScheduleManager
- 管理完整的课表
- 协调课程管理器和存储
- 处理课表的保存和加载

#### ConflictDetector
- 检测课程时间冲突
- 考虑星期、节次、周次、单双周
- 返回详细的冲突信息

#### WeekCalculator
- 计算当前周次
- 处理学期开始日期
- 支持周次范围判断

### src/models/ - 数据模型

#### CourseBase
- 课程基础信息（名称、ID、颜色）
- 一个课程可以有多个上课时间

#### CourseDetail
- 课程详细信息（时间、地点、教师）
- 关联到 CourseBase
- 支持单双周设置

#### Schedule
- 完整的课表数据
- 包含所有课程和配置

#### TimeSlot
- 时间段定义
- 开始和结束时间

#### WeekType
- 周类型枚举（每周/单周/双周）

### src/ui/ - 用户界面

#### MainWindow
- 应用主窗口
- 菜单栏和工具栏
- 协调各个组件

#### ScheduleView
- 课表网格视图
- 显示课程单元格
- 处理点击事件

#### CourseDialog
- 添加/编辑课程对话框
- 表单验证
- 冲突检测

#### SettingsDialog
- 设置对话框
- 多标签页设计
- 学期、时间段、常规设置

#### WebViewImportDialog
- WebView导入对话框
- 内嵌浏览器
- 自动提取课表

### src/importers/ - 导入器

#### BaseImporter
- 导入器基类
- 定义统一接口

#### QiangZhiImporter
- 强智系统通用导入器
- 支持配置化
- 适配多个学校

#### USCImporter
- 南华大学专用导入器
- 继承 QiangZhiImporter
- 配置南华特有参数

#### HTMLImporter / TextImporter / ExcelImporter
- 通用格式导入器
- 支持多种文件格式

### src/storage/ - 数据存储

#### JSONStorage
- JSON格式存储
- 自动备份
- 错误恢复

### src/utils/ - 工具类

#### Validators
- 数据验证
- 格式检查

#### TimeUtils
- 时间处理工具
- 格式转换

#### ColorManager
- 颜色管理
- 基于哈希的颜色分配

## 🧪 测试结构

### 单元测试
- 每个模块都有对应的测试文件
- 测试覆盖核心功能
- 使用 pytest 框架

### 集成测试
- `test_app_integration.py` - 完整流程测试
- 测试模块间协作

### UI测试
- 使用 pytest-qt 插件
- 测试用户交互

## 📚 文档结构

### 用户文档
- QUICKSTART.md - 快速上手
- WEBVIEW_IMPORT_GUIDE.md - 功能指南

### 开发文档
- PROJECT_SUMMARY.md - 项目概览
- QIANGZHI_REFACTOR_SUMMARY.md - 架构设计
- ADD_NEW_SCHOOL_GUIDE.md - 扩展指南

### 维护文档
- PROJECT_CLEANUP_2026.md - 清理记录
- PROJECT_STRUCTURE.md - 结构说明

## 🎯 设计原则

### 1. 模块化
- 清晰的模块划分
- 低耦合高内聚
- 易于测试和维护

### 2. 可扩展性
- 导入器插件化
- 配置化设计
- 易于添加新功能

### 3. 数据分离
- CourseBase + CourseDetail 分离
- 一对多关系
- 灵活的数据结构

### 4. 用户友好
- 直观的界面
- 详细的错误提示
- 完善的文档

## 🔄 数据流

```
用户操作
    ↓
UI 层 (MainWindow, Dialogs)
    ↓
业务逻辑层 (Managers, Detectors)
    ↓
数据模型层 (Models)
    ↓
存储层 (JSONStorage)
    ↓
文件系统
```

## 📝 命名规范

### 文件命名
- 模块文件：`snake_case.py`
- 测试文件：`test_*.py`
- 文档文件：`UPPER_CASE.md`

### 类命名
- 类名：`PascalCase`
- 私有类：`_PascalCase`

### 函数命名
- 函数名：`snake_case`
- 私有函数：`_snake_case`

### 变量命名
- 变量名：`snake_case`
- 常量：`UPPER_CASE`

## 🚀 开发流程

1. **需求分析** → 确定功能需求
2. **设计** → 设计模块和接口
3. **实现** → 编写代码
4. **测试** → 编写和运行测试
5. **文档** → 更新文档
6. **集成** → 集成到主分支

## 📊 项目统计

- **源代码文件**: ~30 个
- **测试文件**: ~15 个
- **文档文件**: ~10 个
- **代码行数**: ~5000+ 行
- **测试覆盖率**: >80%

---

**最后更新**: 2026-01-01
