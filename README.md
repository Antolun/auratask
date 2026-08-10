# AuraTask

AuraTask is a desktop productivity application built with Python and PyQt6 (Qt6), featuring a sleek, minimalist dark mode designed to reduce eye strain. It allows you to organize tasks on a Kanban board, focus using the Pomodoro technique, and analyze your performance through beautiful custom charts.

---

## Features

*   **Kanban Task Board**: Organize tasks across "To Do", "In Progress", and "Completed" columns. Set priorities (Low, Medium, High) and add custom tags.
*   **Focus Timer (Pomodoro)**: Manage your work (25 min) and break (5 min / 15 min) intervals with a custom `QPainter` animated circular countdown timer.
*   **Productivity Analytics**: Visualize your completed focus sessions and daily focus duration using beautiful custom-drawn column charts.
*   **Premium UI (Dark Mode)**: Eye-pleasing design featuring modern indigo/slate color palettes, smooth border radius, and elegant shadows.
*   **Persistent Local Storage**: Your tasks and stats are securely saved locally in a structured JSON file, maintaining data between sessions.

---

## Installation & Build

```bash
# 1. Clone the Repository
git clone https://github.com/TeknoAnka/auratask.git
cd auratask

# 2. Build
chmod +x ./build-pisi.sh
sudo ./build-pisi.sh

# 3. Install
sudo pisi it ./auratask-*-x86_64.pisi
```

*Note: On uninstallation, if any task data exists (`tasks.json`), the script will automatically create a backup called `tasks_backup.json` in your development directory to prevent accidental data loss.*

---

## Running Without Installation

If you prefer to run the application directly from the source directory without installing it:

```bash
python3 AuraTask
```

---
