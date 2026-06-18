import sys
import math
from datetime import datetime, timedelta
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QRectF, QPointF
from PyQt6.QtWidgets import (
    QWidget, QFrame, QVBoxLayout, QHBoxLayout, QLabel, 
    QPushButton, QScrollArea, QDialog, QLineEdit, 
    QTextEdit, QMessageBox, QGraphicsDropShadowEffect, QComboBox
)
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QLinearGradient
from localization import Localization

class CircularTimerWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(220, 220)
        self.progress = 1.0 # 0.0 to 1.0
        self.time_str = "25:00"
        self.is_work_session = True

    def set_progress(self, progress, time_str, is_work_session=True):
        self.progress = max(0.0, min(1.0, progress))
        self.time_str = time_str
        self.is_work_session = is_work_session
        self.update() # Triggers paintEvent

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        width = self.width()
        height = self.height()
        size = min(width, height) - 20
        x = (width - size) / 2
        y = (height - size) / 2

        # Draw outer subtle glow background circle
        rect = QRectF(x, y, size, size)
        
        # Draw background track circle
        track_pen = QPen(QColor("#1e293b"))
        track_pen.setWidth(12)
        painter.setPen(track_pen)
        painter.drawEllipse(rect)

        # Draw active progress arc
        progress_pen_color = QColor("#6366f1") if self.is_work_session else QColor("#10b981") # Indigo for Work, Emerald for Break
        progress_pen = QPen(progress_pen_color)
        progress_pen.setWidth(12)
        progress_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(progress_pen)

        # Draw arc (angle in 1/16th of a degree)
        start_angle = 90 * 16 # Start from top (90 degrees)
        span_angle = int(-self.progress * 360 * 16)
        painter.drawArc(rect, start_angle, span_angle)

        # Draw Time Text
        text_pen = QPen(QColor("#ffffff"))
        painter.setPen(text_pen)
        font = QFont("Inter", 32, QFont.Weight.Bold)
        painter.setFont(font)
        
        # Calculate text rect
        text_rect = QRectF(x, y + (size/2) - 30, size, 50)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, self.time_str)

        # Draw Mode Text below time
        mode_font = QFont("Inter", 11, QFont.Weight.Medium)
        painter.setFont(mode_font)
        mode_color = QColor("#a5b4fc") if self.is_work_session else QColor("#6ee7b7")
        painter.setPen(QPen(mode_color))
        
        mode_rect = QRectF(x, y + (size/2) + 20, size, 25)
        mode_str = Localization.get("work") if self.is_work_session else Localization.get("break")
        painter.drawText(mode_rect, Qt.AlignmentFlag.AlignCenter, mode_str)


class KanbanCardWidget(QFrame):
    # Signals for Card operations
    move_left = pyqtSignal(str) # task_id
    move_right = pyqtSignal(str) # task_id
    edit_task = pyqtSignal(str) # task_id
    delete_task = pyqtSignal(str) # task_id

    def __init__(self, task, parent=None):
        super().__init__(parent)
        self.setObjectName("kanbanCard")
        self.task_id = task["id"]
        self.task_data = task
        self.init_ui(task)

    def init_ui(self, task):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(8)

        # Header: Title & Priority
        header_layout = QHBoxLayout()
        header_layout.setContentsMargins(0, 0, 0, 0)
        
        title_label = QLabel(task["title"])
        title_label.setObjectName("cardTitle")
        title_label.setWordWrap(True)
        header_layout.addWidget(title_label, 1)

        priority = task.get("priority", "medium").lower()
        p_badge = QLabel(Localization.get(priority))
        if priority == "low":
            p_badge.setObjectName("badgeLow")
        elif priority == "high":
            p_badge.setObjectName("badgeHigh")
        else:
            p_badge.setObjectName("badgeMedium")
        p_badge.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header_layout.addWidget(p_badge, 0)
        
        layout.addLayout(header_layout)

        # Description
        desc_label = QLabel(task["description"])
        desc_label.setObjectName("cardDesc")
        desc_label.setWordWrap(True)
        if not task["description"]:
            desc_label.hide()
        layout.addWidget(desc_label)

        # Tags Layout
        tags = task.get("tags", [])
        if tags:
            tags_layout = QHBoxLayout()
            tags_layout.setSpacing(4)
            for tag in tags:
                tag_label = QLabel(f" #{tag} ")
                tag_label.setStyleSheet("color: #818cf8; font-size: 11px; font-weight: bold;")
                tags_layout.addWidget(tag_label)
            tags_layout.addStretch()
            layout.addLayout(tags_layout)

        # Bottom Bar: Buttons
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 4, 0, 0)
        bottom_layout.setSpacing(4)

        # Left Move button
        self.btn_left = QPushButton("←")
        self.btn_left.setObjectName("cardBtn")
        self.btn_left.setToolTip(Localization.get("move_back"))
        self.btn_left.setFixedWidth(28)
        self.btn_left.setFixedHeight(28)
        self.btn_left.clicked.connect(lambda: self.move_left.emit(self.task_id))
        
        # Right Move button
        self.btn_right = QPushButton("→")
        self.btn_right.setObjectName("cardBtn")
        self.btn_right.setToolTip(Localization.get("move_forward"))
        self.btn_right.setFixedWidth(28)
        self.btn_right.setFixedHeight(28)
        self.btn_right.clicked.connect(lambda: self.move_right.emit(self.task_id))

        # Edit button
        self.btn_edit = QPushButton("✏️")
        self.btn_edit.setObjectName("cardBtn")
        self.btn_edit.setToolTip(Localization.get("edit"))
        self.btn_edit.setFixedWidth(28)
        self.btn_edit.setFixedHeight(28)
        self.btn_edit.clicked.connect(lambda: self.edit_task.emit(self.task_id))

        # Delete button
        self.btn_delete = QPushButton("🗑️")
        self.btn_delete.setObjectName("cardBtn")
        self.btn_delete.setToolTip(Localization.get("delete"))
        self.btn_delete.setFixedWidth(28)
        self.btn_delete.setFixedHeight(28)
        self.btn_delete.clicked.connect(lambda: self.delete_task.emit(self.task_id))

        # Show buttons based on column status
        status = task.get("status", "todo")
        if status == "todo":
            self.btn_left.setEnabled(False)
            self.btn_left.hide()
        elif status == "done":
            self.btn_right.setEnabled(False)
            self.btn_right.hide()

        bottom_layout.addWidget(self.btn_left)
        bottom_layout.addWidget(self.btn_edit)
        bottom_layout.addWidget(self.btn_delete)
        bottom_layout.addStretch()
        bottom_layout.addWidget(self.btn_right)

        layout.addLayout(bottom_layout)

        # Drop shadow for card
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(8)
        shadow.setColor(QColor(0, 0, 0, 50))
        shadow.setOffset(0, 2)
        self.setGraphicsEffect(shadow)


class KanbanColumnWidget(QFrame):
    # Pass signals to main app
    add_task_clicked = pyqtSignal(str) # column_id
    clear_clicked = pyqtSignal() # New signal for clearing column
    card_move_left = pyqtSignal(str)
    card_move_right = pyqtSignal(str)
    card_edit = pyqtSignal(str)
    card_delete = pyqtSignal(str)

    def __init__(self, column_id, title, parent=None):
        super().__init__(parent)
        self.setObjectName("kanbanColumn")
        self.column_id = column_id
        self.title = title
        self.init_ui()

    def init_ui(self):
        # Main layout
        self.main_layout = QVBoxLayout(self)
        self.main_layout.setContentsMargins(8, 8, 8, 8)
        self.main_layout.setSpacing(10)

        # Header Frame
        header = QFrame()
        header.setObjectName("kanbanColumnHeader")
        header_layout = QHBoxLayout(header)
        header_layout.setContentsMargins(4, 4, 4, 8)

        # Title
        title_lbl = QLabel(self.title)
        title_lbl.setObjectName("columnTitle")
        header_layout.addWidget(title_lbl)
        
        # Clear Button (only for done column)
        if self.column_id == "done":
            clear_btn = QPushButton("🧹")
            clear_btn.setToolTip(Localization.get("clear_completed"))
            clear_btn.setStyleSheet("padding: 4px; font-size: 14px; background: transparent; color: #94a3b8;")
            clear_btn.setFixedWidth(32)
            clear_btn.clicked.connect(self.clear_clicked.emit)
            header_layout.addWidget(clear_btn)

        # Add Task Button inside header
        add_btn = QPushButton("+ " + Localization.get("add"))
        add_btn.setStyleSheet("padding: 4px 8px; font-size: 11px; max-width: 60px;")
        add_btn.clicked.connect(lambda: self.add_task_clicked.emit(self.column_id))
        header_layout.addWidget(add_btn)

        self.main_layout.addWidget(header)

        # Scroll Area for tasks
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet("background: transparent; border: none;")
        
        # Scroll container widget
        self.scroll_widget = QWidget()
        self.scroll_widget.setStyleSheet("background: transparent;")
        self.list_layout = QVBoxLayout(self.scroll_widget)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(8)
        self.list_layout.addStretch() # Push items to top

        scroll.setWidget(self.scroll_widget)
        self.main_layout.addWidget(scroll)

    def clear_cards(self):
        # Remove widgets from layout
        while self.list_layout.count() > 1:
            item = self.list_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def add_card(self, task):
        card = KanbanCardWidget(task)
        # Connect signals
        card.move_left.connect(self.card_move_left)
        card.move_right.connect(self.card_move_right)
        card.edit_task.connect(self.card_edit)
        card.delete_task.connect(self.card_delete)
        
        # Insert before the stretch
        self.list_layout.insertWidget(self.list_layout.count() - 1, card)


class TaskDialog(QDialog):
    def __init__(self, parent=None, task=None):
        super().__init__(parent)
        self.task = task
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(Localization.get("add_task") if not self.task else Localization.get("edit_task"))
        self.resize(380, 320)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(18, 18, 18, 18)
        layout.setSpacing(12)

        # Title Label
        dlg_title = QLabel(Localization.get("add_task") if not self.task else Localization.get("edit_task"))
        dlg_title.setObjectName("titleLabel")
        layout.addWidget(dlg_title)

        # Title Input
        layout.addWidget(QLabel(Localization.get("title")))
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText(Localization.get("title") + "...")
        layout.addWidget(self.title_input)

        # Description Input
        layout.addWidget(QLabel(Localization.get("description")))
        self.desc_input = QTextEdit()
        self.desc_input.setPlaceholderText(Localization.get("description") + "...")
        self.desc_input.setMaximumHeight(80)
        layout.addWidget(self.desc_input)

        # Priority & Tags Layout
        row = QHBoxLayout()
        
        # Priority
        priority_layout = QVBoxLayout()
        priority_layout.addWidget(QLabel(Localization.get("priority")))
        self.priority_combo = QComboBox()
        
        # Mapping for display names
        self.priority_map = {
            Localization.get("low"): "low",
            Localization.get("medium"): "medium",
            Localization.get("high"): "high"
        }
        self.priority_combo.addItems(list(self.priority_map.keys()))
        self.priority_combo.setCurrentText(Localization.get("medium")) # Default to Medium
        priority_layout.addWidget(self.priority_combo)
        row.addLayout(priority_layout, 1)

        # Tags
        tags_layout = QVBoxLayout()
        tags_layout.addWidget(QLabel(Localization.get("tags_label")))
        self.tags_input = QLineEdit()
        self.tags_input.setPlaceholderText(Localization.get("tags_placeholder"))
        tags_layout.addWidget(self.tags_input)
        row.addLayout(tags_layout, 1)

        layout.addLayout(row)

        # Fill if editing
        if self.task:
            self.title_input.setText(self.task["title"])
            self.desc_input.setText(self.task["description"])
            p_internal = self.task.get("priority", "medium").lower()
            # Find display name for internal priority
            display_name = Localization.get("medium")
            for d_name, i_name in self.priority_map.items():
                if i_name == p_internal:
                    display_name = d_name
                    break
            self.priority_combo.setCurrentText(display_name)
            self.tags_input.setText(", ".join(self.task.get("tags", [])))

        # Buttons
        btn_layout = QHBoxLayout()
        btn_layout.setContentsMargins(0, 10, 0, 0)
        
        self.btn_cancel = QPushButton(Localization.get("cancel"))
        self.btn_cancel.setObjectName("secondaryBtn")
        self.btn_cancel.clicked.connect(self.reject)
        
        self.btn_save = QPushButton(Localization.get("save"))
        self.btn_save.clicked.connect(self.save_clicked)

        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_save)
        
        layout.addLayout(btn_layout)

    def save_clicked(self):
        if not self.title_input.text().strip():
            QMessageBox.warning(self, Localization.get("warning"), Localization.get("title_empty_warning"))
            return
        self.accept()

    def get_data(self):
        tags_raw = self.tags_input.text().split(",")
        tags = [t.strip() for t in tags_raw if t.strip()]
        return {
            "title": self.title_input.text().strip(),
            "description": self.desc_input.toPlainText().strip(),
            "priority": self.priority_map.get(self.priority_combo.currentText(), "medium"),
            "tags": tags
        }


class AnalyticsChartWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(180)
        self.sessions = [] # list of {"date": "YYYY-MM-DD", "minutes": X}

    def set_stats(self, sessions):
        self.sessions = sessions
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Width and Height
        w = self.width()
        h = self.height()
        
        # Margins
        left_m = 40
        right_m = 20
        top_m = 25
        bottom_m = 35

        chart_w = w - left_m - right_m
        chart_h = h - top_m - bottom_m

        # Draw grid lines and Y axis
        grid_pen = QPen(QColor("#1e293b"))
        grid_pen.setWidth(1)
        painter.setPen(grid_pen)
        
        # We draw 4 horizontal grid lines
        for i in range(4):
            grid_y = top_m + chart_h * i / 3
            painter.drawLine(int(left_m), int(grid_y), int(w - right_m), int(grid_y))

        # Get last 7 days including today
        days = []
        today = datetime.now()
        for i in range(6, -1, -1):
            day = today - timedelta(days=i)
            days.append(day.strftime("%Y-%m-%d"))

        # Map day to minutes from sessions
        session_map = {s["date"]: s["minutes"] for s in self.sessions}
        chart_data = []
        for day in days:
            chart_data.append((day, session_map.get(day, 0)))

        # Find max minutes to scale chart
        max_minutes = max([d[1] for d in chart_data])
        if max_minutes < 60:
            max_minutes = 60 # Default scale is 1 hour

        # Draw Y-Axis Labels
        label_pen = QPen(QColor("#94a3b8"))
        painter.setPen(label_pen)
        font = QFont("Inter", 8, QFont.Weight.Medium)
        painter.setFont(font)
        
        # Y labels: 0, Max/2, Max
        m_unit = Localization.get("m")
        painter.drawText(5, int(top_m + chart_h + 4), f"{0}{m_unit}")
        painter.drawText(5, int(top_m + chart_h/2 + 4), f"{int(max_minutes/2)}{m_unit}")
        painter.drawText(5, int(top_m + 4), f"{int(max_minutes)}{m_unit}")

        # Draw Bars
        bar_count = len(chart_data)
        if bar_count == 0:
            return
            
        bar_spacing = chart_w / bar_count
        bar_w = bar_spacing * 0.6

        for idx, (date_str, mins) in enumerate(chart_data):
            # Bar placement
            bar_x = left_m + (idx * bar_spacing) + (bar_spacing - bar_w) / 2
            
            # Scaled height
            scaled_h = (mins / max_minutes) * chart_h
            bar_y = top_m + chart_h - scaled_h

            # Draw bar with gradient
            grad = QLinearGradient(bar_x, bar_y, bar_x, top_m + chart_h)
            grad.setColorAt(0.0, QColor("#6366f1")) # Indigo top
            grad.setColorAt(1.0, QColor("#4338ca")) # Deep indigo bottom
            
            painter.setBrush(QBrush(grad))
            painter.setPen(Qt.PenStyle.NoPen)
            painter.drawRoundedRect(QRectF(bar_x, bar_y, bar_w, scaled_h), 4.0, 4.0)

            # Draw X Label (Date)
            date_obj = datetime.strptime(date_str, "%Y-%m-%d")
            x_label = date_obj.strftime("%d %b") # e.g. "17 Jun"
            
            painter.setPen(label_pen)
            x_rect = QRectF(left_m + (idx * bar_spacing), h - bottom_m + 8, bar_spacing, 20)
            painter.drawText(x_rect, Qt.AlignmentFlag.AlignCenter, x_label)

            # Draw value on top of bar if it's > 0
            if mins > 0:
                val_font = QFont("Inter", 8, QFont.Weight.Bold)
                painter.setFont(val_font)
                painter.setPen(QPen(QColor("#ffffff")))
                val_rect = QRectF(bar_x - 10, bar_y - 15, bar_w + 20, 15)
                painter.drawText(val_rect, Qt.AlignmentFlag.AlignCenter, f"{int(mins)}")
                painter.setFont(font) # Restore default chart font


class PomodoroWidget(QFrame):
    session_completed = pyqtSignal(int) # Emits focus duration in minutes

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setObjectName("sidebarPanel")
        
        # Timer variables
        self.timer_seconds = 25 * 60
        self.total_seconds = 25 * 60
        self.is_running = False
        self.is_work_session = True # True = Work, False = Break

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timer_tick)

        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(15)

        # Title
        title = QLabel(Localization.get("focus_timer"))
        title.setObjectName("columnTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title)

        # Circular Timer View
        self.circular_timer = CircularTimerWidget()
        layout.addWidget(self.circular_timer, 0, Qt.AlignmentFlag.AlignCenter)

        # Controls Button row
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(8)

        self.btn_start = QPushButton(Localization.get("start"))
        self.btn_start.clicked.connect(self.start_timer)
        self.btn_start.setStyleSheet("background-color: #10b981;") # Emerald green for start
        
        self.btn_pause = QPushButton(Localization.get("pause"))
        self.btn_pause.clicked.connect(self.pause_timer)
        self.btn_pause.setObjectName("secondaryBtn")
        self.btn_pause.setEnabled(False)

        self.btn_reset = QPushButton(Localization.get("reset"))
        self.btn_reset.clicked.connect(self.reset_timer)
        self.btn_reset.setObjectName("secondaryBtn")

        btn_layout.addWidget(self.btn_start)
        btn_layout.addWidget(self.btn_pause)
        btn_layout.addWidget(self.btn_reset)
        layout.addLayout(btn_layout)

        # Fast adjustments
        adj_layout = QHBoxLayout()
        adj_layout.setSpacing(6)
        
        self.btn_25min = QPushButton(Localization.get("work_btn"))
        self.btn_25min.setObjectName("secondaryBtn")
        self.btn_25min.setStyleSheet("font-size: 11px; padding: 5px;")
        self.btn_25min.clicked.connect(lambda: self.set_duration(25, True))

        self.btn_5min = QPushButton(Localization.get("break_short_btn"))
        self.btn_5min.setObjectName("secondaryBtn")
        self.btn_5min.setStyleSheet("font-size: 11px; padding: 5px;")
        self.btn_5min.clicked.connect(lambda: self.set_duration(5, False))

        self.btn_15min = QPushButton(Localization.get("break_long_btn"))
        self.btn_15min.setObjectName("secondaryBtn")
        self.btn_15min.setStyleSheet("font-size: 11px; padding: 5px;")
        self.btn_15min.clicked.connect(lambda: self.set_duration(15, False))

        adj_layout.addWidget(self.btn_25min)
        adj_layout.addWidget(self.btn_5min)
        adj_layout.addWidget(self.btn_15min)
        layout.addLayout(adj_layout)

        self.update_display()

    def set_duration(self, minutes, is_work):
        self.timer.stop()
        self.is_running = False
        self.is_work_session = is_work
        self.timer_seconds = minutes * 60
        self.total_seconds = minutes * 60
        
        self.btn_start.setEnabled(True)
        self.btn_start.setText(Localization.get("start"))
        self.btn_start.setStyleSheet("background-color: #10b981;")
        self.btn_pause.setEnabled(False)
        self.update_display()

    def update_display(self):
        mins = self.timer_seconds // 60
        secs = self.timer_seconds % 60
        time_str = f"{mins:02d}:{secs:02d}"
        
        # Calculate progress ratio
        progress = self.timer_seconds / self.total_seconds if self.total_seconds > 0 else 0
        self.circular_timer.set_progress(progress, time_str, self.is_work_session)

    def start_timer(self):
        if not self.is_running:
            self.is_running = True
            self.timer.start(1000)
            self.btn_start.setEnabled(False)
            self.btn_start.setText(Localization.get("running"))
            self.btn_start.setStyleSheet("background-color: #4b5563;")
            self.btn_pause.setEnabled(True)

    def pause_timer(self):
        if self.is_running:
            self.is_running = False
            self.timer.stop()
            self.btn_start.setEnabled(True)
            self.btn_start.setText(Localization.get("resume"))
            self.btn_start.setStyleSheet("background-color: #10b981;")
            self.btn_pause.setEnabled(False)

    def reset_timer(self):
        self.timer.stop()
        self.is_running = False
        self.timer_seconds = self.total_seconds
        
        self.btn_start.setEnabled(True)
        self.btn_start.setText(Localization.get("start"))
        self.btn_start.setStyleSheet("background-color: #10b981;")
        self.btn_pause.setEnabled(False)
        self.update_display()

    def timer_tick(self):
        if self.timer_seconds > 0:
            self.timer_seconds -= 1
            self.update_display()
        else:
            self.timer.stop()
            self.is_running = False
            self.btn_start.setEnabled(True)
            self.btn_start.setText(Localization.get("start"))
            self.btn_start.setStyleSheet("background-color: #10b981;")
            self.btn_pause.setEnabled(False)

            # Session finished
            duration_minutes = self.total_seconds // 60
            if self.is_work_session:
                QMessageBox.information(self, Localization.get("congrats"), Localization.get("work_done_msg"))
                self.session_completed.emit(duration_minutes)
                # Auto set short break
                self.set_duration(5, False)
            else:
                QMessageBox.information(self, Localization.get("break_done_title"), Localization.get("break_done_msg"))
                self.set_duration(25, True)
