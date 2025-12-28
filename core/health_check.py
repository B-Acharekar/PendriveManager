import os

TEST_FILE_NAME = "__health_check.bin"
TEST_SIZE_MB = 32
BLOCK_SIZE_MB = 4

def check_usb_health(drive_letter):
    path = os.path.join(drive_letter, TEST_FILE_NAME)
    block = b"\xAA" * (BLOCK_SIZE_MB * 1024 * 1024)
    errors = 0

    # Write test
    try:
        with open(path, "wb", buffering=0) as f:
            for _ in range(TEST_SIZE_MB // BLOCK_SIZE_MB):
                f.write(block)
                f.flush()
                os.fsync(f.fileno())
    except IOError:
        errors += 1

    # Read test
    try:
        with open(path, "rb", buffering=0) as f:
            for _ in range(TEST_SIZE_MB // BLOCK_SIZE_MB):
                data = f.read(BLOCK_SIZE_MB * 1024 * 1024)
                if data != block:
                    errors += 1
    except IOError:
        errors += 1

    # Cleanup
    if os.path.exists(path):
        os.remove(path)

    status = "OK" if errors == 0 else "WARN"
    message = "Drive looks healthy" if status == "OK" else "Drive may be unreliable"
    return {"status": status, "errors": errors, "message": message}
