#!/usr/bin/python3
from luppo.actionsapi import luppotools
from luppo.actionsapi import shelltools
import os

WorkDir = "."

def build():
    pass

def install():
    src_dir = os.environ.get("AURATASK_SRC_DIR", os.getcwd())

    # Copy application main entry and package directory
    main_py = os.path.join(src_dir, "AuraTask")
    if not os.path.isfile(main_py):
        main_py = "AuraTask"
    if os.path.isfile(main_py):
        luppotools.insinto("/usr/share/auratask", main_py)

    auratask_dir = os.path.join(src_dir, "auratask")
    if not os.path.isdir(auratask_dir):
        auratask_dir = "auratask"
    if os.path.isdir(auratask_dir):
        luppotools.insinto("/usr/share/auratask", auratask_dir)

    # Launcher script (/usr/bin/auratask)
    launcher_path = os.path.join(src_dir, "auratask")
    if not os.path.isfile(launcher_path):
        launcher_path = "auratask"
    
    if not os.path.isfile(launcher_path):
        with open("auratask", "w") as f:
            f.write("#!/bin/bash\nexec python3 /usr/share/auratask/AuraTask \"$@\"\n")
        os.chmod("auratask", 0o755)
        launcher_path = "auratask"

    luppotools.dobin(launcher_path)

    # Desktop entry
    desktop_path = os.path.join(src_dir, "auratask.desktop")
    if not os.path.isfile(desktop_path):
        desktop_path = "auratask.desktop"
    if os.path.isfile(desktop_path):
        luppotools.insinto("/usr/share/applications", desktop_path)

    # App icon
    icon_path = os.path.join(src_dir, "data", "auratask.png")
    if not os.path.isfile(icon_path):
        icon_path = os.path.join("data", "auratask.png")
    if os.path.isfile(icon_path):
        luppotools.insinto("/usr/share/icons/hicolor/128x128/apps", icon_path, "auratask.png")

    # Documentation & License
    readme_path = os.path.join(src_dir, "README.md")
    if not os.path.isfile(readme_path):
        readme_path = "README.md"
    if os.path.isfile(readme_path):
        luppotools.dodoc(readme_path)

    license_path = os.path.join(src_dir, "LICENSE")
    if not os.path.isfile(license_path):
        license_path = "LICENSE"
    if os.path.isfile(license_path):
        luppotools.dodoc(license_path)
