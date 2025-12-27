from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout,
    QPushButton, QListWidget, QLabel
)

from core.device_detector import get_removable_devices

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Pendrive Manager")
        self.setMinimumSize(600, 400)

        self.list_widget = QListWidget()
        self.refresh_btn = QPushButton("Refresh Devices")
        self.status_label = QLabel("Ready")
        self.format_btn = QPushButton("Format Drive")

        layout = QVBoxLayout()
        layout.addWidget(self.list_widget)
        layout.addWidget(self.refresh_btn)
        layout.addWidget(self.status_label)
        layout.addWidget(self.format_btn)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)
        self.format_btn.clicked.connect(self.format_selected)

        self.refresh_btn.clicked.connect(self.load_devices)
        self.load_devices()

    def load_devices(self):
        self.list_widget.clear()
        devices = get_removable_devices()

        if not devices:
            self.status_label.setText("No USB devices detected")
            return

        for dev in devices:
            self.list_widget.addItem(
                f"{dev.drive_letter}  |  {dev.label}  |  {dev.size_gb} GB  |  {dev.filesystem}"
            )

        self.status_label.setText(f"{len(devices)} device(s) detected")

    def format_selected(self):
        selected = self.list_widget.currentItem()
        if not selected:
            self.status_label.setText("Select a device first")
            return

        drive_letter = selected.text().split("|")[0].strip()
        # Ask for quick/full, filesystem via dialog (later)
        try:
            from core.formatter import format_usb_device 
            format_usb_device(
                drive_letter,
                filesystem="FAT32",   # later allow selection via dialog
                quick_format=True      # later allow quick/full choice
            )
            self.status_label.setText(f"{drive_letter} formatted successfully")
            self.load_devices()
        except Exception as e:
            self.status_label.setText(f"Error: {e}")
