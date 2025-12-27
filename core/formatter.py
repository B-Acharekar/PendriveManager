import subprocess
import ctypes
from core.device_detector import get_removable_devices

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def format_usb_device(drive_letter, filesystem="FAT32", quick_format=True):
    # Remove trailing backslash
    drive_letter = drive_letter.rstrip("\\")
    
    # Safety check
    removable = [d.drive_letter.rstrip("\\") for d in get_removable_devices()]
    if drive_letter not in removable:
        raise ValueError(f"Drive {drive_letter} is not a removable USB device.")
    if not is_admin():
        raise PermissionError("Administrator privileges are required to format a USB device.")

    fs_map = {"FAT32": "FAT32", "NTFS": "NTFS", "exFAT": "exFAT"}
    if filesystem not in fs_map:
        raise ValueError(f"Unsupported filesystem: {filesystem}. Supported: {list(fs_map.keys())}")

    quick_flag = "/Q" if quick_format else ""
    # /X forces dismount if needed
    cmd = f'format {drive_letter} /FS:{fs_map[filesystem]} {quick_flag} /V:NewUSB /Y /X'
    
    print("Running command:", cmd)  # debug
    subprocess.run(cmd, shell=True, check=True)
    return True
