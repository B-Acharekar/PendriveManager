class USBDevice:
    def __init__(self,drive_letter,label,size_gb,filesystem):
        self.drive_letter = drive_letter
        self.label = label
        self.size_gb = size_gb
        self.filesystem = filesystem
    
    def __repr__(self):
        return f"USBDevice(drive_letter={self.drive_letter}, label={self.label}, size_gb={self.size_gb}, filesystem={self.filesystem})"