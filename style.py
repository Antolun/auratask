# Modern Premium QSS (Qt Style Sheet) for AuraTask with dynamic themes

class Theme:
    def __init__(self, name, primary, primary_hover, primary_pressed, bg, panel_bg, card_bg, border, text_main, text_muted, name_tr):
        self.name = name
        self.primary = primary
        self.primary_hover = primary_hover
        self.primary_pressed = primary_pressed
        self.bg = bg
        self.panel_bg = panel_bg
        self.card_bg = card_bg
        self.border = border
        self.text_main = text_main
        self.text_muted = text_muted
        self.name_tr = name_tr

THEMES = {
    "default": Theme(
        name="default",
        primary="#14b8a6",        # teal
        primary_hover="#2dd4bf",
        primary_pressed="#0d9488",
        bg="#0d0e15",
        panel_bg="#11131e",
        card_bg="#1e293b",
        border="#334155",
        text_main="#e2e8f0",
        text_muted="#94a3b8",
        name_tr="Varsayılan Koyu"
    ),
    "cyberpunk": Theme(
        name="cyberpunk",
        primary="#ec4899",       # neon pink
        primary_hover="#f472b6",
        primary_pressed="#db2777",
        bg="#0b0914",
        panel_bg="#100d20",
        card_bg="#161426",
        border="#3b2b5c",
        text_main="#00ffff",       # cyan text
        text_muted="#a855f7",      # purple/muted text
        name_tr="Cyberpunk Neon"
    ),
    "nord": Theme(
        name="nord",
        primary="#88c0d0",        # frost blue
        primary_hover="#8fbcbb",
        primary_pressed="#5e81ac",
        bg="#2e3440",
        panel_bg="#353b49",
        card_bg="#3b4252",
        border="#4c566a",
        text_main="#eceff4",
        text_muted="#d8dee9",
        name_tr="Kutup Rüzgarı (Nord)"
    ),
    "emerald": Theme(
        name="emerald",
        primary="#10b981",        # emerald green
        primary_hover="#34d399",
        primary_pressed="#059669",
        bg="#061f17",
        panel_bg="#0a2a20",
        card_bg="#0f3d2e",
        border="#1b5c46",
        text_main="#ecfdf5",
        text_muted="#a7f3d0",
        name_tr="Zümrüt Yeşili (Emerald)"
    )
}

current_theme_name = "default"

def set_active_theme(name):
    global current_theme_name
    if name in THEMES:
        current_theme_name = name

def get_active_theme():
    return THEMES.get(current_theme_name, THEMES["default"])

def get_color(color_name):
    theme = get_active_theme()
    return getattr(theme, color_name, "#ffffff")

BASE_STYLE_SHEET = """
/* Global Styles */
QMainWindow {
    background-color: {BG};
}

QWidget {
    font-family: 'Inter', 'Segoe UI', 'Roboto', sans-serif;
    color: {TEXT_MAIN};
    font-size: 13px;
}

/* ScrollBar Styles */
QScrollBar:vertical {
    border: none;
    background: {BG};
    width: 8px;
    margin: 0px;
    border-radius: 4px;
}

QScrollBar::handle:vertical {
    background: {BORDER};
    min-height: 20px;
    border-radius: 4px;
}

QScrollBar::handle:vertical:hover {
    background: {PRIMARY};
}

QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
    height: 0px;
}

/* Buttons */
QPushButton {
    background-color: {PRIMARY};
    border: none;
    color: #ffffff;
    padding: 8px 16px;
    border-radius: 8px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: {PRIMARY_HOVER};
}

QPushButton:pressed {
    background-color: {PRIMARY_PRESSED};
}

QPushButton:disabled {
    background-color: {BORDER};
    color: {TEXT_MUTED};
}

/* Secondary Button style */
QPushButton#secondaryBtn {
    background-color: {CARD_BG};
    border: 1px solid {BORDER};
    color: {TEXT_MAIN};
}

QPushButton#secondaryBtn:hover {
    background-color: {BORDER};
    border-color: {TEXT_MUTED};
}

/* Urgent / Delete Button style */
QPushButton#dangerBtn {
    background-color: #ef4444;
    color: #ffffff;
}

QPushButton#dangerBtn:hover {
    background-color: #f87171;
}

/* Input Fields & Comboboxes */
QLineEdit, QTextEdit, QComboBox {
    background-color: {CARD_BG};
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 8px 12px;
    color: #f8fafc;
}

QLineEdit:focus, QTextEdit:focus, QComboBox:focus {
    border: 1px solid {PRIMARY};
}

QComboBox::drop-down {
    border: none;
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 25px;
}

QComboBox QAbstractItemView {
    background-color: {CARD_BG};
    border: 1px solid {BORDER};
    selection-background-color: {PRIMARY};
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
    color: {TEXT_MUTED};
}

QLabel#timerDisplay {
    font-size: 64px;
    font-weight: 800;
    color: #ffffff;
    font-family: monospace, 'Courier New';
}

/* Kanban Column */
QFrame#kanbanColumn {
    background-color: {PANEL_BG};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 10px;
}

QFrame#kanbanColumnHeader {
    background: transparent;
    border-bottom: 2px solid {BORDER};
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
    background-color: {CARD_BG};
    border: 1px solid {BORDER};
    border-radius: 8px;
    padding: 12px;
    margin-bottom: 8px;
}

QFrame#kanbanCard:hover {
    border: 1px solid {PRIMARY};
    background-color: {PANEL_BG};
}

QLabel#cardTitle {
    font-size: 14px;
    font-weight: 700;
    color: #f8fafc;
}

QLabel#cardDesc {
    font-size: 12px;
    color: {TEXT_MUTED};
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
    background-color: {BG};
    border: 1px solid {BORDER};
    border-radius: 12px;
}

/* Tabs */
QTabWidget::pane {
    border: none;
    background-color: {BG};
}

QTabBar {
    outline: none;
}

QTabBar::tab {
    background-color: {PANEL_BG};
    border: 1px solid {BORDER};
    border-bottom: none;
    border-top-left-radius: 8px;
    border-top-right-radius: 8px;
    padding: 10px 20px;
    margin-right: 4px;
    font-weight: bold;
    color: {TEXT_MUTED};
    outline: none;
}

QTabBar::tab:hover {
    background-color: {CARD_BG};
    color: {TEXT_MAIN};
}

QTabBar::tab:selected {
    background-color: {CARD_BG};
    color: {PRIMARY};
    border-bottom: 3px solid {PRIMARY};
    border-color: {CARD_BG};
}


/* Card control buttons styling */
QPushButton#cardBtn {
    background-color: transparent;
    padding: 4px;
    border-radius: 4px;
    border: none;
}

QPushButton#cardBtn:hover {
    background-color: {BORDER};
}

/* Sidebar Info Panel */
QFrame#sidebarPanel {
    background-color: {PANEL_BG};
    border: 1px solid {BORDER};
    border-radius: 12px;
    padding: 15px;
}

/* Circular progress simulation label/frame */
QFrame#circularProgress {
    border: 4px solid {BORDER};
    border-radius: 75px; /* Half of width/height */
    background-color: {PANEL_BG};
}
"""

def get_stylesheet():
    theme = get_active_theme()
    style = BASE_STYLE_SHEET
    style = style.replace("{BG}", theme.bg)
    style = style.replace("{PANEL_BG}", theme.panel_bg)
    style = style.replace("{CARD_BG}", theme.card_bg)
    style = style.replace("{BORDER}", theme.border)
    style = style.replace("{PRIMARY}", theme.primary)
    style = style.replace("{PRIMARY_HOVER}", theme.primary_hover)
    style = style.replace("{PRIMARY_PRESSED}", theme.primary_pressed)
    style = style.replace("{TEXT_MAIN}", theme.text_main)
    style = style.replace("{TEXT_MUTED}", theme.text_muted)
    return style

# Keep STYLE_SHEET variable for backwards compatibility if needed at import time
STYLE_SHEET = get_stylesheet()
