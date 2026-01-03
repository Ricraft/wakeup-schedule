"""
课程对话框 (Modern UI v2.1)
src/ui/course_dialog.py

更新：
1. 动态读取 Config 中的课程节数限制
2. 修复周次网格选择器
3. 新增颜色选择功能
"""

from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QFormLayout, QGridLayout,
    QLineEdit, QComboBox, QSpinBox, QTextEdit,
    QPushButton, QLabel, QGroupBox, QMessageBox, QWidget, QColorDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor, QPixmap, QPainter, QAction
import uuid

import sys
from pathlib import Path

current_dir = Path(__file__).resolve().parent
src_dir = current_dir.parent.parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from src.models.course_base import CourseBase
from src.models.course_detail import CourseDetail
from src.models.week_type import WeekType
from src.utils.color_manager import ColorManager
from src.models.config import Config  # 确保导入 Config


class ColorButton(QPushButton):
    """自定义颜色选择按钮"""

    def __init__(self, color="#3498db", parent=None):
        super().__init__(parent)
        self.current_color = color
        self.setFixedSize(30, 30)
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        self.update_style()

    def set_color(self, color):
        self.current_color = color
        self.update_style()

    def get_color(self):
        return self.current_color

    def update_style(self):
        self.setStyleSheet(f"""
            QPushButton {{
                background-color: {self.current_color};
                border: 2px solid #e0e0e0;
                border-radius: 15px;
            }}
            QPushButton:hover {{
                border: 2px solid #7f8c8d;
            }}
        """)


class CourseDialog(QDialog):
    def __init__(self, parent=None, course_base: CourseBase = None, course_detail: CourseDetail = None):
        super().__init__(parent)

        # === [核心修改 1] 加载配置 ===
        self.config = Config.load()

        self.edit_mode = course_base is not None and course_detail is not None
        self.course_base = course_base
        self.course_detail = course_detail

        self.result_course_base = None
        self.result_course_detail = None
        self.custom_color = None

        self._init_ui()
        if self.edit_mode:
            self._load_course_data()
        else:
            self._update_auto_color()

    def _init_ui(self):
        self.setWindowTitle("编辑课程" if self.edit_mode else "添加课程")
        self.setFixedWidth(520)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # --- 1. 基础信息 ---
        group_basic = QGroupBox("基础信息")
        group_basic.setStyleSheet("""
            QGroupBox { font-weight: bold; border: 1px solid #e0e0e0; border-radius: 6px; margin-top: 10px; padding-top: 15px; }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 3px; color: #7f8c8d; }
        """)
        form_layout = QFormLayout(group_basic)

        name_color_layout = QHBoxLayout()
        self.name_edit = QLineEdit()
        self.name_edit.setPlaceholderText("例如：高等数学")
        self.name_edit.textChanged.connect(self._on_name_changed)

        self.btn_color = ColorButton()
        self.btn_color.setToolTip("点击选择颜色 (当前为自动生成)")
        self.btn_color.clicked.connect(self._pick_color)

        self.lbl_color_status = QLabel("(自动)")
        self.lbl_color_status.setStyleSheet("color: #7f8c8d; font-size: 11px;")

        name_color_layout.addWidget(self.name_edit)
        name_color_layout.addWidget(self.btn_color)
        name_color_layout.addWidget(self.lbl_color_status)

        form_layout.addRow("课程名称:", name_color_layout)

        self.teacher_edit = QLineEdit()
        self.location_edit = QLineEdit()

        form_layout.addRow("教师姓名:", self.teacher_edit)
        form_layout.addRow("上课地点:", self.location_edit)
        layout.addWidget(group_basic)

        # --- 2. 时间设置 ---
        group_time = QGroupBox("时间设置")
        group_time.setStyleSheet(group_basic.styleSheet())
        vbox_time = QVBoxLayout(group_time)

        hbox_time = QHBoxLayout()
        self.day_combo = QComboBox()
        self.day_combo.addItems(["周一", "周二", "周三", "周四", "周五", "周六", "周日"])

        self.start_section_spin = QSpinBox()

        # === [核心修改 2] 动态设置最大节数 ===
        # 读取配置中的 total_courses_per_day (默认12)
        max_section = self.config.total_courses_per_day
        self.start_section_spin.setRange(1, max_section)

        self.duration_combo = QComboBox()
        self.duration_combo.addItems([f"{i} 节" for i in range(1, 5)])
        self.duration_combo.setCurrentIndex(1)

        hbox_time.addWidget(QLabel("星期:"))
        hbox_time.addWidget(self.day_combo)
        hbox_time.addWidget(QLabel("第:"))
        hbox_time.addWidget(self.start_section_spin)
        hbox_time.addWidget(QLabel("节  持续:"))
        hbox_time.addWidget(self.duration_combo)
        vbox_time.addLayout(hbox_time)
        layout.addWidget(group_time)

        # --- 3. 周次设置 ---
        group_week = QGroupBox("周次设置")
        group_week.setStyleSheet(group_basic.styleSheet())
        vbox_week = QVBoxLayout(group_week)

        hbox_quick = QHBoxLayout()
        lbl_quick = QLabel("快速选择:")
        lbl_quick.setStyleSheet("color: #7f8c8d; font-weight: normal;")

        btn_all = QPushButton("全选")
        btn_odd = QPushButton("单周")
        btn_even = QPushButton("双周")
        btn_clear = QPushButton("清空")

        for btn in [btn_all, btn_odd, btn_even, btn_clear]:
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setFixedHeight(24)
            btn.setStyleSheet("""
                QPushButton { background: #f0f0f0; border: none; border-radius: 4px; padding: 0 10px; color: #333; }
                QPushButton:hover { background: #e0e0e0; }
            """)
            hbox_quick.addWidget(btn)
        hbox_quick.addStretch()

        vbox_week.addLayout(hbox_quick)
        vbox_week.addWidget(lbl_quick)

        grid_weeks = QGridLayout()
        grid_weeks.setSpacing(5)
        self.week_buttons = []

        for i in range(1, 21):
            btn = QPushButton(f"{i}")
            btn.setCheckable(True)
            btn.setFixedSize(36, 30)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet("""
                QPushButton { background-color: #f5f5f5; border: 1px solid #dcdcdc; border-radius: 4px; color: #666; }
                QPushButton:checked { background-color: #3498db; border: 1px solid #3498db; color: white; font-weight: bold; }
            """)

            row = (i - 1) // 6
            col = (i - 1) % 6
            grid_weeks.addWidget(btn, row, col)
            self.week_buttons.append(btn)

        vbox_week.addLayout(grid_weeks)
        layout.addWidget(group_week)

        btn_all.clicked.connect(lambda: self._quick_select("all"))
        btn_odd.clicked.connect(lambda: self._quick_select("odd"))
        btn_even.clicked.connect(lambda: self._quick_select("even"))
        btn_clear.clicked.connect(lambda: self._quick_select("clear"))

        # --- 底部按钮 ---
        hbox_actions = QHBoxLayout()
        self.btn_delete = QPushButton("🗑️ 删除")
        self.btn_delete.setStyleSheet("color: #e74c3c; background: transparent; font-weight: bold;")
        self.btn_delete.setVisible(self.edit_mode)
        self.btn_delete.clicked.connect(self._on_delete_clicked)

        btn_cancel = QPushButton("取消")
        btn_cancel.clicked.connect(self.reject)

        btn_save = QPushButton("💾 保存")
        btn_save.setStyleSheet("""
            QPushButton { background-color: #3498db; color: white; border-radius: 4px; padding: 6px 20px; font-weight: bold; }
            QPushButton:hover { background-color: #2980b9; }
        """)
        btn_save.clicked.connect(self._on_save)

        hbox_actions.addWidget(self.btn_delete)
        hbox_actions.addStretch()
        hbox_actions.addWidget(btn_cancel)
        hbox_actions.addWidget(btn_save)
        layout.addLayout(hbox_actions)

    def _on_delete_clicked(self):
        reply = QMessageBox.question(self, "确认删除", "确定要删除这门课程吗？",
                                     QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            self.done(2)

    def _on_name_changed(self):
        if self.custom_color is None:
            self._update_auto_color()

    def _update_auto_color(self):
        name = self.name_edit.text()
        auto_color = ColorManager.get_color_for_course(name)
        self.btn_color.set_color(auto_color)
        self.lbl_color_status.setText("(自动)")

    def _pick_color(self):
        current = self.custom_color if self.custom_color else self.btn_color.get_color()
        color = QColorDialog.getColor(QColor(current), self, "选择课程颜色")
        if color.isValid():
            self.custom_color = color.name()
            self.btn_color.set_color(self.custom_color)
            self.lbl_color_status.setText("(手动)")

    def _quick_select(self, mode):
        for i, btn in enumerate(self.week_buttons):
            week_num = i + 1
            if mode == "clear":
                btn.setChecked(False)
            elif mode == "all":
                btn.setChecked(True)
            elif mode == "odd":
                btn.setChecked(week_num % 2 != 0)
            elif mode == "even":
                btn.setChecked(week_num % 2 == 0)

    def _load_course_data(self):
        if self.course_base:
            self.name_edit.setText(self.course_base.name)
            self.custom_color = self.course_base.color
            self.btn_color.set_color(self.custom_color)
            self.lbl_color_status.setText("(当前)")

        if self.course_detail:
            self.teacher_edit.setText(self.course_detail.teacher)
            self.location_edit.setText(self.course_detail.location)
            self.day_combo.setCurrentIndex(self.course_detail.day_of_week - 1)
            self.start_section_spin.setValue(self.course_detail.start_section)
            idx = self.duration_combo.findText(f"{self.course_detail.step} 节")
            if idx >= 0: self.duration_combo.setCurrentIndex(idx)

            start = self.course_detail.start_week
            end = self.course_detail.end_week
            w_type = self.course_detail.week_type

            for i, btn in enumerate(self.week_buttons):
                w = i + 1
                should_check = False
                if start <= w <= end:
                    if w_type == WeekType.EVERY_WEEK:
                        should_check = True
                    elif w_type == WeekType.ODD_WEEK and w % 2 != 0:
                        should_check = True
                    elif w_type == WeekType.EVEN_WEEK and w % 2 == 0:
                        should_check = True
                btn.setChecked(should_check)

    def _on_save(self):
        name = self.name_edit.text().strip()
        if not name:
            QMessageBox.warning(self, "提示", "课程名称不能为空")
            return

        selected_weeks = [i + 1 for i, btn in enumerate(self.week_buttons) if btn.isChecked()]
        if not selected_weeks:
            QMessageBox.warning(self, "提示", "请至少选择一个周次")
            return

        start_week = min(selected_weeks)
        end_week = max(selected_weeks)

        is_all_odd = all(w % 2 != 0 for w in selected_weeks)
        is_all_even = all(w % 2 == 0 for w in selected_weeks)

        week_type = WeekType.EVERY_WEEK
        if is_all_odd:
            week_type = WeekType.ODD_WEEK
        elif is_all_even:
            week_type = WeekType.EVEN_WEEK

        if self.edit_mode:
            course_id = self.course_base.id
        else:
            course_id = str(uuid.uuid4())

        if self.custom_color:
            final_color = self.custom_color
        else:
            final_color = ColorManager.get_color_for_course(name)

        self.result_course_base = CourseBase(name=name, color=final_color, note="", course_id=course_id)

        step = int(self.duration_combo.currentText().split()[0])
        self.result_course_detail = CourseDetail(
            course_id=course_id,
            teacher=self.teacher_edit.text(),
            location=self.location_edit.text(),
            day_of_week=self.day_combo.currentIndex() + 1,
            start_section=self.start_section_spin.value(),
            step=step,
            start_week=start_week,
            end_week=end_week,
            week_type=week_type
        )
        self.accept()

    def get_course_data(self):
        return self.result_course_base, self.result_course_detail