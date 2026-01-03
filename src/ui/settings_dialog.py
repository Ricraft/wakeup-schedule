"""
设置对话框 (Modern UI v2.1)
src/ui/settings_dialog.py
"""
import os
from PyQt6.QtWidgets import (
    QDialog, QWidget, QVBoxLayout, QHBoxLayout, QListWidget, QStackedWidget,
    QLabel, QRadioButton, QButtonGroup, QPushButton, QSlider, QFileDialog,
    QFrame, QCheckBox, QSpinBox, QComboBox, QDateEdit, QGridLayout, QGroupBox,
    QFormLayout, QInputDialog
)
from PyQt6.QtCore import Qt, pyqtSignal, QRectF, QDate, QUrl
from PyQt6.QtGui import QPainter, QPixmap, QPainterPath, QFont, QColor, QDesktopServices

# === 样式常量 ===
FONT_FAMILY = "Microsoft YaHei"
STYLE_HEAD = f"font-family: '{FONT_FAMILY}'; font-size: 16px; font-weight: bold; color: #333; margin: 10px 0 5px 0;"
STYLE_BODY = f"font-family: '{FONT_FAMILY}'; font-size: 14px; color: #333;"
STYLE_HINT = f"font-family: '{FONT_FAMILY}'; font-size: 12px; color: #666;"
STYLE_GROUP = f"QGroupBox {{ font-family: '{FONT_FAMILY}'; font-weight: bold; border: 1px solid #ddd; border-radius: 6px; margin-top: 10px; padding-top: 15px; }}"

# 单选框美化样式 (蓝色圆点)
STYLE_RADIO = f"""
    QRadioButton {{
        font-family: '{FONT_FAMILY}'; 
        font-size: 14px; 
        color: #333; 
        spacing: 8px;
    }}
    QRadioButton::indicator {{
        width: 18px; 
        height: 18px; 
        border-radius: 10px; 
        border: 2px solid #bbb; 
        background-color: white;
    }}
    QRadioButton::indicator:checked {{
        border: 2px solid #2d8cf0;
    }}
    QRadioButton::indicator:checked::inner {{
        background-color: #2d8cf0; 
        width: 10px; 
        height: 10px;
        margin: 3px;
        border-radius: 5px;
    }}
    QRadioButton::indicator:hover {{
        border-color: #2d8cf0;
    }}
"""


# === 自定义预览组件 ===
class PreviewFrame(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.pixmap = None
        self.bg_opacity = 1.0
        self.setObjectName("PreviewFrame")
        self.setStyleSheet("""
            QFrame#PreviewFrame {
                background-color: #f0f0f0; 
                border: 1px solid #ddd;
                border-radius: 8px;
            }
        """)

    def set_image(self, path):
        if path and os.path.exists(path):
            self.pixmap = QPixmap(path)
        else:
            self.pixmap = None
        self.update()

    def set_opacity(self, opacity):
        self.bg_opacity = opacity
        self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        if self.pixmap and not self.pixmap.isNull():
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            path = QPainterPath()
            path.addRoundedRect(QRectF(self.rect()), 8, 8)
            painter.setClipPath(path)

            painter.setOpacity(self.bg_opacity)
            scaled = self.pixmap.scaled(
                self.size(),
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            x = (self.width() - scaled.width()) // 2
            y = (self.height() - scaled.height()) // 2
            painter.drawPixmap(x, y, scaled)


# === 设置窗口主类 ===
class SettingsDialog(QDialog):
    # 信号定义
    bg_opacity_changed = pyqtSignal(float)
    card_opacity_changed = pyqtSignal(float)
    background_changed = pyqtSignal(str)
    header_style_changed = pyqtSignal(str)  # 表头风格信号
    config_updated = pyqtSignal()  # 通用配置更新信号

    # 修复 __init__ 参数，加入 config
    def __init__(self, parent=None, config=None, current_bg="", bg_opacity=0.6, card_opacity=0.85):
        super().__init__(parent)
        self.config = config
        self.setWindowTitle("⚙️ 设置")
        self.resize(800, 600)
        self.current_bg = current_bg

        self.setFont(QFont(FONT_FAMILY, 10))

        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # 1. 左侧导航栏
        self.nav_list = QListWidget()
        self.nav_list.setFixedWidth(160)
        self.nav_list.setFrameShape(QFrame.Shape.NoFrame)
        self.nav_list.addItems(["常规设置", "外观设置", "学期设置", "关于软件"])
        self.nav_list.setStyleSheet(f"""
            QListWidget {{ background-color: #f5f5f5; border-right: 1px solid #e0e0e0; padding-top: 10px; outline: none; }}
            QListWidget::item {{ height: 45px; padding-left: 15px; color: #333; font-family: '{FONT_FAMILY}'; font-size: 14px; }}
            QListWidget::item:selected {{ background-color: #ffffff; color: #2d8cf0; border-left: 4px solid #2d8cf0; font-weight: bold; }}
            QListWidget::item:hover {{ background-color: #e6e6e6; }}
        """)
        main_layout.addWidget(self.nav_list)

        # 2. 右侧内容区
        self.pages = QStackedWidget()
        self.pages.setStyleSheet("background-color: white; padding: 20px;")
        main_layout.addWidget(self.pages)

        # 初始化页面
        self.init_general_page()
        self.init_appearance_page(bg_opacity, card_opacity)
        self.init_semester_page()
        self.init_about_page()

        self.nav_list.currentRowChanged.connect(self.pages.setCurrentIndex)
        self.nav_list.setCurrentRow(1)

    def create_section_title(self, text):
        lbl = QLabel(text)
        lbl.setStyleSheet(STYLE_HEAD)
        return lbl

    def _update_config(self, key, value):
        if self.config:
            setattr(self.config, key, value)
            self.config.save()
            self.config_updated.emit()

    # === 页面 0: 常规设置 ===
    def init_general_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(self.create_section_title("常规设置"))

        group_behavior = QGroupBox("启动与行为")
        group_behavior.setStyleSheet(STYLE_GROUP)
        layout_behavior = QVBoxLayout(group_behavior)

        self.chk_auto_start = QCheckBox("开机自动启动 (仅 Windows)")
        self.chk_tray = QCheckBox("启动时最小化到托盘")
        self.chk_exit_close = QCheckBox("关闭主面板时退出程序 (未勾选则最小化)")

        for chk in [self.chk_auto_start, self.chk_tray, self.chk_exit_close]:
            chk.setStyleSheet(STYLE_BODY)

        layout_behavior.addWidget(self.chk_auto_start)
        layout_behavior.addWidget(self.chk_tray)
        layout_behavior.addWidget(self.chk_exit_close)
        layout.addWidget(group_behavior)

        group_remind = QGroupBox("课前提醒")
        group_remind.setStyleSheet(STYLE_GROUP)
        layout_remind = QFormLayout(group_remind)

        self.chk_notify = QCheckBox("开启桌面通知提醒")
        self.chk_notify.setStyleSheet(STYLE_BODY)
        self.spin_remind_time = QSpinBox()
        self.spin_remind_time.setRange(1, 60)
        self.spin_remind_time.setSuffix(" 分钟")

        layout_remind.addRow(self.chk_notify)
        layout_remind.addRow(QLabel("提前时间:", styleSheet=STYLE_BODY), self.spin_remind_time)
        layout.addWidget(group_remind)

        # 其他
        group_other = QGroupBox("其他")
        group_other.setStyleSheet(STYLE_GROUP)
        layout_other = QFormLayout(group_other)

        self.chk_auto_update = QCheckBox("自动检查更新")
        self.chk_auto_update.setStyleSheet(STYLE_BODY)
        self.combo_lang = QComboBox()
        self.combo_lang.addItems(["简体中文 (Zh-CN)", "English (US)"])

        layout_other.addRow(self.chk_auto_update)
        layout_other.addRow(QLabel("语言:", styleSheet=STYLE_BODY), self.combo_lang)
        layout.addWidget(group_other)
        layout.addStretch()
        self.pages.addWidget(page)

        # 绑定
        if self.config:
            self.chk_auto_start.setChecked(self.config.auto_start)
            self.chk_tray.setChecked(self.config.minimize_to_tray)
            self.chk_exit_close.setChecked(self.config.exit_on_close)
            self.chk_notify.setChecked(self.config.enable_notification)
            self.spin_remind_time.setValue(self.config.remind_minutes)
            self.chk_auto_update.setChecked(self.config.auto_update)

        self.chk_tray.toggled.connect(lambda v: self._update_config("minimize_to_tray", v))
        self.chk_exit_close.toggled.connect(lambda v: self._update_config("exit_on_close", v))
        self.chk_notify.toggled.connect(lambda v: self._update_config("enable_notification", v))
        self.spin_remind_time.valueChanged.connect(lambda v: self._update_config("remind_minutes", v))
        self.chk_auto_start.clicked.connect(self._handle_auto_start)

    # === 页面 1: 外观设置 ===
    def init_appearance_page(self, bg_op, card_op):
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(self.create_section_title("外观设置"))

        layout.addWidget(QLabel("效果预览:", styleSheet=STYLE_BODY))
        self.preview_frame = PreviewFrame()
        self.preview_frame.setFixedSize(300, 180)
        self.preview_frame.set_image(self.current_bg)
        self.preview_frame.set_opacity(bg_op)

        preview_layout = QVBoxLayout(self.preview_frame)
        preview_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.preview_card = QLabel("高等数学\n@1-101")
        self.preview_card.setObjectName("PreviewCard")
        self.preview_card.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)
        self.preview_card.setFixedSize(140, 80)
        self.preview_card.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_card.setWordWrap(True)
        self.update_preview_style(bg_op, card_op)

        preview_layout.addWidget(self.preview_card)
        layout.addWidget(self.preview_frame, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addSpacing(15)

        # 表头风格
        layout.addWidget(QLabel("表头与侧栏风格:", styleSheet=STYLE_BODY))
        h_style = QHBoxLayout()
        self.rb_header_default = QRadioButton("默认实色")
        self.rb_header_translucent = QRadioButton("半透明 (亚克力)")
        self.rb_header_transparent = QRadioButton("全透明")

        for rb in [self.rb_header_default, self.rb_header_translucent, self.rb_header_transparent]:
            rb.setStyleSheet(STYLE_RADIO)

        self.bg_header = QButtonGroup(self)
        self.bg_header.addButton(self.rb_header_default, 0)
        self.bg_header.addButton(self.rb_header_translucent, 1)
        self.bg_header.addButton(self.rb_header_transparent, 2)
        self.bg_header.idClicked.connect(self._on_header_style_clicked)

        h_style.addWidget(self.rb_header_default)
        h_style.addWidget(self.rb_header_translucent)
        h_style.addWidget(self.rb_header_transparent)
        h_style.addStretch()
        layout.addLayout(h_style)
        layout.addSpacing(15)

        # 背景图
        bg_layout = QHBoxLayout()
        btn_img = QPushButton("📂 选择背景图...")
        btn_img.clicked.connect(self.select_image)
        btn_clear = QPushButton("🗑️ 清除")
        btn_clear.clicked.connect(self.clear_image)
        bg_layout.addWidget(btn_img)
        bg_layout.addWidget(btn_clear)
        bg_layout.addStretch()
        layout.addWidget(QLabel("背景图片:", styleSheet=STYLE_BODY))
        layout.addLayout(bg_layout)
        layout.addSpacing(10)

        # 滑块
        layout.addWidget(QLabel("背景不透明度:", styleSheet=STYLE_BODY))
        self.slider_bg = QSlider(Qt.Orientation.Horizontal)
        self.slider_bg.setRange(0, 100)
        self.slider_bg.setValue(int(bg_op * 100))
        self.slider_bg.valueChanged.connect(self.on_slider_changed)
        layout.addWidget(self.slider_bg)

        layout.addWidget(QLabel("卡片不透明度:", styleSheet=STYLE_BODY))
        self.slider_card = QSlider(Qt.Orientation.Horizontal)
        self.slider_card.setRange(0, 100)
        self.slider_card.setValue(int(card_op * 100))
        self.slider_card.valueChanged.connect(self.on_slider_changed)
        layout.addWidget(self.slider_card)
        layout.addStretch()
        self.pages.addWidget(page)

        # 初始化选中
        if self.config:
            s = self.config.header_style
            if s == "transparent":
                self.rb_header_transparent.setChecked(True)
            elif s == "default":
                self.rb_header_default.setChecked(True)
            else:
                self.rb_header_translucent.setChecked(True)

    # === 页面 2: 学期设置 ===
    def init_semester_page(self):
        # 导入自定义对话框 (延迟导入避免循环引用)
        from src.ui.time_table_dialog import TimeTableDialog
        from src.models.time_slot import TimeSlot

        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(self.create_section_title("学期设置"))

        group_info = QGroupBox("当前学期信息")
        group_info.setStyleSheet(STYLE_GROUP)
        layout_info = QVBoxLayout(group_info)

        h_layout_date = QHBoxLayout()
        h_layout_date.addWidget(QLabel("开学日期:", styleSheet=STYLE_BODY))
        self.date_start = QDateEdit()
        self.date_start.setCalendarPopup(True)
        self.date_start.setDisplayFormat("yyyy-MM-dd")
        h_layout_date.addWidget(self.date_start)
        h_layout_date.addStretch()
        layout_info.addLayout(h_layout_date)

        lbl_hint = QLabel("(修改日期将自动重新计算当前周次)")
        lbl_hint.setStyleSheet(STYLE_HINT)
        layout_info.addWidget(lbl_hint)
        layout_info.addSpacing(10)

        h_layout_week = QHBoxLayout()
        self.lbl_current_week = QLabel("当前周次: 计算中...")
        self.lbl_current_week.setStyleSheet(
            f"font-family: '{FONT_FAMILY}'; font-size: 14px; color: #2d8cf0; font-weight: bold;")
        self.btn_calibrate = QPushButton("📍 校准为本周")
        self.btn_calibrate.setCursor(Qt.CursorShape.PointingHandCursor)
        h_layout_week.addWidget(self.lbl_current_week)
        h_layout_week.addStretch()
        h_layout_week.addWidget(self.btn_calibrate)
        layout_info.addLayout(h_layout_week)
        layout.addWidget(group_info)

        group_config = QGroupBox("课程节数配置")
        group_config.setStyleSheet(STYLE_GROUP)
        layout_config = QFormLayout(group_config)

        self.spin_total_daily = QSpinBox();
        self.spin_total_daily.setRange(1, 24)
        h_layout_sections = QHBoxLayout()
        self.spin_morning = QSpinBox();
        self.spin_afternoon = QSpinBox();
        self.spin_evening = QSpinBox()

        for lbl_text, spin in [("上午:", self.spin_morning), ("下午:", self.spin_afternoon),
                               ("晚上:", self.spin_evening)]:
            h_layout_sections.addWidget(QLabel(lbl_text, styleSheet=STYLE_BODY))
            h_layout_sections.addWidget(spin)

        layout_config.addRow(QLabel("每天课程数:", styleSheet=STYLE_BODY), self.spin_total_daily)
        layout_config.addRow(h_layout_sections)
        self.btn_edit_time = QPushButton("🕒 编辑详细作息时间表...")
        layout_config.addWidget(self.btn_edit_time)
        layout.addWidget(group_config)
        layout.addStretch()
        self.pages.addWidget(page)

        if self.config:
            try:
                qdate = QDate.fromString(self.config.semester_start_date, "yyyy-MM-dd")
                self.date_start.setDate(qdate)
                self._update_current_week_label(qdate)
            except:
                self.date_start.setDate(QDate.currentDate())
            self.spin_total_daily.setValue(self.config.total_courses_per_day)
            self.spin_morning.setValue(self.config.morning_count)
            self.spin_afternoon.setValue(self.config.afternoon_count)
            self.spin_evening.setValue(self.config.evening_count)

        self.date_start.dateChanged.connect(self._on_start_date_changed)
        self.btn_calibrate.clicked.connect(self._on_calibrate_week)
        self.spin_total_daily.valueChanged.connect(lambda v: self._update_config("total_courses_per_day", v))
        self.spin_morning.valueChanged.connect(lambda v: self._update_config("morning_count", v))
        self.spin_afternoon.valueChanged.connect(lambda v: self._update_config("afternoon_count", v))
        self.spin_evening.valueChanged.connect(lambda v: self._update_config("evening_count", v))

        # [核心] 连接编辑作息表
        self.btn_edit_time.clicked.connect(self._on_edit_time_table)

    # === 页面 3: 关于软件 ===
    def init_about_page(self):
        from pathlib import Path
        from PyQt6.QtWidgets import QScrollArea
        
        page = QWidget()
        layout = QVBoxLayout(page)
        layout.addWidget(self.create_section_title("关于软件"))

        # 头部：图标居中 + 标题在下方
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # 使用软件图标 (缩小到原图的一半)
        lbl_logo = QLabel()
        lbl_logo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        icon_path = Path(__file__).parent.parent.parent / "resources" / "icon.png"
        if not icon_path.exists():
            icon_path = Path(__file__).parent.parent.parent / "resources" / "icon.ico"
        
        if icon_path.exists():
            pixmap = QPixmap(str(icon_path))
            # 缩小到原图的一半
            new_width = pixmap.width() // 2
            new_height = pixmap.height() // 2
            scaled_pixmap = pixmap.scaled(new_width, new_height, 
                                          Qt.AspectRatioMode.KeepAspectRatio, 
                                          Qt.TransformationMode.SmoothTransformation)
            lbl_logo.setPixmap(scaled_pixmap)
            lbl_logo.setFixedSize(new_width, new_height)
        else:
            lbl_logo.setFixedSize(128, 128)
            lbl_logo.setText("W")
            lbl_logo.setStyleSheet(
                "background-color: #2d8cf0; color: white; font-size: 60px; font-weight: bold; border-radius: 24px;")
        
        header_layout.addWidget(lbl_logo, alignment=Qt.AlignmentFlag.AlignCenter)
        
        # 标题和版本号
        lbl_name = QLabel("WakeUp Schedule")
        lbl_name.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_name.setStyleSheet(f"font-family: '{FONT_FAMILY}'; font-size: 22px; font-weight: bold; color: #333;")
        header_layout.addWidget(lbl_name)
        
        lbl_ver = QLabel("v2.5.0")
        lbl_ver.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_ver.setStyleSheet(f"font-family: '{FONT_FAMILY}'; font-size: 13px; color: #666;")
        header_layout.addWidget(lbl_ver)
        
        # 开发者和协议信息
        lbl_dev = QLabel("开发：Ricraft & Open Source Community")
        lbl_dev.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_dev.setStyleSheet(f"font-family: '{FONT_FAMILY}'; font-size: 12px; color: #888;")
        header_layout.addWidget(lbl_dev)
        
        lbl_license = QLabel("协议：MIT License")
        lbl_license.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_license.setStyleSheet(f"font-family: '{FONT_FAMILY}'; font-size: 12px; color: #888;")
        header_layout.addWidget(lbl_license)
        
        layout.addWidget(header_widget)
        layout.addSpacing(10)

        # 滚动区域包含详细介绍
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.Shape.NoFrame)
        scroll.setStyleSheet("QScrollArea { background: transparent; }")
        
        scroll_content = QWidget()
        scroll_layout = QVBoxLayout(scroll_content)
        scroll_layout.setContentsMargins(0, 0, 10, 0)
        
        # 主标语
        slogan = QLabel("唤醒你的校园时光")
        slogan.setStyleSheet(f"font-family: '{FONT_FAMILY}'; font-size: 16px; color: #2d8cf0; font-weight: bold;")
        scroll_layout.addWidget(slogan)
        scroll_layout.addSpacing(8)
        
        # 简介
        intro_text = ("WakeUp Schedule 是一款专为大学生打造的高颜值、现代化桌面课表管理工具。"
                      "我们致力于将枯燥的课程表转化为桌面上的一道风景，在提供强大功能的同时，为您带来极致的视觉体验。")
        intro = QLabel(intro_text)
        intro.setWordWrap(True)
        intro.setStyleSheet(f"font-family: '{FONT_FAMILY}'; font-size: 13px; color: #555; line-height: 1.6;")
        scroll_layout.addWidget(intro)
        scroll_layout.addSpacing(15)
        
        # 核心亮点
        highlights_title = QLabel("核心亮点")
        highlights_title.setStyleSheet(f"font-family: '{FONT_FAMILY}'; font-size: 14px; font-weight: bold; color: #333;")
        scroll_layout.addWidget(highlights_title)
        scroll_layout.addSpacing(5)
        
        highlights = [
            ("🎨 极致美学设计", "采用 Modern UI v2.1 设计语言，支持沉浸式背景、亚克力半透明磨砂质感与自定义配色，让查课表成为一种享受。"),
            ("⚡ 智能高效导入", "支持 HTML、Excel 及文本文件一键导入，告别繁琐的手动录入，轻松同步教务系统数据。"),
            ("🛠️ 深度个性定制", "从每日节数到详细作息时间，从单双周设置到课程颜色，一切皆可随心定义，完美适配各类校园作息。"),
            ("🔔 贴心课程助理", "支持系统托盘常驻与课前自动提醒，确保你不会错过任何一节重要课程。"),
        ]
        
        for title, desc in highlights:
            h_lbl = QLabel(f"<b>{title}</b><br/><span style='color:#666;'>{desc}</span>")
            h_lbl.setWordWrap(True)
            h_lbl.setStyleSheet(f"font-family: '{FONT_FAMILY}'; font-size: 12px; color: #333; margin-bottom: 8px;")
            scroll_layout.addWidget(h_lbl)
        
        scroll_layout.addSpacing(15)
        
        # 产品理念
        philosophy_title = QLabel("一款懂你审美的高效课表工具")
        philosophy_title.setStyleSheet(f"font-family: '{FONT_FAMILY}'; font-size: 14px; font-weight: bold; color: #333;")
        scroll_layout.addWidget(philosophy_title)
        scroll_layout.addSpacing(5)
        
        philosophy_text = "摒弃传统刻板的表格，我们将「美」与「用」完美融合。"
        philosophy = QLabel(philosophy_text)
        philosophy.setWordWrap(True)
        philosophy.setStyleSheet(f"font-family: '{FONT_FAMILY}'; font-size: 13px; color: #555;")
        scroll_layout.addWidget(philosophy)
        scroll_layout.addSpacing(8)
        
        features = [
            ("看得到的精致", "全透明/亚克力表头风格切换，支持动态 GIF 与静态背景图，随心调节透明度。"),
            ("用得着的便捷", "教务数据一键导入，智能识别单双周与上课地点。"),
            ("离不开的贴心", "桌面右下角静默守护，上课前准时温情提醒。"),
        ]
        
        for title, desc in features:
            f_lbl = QLabel(f"<b>{title}：</b>{desc}")
            f_lbl.setWordWrap(True)
            f_lbl.setStyleSheet(f"font-family: '{FONT_FAMILY}'; font-size: 12px; color: #555;")
            scroll_layout.addWidget(f_lbl)
        
        scroll_layout.addSpacing(10)
        
        ending = QLabel("让每一次查看课程，都成为唤醒活力的一刻。")
        ending.setStyleSheet(f"font-family: '{FONT_FAMILY}'; font-size: 13px; color: #2d8cf0; font-style: italic;")
        scroll_layout.addWidget(ending)
        scroll_layout.addStretch()
        
        scroll.setWidget(scroll_content)
        layout.addWidget(scroll)
        
        # 底部按钮
        grid_btns = QGridLayout()
        self.btn_github = QPushButton("GitHub 仓库")
        self.btn_update = QPushButton("检查更新")
        for btn in [self.btn_github, self.btn_update]:
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(f"height: 32px; font-family: '{FONT_FAMILY}';")
        grid_btns.addWidget(self.btn_github, 0, 0)
        grid_btns.addWidget(self.btn_update, 0, 1)
        layout.addLayout(grid_btns)

        lbl_copy = QLabel("Copyright © 2024-2025 All Rights Reserved")
        lbl_copy.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_copy.setStyleSheet(STYLE_HINT)
        layout.addWidget(lbl_copy)
        self.pages.addWidget(page)

        self.btn_github.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com")))

    # === 逻辑处理函数 ===
    def on_slider_changed(self):
        bg_val = self.slider_bg.value() / 100.0
        card_val = self.slider_card.value() / 100.0
        self.preview_frame.set_opacity(bg_val)
        self.update_preview_style(bg_val, card_val)
        self.bg_opacity_changed.emit(bg_val)
        self.card_opacity_changed.emit(card_val)
        self._update_config("background_opacity", bg_val)
        self._update_config("course_opacity", card_val)

    def update_preview_style(self, bg_val, card_val):
        alpha = int(255 * card_val)
        bg_color = f"rgba(45, 140, 240, {alpha})"
        self.preview_card.setStyleSheet(f"""
            QLabel#PreviewCard {{
                background-color: {bg_color}; color: white; border-radius: 8px; border: none; padding: 4px;
                font-family: 'Microsoft YaHei'; font-size: 14px; font-weight: bold;
            }}
        """)
        self.preview_card.style().unpolish(self.preview_card)
        self.preview_card.style().polish(self.preview_card)
        self.preview_card.update()

    def select_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "选择图片", "", "Images (*.png *.jpg *.jpeg *.bmp)")
        if path:
            self.current_bg = path
            self.preview_frame.set_image(path)
            self.background_changed.emit(path)
            self._update_config("background_path", path)
            self.on_slider_changed()

    def clear_image(self):
        self.current_bg = ""
        self.preview_frame.set_image(None)
        self.background_changed.emit("")
        self._update_config("background_path", "")
        self.on_slider_changed()

    def _on_start_date_changed(self, date):
        date_str = date.toString("yyyy-MM-dd")
        self._update_config("semester_start_date", date_str)
        self._update_current_week_label(date)
        self.config_updated.emit()

    def _update_current_week_label(self, start_date_qt):
        start_date = start_date_qt.toPyDate()
        today = QDate.currentDate().toPyDate()
        delta = (today - start_date).days
        week = (delta // 7) + 1
        self.lbl_current_week.setText(f"当前周次: 第 {week} 周")

    def _on_calibrate_week(self):
        curr, ok = QInputDialog.getInt(self, "校准周次", "将本周设定为第几周？", 1, 1, 30)
        if ok:
            today = QDate.currentDate()
            days_to_monday = today.dayOfWeek() - 1
            monday_of_this_week = today.addDays(-days_to_monday)
            new_start = monday_of_this_week.addDays(-(curr - 1) * 7)
            self.date_start.setDate(new_start)

    def _handle_auto_start(self):
        import sys
        if sys.platform != 'win32': return
        import winreg
        key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
        app_name = "WakeUpSchedule"
        exe_path = sys.executable
        checked = self.chk_auto_start.isChecked()
        self._update_config("auto_start", checked)
        try:
            key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)
            if checked:
                winreg.SetValueEx(key, app_name, 0, winreg.REG_SZ, exe_path)
            else:
                try:
                    winreg.DeleteValue(key, app_name)
                except:
                    pass
            winreg.CloseKey(key)
        except:
            pass

    def _on_header_style_clicked(self, id):
        styles = ["default", "translucent", "transparent"]
        if 0 <= id < 3:
            s = styles[id]
            self.header_style_changed.emit(s)
            if self.config:
                self.config.header_style = s
                self.config.save()

    def _on_edit_time_table(self):
        # 延迟导入
        from src.ui.time_table_dialog import TimeTableDialog
        from src.models.time_slot import TimeSlot
        from datetime import datetime, date, timedelta

        current_slots = []
        if self.config.custom_time_slots:
            for item in self.config.custom_time_slots:
                s = datetime.strptime(item["start"], "%H:%M").time()
                e = datetime.strptime(item["end"], "%H:%M").time()
                current_slots.append(TimeSlot(item["section"], s, e))
        else:
            # 生成默认
            dt = datetime.combine(date.today(), datetime.strptime("08:00", "%H:%M").time())
            for i in range(self.config.total_courses_per_day):
                end = dt + timedelta(minutes=45)
                current_slots.append(TimeSlot(i + 1, dt.time(), end.time()))
                dt = end + timedelta(minutes=10)

        dlg = TimeTableDialog(self, current_slots)
        if dlg.exec():
            new_slots = dlg.get_data()
            serialized = []
            for s in new_slots:
                serialized.append({
                    "section": s.section_number,
                    "start": s.start_time.strftime("%H:%M"),
                    "end": s.end_time.strftime("%H:%M")
                })
            self._update_config("custom_time_slots", serialized)
            self.config_updated.emit()