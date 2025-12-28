# Pendrive Manager (USB Nova)

**Version:** 1.0  
**Prepared By:** B-Acharekar [https://github.com/B-Acharekar]  
**Date:** [28-12-2025]  

---

## 1. Introduction

Pendrive Manager is a native Windows desktop utility designed to manage USB / pendrive devices safely and efficiently. The application focuses on low-level disk operations such as detection, formatting, speed testing, and health analysis while maintaining strict safety controls.  

This tool is intended for:
- Developers
- Testers
- Project stakeholders
- Future contributors

---

## 2. Features

### USB Device Detection
- Detects all removable USB storage devices connected to the system.
- Ignores internal HDD/SSD drives.

### Device Information Display
- Displays drive letter, capacity, file system, and manufacturer details.
- Presents devices in a clean, minimal futuristic UI.

### USB Formatting
- Allows formatting in FAT32, exFAT, and NTFS.
- Supports quick and full format options.
- Safety confirmation before any destructive operation.

### Speed Testing
- Performs sequential read and write speed tests.
- Displays results in MB/s via bar graphs.

### Health Check
- Scans for basic read/write errors.
- Warns the user if reliability is low.
- Displays health as a progress bar.

### UI / UX
- Minimal futuristic UI with monochrome theme.
- Side panel for USB devices and main panel for controls, stats, and graphs.
- Supports light/dark theme toggle.

---

## 3. Installation

### Requirements
- Windows 10 or higher
- Python 3.11+
- PySide6
- Required modules listed in `requirements.txt`

### Installation Steps
1. Clone the repository:
    ```bash
    git clone https://github.com/B-Acharekar/PendriveManager.git
    cd PendriveManager
    ```
2. Create a virtual environment:
    ```bash
    python -m venv venv
    source venv/Scripts/activate
    ```
3. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4. Run the application:
    ```bash
    python main.py
    ```

---

## 4. Usage

1. Launch the application (requires admin privileges for formatting).
2. Select a USB device from the sidebar.
3. Use the controls to:
    - Format the drive
    - Run speed tests
    - Check device health
4. View results in charts or progress bars.
5. Toggle between dark/light theme using the theme button.

---

## 5. Project Structure

````

pendrive-manager/
│
├── core/               # Core functionality (formatting, speed test, health check, device detection)
├── ui/                 # UI components (main window, sidebar, themes)
├── main.py             # Entry point of the application
├── requirements.txt    # Python dependencies
└── README.md

````
---

## 6. Functional Requirements (FR)

- **FR-1:** USB Device Detection
- **FR-2:** Device Information Display
- **FR-3:** USB Formatting
- **FR-4:** Speed Testing
- **FR-5:** Health Check
- **FR-6:** Safety Confirmation (multiple confirmations before destructive actions)

---

## 7. Future Enhancements
- Add detailed device manufacturer info.
- Add historical log of tests and format actions.
- Export speed/health results to CSV or PDF.
- More granular safety checks before formatting (like Rufus).

---

## 8. Contact
For issues, contributions, or feature requests, please open a GitHub issue.
