# 主题系统文档

## 概述

WakeUp 课表现在支持现代化的主题系统，包括浅色、深色和自动（跟随系统）三种模式。

## 功能特性

### 1. 三种主题模式

- **浅色模式 (light)**: 明亮清爽的界面，适合白天使用
- **深色模式 (dark)**: 护眼的深色界面，适合夜间使用
- **自动模式 (auto)**: 自动跟随系统主题设置

### 2. 可配置的透明度

- 支持调整界面透明度 (0.0-1.0)
- 默认透明度为 0.95
- 可以通过配置文件修改

### 3. 背景图片支持（预留）

- 支持自定义背景图片路径
- 为后续的背景图片/GIF 功能做准备

## 使用方法

### 快速切换主题

在主窗口中，通过以下方式切换主题：

1. 点击菜单栏 **设置 → 主题设置**
2. 主题将按照 `浅色 → 深色 → 自动` 的顺序循环切换
3. 状态栏会显示当前主题模式

### 通过配置文件设置

配置文件位置：`%APPDATA%\WakeupSchedule\config.json`

```json
{
  "theme_mode": "dark",
  "opacity": 0.95,
  "background_image": null
}
```

**配置项说明：**

- `theme_mode`: 主题模式，可选值：`"light"`, `"dark"`, `"auto"`
- `opacity`: 透明度，范围 0.0-1.0
- `background_image`: 背景图片路径（暂未实现）

## 技术实现

### ThemeManager 类

主题管理器负责生成和管理 QSS 样式表。

**主要方法：**

- `get_qss(mode=None)`: 获取指定模式的 QSS 样式表
- `get_current_mode()`: 获取当前实际使用的主题模式
- `_light_qss()`: 生成浅色主题样式
- `_dark_qss()`: 生成深色主题样式

**信号：**

- `theme_changed(str)`: 主题变更时发出，参数为新的主题模式

### 在 MainWindow 中集成

```python
# 初始化主题管理器
self.theme_manager = ThemeManager(self.config)

# 应用主题
self.apply_theme()

# 切换主题
self.config.theme_mode = "dark"
self.apply_theme()
```

## 依赖项

### darkdetect

用于检测系统主题（自动模式需要）。

**安装：**

```bash
pip install darkdetect
```

**注意：** 如果未安装 darkdetect，自动模式将默认使用浅色主题。

## 样式定制

### 修改颜色

在 `theme_manager.py` 中修改 `_light_qss()` 或 `_dark_qss()` 方法：

```python
def _light_qss(self) -> str:
    return f"""
    QMainWindow {{
        background-color: #YOUR_COLOR;  /* 修改背景色 */
    }}
    """
```

### 添加新组件样式

在 QSS 字符串中添加新的选择器：

```python
/* 自定义组件 */
QCustomWidget {{
    background-color: #FFFFFF;
    border: 1px solid #E0E0E0;
}}
```

## 下一步计划

### 第二步：背景层架构

- 实现自定义背景图片支持
- 支持 GIF 动画背景
- 实现磨砂玻璃效果

### 第三步：高级主题功能

- 更多预设主题
- 自定义颜色选择器
- 主题导入/导出

## 故障排除

### 问题：自动模式不工作

**原因：** darkdetect 未安装

**解决方案：**

```bash
pip install darkdetect
```

### 问题：主题切换后样式未更新

**原因：** 可能是 QSS 缓存问题

**解决方案：**

1. 重启应用程序
2. 或在代码中强制刷新：

```python
self.setStyleSheet("")  # 清空样式
self.apply_theme()      # 重新应用
```

### 问题：透明度设置无效

**原因：** 某些 Windows 版本可能不支持窗口透明度

**解决方案：**

- 确保 Windows 启用了 Aero 效果
- 或将透明度设置为 1.0（完全不透明）

## 测试

运行测试脚本验证主题管理器功能：

```bash
cd wakeup-schedule
python test_theme_manager.py
```

## 参考资料

- [PyQt6 样式表文档](https://doc.qt.io/qt-6/stylesheet.html)
- [darkdetect 文档](https://github.com/albertosottile/darkdetect)
- [Material Design 颜色系统](https://material.io/design/color)
