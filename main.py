# main.py

import sys
import ctypes
from PySide6.QtWidgets import QApplication, QMessageBox
from PySide6.QtCore import Qt

from ui.main_window import MainWindow
from ui.splash import NovaSplash
from ui.theme import DARK_THEME


# ---------- ADMIN CHECK ----------
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except Exception:
        return False


def relaunch_as_admin():
    params = " ".join(f'"{a}"' for a in sys.argv)
    ctypes.windll.shell32.ShellExecuteW(
        None,
        "runas",
        sys.executable,
        params,
        None,
        1
    )
    sys.exit(0)


# ---------- MAIN ----------
def main():
    app = QApplication(sys.argv)
    app.setApplicationName("USB NOVA")
    app.setQuitOnLastWindowClosed(True)
    app.setStyleSheet(DARK_THEME)

    # ---- ADMIN PROMPT ----
    if not is_admin():
        msg = QMessageBox()
        msg.setWindowTitle("Administrator Privileges Required")
        msg.setText(
            "USB NOVA requires administrator privileges to manage USB devices.\n\n"
            "Restart with administrator access?"
        )
        msg.setIcon(QMessageBox.Warning)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.Yes)
        msg.setWindowFlag(Qt.WindowStaysOnTopHint)

        if msg.exec() == QMessageBox.Yes:
            relaunch_as_admin()

        sys.exit(0)

    # ---- SPLASH ----
    splash = NovaSplash(dark=True)
    splash.show()
    app.processEvents()

    splash.set_status("Loading core modules…")
    app.processEvents()

    splash.set_status("Detecting USB devices…")
    app.processEvents()

    # ---- MAIN WINDOW ----
    window = MainWindow()

    splash.set_status("Initializing interface…")
    app.processEvents()

    window.show()
    splash.finish(window)

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
