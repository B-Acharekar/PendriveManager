from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QComboBox,
    QCheckBox, QMessageBox, QProgressBar
)
from PySide6.QtCharts import QChart, QChartView, QBarSeries, QBarSet, QValueAxis
from PySide6.QtGui import QPainter
from PySide6.QtCore import Qt, QThread, Signal
from PySide6.QtWidgets import QApplication

from ui.sidebar import Sidebar
from ui.theme import DARK_THEME, LIGHT_THEME

from core.device_detector import get_removable_devices
from core.formatter import format_usb_device
from core.speed_test import write_speed_test, read_speed_test
from core.health_check import check_usb_health


# ---------- THREADS ----------
class SpeedThread(QThread):
    done = Signal(float, float)

    def __init__(self, drive):
        super().__init__()
        self.drive = drive

    def run(self):
        self.done.emit(
            write_speed_test(self.drive),
            read_speed_test(self.drive)
        )


class HealthThread(QThread):
    done = Signal(dict)

    def __init__(self, drive):
        super().__init__()
        self.drive = drive

    def run(self):
        self.done.emit(check_usb_health(self.drive))


# ---------- MAIN ----------
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("USB NOVA")
        self.resize(960, 560)

        self.dark_mode = True
        self.current_device = None

        # ===== SIDEBAR =====
        self.sidebar = Sidebar()
        self.sidebar.device_selected.connect(self.on_device_selected)

        # ===== HEADER =====
        title = QLabel("USB NOVA")
        title.setStyleSheet("font-size:18px;font-weight:700;")

        subtitle = QLabel("Pendrive Manager")
        subtitle.setObjectName("Subtitle")

        self.theme_btn = QPushButton("🌙")
        self.theme_btn.setFixedWidth(36)
        self.theme_btn.clicked.connect(self.toggle_theme)

        self.refresh_btn = QPushButton("↻")
        self.refresh_btn.setFixedWidth(36)
        self.refresh_btn.clicked.connect(self.refresh_devices)

        header_row = QHBoxLayout()
        header_row.addWidget(title)
        header_row.addStretch()
        header_row.addWidget(self.refresh_btn)
        header_row.addWidget(self.theme_btn)

        header = QVBoxLayout()
        header.addLayout(header_row)
        header.addWidget(subtitle)

        # ===== CONTROLS =====
        self.fs = QComboBox()
        self.fs.addItems(["FAT32", "exFAT", "NTFS"])

        self.quick = QCheckBox("Quick")

        self.btn_format = QPushButton("Format")
        self.btn_speed = QPushButton("Speed")
        self.btn_health = QPushButton("Health")

        controls = QHBoxLayout()
        controls.addWidget(self.fs)
        controls.addWidget(self.quick)
        controls.addStretch()
        controls.addWidget(self.btn_format)
        controls.addWidget(self.btn_speed)
        controls.addWidget(self.btn_health)

        # ===== HEALTH =====
        self.health = QProgressBar()
        self.health.setFixedHeight(18)
        self.health.setFormat("Health —")

        # ===== CHART =====
        self.chart = QChart()
        self.chart.setBackgroundBrush(Qt.transparent)
        self.chart.legend().setVisible(False)

        self.chart_view = QChartView(self.chart)
        self.chart_view.setRenderHint(QPainter.Antialiasing)

        # ===== STATUS =====
        self.status = QLabel("Ready")
        self.status.setObjectName("StatusLabel")

        # ===== MAIN PANEL =====
        panel = QVBoxLayout()
        panel.setContentsMargins(10, 10, 10, 10)
        panel.setSpacing(8)
        panel.addLayout(header)
        panel.addLayout(controls)
        panel.addWidget(self.health)
        panel.addWidget(self.chart_view)
        panel.addWidget(self.status)

        panel_widget = QWidget()
        panel_widget.setLayout(panel)

        root = QHBoxLayout()
        root.addWidget(self.sidebar)
        root.addWidget(panel_widget, 1)

        container = QWidget()
        container.setLayout(root)
        self.setCentralWidget(container)

        # ===== SIGNALS =====
        self.btn_format.clicked.connect(self.format_drive)
        self.btn_speed.clicked.connect(self.speed_test)
        self.btn_health.clicked.connect(self.health_check)

        # ===== INIT =====
        QApplication.instance().setStyleSheet(DARK_THEME)
        self.refresh_devices()

    # ---------- DEVICE ----------
    def refresh_devices(self):
        devices = get_removable_devices()
        self.sidebar.set_devices(devices)
        self.status.setText(f"{len(devices)} device(s) detected")

    def on_device_selected(self, device):
        self.current_device = device
        self.health.setValue(0)
        self.health.setFormat("Health —")
        self.chart.removeAllSeries()
        self.status.setText(f"Selected {device.drive_letter}")

    # ---------- ACTIONS ----------
    def format_drive(self):
        if not self.current_device:
            return
        d = self.current_device.drive_letter
        if QMessageBox.question(self, "Confirm", f"Format {d}?") != QMessageBox.Yes:
            return
        format_usb_device(d, self.fs.currentText(), self.quick.isChecked())
        self.refresh_devices()

    def speed_test(self):
        if not self.current_device:
            return
        self.chart.removeAllSeries()
        self.status.setText("Testing speed...")
        self.t = SpeedThread(self.current_device.drive_letter)
        self.t.done.connect(self.update_chart)
        self.t.start()

    def update_chart(self, w, r):
        s = QBarSeries()
        ws = QBarSet("Write"); ws.append(w)
        rs = QBarSet("Read"); rs.append(r)
        s.append(ws); s.append(rs)
        self.chart.addSeries(s)

        ax = QValueAxis()
        ax.setRange(0, max(w, r) * 1.2)
        self.chart.setAxisY(ax, s)
        self.status.setText(f"W {w:.1f} MB/s | R {r:.1f} MB/s")

    def health_check(self):
        if not self.current_device:
            return
        self.status.setText("Checking health...")
        self.h = HealthThread(self.current_device.drive_letter)
        self.h.done.connect(self.update_health)
        self.h.start()

    def update_health(self, r):
        pct = int(r.get("percentage", -1))
        if pct >= 0:
            self.health.setValue(pct)
            self.health.setFormat(f"Health {pct}%")
        else:
            self.health.setFormat("Health Unknown")

        self.status.setText(r.get("status", "Unknown"))

    # ---------- THEME ----------
    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        QApplication.instance().setStyleSheet(
            DARK_THEME if self.dark_mode else LIGHT_THEME
        )
        self.theme_btn.setText("🌙" if self.dark_mode else "☀️")
