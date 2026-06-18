# 🌌 AuraTask - Premium Personal Productivity & Task Management Dashboard

AuraTask is a desktop productivity application built with Python and PyQt6 (Qt6), featuring a sleek, minimalist dark mode designed to reduce eye strain. It allows you to organize tasks on a Kanban board, focus using the Pomodoro technique, and analyze your performance through beautiful custom charts.

---

## ✨ Features

*   **📋 Kanban Task Board**: Organize tasks across "To Do", "In Progress", and "Completed" columns. Set priorities (Low, Medium, High) and add custom tags.
*   **⏱️ Focus Timer (Pomodoro)**: Manage your work (25 min) and break (5 min / 15 min) intervals with a custom `QPainter` animated circular countdown timer.
*   **📈 Productivity Analytics**: Visualize your completed focus sessions and daily focus duration using beautiful custom-drawn column charts.
*   **🎨 Premium UI (Dark Mode)**: Eye-pleasing design featuring modern indigo/slate color palettes, smooth border radius, and elegant shadows.
*   **💾 Persistent Local Storage**: Your tasks and stats are securely saved locally in a structured JSON file, maintaining data between sessions.

---

## 🛠️ System Requirements

*   **Python 3.x**
*   **PyQt6** (`pip install PyQt6`)
*   **Pillow** (`pip install Pillow` - *Used for logo rendering*)

---

## 🚀 Installation (KDE Plasma & Other Desktop Environments)

A custom installation script is provided to register the application in the desktop menus (complete with launcher search and application icon).

### 1. Install
Open your terminal in the project directory and run:

```bash
chmod +x install.sh
./install.sh --install
```

This script will:
1.  Deploy application code files and assets to `~/.local/share/auratask/`.
2.  Generate and configure a desktop entry shortcut (`auratask.desktop`).
3.  Register it inside your local application launcher databases.

After installation, you can launch the app from the application menu (e.g. Kickoff) or via search tools like **KRunner (Alt+F2)** by typing **"AuraTask"**.

### 2. Uninstall
To completely remove the application files, desktop shortcuts, and configurations from your system:

```bash
./install.sh --uninstall
```

*Note: On uninstallation, if any task data exists (`tasks.json`), the script will automatically create a backup called `tasks_backup.json` in your development directory to prevent accidental data loss.*

---

## 💻 Running Without Installation

If you prefer to run the application directly from the source directory without installing it:

```bash
python3 main.py
```

---

## 📁 Project Structure

*   `main.py`: Main entry point and main window coordination.
*   `widgets.py`: Custom GUI elements including Kanban cards, columns, Pomodoro timer, dialog forms, and custom analytics chart.
*   `database.py`: Handles saving, loading, and structural checks of task and stats data.
*   `style.py`: Contains QSS (Qt Style Sheet) rules for the global dark mode theme.
*   `install.sh`: Setup script for deployment and KDE menu integration.
*   `data/logo.png`: Transparent application logo asset.
