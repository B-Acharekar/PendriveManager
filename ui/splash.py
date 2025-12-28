# ui/splash.py

from PySide6.QtWidgets import QSplashScreen, QLabel, QVBoxLayout, QWidget
from PySide6.QtGui import QPixmap, QFont, QPainter
from PySide6.QtCore import Qt, QPropertyAnimation


class NovaSplash(QSplashScreen):
    def __init__(self, dark=True):
        pix = QPixmap(440, 260)
        pix.fill(Qt.transparent)
        super().__init__(pix)

        self.setWindowFlags(
            Qt.SplashScreen |
            Qt.FramelessWindowHint |
            Qt.WindowStaysOnTopHint
        )

        # ---- Colors ----
        self.bg = "#0d1117" if dark else "#f4f6f8"
        self.fg = "#e6edf3" if dark else "#111"
        self.sub = "#8b949e" if dark else "#555"

        # ---- Central Widget ----
        w = QWidget(self)
        w.setGeometry(0, 0, 440, 260)
        w.setStyleSheet(f"""
            QWidget {{
                background:{self.bg};
                border-radius:16px;
            }}
        """)

        layout = QVBoxLayout(w)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        layout.addStretch()

        # ---- Title ----
        self.title = QLabel("USB NOVA")
        self.title.setFont(QFont("Segoe UI", 30, QFont.Bold))
        self.title.setAlignment(Qt.AlignCenter)
        self.title.setStyleSheet(f"color:{self.fg};")

        # ---- Subtitle ----
        self.subtitle = QLabel("Initializing device engine…")
        self.subtitle.setFont(QFont("Segoe UI", 11))
        self.subtitle.setAlignment(Qt.AlignCenter)
        self.subtitle.setStyleSheet(f"color:{self.sub};")

        layout.addWidget(self.title)
        layout.addWidget(self.subtitle)
        layout.addStretch()

        # ---- Fade In ----
        self.setWindowOpacity(0.0)
        self.fade_in = QPropertyAnimation(self, b"windowOpacity")
        self.fade_in.setDuration(450)
        self.fade_in.setStartValue(0.0)
        self.fade_in.setEndValue(1.0)
        self.fade_in.start()

        self._main_window = None

    # ---------- Public API ----------
    def set_status(self, text: str):
        self.subtitle.setText(text)

    def finish(self, main_window):
        self._main_window = main_window

        self.fade_out = QPropertyAnimation(self, b"windowOpacity")
        self.fade_out.setDuration(300)
        self.fade_out.setStartValue(1.0)
        self.fade_out.setEndValue(0.0)
        self.fade_out.finished.connect(self._on_fade_out_finished)
        self.fade_out.start()

    def _on_fade_out_finished(self):
        # Explicit base class call (SAFE)
        QSplashScreen.finish(self, self._main_window)

    # ---------- Rounded Mask ----------
    def drawContents(self, painter: QPainter):
        painter.setRenderHint(QPainter.Antialiasing)
