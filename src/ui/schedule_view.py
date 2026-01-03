"""
课表视图组件 (Modern UI v2.2 - 修复背景绘制)
src/ui/schedule_view.py

修复方案：
1. 移除 WA_TranslucentBackground 属性，避免 paintEngine 报错
2. 使用 eventFilter 在 viewport 上绘制背景
3. 确保背景在表格内容之下正确渲染
"""

from PyQt6.QtWidgets import (
    QTableWidget, QTableWidgetItem, QHeaderView, QAbstractItemView,
    QWidget, QLabel, QVBoxLayout, QStyledItemDelegate,
    QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, pyqtSignal, QRect, QEvent
from PyQt6.QtGui import QColor, QFont, QMovie, QPainter, QPixmap, QPen
from typing import List
from datetime import date, timedelta
from pathlib import Path as FilePath
import sys
from pathlib import Path

current_dir = Path(__file__).resolve().parent
src_dir = current_dir.parent.parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

from src.models.course_base import CourseBase
from src.models.course_detail import CourseDetail
from src.models.time_slot import TimeSlot
from src.ui.overlay_scrollbar import OverlayScrollBar


class TimeColumnDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        painter.save()
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # 画底部分割线
        painter.setPen(QColor(0, 0, 0, 30))
        painter.drawLine(option.rect.bottomLeft(), option.rect.bottomRight())

        text = index.data()
        if text:
            parts = text.split('\n')
            rect = option.rect

            if len(parts) >= 1:
                section_num = parts[0]
                font_sec = QFont("Microsoft YaHei", 16, QFont.Weight.Bold)
                painter.setFont(font_sec)
                painter.setPen(QColor("#2c3e50"))
                sec_rect = QRect(rect.left(), rect.top() + 10, rect.width(), 30)
                painter.drawText(sec_rect, Qt.AlignmentFlag.AlignCenter, section_num)

            if len(parts) >= 3:
                start_time = parts[1]
                end_time = parts[2]
                font_time = QFont("Arial", 9)
                painter.setFont(font_time)
                painter.setPen(QColor("#7f8c8d"))

                t1_rect = QRect(rect.left(), rect.top() + 40, rect.width(), 15)
                painter.drawText(t1_rect, Qt.AlignmentFlag.AlignCenter, start_time)

                t2_rect = QRect(rect.left(), rect.top() + 58, rect.width(), 15)
                painter.drawText(t2_rect, Qt.AlignmentFlag.AlignCenter, end_time)

        painter.restore()


class CourseWidget(QWidget):
    clicked = pyqtSignal()

    def __init__(self, course_name, location, teacher, color, parent=None):
        super().__init__(parent)
        self.base_color = color

        r, g, b, a = color.red(), color.green(), color.blue(), color.alpha()
        bg_style = f"rgba({r}, {g}, {b}, {a})"

        self.setStyleSheet(
            f"QWidget#CardContent {{ background-color: {bg_style}; border-radius: 8px; }} "
            f"QLabel {{ background: transparent; border: none; font-family: 'Microsoft YaHei'; }}"
        )

        main = QVBoxLayout(self)
        main.setContentsMargins(2, 2, 2, 2)
        self.content = QWidget()
        self.content.setObjectName("CardContent")
        main.addWidget(self.content)

        layout = QVBoxLayout(self.content)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(2)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        is_dark = (0.299 * r + 0.587 * g + 0.114 * b) < 128
        tc = "white" if is_dark else "#333333"

        lbl_n = QLabel(course_name)
        lbl_n.setFont(QFont("Microsoft YaHei", 10, QFont.Weight.Bold))
        lbl_n.setWordWrap(True)
        lbl_n.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_n.setStyleSheet(f"color: {tc};")

        lbl_t = None
        if teacher:
            lbl_t = QLabel(teacher)
            lbl_t.setFont(QFont("Microsoft YaHei", 9))
            lbl_t.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl_t.setStyleSheet(f"color: {tc}; opacity: 0.9;")

        lbl_l = QLabel(f"@{location}")
        lbl_l.setFont(QFont("Microsoft YaHei", 9, QFont.Weight.Bold))
        lbl_l.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_l.setStyleSheet(f"color: {tc};")

        layout.addStretch()
        layout.addWidget(lbl_n)
        if lbl_t: layout.addWidget(lbl_t)
        layout.addWidget(lbl_l)
        layout.addStretch()

        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(8)
        shadow.setColor(QColor(0, 0, 0, 30))
        shadow.setOffset(0, 2)
        self.content.setGraphicsEffect(shadow)

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        self.clicked.emit()

    def update_opacity(self, opacity):
        c = self.base_color
        new_alpha = int(255 * opacity)
        new_bg = f"rgba({c.red()}, {c.green()}, {c.blue()}, {new_alpha})"
        self.setStyleSheet(
            f"QWidget#CardContent {{ background-color: {new_bg}; border-radius: 8px; }} "
            f"QLabel {{ background: transparent; border: none; font-family: 'Microsoft YaHei'; }}"
        )


class ScheduleView(QTableWidget):
    course_clicked = pyqtSignal(object, object)
    empty_cell_clicked = pyqtSignal(int, int)

    def __init__(self, time_slots: List[TimeSlot], parent=None):
        super().__init__(len(time_slots), 8, parent)
        self.time_slots = time_slots
        self.current_week = 1
        self.semester_start_date = date.today()
        self.background_opacity = 1.0
        self.course_opacity = 0.95
        self.background_movie = None
        self.background_pixmap = None
        self.cell_courses = {}

        self._init_table_ui()
        self.cellClicked.connect(self._on_cell_clicked)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.overlay_scroll = OverlayScrollBar(self)

        # === [核心修复] 背景绘制配置 ===
        # 1. 视口不自动填充背景
        self.viewport().setAutoFillBackground(False)

        # 2. 移除边框
        self.setFrameShape(QTableWidget.Shape.NoFrame)
        
        # 3. 安装事件过滤器在 viewport 上绘制背景
        self.viewport().installEventFilter(self)
        
        # 4. 让表头也能透明显示背景
        self.horizontalHeader().setAutoFillBackground(False)
        self.horizontalHeader().installEventFilter(self)

    def _init_table_ui(self):
        headers = ["", "周一", "周二", "周三", "周四", "周五", "周六", "周日"]
        self.setHorizontalHeaderLabels(headers)
        self.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.horizontalHeader().setSectionResizeMode(0, QHeaderView.ResizeMode.Fixed)
        self.setColumnWidth(0, 70)
        self.verticalHeader().setVisible(False)
        self.setSelectionMode(QAbstractItemView.SelectionMode.NoSelection)
        self.setShowGrid(False)
        self.setFrameShape(QTableWidget.Shape.NoFrame)

        self.setItemDelegateForColumn(0, TimeColumnDelegate(self))
        self._refresh_time_column()
        for i in range(self.rowCount()): 
            self.setRowHeight(i, 75)
        
        # 设置默认透明样式
        self.set_header_style("transparent")

    def eventFilter(self, obj, event):
        """事件过滤器：在 viewport 和表头上绘制背景"""
        if event.type() == QEvent.Type.Paint:
            # 获取背景图片
            pixmap = None
            if self.background_movie:
                pixmap = self.background_movie.currentPixmap()
            elif self.background_pixmap:
                pixmap = self.background_pixmap
            
            if obj == self.viewport():
                # 在 viewport 上绘制背景
                painter = QPainter(self.viewport())
                if painter.isActive():
                    self._draw_background(painter, self.viewport().rect(), pixmap, 
                                         offset_y=0)
                    painter.end()
            
            elif obj == self.horizontalHeader():
                # 在表头上绘制背景的对应部分
                painter = QPainter(self.horizontalHeader())
                if painter.isActive():
                    # 表头的背景需要从整体背景的顶部开始
                    header_rect = self.horizontalHeader().rect()
                    self._draw_background(painter, header_rect, pixmap, 
                                         offset_y=0, is_header=True)
                    painter.end()
        
        # 继续传递事件
        return super().eventFilter(obj, event)
    
    def _draw_background(self, painter, rect, pixmap, offset_y=0, is_header=False):
        """
        绘制背景图片
        
        Args:
            painter: QPainter 对象
            rect: 绘制区域
            pixmap: 背景图片
            offset_y: Y 轴偏移量
            is_header: 是否是表头
        """
        painter.setRenderHint(QPainter.RenderHint.SmoothPixmapTransform)
        
        if pixmap and not pixmap.isNull():
            painter.setOpacity(self.background_opacity)
            
            # 计算整个表格的大小（包括表头）
            header_height = self.horizontalHeader().height()
            total_height = self.viewport().height() + header_height
            total_width = self.viewport().width()
            
            # 缩放图片以覆盖整个区域
            from PyQt6.QtCore import QSize
            total_size = QSize(total_width, total_height)
            scaled = pixmap.scaled(
                total_size,
                Qt.AspectRatioMode.KeepAspectRatioByExpanding,
                Qt.TransformationMode.SmoothTransformation
            )
            
            # 计算居中位置
            x = (total_width - scaled.width()) // 2
            y = (total_height - scaled.height()) // 2
            
            if is_header:
                # 表头只绘制背景的顶部部分
                painter.drawPixmap(x, y, scaled)
            else:
                # viewport 绘制时需要偏移表头高度
                painter.drawPixmap(x, y - header_height, scaled)
        else:
            # 默认绘制白底
            painter.fillRect(rect, Qt.GlobalColor.white)

    def _refresh_time_column(self):
        """刷新时间列内容"""
        for i, time_slot in enumerate(self.time_slots):
            start_str = time_slot.start_time.strftime('%H:%M')
            end_str = time_slot.end_time.strftime('%H:%M')
            time_text = f"{time_slot.section_number}\n{start_str}\n{end_str}"
            item = QTableWidgetItem(time_text)
            item.setFlags(Qt.ItemFlag.ItemIsEnabled)
            self.setItem(i, 0, item)
    
    def _update_time_column_style(self, style_mode):
        """
        更新时间列样式以匹配表头
        
        Args:
            style_mode: 样式模式 ("translucent", "transparent", 或其他)
        """
        if style_mode == "translucent":
            bg_color = QColor(255, 255, 255, 102)  # 40% 不透明度
            fg_color = QColor("#5f6368")
        elif style_mode == "transparent":
            bg_color = QColor(255, 255, 255, 0)  # 完全透明
            fg_color = QColor("#2c3e50")  # 深色文字
        else:
            bg_color = QColor(248, 249, 250, 255)  # 不透明
            fg_color = QColor("#444444")
        
        # 更新所有时间列单元格
        for row in range(self.rowCount()):
            item = self.item(row, 0)
            if item:
                item.setBackground(bg_color)
                item.setForeground(fg_color)

    def update_courses(self, courses):
        self._clear_course_cells()
        self.cell_courses.clear()
        course_grid = {}

        for base, detail in courses:
            if not (detail.start_week <= self.current_week <= detail.end_week): 
                continue
            if not detail.week_type.matches_week(self.current_week): 
                continue

            day = detail.day_of_week
            for section in range(detail.start_section, detail.end_section + 1):
                key = (day, section)
                if key not in course_grid: 
                    course_grid[key] = []
                course_grid[key].append((base, detail))

        for (day, section), course_list in course_grid.items():
            row = self._get_row_for_section(section)
            if row is not None and course_list:
                base, detail = course_list[0]
                if section == detail.start_section:
                    self._set_course_cell(row, day, base, detail)

    def _get_row_for_section(self, section):
        for i, ts in enumerate(self.time_slots):
            if ts.section_number == section: 
                return i
        return None

    def _set_course_cell(self, row, col, base, detail):
        try:
            base_color = QColor(base.color)
        except:
            base_color = QColor("#E3F2FD")

        current_alpha = int(255 * self.course_opacity)
        final_color = QColor(
            base_color.red(), 
            base_color.green(), 
            base_color.blue(), 
            current_alpha
        )

        course_widget = CourseWidget(
            base.name, 
            detail.location, 
            detail.teacher, 
            final_color
        )
        course_widget.clicked.connect(
            lambda: self._on_course_widget_clicked(row, col)
        )

        self.setCellWidget(row, col, course_widget)
        if detail.step > 1: 
            self.setSpan(row, col, detail.step, 1)
        self.cell_courses[(row, col)] = (base, detail)

    def _on_course_widget_clicked(self, row, col):
        if (row, col) in self.cell_courses: 
            self.course_clicked.emit(*self.cell_courses[(row, col)])

    def _clear_course_cells(self):
        self.clearSpans()
        for row in range(self.rowCount()):
            for col in range(1, self.columnCount()): 
                self.removeCellWidget(row, col)
                self.setItem(row, col, QTableWidgetItem(""))

    def _on_cell_clicked(self, row, col):
        if col == 0: 
            return
        if not self.cellWidget(row, col):
            if row < len(self.time_slots): 
                self.empty_cell_clicked.emit(col, self.time_slots[row].section_number)

    def set_semester_start_date(self, start_date: date):
        self.semester_start_date = start_date
        self.update_header_dates()

    def update_header_dates(self):
        week_start = self.semester_start_date + timedelta(weeks=self.current_week - 1)
        current_month = date.today().month
        item_0 = QTableWidgetItem(f"{current_month}\n月")
        item_0.setFont(QFont("Microsoft YaHei", 12, QFont.Weight.Bold))
        item_0.setForeground(QColor("#2d8cf0"))
        self.setHorizontalHeaderItem(0, item_0)

        week_names = ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
        today = date.today()
        for i in range(7):
            current_date = week_start + timedelta(days=i)
            text = f"{week_names[i]}\n{current_date.strftime('%m/%d')}"
            item = QTableWidgetItem(text)
            font = QFont("Microsoft YaHei")
            font.setPixelSize(13)
            col_index = i + 1
            if current_date == today:
                font.setBold(True)
                font.setPixelSize(14)
                item.setForeground(QColor("#2d8cf0"))
            else:
                font.setBold(False)
                item.setForeground(QColor("#5f6368"))
            item.setFont(font)
            self.setHorizontalHeaderItem(col_index, item)

    def set_week(self, week):
        self.current_week = week
        self.update_header_dates()

    def set_background_opacity(self, opacity: float):
        self.background_opacity = opacity
        self.viewport().update()
        self.horizontalHeader().update()

    def set_course_opacity(self, opacity: float):
        self.course_opacity = opacity
        for row in range(self.rowCount()):
            for col in range(self.columnCount()):
                widget = self.cellWidget(row, col)
                if isinstance(widget, CourseWidget): 
                    widget.update_opacity(opacity)

    def set_background(self, image_path: str, opacity: float):
        self.background_opacity = opacity
        if self.background_movie: 
            self.background_movie.stop()
            self.background_movie = None
        
        if not image_path or not FilePath(image_path).exists():
            self.background_pixmap = None
        elif image_path.lower().endswith('.gif'):
            self.background_movie = QMovie(image_path)
            # 连接到 viewport 和表头的更新
            self.background_movie.frameChanged.connect(self.viewport().update)
            self.background_movie.frameChanged.connect(self.horizontalHeader().update)
            self.background_movie.start()
            self.background_pixmap = None
        else:
            self.background_pixmap = QPixmap(image_path)
        
        self.viewport().update()
        self.horizontalHeader().update()

    def update_time_slots(self, time_slots: List[TimeSlot]):
        self.time_slots = time_slots
        self.setRowCount(len(time_slots))
        for i in range(self.rowCount()): 
            self.setRowHeight(i, 75)
        self._refresh_time_column()
        self.viewport().update()

    def set_header_style(self, style_mode):
        """
        设置表头样式
        
        Args:
            style_mode: 样式模式
                - "translucent": 半透明毛玻璃效果 (40% 不透明度)
                - "transparent": 完全透明，显示背景图片
                - 其他: 默认不透明样式
        """
        if style_mode == "translucent":
            bg_color = "rgba(255, 255, 255, 102)"  # 40% 不透明度
            border_color = "rgba(0, 0, 0, 20)"
            text_color = "#5f6368"
        elif style_mode == "transparent":
            bg_color = "rgba(255, 255, 255, 0)"  # 完全透明
            border_color = "rgba(255, 255, 255, 80)"  # 半透明白色边框
            text_color = "#2c3e50"  # 深色文字，确保在背景上可读
        else:
            bg_color = "rgba(248, 249, 250, 255)"
            border_color = "#E0E0E0"
            text_color = "#5f6368"

        style = f"""
            QHeaderView::section {{
                background-color: {bg_color};
                color: {text_color};
                border: none;
                border-bottom: 1px solid {border_color};
                border-right: 1px solid {border_color};
                padding: 4px;
                font-weight: bold;
            }}
            QTableCornerButton::section {{
                background-color: {bg_color};
                border: none;
                border-bottom: 1px solid {border_color};
                border-right: 1px solid {border_color};
            }}
        """
        self.horizontalHeader().setStyleSheet(style)
        
        # 更新角落按钮样式
        if self.findChild(QWidget):
            corner = self.findChild(QWidget)
            if corner: 
                corner.setStyleSheet(
                    f"background-color: {bg_color}; "
                    f"border-bottom: 1px solid {border_color};"
                )
        
        # 更新时间列样式以匹配表头
        self._update_time_column_style(style_mode)

    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.viewport().update()
        self.horizontalHeader().update()
        if hasattr(self, 'overlay_scroll'):
            self.overlay_scroll.update_position()
