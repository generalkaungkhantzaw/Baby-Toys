#!/usr/bin/env python3

import os


SIGNATURES = [
    (b"\x89PNG\r\n\x1a\n", "PNG image"),
    (b"\xff\xd8\xff", "JPEG image"),
    (b"GIF87a", "GIF image"),
    (b"GIF89a", "GIF image"),
    (b"%PDF-", "PDF document"),
    (b"PK\x03\x04", "ZIP archive"),
    (b"PK\x05\x06", "ZIP archive"),
    (b"PK\x07\x08", "ZIP archive"),
    (b"\x1f\x8b", "GZIP compressed data"),
    (b"7z\xbc\xaf\x27\x1c", "7-Zip archive"),
    (b"Rar!\x1a\x07\x00", "RAR archive"),
    (b"Rar!\x1a\x07\x01\x00", "RAR archive"),
    (b"\x7fELF", "ELF executable"),
    (b"MZ", "Windows executable"),
    (b"BM", "BMP image"),
    (b"ID3", "MP3 audio"),
    (b"SQLite format 3\x00", "SQLite database"),
]


def detect_type(data):
    for signature, file_type in SIGNATURES:
        if data.startswith(signature):
            return file_type

    if data.startswith(b"RIFF") and len(data) >= 12:
        if data[8:12] == b"WAVE":
            return "WAV audio"

        if data[8:12] == b"AVI ":
            return "AVI video"

        if data[8:12] == b"WEBP":
            return "WebP image"

        return "RIFF container"

    return "Unknown"


def main():
    filename = input("Input file: ")

    if not os.path.isfile(filename):
        print("File not found.")
        return

    try:
        with open(filename, "rb") as file:
            header = file.read(32)
    except PermissionError:
        print("Permission denied.")
        return

    file_size = os.path.getsize(filename)

    print("\n========== MAGIC ==========")
    print("File:     ", filename)
    print("Size:     ", file_size, "bytes")

    if header:
        print("Header:   ", header.hex(" "))
        print("Detected: ", detect_type(header))
    else:
        print("Header:    Empty")
        print("Detected: Empty file")

    print("===========================")


if __name__ == "__main__":
    main()
