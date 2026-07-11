#!/usr/bin/env bash

# AuraTask KDE Plasma Desktop Installer & Uninstaller
# Installs application to ~/.local/share/auratask

# Colors for modern terminal output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Directories
SOURCE_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )"
INSTALL_DIR="$HOME/.local/share/auratask"
DESKTOP_DIR="$HOME/.local/share/applications"
DESKTOP_FILE="$DESKTOP_DIR/auratask.desktop"

# Target paths in installation directory
EXEC_PATH="$INSTALL_DIR/AuraTask"
ICON_PATH="$INSTALL_DIR/data/logo.png"

# Show usage help
show_usage() {
    echo -e "Usage: $0 [OPTION]"
    echo -e "Options:"
    echo -e "  -i, --install     Installs the application to '$INSTALL_DIR' and integrates with menu (Default)"
    echo -e "  -u, --uninstall   Completely uninstalls the application and menu entries"
    echo -e "  -h, --help        Shows this help message"
}

# Perform installation
install_app() {
    echo -e "${CYAN}====================================================${NC}"
    echo -e "${CYAN}        AuraTask KDE Desktop Installation Wizard    ${NC}"
    echo -e "${CYAN}====================================================${NC}"

    # 1. Dependency checks
    echo -e "${BLUE}[1/5] Checking requirements...${NC}"
    if python3 -c "import PyQt6" &> /dev/null; then
        echo -e "${GREEN}✓ PyQt6 library is installed.${NC}"
    else
        echo -e "${RED}✗ Error: PyQt6 not found. Please install it first: pip install PyQt6${NC}"
        exit 1
    fi

    # 2. Create target directories
    echo -e "${BLUE}[2/5] Creating installation directories...${NC}"
    echo -e "Target Directory: $INSTALL_DIR"
    mkdir -p "$INSTALL_DIR"
    mkdir -p "$INSTALL_DIR/data"
    echo -e "${GREEN}✓ Directories created.${NC}"

    # 3. Copy application files
    echo -e "${BLUE}[3/5] Copying application files...${NC}"
    
    # Copy main code files
    cp "$SOURCE_DIR/AuraTask" "$INSTALL_DIR/"
    cp "$SOURCE_DIR/database.py" "$INSTALL_DIR/"
    cp "$SOURCE_DIR/style.py" "$INSTALL_DIR/"
    cp "$SOURCE_DIR/widgets.py" "$INSTALL_DIR/"
    cp "$SOURCE_DIR/localization.py" "$INSTALL_DIR/"
    
    # Copy logo if exists
    if [ -f "$SOURCE_DIR/data/logo.png" ]; then
        cp "$SOURCE_DIR/data/logo.png" "$INSTALL_DIR/data/logo.png"
    fi

    # Set executable permissions on target AuraTask
    chmod +x "$EXEC_PATH"
    echo -e "${GREEN}✓ Files copied and execution permissions set.${NC}"

    # 4. Create desktop entry pointing to installation directory
    echo -e "${BLUE}[4/5] Creating KDE Desktop Entry (.desktop)...${NC}"
    mkdir -p "$DESKTOP_DIR"

    cat <<EOF > "$DESKTOP_FILE"
[Desktop Entry]
Name=AuraTask
Comment=Personal Focus & Task Manager
Exec=/usr/bin/python3 $EXEC_PATH
Icon=$ICON_PATH
Terminal=false
Type=Application
Categories=Office;Utility;Development;
Keywords=todo;task;pomodoro;kanban;productivity;focus;
StartupNotify=true
StartupWMClass=auratask
EOF

    chmod +x "$DESKTOP_FILE"
    echo -e "${GREEN}✓ Desktop file created: $DESKTOP_FILE${NC}"

    # 5. Refresh KDE Launcher Menu Database
    echo -e "${BLUE}[5/5] Updating KDE Plasma application menu database...${NC}"
    if command -v update-desktop-database &> /dev/null; then
        update-desktop-database "$DESKTOP_DIR"
        echo -e "${GREEN}✓ Desktop database updated.${NC}"
    else
        echo -e "${CYAN}! Info: update-desktop-database command not found, menu will auto-refresh soon.${NC}"
    fi

    echo -e "${CYAN}====================================================${NC}"
    echo -e "${GREEN}🎉 AuraTask successfully installed to '$INSTALL_DIR'!${NC}"
    echo -e "${BLUE}You can now launch it from application launcher menu or KRunner search by typing:${NC}"
    echo -e "${CYAN}\"AuraTask\"${NC}"
    echo -e "${CYAN}====================================================${NC}"
}

# Perform uninstallation
uninstall_app() {
    echo -e "${YELLOW}====================================================${NC}"
    echo -e "${YELLOW}        AuraTask KDE Desktop Uninstallation Wizard  ${NC}"
    echo -e "${YELLOW}====================================================${NC}"

    # 1. Remove desktop file
    if [ -f "$DESKTOP_FILE" ]; then
        echo -e "${BLUE}[1/3] Removing desktop shortcut...${NC}"
        rm -f "$DESKTOP_FILE"
        echo -e "${GREEN}✓ $DESKTOP_FILE removed.${NC}"
    else
        echo -e "${YELLOW}! Info: Desktop shortcut file not found.${NC}"
    fi

    # 2. Remove installation folder
    if [ -d "$INSTALL_DIR" ]; then
        echo -e "${BLUE}[2/3] Cleaning up installation folder...${NC}"
        echo -e "Removing directory: $INSTALL_DIR"
        
        # Backup tasks.json if it exists to source folder before deleting, just in case
        if [ -f "$INSTALL_DIR/data/tasks.json" ]; then
            cp "$INSTALL_DIR/data/tasks.json" "$SOURCE_DIR/tasks_backup.json" 2>/dev/null
            echo -e "${YELLOW}! Info: Your task data was backed up to '$SOURCE_DIR/tasks_backup.json'.${NC}"
        fi
        
        rm -rf "$INSTALL_DIR"
        echo -e "${GREEN}✓ Application files and directory successfully removed.${NC}"
    else
        echo -e "${YELLOW}! Info: Installation directory ($INSTALL_DIR) not found.${NC}"
    fi

    # 3. Refresh KDE Launcher Menu Database
    echo -e "${BLUE}[3/3] Updating KDE Plasma application menu database...${NC}"
    if command -v update-desktop-database &> /dev/null; then
        update-desktop-database "$DESKTOP_DIR"
        echo -e "${GREEN}✓ Desktop database updated.${NC}"
    else
        echo -e "${CYAN}! Info: update-desktop-database command not found.${NC}"
    fi

    echo -e "${YELLOW}====================================================${NC}"
    echo -e "${GREEN}✓ AuraTask has been completely removed from your system!${NC}"
    echo -e "${YELLOW}====================================================${NC}"
}

# Parse command line options
ACTION="install"

while [[ "$#" -gt 0 ]]; do
    case $1 in
        -i|--install) ACTION="install"; shift ;;
        -u|--uninstall) ACTION="uninstall"; shift ;;
        -h|--help) show_usage; exit 0 ;;
        *) echo -e "${RED}Invalid option: $1${NC}"; show_usage; exit 1 ;;
    esac
done

if [ "$ACTION" == "install" ]; then
    install_app
elif [ "$ACTION" == "uninstall" ]; then
    uninstall_app
fi
