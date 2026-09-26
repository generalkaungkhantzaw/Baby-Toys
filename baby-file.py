#!/usr/bin/env python3

import os
import mimetypes
from datetime import datetime


def format_size(size):
    units = ["B", "KB", "MB", "GB", "TB"]

    for unit in units:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024

    return f"{size:.2f} PB"


def get_file_type(filename):
    file_type, encoding = mimetypes.guess_type(filename)

    if file_type:
        return file_type

    return "Unknown"


def main():
    filename = input("Input file: ")

    if not os.path.isfile(filename):
        print("File not found.")
        return

    info = os.stat(filename)

    print("\n========== FILE INFO ==========")

    print("Name:       ", os.path.basename(filename))
    print("Path:       ", os.path.abspath(filename))
    print("Type:       ", get_file_type(filename))
    print("Size:       ", format_size(info.st_size))
    print("Bytes:      ", info.st_size)
    print("Permissions:", oct(info.st_mode & 0o777))
    print("Modified:   ", datetime.fromtimestamp(info.st_mtime))
    print("Accessed:   ", datetime.fromtimestamp(info.st_atime))
    print("Changed:    ", datetime.fromtimestamp(info.st_ctime))

    print("===============================")


if __name__ == "__main__":
    main()
