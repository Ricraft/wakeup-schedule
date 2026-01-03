"""
常规设置页面
src/ui/general_settings_tab.py
"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QDateEdit,
    QCheckBox, QLabel, QGroupBox, QPushButton, QMessageBox
)
from PyQt6.QtCore import QDate, Qt
from src.models.config import Config

class GeneralSettingsTab(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.config = Config.load()
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        # 标题
        title = QLabel("常规设置")
        title.setStyleSheet("font-size: 18px; font-weight: bold; color: #2c3e50;")
        layout.addWidget(title)

        # --- 学期设置组 ---
        group_semester = QGroupBox("学期设置")
        group_semester.setStyleSheet("""
            QGroupBox { border: 1px solid #e0e0e0; border-radius: 8px; margin-top: 10px; padding-top: 15px; font-weight: bold; }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; color: #7f8c8d; }
        """)
        form_layout = QFormLayout(group_semester)
        form_layout.setSpacing(15)

        # 开学日期选择器
        self.date_edit = QDateEdit()
        self.date_edit.setCalendarPopup(True)
        self.date_edit.setDisplayFormat("yyyy-MM-dd")

        # 加载当前配置的日期
        try:
            current_date = QDate.fromString(self.config.semester_start_date, "yyyy-MM-dd")
            self.date_edit.setDate(current_date)
        except:
            self.date_edit.setDate(QDate.currentDate())

        form_layout.addRow("当前学期开始日期:", self.date_edit)
        layout.addWidget(group_semester)

        # --- 其他设置组 (示例) ---
        group_other = QGroupBox("启动选项")
        group_other.setStyleSheet(group_semester.styleSheet())
        vbox_other = QVBoxLayout(group_other)

        self.check_startup = QCheckBox("开机自动启动 (开发中...)")
        self.check_startup.setEnabled(False) # 暂时禁用
        vbox_other.addWidget(self.check_startup)

        layout.addWidget(group_other)

        layout.addStretch()

        # 保存按钮
        btn_save = QPushButton("💾 保存常规设置")
        btn_save.setObjectName("PrimaryButton")
        btn_save.setStyleSheet("""
            QPushButton { background-color: #3498db; color: white; border-radius: 6px; padding: 8px 15px; font-weight: bold; }
            QPushButton:hover { background-color: #2980b9; }
        """)
        btn_save.clicked.connect(self._on_save)
        layout.addWidget(btn_save)

    def _on_save(self):
        """保存配置"""
        try:
            # 更新配置对象
            new_date = self.date_edit.date().toString("yyyy-MM-dd")
            self.config.semester_start_date = new_date

            # 保存到文件
            self.config.save()

            QMessageBox.information(self, "成功", "常规设置已保存，重启或刷新后生效。")

            # 这里可以发送信号通知主窗口刷新，但为了简单起见，暂不实现

        except Exception as e:
            QMessageBox.warning(self, "错误", f"保存失败: {str(e)}")