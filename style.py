# Modern Premium QSS (Qt Style Sheet) for AuraTask

STYLE_SHEET = """
/* Global Styles */
QMainWindow {
    background-color: #0d0e15;
}

QWidget {
    font-family: 'Inter', 'Segoe UI', 'Roboto', sans-serif;
    color: #e2e8f0;
    font-size: 13px;
}

/* ScrollBar Styles */
QScrollBar:vertical {
    border: none;
    background: #0d0e15;
    width: 8px;
    margin: 0px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background: #2d3142;
    min-height: 20px;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background: #4f46e5;
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* Buttons */
QPushButton {
    background-color: #4f46e5;
    border: none;
    color: #ffffff;
    padding: 8px 16px;
    border-radius: 8px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #6366f1;
}

QPushButton:pressed {
    background-color: #4338ca;
}

QPushButton:disabled {
    background-color: #1e1b4b;
    color: #64748b;
}

/* Secondary Button style */
QPushButton#secondaryBtn {
    background-color: #1e293b;
    border: 1px solid #334155;
    color: #e2e8f0;
}

QPushButton#secondaryBtn:hover {
    background-color: #334155;
    border-color: #475569;
}

/* Urgent / Delete Button style */
QPushButton#dangerBtn {
    background-color: #ef4444;
}

QPushButton#dangerBtn:hover {
    background-color: #f87171;
}

/* Input Fields & Comboboxes */
QLineEdit, QTextEdit, QComboBox {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 8px 12px;
    color: #f8fafc;
}

QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
    border: 1px solid #6366f1;
}

QComboBox::drop-down {
    border: none;
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 25px;
}

QComboBox QAbstractItemView {
    background-color: #1e293b;
    border: 1px solid #334155;
    selection-background-color: #4f46e5;
    selection-color: #ffffff;
}

/* Labels */
QLabel {
    font-weight: 500;
}

QLabel#titleLabel {
    font-size: 20px;
    font-weight: 800;
    color: #f8fafc;
}

QLabel#subtitleLabel {
    font-size: 13px;
    color: #94a3b8;
}

QLabel#timerDisplay {
    font-size: 64px;
    font-weight: 800;
    color: #ffffff;
    font-family: monospace, 'Courier New';
}

/* Kanban Column */
QFrame#kanbanColumn {
    background-color: #11131e;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 10px;
}

QFrame#kanbanColumnHeader {
    background: transparent;
    border-bottom: 2px solid #334155;
    padding-bottom: 5px;
    margin-bottom: 10px;
}

QLabel#columnTitle {
    font-size: 15px;
    font-weight: 700;
    color: #f8fafc;
}

/* Kanban Card */
QFrame#kanbanCard {
    background-color: #1e293b;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 12px;
    margin-bottom: 8px;
}

QFrame#kanbanCard:hover {
    border: 1px solid #4f46e5;
    background-color: #243049;
}

QLabel#cardTitle {
    font-size: 14px;
    font-weight: 700;
    color: #f8fafc;
}

QLabel#cardDesc {
    font-size: 12px;
    color: #94a3b8;
}

/* Task Priority Badges */
QLabel#badgeLow {
    background-color: #064e3b;
    color: #34d399;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 10px;
    font-weight: bold;
}

QLabel#badgeMedium {
    background-color: #78350f;
    color: #fbbf24;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 10px;
    font-weight: bold;
}

QLabel#badgeHigh {
    background-color: #7f1d1d;
    color: #f87171;
    padding: 2px 6px;
    border-radius: 4px;
    font-size: 10px;
    font-weight: bold;
}

/* Dialogs */
QDialog {
    background-color: #0d0e15;
    border: 1px solid #334155;
    border-radius: 12px;
}

/* Tabs */
QTabWidget::pane {
    border: none;
    background-color: #0d0e15;
}

QTabBar::tab {
    background-color: #11131e;
    border: 1px solid #1e293b;
    border-bottom: none;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    padding: 10px 20px;
    margin-right: 4px;
    font-weight: bold;
    color: #94a3b8;
}

QTabBar::tab:hover {
    background-color: #1e293b;
    color: #e2e8f0;
}

QTabBar::tab:selected {
    background-color: #4f46e5;
    color: #ffffff;
    border-color: #4f46e5;
}

/* Card control buttons styling */
QPushButton#cardBtn {
    background-color: transparent;
    padding: 4px;
    border-radius: 4px;
    border: none;
}

QPushButton#cardBtn:hover {
    background-color: #334155;
}

/* Sidebar Info Panel */
QFrame#sidebarPanel {
    background-color: #11131e;
    border: 1px solid #1e293b;
    border-radius: 12px;
    padding: 15px;
}

/* Circular progress simulation label/frame */
QFrame#circularProgress {
    border: 4px solid #1e293b;
    border-radius: 75px; /* Half of width/height */
    background-color: #11131e;
}
"""
