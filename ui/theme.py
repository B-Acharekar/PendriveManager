# ui/theme.py

DARK_THEME = """
QWidget {
    background-color: #0d1117;
    color: #e6edf3;
    font-family: Segoe UI;
    font-size: 12px;
}

QLabel {
    color: #e6edf3;
}

QLabel#Subtitle {
    color: #8b949e;
    font-size: 11px;
}

QLabel#StatusLabel {
    color: #58a6ff;
    font-size: 11px;
}

QListWidget {
    background: #161b22;
    border-radius: 6px;
}

QListWidget::item {
    padding: 6px;
}

QListWidget::item:selected {
    background: #1f6feb;
    color: white;
}

QPushButton {
    background: #21262d;
    border-radius: 6px;
    padding: 6px 10px;
    font-weight: 600;
}

QPushButton:hover {
    background: #30363d;
}

QComboBox {
    background: #161b22;
    border-radius: 6px;
    padding: 4px;
}

QProgressBar {
    background: #161b22;
    border-radius: 6px;
    text-align: center;
    font-size: 11px;
}

QProgressBar::chunk {
    background: #39c5bb;
    border-radius: 6px;
}
"""


LIGHT_THEME = """
QWidget {
    background-color: #f4f6f8;
    color: #111;
    font-family: Segoe UI;
    font-size: 12px;
}

QLabel {
    color: #111;
}

QLabel#Subtitle {
    color: #555;
    font-size: 11px;
}

QLabel#StatusLabel {
    color: #2563eb;
    font-size: 11px;
}

QListWidget {
    background: #ffffff;
    border-radius: 6px;
}

QListWidget::item {
    padding: 6px;
}

QListWidget::item:selected {
    background: #0066cc;
    color: white;
}

QPushButton {
    background: #e5e7eb;
    border-radius: 6px;
    padding: 6px 10px;
    font-weight: 600;
}

QPushButton:hover {
    background: #d1d5db;
}

QComboBox {
    background: #ffffff;
    border-radius: 6px;
    padding: 4px;
}

QProgressBar {
    background: #e5e7eb;
    border-radius: 6px;
    text-align: center;
    font-size: 11px;
}

QProgressBar::chunk {
    background: #2563eb;
    border-radius: 6px;
}
"""
