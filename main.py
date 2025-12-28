import sys
import os
import ctypes
from PySide6.QtWidgets import QApplication, QMessageBox
from ui.main_window import MainWindow


def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def relaunch_as_admin():
    params = " ".join([f'"{arg}"' for arg in sys.argv])
    ctypes.windll.shell32.ShellExecuteW(
        None,
        "runas",
        sys.executable,
        params,
        None,
        1
    )
    sys.exit(0)


if __name__ == "__main__":
    if not is_admin():
        app = QApplication(sys.argv)

        reply = QMessageBox.question(
            None,
            "Administrator Privileges Required",
            "Pendrive Manager requires administrator privileges to manage USB devices.\n\n"
            "Restart with administrator access?",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            relaunch_as_admin()

        sys.exit(0)

    # ---- ADMIN MODE ----
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
