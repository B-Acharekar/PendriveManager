from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QListWidget, QLabel, QComboBox, QCheckBox, QMessageBox
)
from core.device_detector import get_removable_devices
from core.formatter import format_usb_device


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pendrive Manager")
        self.setMinimumSize(700, 450)

        # --- Widgets ---
        self.list_widget = QListWidget()
        self.status_label = QLabel("Ready")

        self.refresh_btn = QPushButton("Refresh Devices")
        self.format_btn = QPushButton("Format Drive")

        self.fs_combo = QComboBox()
        self.fs_combo.addItems(["FAT32", "exFAT", "NTFS"])
        self.quick_checkbox = QCheckBox("Quick Format")
        self.quick_checkbox.setChecked(True)

        # --- Layouts ---
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.list_widget)

        # Bottom controls
        controls_layout = QHBoxLayout()
        controls_layout.addWidget(self.refresh_btn)
        controls_layout.addStretch()
        controls_layout.addWidget(QLabel("FileSystem:"))
        controls_layout.addWidget(self.fs_combo)
        controls_layout.addWidget(self.quick_checkbox)
        controls_layout.addWidget(self.format_btn)
        main_layout.addLayout(controls_layout)

        # Status label at bottom
        main_layout.addWidget(self.status_label)

        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # --- Signals ---
        self.refresh_btn.clicked.connect(self.load_devices)
        self.format_btn.clicked.connect(self.format_selected)

        # Load USBs initially
        self.load_devices()

        # --- Minimal Monochrome Styling ---
        self.setStyleSheet("""
            QWidget {
                font-family: 'Segoe UI', sans-serif;
                font-size: 11pt;
                color: #222222;
                background-color: #F5F5F5;
            }
            QListWidget {
                border: 1px solid #CCCCCC;
                background-color: #FFFFFF;
                selection-background-color: #E0E0E0;
            }
            QPushButton {
                border: 1px solid #AAAAAA;
                padding: 5px 12px;
                background-color: #FFFFFF;
            }
            QPushButton:hover {
                background-color: #F0F0F0;
            }
            QComboBox, QCheckBox {
                background-color: #FFFFFF;
            }
            QLabel {
                padding: 2px;
            }
        """)

    # --- Functions ---
    def load_devices(self):
        self.list_widget.clear()
        devices = get_removable_devices()
        if not devices:
            self.status_label.setText("No USB devices detected")
            return

        for dev in devices:
            self.list_widget.addItem(
                f"{dev.drive_letter} | {dev.label} | {dev.size_gb} GB | {dev.filesystem}"
            )
        self.status_label.setText(f"{len(devices)} device(s) detected")

    def format_selected(self):
        selected = self.list_widget.currentItem()
        if not selected:
            self.status_label.setText("Select a device first")
            return

        drive_letter = selected.text().split("|")[0].strip()
        filesystem = self.fs_combo.currentText()
        quick = self.quick_checkbox.isChecked()

        reply = QMessageBox.question(
            self,
            "Confirm Format",
            f"Are you sure you want to format {drive_letter} as {filesystem}? This will erase all data!",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply != QMessageBox.Yes:
            return

        try:
            format_usb_device(drive_letter, filesystem=filesystem, quick_format=quick)
            self.status_label.setText(f"{drive_letter} formatted successfully")
            self.load_devices()
        except Exception as e:
            self.status_label.setText(f"Error: {e}")
