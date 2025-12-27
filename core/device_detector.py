import win32api
import win32file
import win32con

from core.models import USBDevice


def get_removable_devices():
    devices = []

    drives = win32api.GetLogicalDriveStrings().split('\x00')
    for drive in drives:
        if not drive:
            continue

        try:
            drive_type = win32file.GetDriveType(drive)
            if drive_type != win32file.DRIVE_REMOVABLE:
                continue

            volume_info = win32api.GetVolumeInformation(drive)
            label = volume_info[0]
            filesystem = volume_info[4]

            free, total, _ = win32api.GetDiskFreeSpaceEx(drive)
            size_gb = round(total / (1024 ** 3), 2)

            devices.append(
                USBDevice(
                    drive_letter=drive,
                    label=label,
                    size_gb=size_gb,
                    filesystem=filesystem
                )
            )

        except Exception:
            # ignore inaccessible drives
            continue

    return devices
