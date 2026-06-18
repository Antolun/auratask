#!/usr/bin/env python3
import sys
import os
import datetime
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QHBoxLayout, 
    QVBoxLayout, QTabWidget, QLabel, QFrame, QMessageBox,
    QLineEdit, QComboBox, QDialog
)
from PyQt6.QtGui import QIcon, QColor, QPixmap
from PyQt6.QtCore import Qt

from database import Database
from style import STYLE_SHEET
from widgets import (
    KanbanColumnWidget, PomodoroWidget, 
    TaskDialog, AnalyticsChartWidget
)
from localization import Localization

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        
        self.setWindowTitle(Localization.get("app_title"))
        self.resize(1150, 750)
        self.setMinimumSize(950, 600)
        
        # Set Window Icon
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "logo.png")
        if os.path.exists(logo_path):
            self.setWindowIcon(QIcon(logo_path))
        
        self.init_ui()
        self.refresh_all()

    def init_ui(self):
        # Central Widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Main Horizontal Layout
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(15, 15, 15, 15)
        main_layout.setSpacing(15)

        # ==========================================
        # LEFT REGION: TAB WIDGET (Kanban & Analytics)
        # ==========================================
        self.tab_widget = QTabWidget()
        
        # Tab 1: Kanban Board
        kanban_tab = QWidget()
        kanban_main_layout = QVBoxLayout(kanban_tab)
        kanban_main_layout.setContentsMargins(0, 0, 0, 0)
        kanban_main_layout.setSpacing(5)

        # Priority Filter Bar
        filter_bar = QHBoxLayout()
        filter_bar.setContentsMargins(5, 10, 5, 0)
        
        # Search Input
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText(Localization.get("search_placeholder"))
        self.search_input.setStyleSheet("max-width: 200px; padding: 4px 8px; font-size: 12px;")
        self.search_input.textChanged.connect(self.refresh_columns)
        filter_bar.addWidget(self.search_input)

        filter_bar.addStretch()
        
        filter_lbl = QLabel(Localization.get("filter_priority"))
        filter_lbl.setStyleSheet("color: #94a3b8; font-size: 12px;")
        filter_bar.addWidget(filter_lbl)

        self.filter_combo = QComboBox()
        self.filter_combo.setStyleSheet("max-width: 150px; padding: 4px 8px; font-size: 12px;")
        self.filter_combo.addItem(Localization.get("all_priorities"), "all")
        self.filter_combo.addItem(Localization.get("low"), "low")
        self.filter_combo.addItem(Localization.get("medium"), "medium")
        self.filter_combo.addItem(Localization.get("high"), "high")
        self.filter_combo.currentIndexChanged.connect(self.refresh_columns)
        filter_bar.addWidget(self.filter_combo)
        
        kanban_main_layout.addLayout(filter_bar)

        kanban_cols_layout = QHBoxLayout()
        kanban_cols_layout.setContentsMargins(0, 0, 0, 0)
        kanban_cols_layout.setSpacing(10)

        # 3 Columns - Using internal IDs: todo, doing, done
        self.col_todo = KanbanColumnWidget("todo", Localization.get("todo"))
        self.col_doing = KanbanColumnWidget("doing", Localization.get("doing"))
        self.col_done = KanbanColumnWidget("done", Localization.get("done"))

        # Connect Column Signals
        for col in [self.col_todo, self.col_doing, self.col_done]:
            col.add_task_clicked.connect(self.on_add_task)
            col.card_move_left.connect(self.on_move_left)
            col.card_move_right.connect(self.on_move_right)
            col.card_edit.connect(self.on_edit_task)
            col.card_delete.connect(self.on_delete_task)
            if col.column_id == "done":
                col.clear_clicked.connect(self.on_clear_completed)

        kanban_cols_layout.addWidget(self.col_todo)
        kanban_cols_layout.addWidget(self.col_doing)
        kanban_cols_layout.addWidget(self.col_done)
        
        kanban_main_layout.addLayout(kanban_cols_layout)
        
        self.tab_widget.addTab(kanban_tab, Localization.get("task_board"))

        # Tab 2: Analytics & Stats
        analytics_tab = QWidget()
        analytics_layout = QVBoxLayout(analytics_tab)
        analytics_layout.setContentsMargins(10, 20, 10, 10)
        analytics_layout.setSpacing(15)

        # Big stats cards row
        stats_cards_row = QHBoxLayout()
        stats_cards_row.setSpacing(15)

        # Stat Card 1: Total Focus Minutes
        self.card_total_time = QFrame()
        self.card_total_time.setObjectName("sidebarPanel")
        time_card_layout = QVBoxLayout(self.card_total_time)
        time_card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_stat_time_val = QLabel("0 " + Localization.get("min"))
        self.lbl_stat_time_val.setStyleSheet("font-size: 24px; font-weight: bold; color: #6366f1;")
        lbl_stat_time_title = QLabel(Localization.get("total_focus_time"))
        lbl_stat_time_title.setStyleSheet("font-size: 12px; color: #94a3b8;")
        time_card_layout.addWidget(self.lbl_stat_time_val, 0, Qt.AlignmentFlag.AlignCenter)
        time_card_layout.addWidget(lbl_stat_time_title, 0, Qt.AlignmentFlag.AlignCenter)

        # Stat Card 2: Total Sessions Completed
        self.card_total_pomos = QFrame()
        self.card_total_pomos.setObjectName("sidebarPanel")
        pomo_card_layout = QVBoxLayout(self.card_total_pomos)
        pomo_card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_stat_pomo_val = QLabel("0 " + Localization.get("sessions"))
        self.lbl_stat_pomo_val.setStyleSheet("font-size: 24px; font-weight: bold; color: #10b981;")
        lbl_stat_pomo_title = QLabel(Localization.get("completed_pomodoros"))
        lbl_stat_pomo_title.setStyleSheet("font-size: 12px; color: #94a3b8;")
        pomo_card_layout.addWidget(self.lbl_stat_pomo_val, 0, Qt.AlignmentFlag.AlignCenter)
        pomo_card_layout.addWidget(lbl_stat_pomo_title, 0, Qt.AlignmentFlag.AlignCenter)

        stats_cards_row.addWidget(self.card_total_time)
        stats_cards_row.addWidget(self.card_total_pomos)
        analytics_layout.addLayout(stats_cards_row)

        # Custom Bar Chart
        chart_title = QLabel(Localization.get("last_7_days"))
        chart_title.setStyleSheet("font-size: 14px; font-weight: bold; color: #ffffff; margin-top: 10px;")
        analytics_layout.addWidget(chart_title)

        self.chart_widget = AnalyticsChartWidget()
        analytics_layout.addWidget(self.chart_widget, 1)

        self.tab_widget.addTab(analytics_tab, Localization.get("analytics"))
        
        main_layout.addWidget(self.tab_widget, 3)

        # ==========================================
        # RIGHT REGION: SIDEBAR (Timer & Quick Stats)
        # ==========================================
        sidebar_layout = QVBoxLayout()
        sidebar_layout.setSpacing(15)

        # App branding header
        branding_frame = QFrame()
        branding_frame.setStyleSheet("background: transparent;")
        branding_layout = QHBoxLayout(branding_frame)
        branding_layout.setContentsMargins(0, 0, 0, 0)
        branding_layout.setSpacing(10)
        
        logo_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "logo.png")
        if os.path.exists(logo_path):
            logo_label = QLabel()
            pixmap = QPixmap(logo_path)
            scaled_pixmap = pixmap.scaled(48, 48, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            logo_label.setPixmap(scaled_pixmap)
            branding_layout.addWidget(logo_label)

        # Title and subtitle layout
        title_layout = QVBoxLayout()
        title_layout.setSpacing(2)
        title_layout.setContentsMargins(0, 0, 0, 0)
        
        app_title = QLabel("AuraTask")
        app_title.setObjectName("titleLabel")
        app_subtitle = QLabel(Localization.get("app_subtitle"))
        app_subtitle.setObjectName("subtitleLabel")
        
        title_layout.addWidget(app_title)
        title_layout.addWidget(app_subtitle)
        
        branding_layout.addLayout(title_layout)
        branding_layout.addStretch()
        
        sidebar_layout.addWidget(branding_frame)

        # Pomodoro Timer
        self.pomodoro_widget = PomodoroWidget()
        self.pomodoro_widget.session_completed.connect(self.on_pomodoro_completed)
        sidebar_layout.addWidget(self.pomodoro_widget)

        # Quick summary panel
        summary_panel = QFrame()
        summary_panel.setObjectName("sidebarPanel")
        sum_layout = QVBoxLayout(summary_panel)
        sum_layout.setSpacing(8)
        
        sum_title = QLabel(Localization.get("summary_stats"))
        sum_title.setStyleSheet("font-size: 13px; font-weight: bold; color: #f8fafc;")
        sum_layout.addWidget(sum_title)

        self.lbl_today_time = QLabel(Localization.get("today_focus", 0))
        self.lbl_today_time.setStyleSheet("color: #94a3b8; font-size: 12px;")
        sum_layout.addWidget(self.lbl_today_time)

        self.lbl_total_tasks = QLabel(Localization.get("total_tasks", 0))
        self.lbl_total_tasks.setStyleSheet("color: #94a3b8; font-size: 12px;")
        sum_layout.addWidget(self.lbl_total_tasks)

        sidebar_layout.addWidget(summary_panel)
        sidebar_layout.addStretch()

        main_layout.addLayout(sidebar_layout, 1)

    # ==========================================
    # LOGIC AND EVENT HANDLERS
    # ==========================================
    def refresh_all(self):
        self.refresh_columns()
        self.refresh_stats()

    def refresh_columns(self):
        # Clear all columns
        self.col_todo.clear_cards()
        self.col_doing.clear_cards()
        self.col_done.clear_cards()

        # Reload tasks
        tasks = self.db.get_tasks()
        
        # Get filter values
        filter_priority = self.filter_combo.currentData()
        search_text = self.search_input.text().lower().strip()
        
        for task in tasks:
            # Apply priority filter
            if filter_priority != "all" and task.get("priority", "medium").lower() != filter_priority:
                continue
            
            # Apply search filter
            if search_text:
                title = task.get("title", "").lower()
                desc = task.get("description", "").lower()
                tags = " ".join(task.get("tags", [])).lower()
                if search_text not in title and search_text not in desc and search_text not in tags:
                    continue

            status = task.get("status", "todo")
            if status == "todo":
                self.col_todo.add_card(task)
            elif status == "doing":
                self.col_doing.add_card(task)
            elif status == "done":
                self.col_done.add_card(task)

        # Update total tasks count in sidebar summary
        self.lbl_total_tasks.setText(Localization.get("total_tasks", len(tasks)))

    def on_clear_completed(self):
        reply = QMessageBox.question(
            self, Localization.get("clear_completed"), 
            Localization.get("delete_confirm"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            tasks = self.db.get_tasks()
            to_delete = [t["id"] for t in tasks if t.get("status") == "done"]
            for task_id in to_delete:
                self.db.delete_task(task_id)
            self.refresh_columns()

    def refresh_stats(self):
        stats = self.db.get_stats()
        
        # Update Big Stats Cards in Tab 2
        total_mins = stats.get("total_focus_minutes", 0)
        self.lbl_stat_time_val.setText(f"{total_mins} " + Localization.get("min"))
        
        total_pomos = stats.get("completed_pomodoros", 0)
        self.lbl_stat_pomo_val.setText(f"{total_pomos} " + Localization.get("sessions"))

        # Update Chart Widget
        sessions = stats.get("focus_sessions", [])
        self.chart_widget.set_stats(sessions)

        # Update Today's info in sidebar
        today_str = datetime.datetime.now().strftime("%Y-%m-%d")
        today_mins = 0
        for session in sessions:
            if session["date"] == today_str:
                today_mins = session["minutes"]
                break
        self.lbl_today_time.setText(Localization.get("today_focus", today_mins))

    def on_add_task(self, column_id):
        # Open dialog
        dlg = TaskDialog(self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            data = dlg.get_data()
            task = self.db.add_task(
                title=data["title"],
                description=data["description"],
                priority=data["priority"],
                tags=data["tags"]
            )
            # Match the starting column status (column_id is now todo, doing, or done)
            if column_id != "todo":
                self.db.update_task_status(task["id"], column_id)
                
            self.refresh_columns()

    def on_edit_task(self, task_id):
        # Find task
        tasks = self.db.get_tasks()
        target_task = None
        for task in tasks:
            if task["id"] == task_id:
                target_task = task
                break
        
        if not target_task:
            return

        # Open dialog
        dlg = TaskDialog(self, target_task)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            data = dlg.get_data()
            self.db.edit_task(
                task_id=task_id,
                title=data["title"],
                description=data["description"],
                priority=data["priority"],
                tags=data["tags"]
            )
            self.refresh_columns()

    def on_delete_task(self, task_id):
        reply = QMessageBox.question(
            self, Localization.get("delete_title"), 
            Localization.get("delete_confirm"),
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            QMessageBox.StandardButton.No
        )
        if reply == QMessageBox.StandardButton.Yes:
            if self.db.delete_task(task_id):
                self.refresh_columns()

    def on_move_left(self, task_id):
        # Move state backward
        tasks = self.db.get_tasks()
        for task in tasks:
            if task["id"] == task_id:
                curr_status = task.get("status", "todo")
                if curr_status == "doing":
                    self.db.update_task_status(task_id, "todo")
                elif curr_status == "done":
                    self.db.update_task_status(task_id, "doing")
                break
        self.refresh_columns()

    def on_move_right(self, task_id):
        # Move state forward
        tasks = self.db.get_tasks()
        for task in tasks:
            if task["id"] == task_id:
                curr_status = task.get("status", "todo")
                if curr_status == "todo":
                    self.db.update_task_status(task_id, "doing")
                elif curr_status == "doing":
                    self.db.update_task_status(task_id, "done")
                break
        self.refresh_columns()

    def on_pomodoro_completed(self, minutes):
        self.db.add_focus_time(minutes)
        self.refresh_stats()

    def on_pomodoro_completed(self, minutes):
        self.db.add_focus_time(minutes)
        self.refresh_stats()


def main():
    app = QApplication(sys.argv)
    app.setStyleSheet(STYLE_SHEET)
    
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
