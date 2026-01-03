"""
UI 样式定义 (Modern UI v2.1)
src/ui/styles.py
"""

class ModernStyles:
    # --- 核心配色 ---
    COLOR_FRAME_BG = "rgba(255, 255, 255, 250)"
    COLOR_TEXT_PRIMARY = "#2c3e50"
    COLOR_TEXT_SECONDARY = "#7f8c8d"
    COLOR_ACCENT = "#3498db"
    COLOR_BORDER = "#E0E0E0"

    # --- 全局字体 ---
    FONT_FAMILY = "Microsoft YaHei, Segoe UI, sans-serif"

    # --- 滚动条美化 (新增) ---
    SCROLLBAR = f"""
        QScrollBar:vertical {{
            border: none;
            background: #f0f0f0;
            width: 8px; /* 滚动条宽度变窄 */
            margin: 0px 0px 0px 0px;
        }}
        QScrollBar::handle:vertical {{
            background: #cdcdcd;
            min-height: 20px;
            border-radius: 4px; /* 圆角滑块 */
        }}
        QScrollBar::handle:vertical:hover {{
            background: #a6a6a6;
        }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
            height: 0px; /* 隐藏上下箭头 */
        }}
        QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
            background: none;
        }}
        
        /* 水平滚动条 (如果出现的话) */
        QScrollBar:horizontal {{
            border: none;
            background: #f0f0f0;
            height: 8px;
            margin: 0px 0px 0px 0px;
        }}
        QScrollBar::handle:horizontal {{
            background: #cdcdcd;
            min-width: 20px;
            border-radius: 4px;
        }}
        QScrollBar::handle:horizontal:hover {{
            background: #a6a6a6;
        }}
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{
            width: 0px;
        }}
    """

    # --- 全局默认样式 ---
    GLOBAL = f"""
        QWidget {{
            font-family: "{FONT_FAMILY}";
            color: {COLOR_TEXT_PRIMARY};
        }}
        {SCROLLBAR}  /* 将滚动条样式注入全局 */
    """

    # --- 对话框样式 ---
    DIALOG = f"""
        QDialog {{ background-color: #ffffff; }}
    """

    # --- 主窗口工具栏 ---
    TOOLBAR = f"""
        QToolBar {{
            background-color: {COLOR_FRAME_BG};
            border-bottom: 1px solid {COLOR_BORDER};
            spacing: 10px;
            padding: 5px;
        }}
        QToolButton {{
            background-color: transparent;
            border: none;
            border-radius: 4px;
            padding: 6px;
            font-weight: bold;
            color: {COLOR_TEXT_PRIMARY};
        }}
        QToolButton:hover {{
            background-color: #f0f0f0;
        }}
        QToolButton:pressed {{
            background-color: #e0e0e0;
        }}
        /* 菜单样式 */
        QMenu {{
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            padding: 5px;
        }}
        QMenu::item {{
            padding: 5px 20px;
            border-radius: 4px;
        }}
        QMenu::item:selected {{
            background-color: #f0f0f0;
            color: {COLOR_ACCENT};
        }}
    """

    # --- 设置列表样式 ---
    SETTINGS_LIST = f"""
        QListWidget {{
            background-color: #f8f9fa;
            border: none;
            outline: none;
            border-right: 1px solid {COLOR_BORDER};
        }}
        QListWidget::item {{
            height: 45px;
            padding-left: 15px;
            border-left: 3px solid transparent;
            color: {COLOR_TEXT_SECONDARY};
            font-weight: 500;
        }}
        QListWidget::item:selected {{
            background-color: #ffffff;
            color: {COLOR_ACCENT};
            border-left: 3px solid {COLOR_ACCENT};
            font-weight: bold;
        }}
        QListWidget::item:hover {{
            background-color: #e9ecef;
        }}
    """