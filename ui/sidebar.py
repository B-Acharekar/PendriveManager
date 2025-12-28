# ui/sidebar.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QListWidget
from PySide6.QtCore import Signal, Qt

class Sidebar(QWidget):
    device_selected = Signal(object)

    def __init__(self):
        super().__init__()
        self.setFixedWidth(260)

        title = QLabel("Devices")
        title.setAlignment(Qt.AlignLeft)
        title.setStyleSheet("font-weight:700; padding:10px;")

        self.list = QListWidget()
        self.list.itemClicked.connect(self._clicked)

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(8)
        layout.addWidget(title)
        layout.addWidget(self.list)

        self.setLayout(layout)
        self.devices = []

    def set_devices(self, devices):
        self.devices = devices
        self.list.clear()
        for d in devices:
            self.list.addItem(
                f"{d.drive_letter}  |  {d.label}  |  {d.size_gb}GB"
            )

    def _clicked(self, item):
        idx = self.list.row(item)
        if 0 <= idx < len(self.devices):
            self.device_selected.emit(self.devices[idx])
