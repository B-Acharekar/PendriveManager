import os
import time

TEST_FILE_NAME = "__speed_test.bin"
TEST_FILE_SIZE_MB = 256
BLOCK_SIZE_MB = 4

def write_speed_test(drive_letter):
    path = os.path.join(drive_letter, TEST_FILE_NAME)
    block = b"\0" * (BLOCK_SIZE_MB * 1024 * 1024)

    total_bytes = TEST_FILE_SIZE_MB * 1024 * 1024
    written_bytes = 0

    start_time = time.time()
    with open(path, "wb", buffering=0) as f:
        while written_bytes < total_bytes:
            f.write(block)
            written_bytes += len(block)
            f.flush()
            os.fsync(f.fileno())
    end_time = time.time()

    mb_per_sec = TEST_FILE_SIZE_MB / (end_time - start_time)
    return round(mb_per_sec, 2)

def read_speed_test(drive_letter):
    path = os.path.join(drive_letter, TEST_FILE_NAME)
    block_size = BLOCK_SIZE_MB * 1024 * 1024

    total_bytes = TEST_FILE_SIZE_MB * 1024 * 1024
    read_bytes = 0

    start_time = time.time()
    with open(path, "rb", buffering=0) as f:
        while read_bytes < total_bytes:
            data = f.read(block_size)
            if not data:
                break
            read_bytes += len(data)
    end_time = time.time()

    mb_per_sec = TEST_FILE_SIZE_MB / (end_time - start_time)
    os.remove(path)
    return round(mb_per_sec, 2)