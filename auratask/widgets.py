import sys
import math
from datetime import datetime, timedelta
from PyQt6.QtCore import Qt, QTimer, pyqtSignal, QRectF, QPointF
from PyQt6.QtWidgets import (
    QWidget, QFrame, QVBoxLayout, QHBoxLayout, QGridLayout, QLabel,
    QPushButton, QScrollArea, QDialog, QLineEdit,
    QTextEdit, QMessageBox, QGraphicsDropShadowEffect, QComboBox,
    QCheckBox, QDateEdit, QProgressBar, QListWidget, QListWidgetItem,
    QToolTip, QInputDialog
)
from PyQt6.QtGui import QPainter, QColor, QPen, QBrush, QFont, QLinearGradient, QIcon, QPixmap, QPainterPath
from auratask.localization import Localization
import auratask.style as _style_mod

import os
import json as _json_mod

# Deterministic tag color palette - each tag always gets the same color via hash (fallback)
TAG_COLORS = [
    ("#14b8a6", "#042f2e"),  # teal
    ("#8b5cf6", "#2e1065"),  # violet
    ("#f59e0b", "#451a03"),  # amber
    ("#ef4444", "#450a0a"),  # red
    ("#10b981", "#052e16"),  # emerald
    ("#3b82f6", "#172554"),  # blue
    ("#ec4899", "#4a044e"),  # pink
    ("#f97316", "#431407"),  # orange
    ("#06b6d4", "#083344"),  # cyan
    ("#84cc16", "#1a2e05"),  # lime
]

# Selectable preset colors for the tag color picker (text_color, bg_color, label)
TAG_COLOR_PRESETS = [
    ("#14b8a6", "#042f2e", "tag_colors_preset_turkuaz"),
    ("#8b5cf6", "#2e1065", "tag_colors_preset_mor"),
    ("#f59e0b", "#451a03", "tag_colors_preset_amber"),
    ("#ef4444", "#450a0a", "tag_colors_preset_kirmizi"),
    ("#10b981", "#052e16", "tag_colors_preset_yesil"),
    ("#3b82f6", "#172554", "tag_colors_preset_mavi"),
    ("#ec4899", "#4a044e", "tag_colors_preset_pembe"),
    ("#f97316", "#431407", "tag_colors_preset_turuncu"),
    ("#06b6d4", "#083344", "tag_colors_preset_cyan"),
    ("#84cc16", "#1a2e05", "tag_colors_preset_lime"),
    ("#a855f7", "#3b0764", "tag_colors_preset_lavanta"),
    ("#64748b", "#0f172a", "tag_colors_preset_gri"),
]

_TAG_COLORS_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "tag_colors.json")

class TagColorManager:
    """Singleton manager for persistent custom tag colors."""
    _instance = None
    _custom_colors: dict = {}  # tag_name -> (text_color, bg_color)

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._load()
        return cls._instance

    def _load(self):
        try:
            if os.path.exists(_TAG_COLORS_FILE):
                with open(_TAG_COLORS_FILE, "r", encoding="utf-8") as f:
                    raw = _json_mod.load(f)
                    self._custom_colors = {k: tuple(v) for k, v in raw.items()}
        except Exception:
            self._custom_colors = {}

    def save(self):
        try:
            os.makedirs(os.path.dirname(_TAG_COLORS_FILE), exist_ok=True)
            with open(_TAG_COLORS_FILE, "w", encoding="utf-8") as f:
                _json_mod.dump({k: list(v) for k, v in self._custom_colors.items()}, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[TagColorManager] save error: {e}")

    def get(self, tag_name: str):
        """Returns (text_color, bg_color). Custom first, then hash-based fallback."""
        key = tag_name.lower().strip()
        if key in self._custom_colors:
            return self._custom_colors[key]
        idx = hash(key) % len(TAG_COLORS)
        return TAG_COLORS[idx]

    def set(self, tag_name: str, text_color: str, bg_color: str):
        self._custom_colors[tag_name.lower().strip()] = (text_color, bg_color)
        self.save()

    def all_custom(self) -> dict:
        return dict(self._custom_colors)

# Global singleton
_tag_color_mgr = TagColorManager()

def get_tag_color(tag_name: str):
    """Returns (text_color, bg_color) for a tag name. Custom colors take priority."""
    return _tag_color_mgr.get(tag_name)

def set_tag_color(tag_name: str, text_color: str, bg_color: str):
    """Set a custom color for a tag and persist it."""
    _tag_color_mgr.set(tag_name, text_color, bg_color)


def create_vector_icon(icon_type, color_hex="#14b8a6", size=32):
    pixmap = QPixmap(size, size)
    pixmap.fill(Qt.GlobalColor.transparent)
    
    painter = QPainter(pixmap)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing)
    
    color = QColor(color_hex)
    pen = QPen(color)
    pen.setCapStyle(Qt.PenCapStyle.RoundCap)
    pen.setJoinStyle(Qt.PenJoinStyle.RoundJoin)
    
    brush = QBrush(color)
    
    if icon_type == "arrow_left":
        pen.setWidth(max(1, int(size * 0.08)))
        painter.setPen(pen)
        painter.drawLine(int(size * 0.8), int(size * 0.5), int(size * 0.2), int(size * 0.5))
        painter.drawLine(int(size * 0.45), int(size * 0.25), int(size * 0.2), int(size * 0.5))
        painter.drawLine(int(size * 0.45), int(size * 0.75), int(size * 0.2), int(size * 0.5))
        
    elif icon_type == "arrow_right":
        pen.setWidth(max(1, int(size * 0.08)))
        painter.setPen(pen)
        painter.drawLine(int(size * 0.2), int(size * 0.5), int(size * 0.8), int(size * 0.5))
        painter.drawLine(int(size * 0.55), int(size * 0.25), int(size * 0.8), int(size * 0.5))
        painter.drawLine(int(size * 0.55), int(size * 0.75), int(size * 0.8), int(size * 0.5))
        
    elif icon_type == "edit":
        pen.setWidth(max(1, int(size * 0.08)))
        painter.setPen(pen)
        painter.drawLine(int(size * 0.35), int(size * 0.65), int(size * 0.65), int(size * 0.35))
        painter.drawLine(int(size * 0.42), int(size * 0.72), int(size * 0.72), int(size * 0.42))
        painter.drawLine(int(size * 0.65), int(size * 0.35), int(size * 0.72), int(size * 0.42))
        painter.drawLine(int(size * 0.70), int(size * 0.30), int(size * 0.80), int(size * 0.40))
        painter.drawLine(int(size * 0.35), int(size * 0.65), int(size * 0.20), int(size * 0.80))
        painter.drawLine(int(size * 0.42), int(size * 0.72), int(size * 0.20), int(size * 0.80))
        
    elif icon_type == "delete":
        pen.setWidth(max(1, int(size * 0.08)))
        painter.setPen(pen)
        painter.drawLine(int(size * 0.2), int(size * 0.25), int(size * 0.8), int(size * 0.25))
        painter.drawRect(int(size * 0.4), int(size * 0.15), int(size * 0.2), int(size * 0.1))
        painter.drawRect(int(size * 0.28), int(size * 0.25), int(size * 0.44), int(size * 0.6))
        painter.drawLine(int(size * 0.42), int(size * 0.35), int(size * 0.42), int(size * 0.75))
        painter.drawLine(int(size * 0.58), int(size * 0.35), int(size * 0.58), int(size * 0.75))
        
    elif icon_type == "clean":
        pen.setWidth(max(1, int(size * 0.08)))
        painter.setPen(pen)
        painter.drawLine(int(size * 0.75), int(size * 0.25), int(size * 0.45), int(size * 0.55))
        path = QPainterPath()
        path.moveTo(int(size * 0.45), int(size * 0.55))
        path.lineTo(int(size * 0.25), int(size * 0.65))
        path.lineTo(int(size * 0.35), int(size * 0.75))
        path.closeSubpath()
        painter.setBrush(brush)
        painter.drawPath(path)
        
    elif icon_type == "calendar":
        pen.setWidth(max(1, int(size * 0.06)))
        painter.setPen(pen)
        painter.drawRect(int(size * 0.2), int(size * 0.25), int(size * 0.6), int(size * 0.55))
        painter.drawLine(int(size * 0.2), int(size * 0.4), int(size * 0.8), int(size * 0.4))
        painter.drawLine(int(size * 0.35), int(size * 0.15), int(size * 0.35), int(size * 0.3))
        painter.drawLine(int(size * 0.65), int(size * 0.15), int(size * 0.65), int(size * 0.3))
        painter.setBrush(brush)
        painter.drawEllipse(int(size * 0.32), int(size * 0.5), max(2, int(size * 0.06)), max(2, int(size * 0.06)))
        painter.drawEllipse(int(size * 0.47), int(size * 0.5), max(2, int(size * 0.06)), max(2, int(size * 0.06)))
        painter.drawEllipse(int(size * 0.62), int(size * 0.5), max(2, int(size * 0.06)), max(2, int(size * 0.06)))
        painter.drawEllipse(int(size * 0.32), int(size * 0.65), max(2, int(size * 0.06)), max(2, int(size * 0.06)))
        painter.drawEllipse(int(size * 0.47), int(size * 0.65), max(2, int(size * 0.06)), max(2, int(size * 0.06)))
        painter.drawEllipse(int(size * 0.62), int(size * 0.65), max(2, int(size * 0.06)), max(2, int(size * 0.06)))

    elif icon_type == "settings":
        pen.setWidth(max(1, int(size * 0.08)))
        painter.setPen(pen)
        # Gear circle
        painter.drawEllipse(int(size * 0.3), int(size * 0.3), int(size * 0.4), int(size * 0.4))
        painter.drawEllipse(int(size * 0.44), int(size * 0.44), int(size * 0.12), int(size * 0.12))
        # Teeth
        cx, cy = size / 2.0, size / 2.0
        for i in range(8):
            angle = i * 45
            rad = math.radians(angle)
            x1 = cx + (size * 0.2) * math.cos(rad)
            y1 = cy + (size * 0.2) * math.sin(rad)
            x2 = cx + (size * 0.35) * math.cos(rad)
            y2 = cy + (size * 0.35) * math.sin(rad)
            painter.drawLine(int(x1), int(y1), int(x2), int(y2))

        
    elif icon_type == "timer":
        pen.setWidth(max(1, int(size * 0.08)))
        painter.setPen(pen)
        painter.drawEllipse(int(size * 0.2), int(size * 0.22), int(size * 0.6), int(size * 0.6))
        painter.drawRect(int(size * 0.44), int(size * 0.12), int(size * 0.12), int(size * 0.1))
        painter.drawLine(int(size * 0.25), int(size * 0.18), int(size * 0.35), int(size * 0.25))
        painter.drawLine(int(size * 0.75), int(size * 0.18), int(size * 0.65), int(size * 0.25))
        painter.drawLine(int(size * 0.5), int(size * 0.52), int(size * 0.5), int(size * 0.35))
        painter.drawLine(int(size * 0.5), int(size * 0.52), int(size * 0.65), int(size * 0.52))

    elif icon_type == "search":
        pen.setWidth(max(1, int(size * 0.08)))
        painter.setPen(pen)
        painter.drawEllipse(int(size * 0.2), int(size * 0.2), int(size * 0.45), int(size * 0.45))
        painter.drawLine(int(size * 0.55), int(size * 0.55), int(size * 0.8), int(size * 0.8))

    elif icon_type == "plus":
        pen.setWidth(max(1, int(size * 0.1)))
        painter.setPen(pen)
        painter.drawLine(int(size * 0.25), int(size * 0.5), int(size * 0.75), int(size * 0.5))
        painter.drawLine(int(size * 0.5), int(size * 0.25), int(size * 0.5), int(size * 0.75))

    elif icon_type == "pin":
        pen.setWidth(max(1, int(size * 0.08)))
        painter.setPen(pen)
        painter.drawLine(int(size * 0.35), int(size * 0.25), int(size * 0.65), int(size * 0.25))
        painter.drawRect(int(size * 0.4), int(size * 0.25), int(size * 0.2), int(size * 0.3))
        painter.drawLine(int(size * 0.3), int(size * 0.55), int(size * 0.7), int(size * 0.55))
        painter.drawLine(int(size * 0.5), int(size * 0.55), int(size * 0.5), int(size * 0.85))

    elif icon_type == "board":
        pen.setWidth(max(1, int(size * 0.08)))
        painter.setPen(pen)
        painter.drawRect(int(size * 0.22), int(size * 0.25), int(size * 0.56), int(size * 0.6))
        painter.drawRect(int(size * 0.38), int(size * 0.15), int(size * 0.24), int(size * 0.1))
        painter.drawLine(int(size * 0.32), int(size * 0.42), int(size * 0.68), int(size * 0.42))
        painter.drawLine(int(size * 0.32), int(size * 0.58), int(size * 0.68), int(size * 0.58))
        painter.drawLine(int(size * 0.32), int(size * 0.74), int(size * 0.68), int(size * 0.74))

    elif icon_type == "chart":
        pen.setWidth(max(1, int(size * 0.08)))
        painter.setPen(pen)
        painter.drawLine(int(size * 0.2), int(size * 0.2), int(size * 0.2), int(size * 0.8))
        painter.drawLine(int(size * 0.2), int(size * 0.8), int(size * 0.8), int(size * 0.8))
        painter.setBrush(brush)
        painter.drawRect(int(size * 0.3), int(size * 0.55), int(size * 0.12), int(size * 0.25))
        painter.drawRect(int(size * 0.48), int(size * 0.35), int(size * 0.12), int(size * 0.45))
        painter.drawRect(int(size * 0.66), int(size * 0.45), int(size * 0.12), int(size * 0.35))

    elif icon_type == "archive":
        pen.setWidth(max(1, int(size * 0.08)))
        painter.setPen(pen)
        painter.drawRect(int(size * 0.2), int(size * 0.32), int(size * 0.6), int(size * 0.48))
        painter.drawRect(int(size * 0.16), int(size * 0.2), int(size * 0.68), int(size * 0.12))
        painter.drawRect(int(size * 0.4), int(size * 0.42), int(size * 0.2), int(size * 0.08))

    elif icon_type == "sub_add":
        # Checklist lines on left, plus sign on right
        pen.setWidth(max(1, int(size * 0.07)))
        painter.setPen(pen)
        # Three short lines representing a list
        painter.drawLine(int(size * 0.18), int(size * 0.32), int(size * 0.55), int(size * 0.32))
        painter.drawLine(int(size * 0.18), int(size * 0.50), int(size * 0.55), int(size * 0.50))
        painter.drawLine(int(size * 0.18), int(size * 0.68), int(size * 0.40), int(size * 0.68))
        # Small tick marks on the left
        painter.drawLine(int(size * 0.10), int(size * 0.30), int(size * 0.14), int(size * 0.34))
        painter.drawLine(int(size * 0.14), int(size * 0.34), int(size * 0.18), int(size * 0.28))
        painter.drawLine(int(size * 0.10), int(size * 0.48), int(size * 0.14), int(size * 0.52))
        painter.drawLine(int(size * 0.14), int(size * 0.52), int(size * 0.18), int(size * 0.46))
        # Plus sign in bottom-right area
        plus_pen = QPen(QColor("#2dd4bf"))
        plus_pen.setWidth(max(1, int(size * 0.10)))
        plus_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(plus_pen)
        painter.drawLine(int(size * 0.62), int(size * 0.55), int(size * 0.88), int(size * 0.55))
        painter.drawLine(int(size * 0.75), int(size * 0.42), int(size * 0.75), int(size * 0.68))

    elif icon_type == "export":
        # Arrow going out of a box (upload/export)
        pen.setWidth(max(1, int(size * 0.08)))
        painter.setPen(pen)
        # Box bottom
        painter.drawLine(int(size * 0.2), int(size * 0.6), int(size * 0.2), int(size * 0.82))
        painter.drawLine(int(size * 0.2), int(size * 0.82), int(size * 0.8), int(size * 0.82))
        painter.drawLine(int(size * 0.8), int(size * 0.82), int(size * 0.8), int(size * 0.6))
        # Arrow upward
        painter.drawLine(int(size * 0.5), int(size * 0.62), int(size * 0.5), int(size * 0.20))
        painter.drawLine(int(size * 0.5), int(size * 0.20), int(size * 0.33), int(size * 0.38))
        painter.drawLine(int(size * 0.5), int(size * 0.20), int(size * 0.67), int(size * 0.38))

    elif icon_type == "import":
        # Arrow going into a box (download/import)
        pen.setWidth(max(1, int(size * 0.08)))
        painter.setPen(pen)
        # Box bottom
        painter.drawLine(int(size * 0.2), int(size * 0.6), int(size * 0.2), int(size * 0.82))
        painter.drawLine(int(size * 0.2), int(size * 0.82), int(size * 0.8), int(size * 0.82))
        painter.drawLine(int(size * 0.8), int(size * 0.82), int(size * 0.8), int(size * 0.6))
        # Arrow downward
        painter.drawLine(int(size * 0.5), int(size * 0.18), int(size * 0.5), int(size * 0.60))
        painter.drawLine(int(size * 0.5), int(size * 0.60), int(size * 0.33), int(size * 0.42))
        painter.drawLine(int(size * 0.5), int(size * 0.60), int(size * 0.67), int(size * 0.42))

    elif icon_type == "tag":
        # Tag/label icon
        pen.setWidth(max(1, int(size * 0.07)))
        painter.setPen(pen)
        path = QPainterPath()
        path.moveTo(int(size * 0.22), int(size * 0.22))
        path.lineTo(int(size * 0.55), int(size * 0.22))
        path.lineTo(int(size * 0.80), int(size * 0.50))
        path.lineTo(int(size * 0.55), int(size * 0.78))
        path.lineTo(int(size * 0.22), int(size * 0.78))
        path.closeSubpath()
        painter.drawPath(path)
        painter.setBrush(brush)
        painter.drawEllipse(int(size * 0.30), int(size * 0.44), max(2, int(size * 0.12)), max(2, int(size * 0.12)))

    painter.end()
    return QIcon(pixmap)

def create_icon_label(icon_type, text, color_hex="#14b8a6", text_color="#cbd5e1"):
    widget = QWidget()
    layout = QHBoxLayout(widget)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(4)
    
    icon_lbl = QLabel()
    icon_lbl.setPixmap(create_vector_icon(icon_type, color_hex, 16).pixmap(16, 16))
    layout.addWidget(icon_lbl)
    
    text_lbl = QLabel(text)
    text_lbl.setStyleSheet(f"color: {text_color}; font-size: 11px; font-weight: bold;")
    layout.addWidget(text_lbl)
    
    return widget


class CircularGoalWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(95, 95)
        self.progress = 0.0 # 0.0 to 1.0
        self.text = "0/100m"

    def set_progress(self, current, goal):
        self.progress = min(1.0, max(0.0, current / goal)) if goal > 0 else 0.0
        self.text = f"{int(current)}/{int(goal)} {Localization.get('min')}"
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        theme = _style_mod.get_active_theme()
        width = self.width()
        height = self.height()
        size = min(width, height) - 10
        x = (width - size) / 2
        y = (height - size) / 2

        rect = QRectF(x, y, size, size)
        
        # Background track
        track_pen = QPen(QColor(theme.card_bg))
        track_pen.setWidth(6)
        painter.setPen(track_pen)
        painter.drawEllipse(rect)

        # Active Progress Arc
        progress_pen = QPen(QColor(theme.primary))
        progress_pen.setWidth(6)
        progress_pen.setCapStyle(Qt.PenCapStyle.RoundCap)
        painter.setPen(progress_pen)

        start_angle = 90 * 16
        span_angle = int(-self.progress * 360 * 16)
        painter.drawArc(rect, start_angle, span_angle)

        # Draw text inside
        font = QFont("Inter", 9, QFont.Weight.Bold)
        painter.setFont(font)
        painter.setPen(QPen(QColor("#ffffff")))
        
        # Draw percent
        pct_text = f"{int(self.progress * 100)}%"
        painter.drawText(QRectF(x, y + (size/2) - 14, size, 14), Qt.AlignmentFlag.AlignCenter, pct_text)
        
        # Draw stats text below percent
        font_sub = QFont("Inter", 7, QFont.Weight.Medium)
        painter.setFont(font_sub)
        painter.setPen(QPen(QColor(theme.text_muted)))
        painter.drawText(QRectF(x, y + (size/2) + 2, size, 12), Qt.AlignmentFlag.AlignCenter, self.text)


class CircularTimerWidget(QWidget):
    double_clicked = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(160, 160)
        self.progress = 1.0 # 0.0 to 1.0
        self.time_str = "25:00"
        self.is_work_session = True
        self.setToolTip(Localization.get("timer_double_click_tooltip"))

    def mouseDoubleClickEvent(self, event):
        self.double_clicked.emit()

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
        
        theme = _style_mod.get_active_theme()

        # Draw background track circle
        track_pen = QPen(QColor(theme.card_bg))
        track_pen.setWidth(12)
        painter.setPen(track_pen)
        painter.drawEllipse(rect)

        # Draw active progress arc - use primary for work, a lighter variant for break
        progress_pen_color = QColor(theme.primary) if self.is_work_session else QColor(theme.primary_hover)
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
        font = QFont("Inter", 26, QFont.Weight.Bold)
        painter.setFont(font)
        
        # Calculate text rect
        text_rect = QRectF(x, y + (size/2) - 26, size, 40)
        painter.drawText(text_rect, Qt.AlignmentFlag.AlignCenter, self.time_str)

        # Draw Mode Text below time
        mode_font = QFont("Inter", 9, QFont.Weight.Medium)
        painter.setFont(mode_font)
        painter.setPen(QPen(QColor(theme.text_muted)))
        
        mode_rect = QRectF(x, y + (size/2) + 14, size, 20)
        mode_str = Localization.get("work") if self.is_work_session else Localization.get("break")
        painter.drawText(mode_rect, Qt.AlignmentFlag.AlignCenter, mode_str)



class KanbanCardWidget(QFrame):
    # Signals for Card operations
    move_left = pyqtSignal(str) # task_id
    move_right = pyqtSignal(str) # task_id
    edit_task = pyqtSignal(str) # task_id
    delete_task = pyqtSignal(str) # task_id
    subtask_toggled = pyqtSignal(str, int, bool) # task_id, subtask_index, is_done

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
                text_color, bg_color = get_tag_color(tag)
                tag_label = QLabel(f" #{tag} ")
                tag_label.setStyleSheet(
                    f"color: {text_color}; background: {bg_color}; "
                    f"font-size: 10px; font-weight: bold; "
                    f"border: 1px solid {text_color}; border-radius: 4px; padding: 1px 2px;"
                )
                tags_layout.addWidget(tag_label)
            tags_layout.addStretch()
            layout.addLayout(tags_layout)

        # Info Row (Due Date & Focus Time)
        info_layout = QHBoxLayout()
        info_layout.setSpacing(10)
        
        # Focus Time
        focus_mins = task.get("focus_time", 0)
        if focus_mins > 0:
            focus_lbl = create_icon_label("timer", f"{focus_mins} {Localization.get('min')}", "#14b8a6")
            info_layout.addWidget(focus_lbl)
            
        # Due Date
        due_date_str = task.get("due_date", "")
        if due_date_str:
            try:
                date_obj = datetime.strptime(due_date_str, "%Y-%m-%d")
                formatted_date = date_obj.strftime("%d %b")
                
                # Check if overdue
                is_overdue = False
                if task.get("status", "todo") != "done":
                    if date_obj.date() < datetime.now().date():
                        is_overdue = True
                        
                if is_overdue:
                    due_lbl = create_icon_label("calendar", f"{formatted_date} ({Localization.get('overdue')})", "#ef4444", "#ef4444")
                else:
                    due_lbl = create_icon_label("calendar", formatted_date, "#94a3b8", "#94a3b8")
                    
                info_layout.addWidget(due_lbl)
            except Exception as e:
                print(f"Error parsing due date: {e}")
                
        info_layout.addStretch()
        
        if focus_mins > 0 or due_date_str:
            layout.addLayout(info_layout)

        # Subtasks Progress & Checklist
        subtasks = task.get("subtasks", [])
        if subtasks:
            done_count = sum(1 for s in subtasks if s["done"])
            total_count = len(subtasks)
            progress_percent = int((done_count / total_count) * 100) if total_count > 0 else 0
            
            # Progress text and bar
            prog_layout = QHBoxLayout()
            theme = _style_mod.get_active_theme()
            prog_lbl = create_icon_label("board", f"{done_count}/{total_count}", theme.primary)
            prog_layout.addWidget(prog_lbl)
            
            pbar = QProgressBar()
            pbar.setMaximum(100)
            pbar.setValue(progress_percent)
            pbar.setTextVisible(False)
            pbar.setFixedHeight(6)
            pbar.setStyleSheet(f"""
                QProgressBar {{
                    background-color: {theme.card_bg};
                    border: 1px solid {theme.border};
                    border-radius: 3px;
                }}
                QProgressBar::chunk {{
                    background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                        stop:0 {theme.primary}, stop:1 {theme.primary_hover});
                    border-radius: 3px;
                }}
            """)
            prog_layout.addWidget(pbar, 1)
            layout.addLayout(prog_layout)
            
            # Subtasks checklist
            subtasks_layout = QVBoxLayout()
            subtasks_layout.setSpacing(2)
            subtasks_layout.setContentsMargins(4, 2, 4, 2)
            for idx, sub in enumerate(subtasks):
                chk = QCheckBox(sub["title"])
                chk.setChecked(sub["done"])
                chk.setStyleSheet("font-size: 11px; color: #cbd5e1;")
                chk.setToolTip(Localization.get("subtask_edit_card_tooltip"))
                # Connect checkbox state change
                chk.stateChanged.connect(lambda state, i=idx: self.subtask_toggled.emit(self.task_id, i, state == 2 or state == Qt.CheckState.Checked.value))
                subtasks_layout.addWidget(chk)
            layout.addLayout(subtasks_layout)

        # Bottom Bar: Buttons
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(0, 4, 0, 0)
        bottom_layout.setSpacing(4)

        # Left Move button
        self.btn_left = QPushButton()
        self.btn_left.setIcon(create_vector_icon("arrow_left"))
        self.btn_left.setObjectName("cardBtn")
        self.btn_left.setToolTip(Localization.get("move_back"))
        self.btn_left.setFixedWidth(28)
        self.btn_left.setFixedHeight(28)
        self.btn_left.clicked.connect(lambda: self.move_left.emit(self.task_id))
        
        # Right Move button
        self.btn_right = QPushButton()
        self.btn_right.setIcon(create_vector_icon("arrow_right"))
        self.btn_right.setObjectName("cardBtn")
        self.btn_right.setToolTip(Localization.get("move_forward"))
        self.btn_right.setFixedWidth(28)
        self.btn_right.setFixedHeight(28)
        self.btn_right.clicked.connect(lambda: self.move_right.emit(self.task_id))

        # Edit button
        self.btn_edit = QPushButton()
        self.btn_edit.setIcon(create_vector_icon("edit"))
        self.btn_edit.setObjectName("cardBtn")
        self.btn_edit.setToolTip(Localization.get("edit"))
        self.btn_edit.setFixedWidth(28)
        self.btn_edit.setFixedHeight(28)
        self.btn_edit.clicked.connect(lambda: self.edit_task.emit(self.task_id))

        # Delete button
        self.btn_delete = QPushButton()
        self.btn_delete.setIcon(create_vector_icon("delete", "#ef4444"))
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
    card_subtask_toggled = pyqtSignal(str, int, bool)

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
            clear_btn = QPushButton()
            clear_btn.setIcon(create_vector_icon("clean", "#94a3b8"))
            clear_btn.setToolTip(Localization.get("clear_completed"))
            clear_btn.setStyleSheet("padding: 4px; background: transparent; border: none;")
            clear_btn.setFixedWidth(28)
            clear_btn.setFixedHeight(28)
            clear_btn.clicked.connect(self.clear_clicked.emit)
            header_layout.addWidget(clear_btn)

        # Add Task Button inside header
        add_btn = QPushButton()
        add_btn.setIcon(create_vector_icon("plus", "#ffffff"))
        add_btn.setStyleSheet("padding: 4px; max-width: 32px;")
        add_btn.setToolTip(Localization.get("add_task"))
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
        card.subtask_toggled.connect(self.card_subtask_toggled)
        
        # Insert before the stretch
        self.list_layout.insertWidget(self.list_layout.count() - 1, card)



class TagColorPickerDialog(QDialog):
    """Dialog to pick colors for each tag from preset swatches."""

    def __init__(self, tags: list, parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.tags = tags
        self.setWindowTitle(Localization.get("tag_colors_title"))
        self.setMinimumWidth(460)
        self.setStyleSheet("""
            QDialog { background-color: #0f172a; }
            QLabel { color: #e2e8f0; }
        """)
        self._init_ui()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(14)

        title_lbl = QLabel(Localization.get("tag_colors_title"))
        title_lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #ffffff;")
        layout.addWidget(title_lbl)

        hint = QLabel(Localization.get("tag_colors_hint"))
        hint.setStyleSheet("font-size: 11px; color: #64748b;")
        hint.setWordWrap(True)
        layout.addWidget(hint)

        # Per-tag rows
        self._preview_labels = {}  # normalized_tag -> QLabel pill
        for tag in self.tags:
            norm_tag = tag.lower().strip()  # normalized key used everywhere
            row_frame = QFrame()
            row_frame.setStyleSheet(
                "background: #1e293b; border: 1px solid #334155; border-radius: 8px;"
            )
            row_layout = QVBoxLayout(row_frame)
            row_layout.setContentsMargins(10, 8, 10, 8)
            row_layout.setSpacing(6)

            # Tag name + current pill preview
            top_row = QHBoxLayout()
            tag_name_lbl = QLabel(f"#{tag}")
            tag_name_lbl.setStyleSheet("font-size: 13px; font-weight: bold; color: #f8fafc;")
            top_row.addWidget(tag_name_lbl)
            top_row.addStretch()

            tc, bc = get_tag_color(norm_tag)
            pill = QLabel(f" #{tag} ")
            pill.setStyleSheet(
                f"color: {tc}; background: {bc}; font-size: 10px; font-weight: bold;"
                f" border: 1px solid {tc}; border-radius: 4px; padding: 2px 5px;"
            )
            top_row.addWidget(pill)
            self._preview_labels[norm_tag] = pill
            row_layout.addLayout(top_row)

            # Color swatches - use functools.partial for guaranteed arg binding
            from functools import partial
            swatches_row = QHBoxLayout()
            swatches_row.setSpacing(5)
            for preset_tc, preset_bc, label_p in TAG_COLOR_PRESETS:
                swatch_btn = QPushButton()
                swatch_btn.setFixedSize(26, 26)
                swatch_btn.setToolTip(Localization.get(label_p))
                swatch_btn.setStyleSheet(
                    f"background-color: {preset_tc}; border: 2px solid {preset_bc}; border-radius: 13px;"
                    " padding: 0; margin: 0;"
                )
                swatch_btn.clicked.connect(
                    partial(self._apply_color, norm_tag, preset_tc, preset_bc)
                )
                swatches_row.addWidget(swatch_btn)

            # Reset button
            reset_btn = QPushButton("↺")
            reset_btn.setFixedSize(26, 26)
            reset_btn.setToolTip(Localization.get("tag_colors_reset_tooltip"))
            reset_btn.setStyleSheet(
                "background-color: #334155; color: #94a3b8; font-size: 14px;"
                " border: 1px solid #475569; border-radius: 13px; padding: 0;"
            )
            reset_btn.clicked.connect(partial(self._reset_color, norm_tag))
            swatches_row.addWidget(reset_btn)
            swatches_row.addStretch()

            row_layout.addLayout(swatches_row)
            layout.addWidget(row_frame)

        # Close button
        close_btn = QPushButton(Localization.get("close"))
        close_btn.clicked.connect(self.accept)
        layout.addWidget(close_btn)

    def _apply_color(self, tag: str, text_color: str, bg_color: str, _checked=False):
        norm = tag.lower().strip()
        set_tag_color(norm, text_color, bg_color)
        pill = self._preview_labels.get(norm)
        if pill:
            pill.setStyleSheet(
                f"color: {text_color}; background: {bg_color}; font-size: 10px; font-weight: bold;"
                f" border: 1px solid {text_color}; border-radius: 4px; padding: 2px 5px;"
            )

    def _reset_color(self, tag: str, _checked=False):
        """Remove custom color for this tag so it falls back to hash-based default."""
        norm = tag.lower().strip()
        _tag_color_mgr._custom_colors.pop(norm, None)
        _tag_color_mgr.save()
        # Update preview
        tc, bc = get_tag_color(norm)
        pill = self._preview_labels.get(norm)
        if pill:
            pill.setStyleSheet(
                f"color: {tc}; background: {bc}; font-size: 10px; font-weight: bold;"
                f" border: 1px solid {tc}; border-radius: 4px; padding: 2px 5px;"
            )


class TaskDialog(QDialog):
    def __init__(self, parent=None, task=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.task = task
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle(Localization.get("add_task") if not self.task else Localization.get("edit_task"))
        self.resize(400, 480)
        
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

        # Due Date Selection Row
        due_layout = QHBoxLayout()
        self.due_checkbox = QCheckBox(Localization.get("has_due_date"))
        self.due_date_edit = QDateEdit()
        self.due_date_edit.setCalendarPopup(True)
        self.due_date_edit.setDate(datetime.now().date())
        self.due_date_edit.setEnabled(False)
        self.due_checkbox.toggled.connect(self.due_date_edit.setEnabled)
        due_layout.addWidget(self.due_checkbox)
        due_layout.addWidget(self.due_date_edit)
        layout.addLayout(due_layout)

        # Subtasks Editor Section
        layout.addWidget(QLabel(Localization.get("subtasks")))
        
        sub_input_layout = QHBoxLayout()
        self.sub_input = QLineEdit()
        self.sub_input.setPlaceholderText(Localization.get("subtask_placeholder"))
        self.btn_add_sub = QPushButton()
        self.btn_add_sub.setIcon(create_vector_icon("sub_add", "#14b8a6", 28))
        self.btn_add_sub.setToolTip(Localization.get("add_subtask"))
        self.btn_add_sub.setFixedWidth(36)
        self.btn_add_sub.setFixedHeight(32)
        self.btn_add_sub.setObjectName("cardBtn")
        self.btn_add_sub.clicked.connect(self.add_subtask_to_list)
        self.sub_input.returnPressed.connect(self.add_subtask_to_list)
        sub_input_layout.addWidget(self.sub_input)
        sub_input_layout.addWidget(self.btn_add_sub)
        layout.addLayout(sub_input_layout)
        
        self.sub_list_widget = QListWidget()
        self.sub_list_widget.setMaximumHeight(85)
        self.sub_list_widget.setToolTip(Localization.get("subtask_edit_tooltip"))
        self.sub_list_widget.itemDoubleClicked.connect(lambda item: self.sub_list_widget.takeItem(self.sub_list_widget.row(item)))
        layout.addWidget(self.sub_list_widget)

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

        tags_input_row = QHBoxLayout()
        self.tags_input = QLineEdit()
        self.tags_input.setPlaceholderText(Localization.get("tags_placeholder"))
        self.tags_input.textChanged.connect(self._refresh_tag_preview)
        tags_input_row.addWidget(self.tags_input)

        self.btn_tag_colors = QPushButton()
        self.btn_tag_colors.setIcon(create_vector_icon("tag", "#8b5cf6", 22))
        self.btn_tag_colors.setToolTip(Localization.get("tag_colors_edit_tooltip"))
        self.btn_tag_colors.setFixedWidth(34)
        self.btn_tag_colors.setFixedHeight(30)
        self.btn_tag_colors.setObjectName("cardBtn")
        self.btn_tag_colors.clicked.connect(self._open_tag_color_picker)
        tags_input_row.addWidget(self.btn_tag_colors)

        tags_layout.addLayout(tags_input_row)

        # Tag pill preview row
        self.tag_preview_widget = QWidget()
        self.tag_preview_layout = QHBoxLayout(self.tag_preview_widget)
        self.tag_preview_layout.setContentsMargins(0, 2, 0, 0)
        self.tag_preview_layout.setSpacing(4)
        tags_layout.addWidget(self.tag_preview_widget)

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
            
            # Load due date
            due_date_str = self.task.get("due_date", "")
            if due_date_str:
                from PyQt6.QtCore import QDate
                qdate = QDate.fromString(due_date_str, "yyyy-MM-dd")
                if qdate.isValid():
                    self.due_checkbox.setChecked(True)
                    self.due_date_edit.setDate(qdate)
                    self.due_date_edit.setEnabled(True)
                    
            # Load subtasks
            subtasks = self.task.get("subtasks", [])
            for sub in subtasks:
                item = QListWidgetItem(sub["title"])
                item.setData(Qt.ItemDataRole.UserRole, sub["done"])
                if sub["done"]:
                    font = item.font()
                    font.setStrikeOut(True)
                    item.setFont(font)
                    item.setForeground(QColor("#64748b"))
                self.sub_list_widget.addItem(item)

        # Initial tag preview
        self._refresh_tag_preview()

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

    def _refresh_tag_preview(self):
        """Rebuild the tag pill preview row based on current input."""
        # Clear existing pills
        while self.tag_preview_layout.count():
            item = self.tag_preview_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        tags_raw = self.tags_input.text().split(",")
        tags = [t.strip() for t in tags_raw if t.strip()]
        for tag in tags:
            text_color, bg_color = get_tag_color(tag)
            pill = QLabel(f" #{tag} ")
            pill.setStyleSheet(
                f"color: {text_color}; background: {bg_color}; "
                f"font-size: 10px; font-weight: bold; "
                f"border: 1px solid {text_color}; border-radius: 4px; padding: 1px 3px;"
            )
            self.tag_preview_layout.addWidget(pill)
        self.tag_preview_layout.addStretch()

    def _open_tag_color_picker(self):
        """Open TagColorPickerDialog for current tags."""
        tags_raw = self.tags_input.text().split(",")
        tags = [t.strip() for t in tags_raw if t.strip()]
        if not tags:
            QMessageBox.information(self, Localization.get("tag_colors_no_tags_title"),
                Localization.get("tag_colors_no_tags_msg"))
            return
        dlg = TagColorPickerDialog(tags, self)
        dlg.exec()
        self._refresh_tag_preview()

    def save_clicked(self):
        if not self.title_input.text().strip():
            QMessageBox.warning(self, Localization.get("warning"), Localization.get("title_empty_warning"))
            return
        self.accept()

    def add_subtask_to_list(self):
        text = self.sub_input.text().strip()
        if text:
            item = QListWidgetItem(text)
            item.setData(Qt.ItemDataRole.UserRole, False)
            self.sub_list_widget.addItem(item)
            self.sub_input.clear()

    def get_data(self):
        tags_raw = self.tags_input.text().split(",")
        tags = [t.strip() for t in tags_raw if t.strip()]
        due_date = ""
        if self.due_checkbox.isChecked():
            due_date = self.due_date_edit.date().toString("yyyy-MM-dd")
            
        # Get subtasks
        subtasks = []
        for i in range(self.sub_list_widget.count()):
            item = self.sub_list_widget.item(i)
            done = item.data(Qt.ItemDataRole.UserRole)
            subtasks.append({"title": item.text(), "done": bool(done)})
            
        return {
            "title": self.title_input.text().strip(),
            "description": self.desc_input.toPlainText().strip(),
            "priority": self.priority_map.get(self.priority_combo.currentText(), "medium"),
            "tags": tags,
            "due_date": due_date,
            "subtasks": subtasks
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

        theme = _style_mod.get_active_theme()

        # Draw grid lines and Y axis
        grid_pen = QPen(QColor(theme.card_bg))
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
        label_pen = QPen(QColor(theme.text_muted))
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

            # Draw bar with gradient using theme primary colors
            grad = QLinearGradient(bar_x, bar_y, bar_x, top_m + chart_h)
            grad.setColorAt(0.0, QColor(theme.primary_hover))
            grad.setColorAt(1.0, QColor(theme.primary_pressed))
            
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


class HeatmapWidget(QWidget):
    """GitHub contribution graph style heatmap of focus sessions over the last 84 days."""

    # Color levels based on focus minutes - these are overridden dynamically from theme
    COLOR_EMPTY  = "#1e293b"  # 0 min (fallback)
    COLOR_LOW    = "#134e4a"  # 1-30 min (fallback)
    COLOR_MED    = "#0f766e"  # 31-60 min (fallback)
    COLOR_HIGH   = "#14b8a6"  # 61-120 min (fallback)
    COLOR_MAX    = "#2dd4bf"  # 120+ min (fallback)

    CELL_SIZE = 14  # px per square
    GAP = 2         # px gap between squares
    WEEKS = 12
    DAYS  = 7

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumHeight(140)
        self.setMouseTracking(True)
        self._sessions = {}       # date_str -> minutes
        self._hovered_cell = None # (col, row) or None
        self._build_day_list()

    def _build_day_list(self):
        """Build the list of 84 dates (oldest first) ending today."""
        today = datetime.now().date()
        self._days = []
        for i in range(self.WEEKS * self.DAYS - 1, -1, -1):
            self._days.append(today - timedelta(days=i))

    def set_stats(self, sessions):
        """Accept list of {"date": "YYYY-MM-DD", "minutes": X} dicts."""
        self._sessions = {s["date"]: s["minutes"] for s in sessions}
        self._build_day_list()
        self.update()

    def _cell_color(self, minutes):
        theme = _style_mod.get_active_theme()
        # Derive heatmap levels from theme primary color dynamically
        empty_color = QColor(theme.card_bg)
        primary_c = QColor(theme.primary)
        pressed_c = QColor(theme.primary_pressed)
        if minutes <= 0:
            return empty_color
        elif minutes <= 30:
            # Very dark tint
            c = QColor(pressed_c)
            c.setAlpha(160)
            return pressed_c.darker(160)
        elif minutes <= 60:
            return pressed_c
        elif minutes <= 120:
            return primary_c
        else:
            return QColor(theme.primary_hover)

    def _cell_rect(self, col, row, left_offset, top_offset):
        x = left_offset + col * (self.CELL_SIZE + self.GAP)
        y = top_offset  + row * (self.CELL_SIZE + self.GAP)
        return QRectF(x, y, self.CELL_SIZE, self.CELL_SIZE)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        LEFT_OFFSET = 22   # space for day labels
        TOP_OFFSET  = 22   # space for month labels

        # --- Month labels ---
        month_font = QFont("Inter", 8, QFont.Weight.Medium)
        painter.setFont(month_font)
        painter.setPen(QPen(QColor("#94a3b8")))

        last_month = None
        for col in range(self.WEEKS):
            day_idx = col * self.DAYS
            if day_idx < len(self._days):
                d = self._days[day_idx]
                if d.month != last_month:
                    last_month = d.month
                    x = LEFT_OFFSET + col * (self.CELL_SIZE + self.GAP)
                    painter.drawText(int(x), int(TOP_OFFSET - 6), d.strftime("%b"))

        # --- Day labels (M, W, F) ---
        day_labels = {1: "M", 3: "W", 5: "F"}  # 0=Mon index
        for row in range(self.DAYS):
            label = day_labels.get(row)
            if label:
                y = TOP_OFFSET + row * (self.CELL_SIZE + self.GAP) + self.CELL_SIZE - 2
                painter.drawText(2, int(y), label)

        # --- Grid cells ---
        painter.setPen(Qt.PenStyle.NoPen)
        for col in range(self.WEEKS):
            for row in range(self.DAYS):
                idx = col * self.DAYS + row
                if idx >= len(self._days):
                    continue
                d = self._days[idx]
                mins = self._sessions.get(d.strftime("%Y-%m-%d"), 0)
                color = self._cell_color(mins)

                # Highlight hovered cell
                if self._hovered_cell == (col, row):
                    color = color.lighter(150)

                painter.setBrush(QBrush(color))
                rect = self._cell_rect(col, row, LEFT_OFFSET, TOP_OFFSET)
                painter.drawRoundedRect(rect, 2.0, 2.0)

    def mouseMoveEvent(self, event):
        LEFT_OFFSET = 22
        TOP_OFFSET  = 22
        step = self.CELL_SIZE + self.GAP

        mx, my = event.position().x(), event.position().y()
        col = int((mx - LEFT_OFFSET) // step)
        row = int((my - TOP_OFFSET)  // step)

        if 0 <= col < self.WEEKS and 0 <= row < self.DAYS:
            idx = col * self.DAYS + row
            if idx < len(self._days):
                d = self._days[idx]
                mins = self._sessions.get(d.strftime("%Y-%m-%d"), 0)
                tooltip_text = f"{d.strftime('%d %b %Y')} — {mins} {Localization.get('min')}"
                QToolTip.showText(event.globalPosition().toPoint(), tooltip_text, self)
                if self._hovered_cell != (col, row):
                    self._hovered_cell = (col, row)
                    self.update()
                return

        QToolTip.hideText()
        if self._hovered_cell is not None:
            self._hovered_cell = None
            self.update()

    def leaveEvent(self, event):
        if self._hovered_cell is not None:
            self._hovered_cell = None
            self.update()
        super().leaveEvent(event)


class DonutChartWidget(QWidget):
    """Generic donut chart supporting priority-based and tag-based focus distribution."""

    COLOR_HIGH   = "#ef4444"  # red (priority high)
    COLOR_MEDIUM = "#f59e0b"  # amber (priority medium)
    COLOR_LOW    = "#10b981"  # emerald (priority low)
    ARC_WIDTH    = 22

    # Palette for tag mode (up to 8 distinct colors)
    TAG_PALETTE = [
        "#14b8a6", "#8b5cf6", "#f59e0b", "#ef4444",
        "#3b82f6", "#ec4899", "#f97316", "#84cc16"
    ]

    MODE_PRIORITY = "priority"
    MODE_TAGS     = "tags"

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setMinimumSize(200, 180)
        self._mode = self.MODE_PRIORITY
        # Priority mode data
        self._high   = 0
        self._medium = 0
        self._low    = 0
        # Tag mode data: list of (label, value, color_hex)
        self._tag_items = []

    def set_mode(self, mode):
        """Switch between MODE_PRIORITY and MODE_TAGS."""
        if mode in (self.MODE_PRIORITY, self.MODE_TAGS):
            self._mode = mode
            self.update()

    def set_data(self, high_count, medium_count, low_count):
        """Update priority distribution counts and repaint."""
        self._high   = max(0, high_count)
        self._medium = max(0, medium_count)
        self._low    = max(0, low_count)
        self.update()

    def set_tag_data(self, tag_focus_list):
        """Set tag-based focus data.
        tag_focus_list: list of (tag_label, focus_minutes) sorted desc.
        Top 5 shown, rest as 'Diğer'.
        """
        palette = self.TAG_PALETTE
        items = []
        other_total = 0
        for i, (tag, mins) in enumerate(tag_focus_list):
            if i < len(palette):
                items.append((tag, mins, palette[i % len(palette)]))
            else:
                other_total += mins
        if other_total > 0:
            items.append((Localization.get("donut_other"), other_total, "#64748b"))
        self._tag_items = items
        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        theme = _style_mod.get_active_theme()
        w = self.width()
        h = self.height()

        # Reserve right side for legend
        LEGEND_W  = 100
        donut_area_w = w - LEGEND_W
        donut_size = min(donut_area_w, h) - 20
        if donut_size < 40:
            donut_size = 40

        cx = (donut_area_w - donut_size) / 2
        cy = (h - donut_size) / 2
        donut_rect = QRectF(cx, cy, donut_size, donut_size)

        # Build segments based on mode
        if self._mode == self.MODE_PRIORITY:
            total = self._high + self._medium + self._low
            segments = [
                (self._high,   QColor(self.COLOR_HIGH),   Localization.get("donut_high")),
                (self._medium, QColor(self.COLOR_MEDIUM),  Localization.get("donut_medium")),
                (self._low,    QColor(self.COLOR_LOW),     Localization.get("donut_low")),
            ]
            center_text = str(total)
            unit_label = Localization.get("donut_tasks_unit")
        else:
            total = sum(v for _, v, _ in self._tag_items)
            segments = [(v, QColor(c), lbl) for lbl, v, c in self._tag_items]
            center_text = f"{total}"
            unit_label = Localization.get("donut_time_unit")

        # Draw background track
        track_pen = QPen(QColor(theme.card_bg))
        track_pen.setWidth(self.ARC_WIDTH)
        painter.setPen(track_pen)
        painter.drawEllipse(donut_rect)

        # Draw segments
        start_angle = 90 * 16  # top
        if total > 0:
            for count, color, _ in segments:
                if count == 0:
                    continue
                span = int(-(count / total) * 360 * 16)
                pen = QPen(color)
                pen.setWidth(self.ARC_WIDTH)
                pen.setCapStyle(Qt.PenCapStyle.FlatCap)
                painter.setPen(pen)
                painter.drawArc(donut_rect, start_angle, span)
                start_angle += span
        else:
            # Draw empty placeholder arc
            pen = QPen(QColor(theme.border))
            pen.setWidth(self.ARC_WIDTH)
            painter.setPen(pen)
            painter.drawArc(donut_rect, 90*16, -360*16)

        # Center text
        painter.setPen(QPen(QColor("#ffffff")))
        font_big = QFont("Inter", 14, QFont.Weight.Bold)
        painter.setFont(font_big)
        painter.drawText(donut_rect.adjusted(0, -8, 0, -8), Qt.AlignmentFlag.AlignCenter, center_text)
        font_small = QFont("Inter", 8)
        painter.setFont(font_small)
        painter.setPen(QPen(QColor(theme.text_muted)))
        painter.drawText(donut_rect.adjusted(0, 12, 0, 12), Qt.AlignmentFlag.AlignCenter, unit_label)

        # Legend
        legend_x = donut_area_w + 8
        legend_y = cy + 10
        legend_font = QFont("Inter", 9, QFont.Weight.Medium)
        painter.setFont(legend_font)

        for count, lcolor, ltext in segments:
            if legend_y + 22 > h:
                break
            # Colored circle
            painter.setPen(Qt.PenStyle.NoPen)
            painter.setBrush(QBrush(lcolor))
            painter.drawEllipse(QRectF(legend_x, legend_y, 10, 10))
            # Label
            painter.setPen(QPen(QColor(theme.text_main)))
            display = ltext if len(ltext) <= 10 else ltext[:9]+"…"
            painter.drawText(int(legend_x + 14), int(legend_y + 10), f"{display}: {count}")
            legend_y += 26



class PomodoroSettingsDialog(QDialog):
    def __init__(self, work, short_break, long_break, daily_goal, parent=None):
        super().__init__(parent)
        self.setWindowFlag(Qt.WindowType.FramelessWindowHint)
        self.setWindowTitle(Localization.get("timer_settings_title"))
        self.resize(320, 280)
        self.setStyleSheet("""
            QDialog { background-color: #0f172a; }
            QLabel { color: #e2e8f0; }
        """)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(15, 15, 15, 15)
        layout.setSpacing(10)
        
        title = QLabel(Localization.get("timer_settings_header"))
        title.setStyleSheet("font-size: 14px; font-weight: bold; color: #ffffff;")
        layout.addWidget(title)
        
        # Work minutes input
        layout.addWidget(QLabel(Localization.get("timer_work_label")))
        self.work_input = QLineEdit()
        self.work_input.setText(str(work))
        layout.addWidget(self.work_input)
        
        # Short break minutes input
        layout.addWidget(QLabel(Localization.get("timer_short_break_label")))
        self.break_input = QLineEdit()
        self.break_input.setText(str(short_break))
        layout.addWidget(self.break_input)

        # Long break minutes input
        layout.addWidget(QLabel(Localization.get("timer_long_break_label")))
        self.long_break_input = QLineEdit()
        self.long_break_input.setText(str(long_break))
        layout.addWidget(self.long_break_input)

        # Daily goal input
        layout.addWidget(QLabel(Localization.get("timer_daily_goal_label")))
        self.goal_input = QLineEdit()
        self.goal_input.setText(str(daily_goal))
        layout.addWidget(self.goal_input)
        
        # Buttons
        btn_layout = QHBoxLayout()
        self.btn_cancel = QPushButton(Localization.get("cancel"))
        self.btn_cancel.setObjectName("secondaryBtn")
        self.btn_cancel.clicked.connect(self.reject)
        
        self.btn_save = QPushButton(Localization.get("save"))
        self.btn_save.clicked.connect(self.validate_and_save)
        
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_save)
        layout.addLayout(btn_layout)
        
    def validate_and_save(self):
        try:
            w = int(self.work_input.text())
            b = int(self.break_input.text())
            lb = int(self.long_break_input.text())
            g = int(self.goal_input.text())
            if w <= 0 or b <= 0 or lb <= 0 or g <= 0:
                raise ValueError()
            self.accept()
        except ValueError:
            QMessageBox.warning(self, Localization.get("export_error_title"), Localization.get("timer_validation_error"))
            
    def get_values(self):
        return (
            int(self.work_input.text()),
            int(self.break_input.text()),
            int(self.long_break_input.text()),
            int(self.goal_input.text())
        )


class PomodoroWidget(QFrame):
    session_completed = pyqtSignal(int, str) # Emits focus duration in minutes and selected task ID (or empty string)
    settings_changed = pyqtSignal() # Emitted when durations or goal change

    def __init__(self, db=None, parent=None):
        super().__init__(parent)
        self.db = db
        self.setObjectName("sidebarPanel")
        
        # Timer default variables
        self.work_minutes = 25
        self.break_minutes = 5
        self.long_break_minutes = 15
        self.daily_goal = 100

        if self.db:
            stats = self.db.get_stats()
            self.work_minutes = stats.get("pomodoro_work_minutes", 25)
            self.break_minutes = stats.get("pomodoro_break_minutes", 5)
            self.long_break_minutes = stats.get("pomodoro_long_break_minutes", 15)
            self.daily_goal = stats.get("daily_goal_minutes", 100)
        
        # Timer variables
        self.timer_seconds = self.work_minutes * 60
        self.total_seconds = self.work_minutes * 60
        self.is_running = False
        self.is_work_session = True # True = Work, False = Break

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.timer_tick)

        self.init_ui()


    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(15)

        # Title Row with Settings Button
        title_layout = QHBoxLayout()
        title = QLabel(Localization.get("focus_timer"))
        title.setObjectName("columnTitle")
        title_layout.addWidget(title)
        title_layout.addStretch()

        self.btn_settings = QPushButton()
        self.btn_settings.setIcon(create_vector_icon("settings", "#94a3b8", 18))
        self.btn_settings.setFixedSize(24, 24)
        self.btn_settings.setStyleSheet("background: transparent; border: none; padding: 0;")
        self.btn_settings.setToolTip(Localization.get("timer_settings_tooltip"))
        self.btn_settings.clicked.connect(self.open_settings)
        title_layout.addWidget(self.btn_settings)
        layout.addLayout(title_layout)

        # Circular Timer View
        self.circular_timer = CircularTimerWidget()
        layout.addWidget(self.circular_timer, 0, Qt.AlignmentFlag.AlignCenter)


        # Task Selection dropdown
        task_sel_layout = QVBoxLayout()
        task_sel_layout.setSpacing(4)
        
        task_lbl = QLabel(Localization.get("focus_on_task"))
        task_lbl.setStyleSheet("color: #94a3b8; font-size: 11px;")
        task_sel_layout.addWidget(task_lbl)
        
        self.task_combo = QComboBox()
        self.task_combo.setStyleSheet("padding: 6px; font-size: 12px;")
        self.task_combo.addItem(Localization.get("general_focus"), "")
        task_sel_layout.addWidget(self.task_combo)
        
        layout.addLayout(task_sel_layout)

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
        
        self.btn_25min = QPushButton(Localization.get("work_btn", self.work_minutes))
        self.btn_25min.setObjectName("secondaryBtn")
        self.btn_25min.setStyleSheet("font-size: 11px; padding: 5px;")
        self.btn_25min.clicked.connect(lambda: self.set_duration(self.work_minutes, True))

        self.btn_5min = QPushButton(Localization.get("break_short_btn", self.break_minutes))
        self.btn_5min.setObjectName("secondaryBtn")
        self.btn_5min.setStyleSheet("font-size: 11px; padding: 5px;")
        self.btn_5min.clicked.connect(lambda: self.set_duration(self.break_minutes, False))

        self.btn_15min = QPushButton(Localization.get("break_long_btn", self.long_break_minutes))
        self.btn_15min.setObjectName("secondaryBtn")
        self.btn_15min.setStyleSheet("font-size: 11px; padding: 5px;")
        self.btn_15min.clicked.connect(lambda: self.set_duration(self.long_break_minutes, False))

        adj_layout.addWidget(self.btn_25min)
        adj_layout.addWidget(self.btn_5min)
        adj_layout.addWidget(self.btn_15min)
        layout.addLayout(adj_layout)

        self.circular_timer.double_clicked.connect(self.on_timer_double_clicked)

        self.update_display()

    def on_timer_double_clicked(self):
        """Allow setting custom focus duration on double click."""
        curr_mins = self.timer_seconds // 60
        new_mins, ok = QInputDialog.getInt(
            self, Localization.get("timer_customize_title"),
            Localization.get("timer_customize_label"),
            curr_mins, 1, 300, 1
        )
        if ok:
            self.set_duration(new_mins, self.is_work_session)

    def open_settings(self):
        """Open settings dialog to customize work and break times."""
        dlg = PomodoroSettingsDialog(self.work_minutes, self.break_minutes, self.long_break_minutes, self.daily_goal, self)
        if dlg.exec() == QDialog.DialogCode.Accepted:
            w, b, lb, g = dlg.get_values()
            self.work_minutes = w
            self.break_minutes = b
            self.long_break_minutes = lb
            self.daily_goal = g
            
            if self.db:
                self.db.set_pomodoro_settings(w, b, lb)
                self.db.set_daily_goal(g)
                
            self.btn_25min.setText(Localization.get("work_btn", self.work_minutes))
            self.btn_5min.setText(Localization.get("break_short_btn", self.break_minutes))
            self.btn_15min.setText(Localization.get("break_long_btn", self.long_break_minutes))
            
            self.set_duration(self.work_minutes, True)
            self.settings_changed.emit()



    def update_tasks(self, tasks):
        curr_id = self.task_combo.currentData()
        
        self.task_combo.clear()
        self.task_combo.addItem(Localization.get("general_focus"), "")
        
        for task in tasks:
            if task.get("status", "todo") in ["todo", "doing"]:
                title = task.get("title", "")
                if len(title) > 25:
                    title = title[:22] + "..."
                self.task_combo.addItem(create_vector_icon("pin"), title, task.get("id"))
                
        # Restore selection if it still exists
        if curr_id:
            idx = self.task_combo.findData(curr_id)
            if idx >= 0:
                self.task_combo.setCurrentIndex(idx)

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
        self.task_combo.setEnabled(True) # Enable task dropdown
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
            self.task_combo.setEnabled(False) # Disable task dropdown

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
        self.task_combo.setEnabled(True) # Enable task dropdown
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
            self.task_combo.setEnabled(True) # Enable task dropdown

            # Session finished
            duration_minutes = self.total_seconds // 60
            if self.is_work_session:
                QMessageBox.information(self, Localization.get("congrats"), Localization.get("work_done_msg"))
                self.session_completed.emit(duration_minutes, self.task_combo.currentData())
                # Auto set short break
                self.set_duration(self.break_minutes, False)
            else:
                QMessageBox.information(self, Localization.get("break_done_title"), Localization.get("break_done_msg"))
                self.set_duration(self.work_minutes, True)



class CalendarViewWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.tasks = []
        self.current_year = datetime.now().year
        self.current_month = datetime.now().month
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(8)

        # Nav bar: Prev button, Month/Year label, Next button
        nav_layout = QHBoxLayout()
        self.btn_prev = QPushButton()
        self.btn_prev.setIcon(create_vector_icon("arrow_left", "#94a3b8", 24))
        self.btn_prev.setFixedSize(32, 32)
        self.btn_prev.setStyleSheet("background: transparent; border: none;")
        self.btn_prev.clicked.connect(self.go_prev_month)

        self.lbl_month = QLabel()
        self.lbl_month.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.lbl_month.setStyleSheet("font-size: 15px; font-weight: bold; color: #f8fafc;")

        self.btn_next = QPushButton()
        self.btn_next.setIcon(create_vector_icon("arrow_right", "#94a3b8", 24))
        self.btn_next.setFixedSize(32, 32)
        self.btn_next.setStyleSheet("background: transparent; border: none;")
        self.btn_next.clicked.connect(self.go_next_month)

        nav_layout.addWidget(self.btn_prev)
        nav_layout.addStretch()
        nav_layout.addWidget(self.lbl_month)
        nav_layout.addStretch()
        nav_layout.addWidget(self.btn_next)
        layout.addLayout(nav_layout)

        # Calendar grid (7 columns for days)
        self.grid_widget = QWidget()
        self.grid_layout = QGridLayout(self.grid_widget)
        self.grid_layout.setSpacing(3)
        layout.addWidget(self.grid_widget)

        self.update_calendar()

    def update_tasks(self, tasks):
        self.tasks = tasks
        self.update_calendar()

    def go_prev_month(self):
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.update_calendar()

    def go_next_month(self):
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.update_calendar()

    def update_calendar(self):
        # Clear grid
        while self.grid_layout.count():
            item = self.grid_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        month_names = Localization.get("month_names").split(",")
        self.lbl_month.setText(f"{month_names[self.current_month - 1]} {self.current_year}")

        # Day headers
        day_names = Localization.get("day_names").split(",")
        for col, day_name in enumerate(day_names):
            lbl = QLabel(day_name)
            lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
            lbl.setStyleSheet("color: #64748b; font-size: 11px; font-weight: bold; padding: 4px;")
            self.grid_layout.addWidget(lbl, 0, col)

        # Build task dict keyed by date string
        task_by_date = {}
        for task in self.tasks:
            d = task.get("due_date", "")
            if d:
                if d not in task_by_date:
                    task_by_date[d] = []
                task_by_date[d].append(task)

        import calendar
        first_weekday, days_in_month = calendar.monthrange(self.current_year, self.current_month)
        # Monday=0

        today = datetime.now().date()

        cell_row = 1
        cell_col = first_weekday  # start from correct weekday

        for day in range(1, days_in_month + 1):
            date_str = f"{self.current_year}-{self.current_month:02d}-{day:02d}"

            cell = QFrame()
            cell.setMinimumSize(60, 54)
            cell.setMaximumHeight(80)

            # Highlight today
            if (self.current_year == today.year and
                    self.current_month == today.month and
                    day == today.day):
                cell.setStyleSheet(
                    "background: #134e4a; border: 1.5px solid #14b8a6; border-radius: 8px;"
                )
            else:
                cell.setStyleSheet(
                    "background: #1e293b; border: 1px solid #2d3748; border-radius: 8px;"
                )

            cell_layout = QVBoxLayout(cell)
            cell_layout.setContentsMargins(4, 4, 4, 4)
            cell_layout.setSpacing(2)

            day_lbl = QLabel(str(day))
            day_lbl.setAlignment(Qt.AlignmentFlag.AlignRight)
            day_lbl.setStyleSheet("color: #94a3b8; font-size: 12px; font-weight: bold;")
            cell_layout.addWidget(day_lbl)

            # Add task chips
            tasks_on_day = task_by_date.get(date_str, [])
            for t in tasks_on_day[:2]:  # max 2 chips per cell
                p = t.get("priority", "medium")
                chip_color = {"high": "#ef4444", "medium": "#f59e0b", "low": "#14b8a6"}.get(p, "#14b8a6")
                chip = QLabel(t["title"][:10] + ("..." if len(t["title"]) > 10 else ""))
                chip.setStyleSheet(
                    f"background: {chip_color}; color: #ffffff; font-size: 9px;"
                    " border-radius: 3px; padding: 1px 3px;"
                )
                chip.setToolTip(t["title"])
                cell_layout.addWidget(chip)

            if len(tasks_on_day) > 2:
                more_lbl = QLabel(f"+{len(tasks_on_day) - 2}")
                more_lbl.setStyleSheet("color: #64748b; font-size: 9px;")
                cell_layout.addWidget(more_lbl)

            cell_layout.addStretch()
            self.grid_layout.addWidget(cell, cell_row, cell_col)

            cell_col += 1
            if cell_col == 7:
                cell_col = 0
                cell_row += 1
