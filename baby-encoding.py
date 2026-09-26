#!/usr/bin/env python3

import base64
from urllib.parse import quote, unquote
import codecs
import string


text = input("Input: ")

print("\n========== RESULTS ==========")

# Detect input type
detected = "Text"
data = text.encode("utf-8")

try:
    if text.startswith(("0b", "0B")):
        data = int(text, 2).to_bytes(
            max(1, (int(text, 2).bit_length() + 7) // 8), "big"
        )
        detected = "Binary"

    elif all(c in "01" for c in text.replace(" ", "")) and text.strip():
        binary = text.replace(" ", "")
        if len(binary) % 8 == 0:
            data = bytes(
                int(binary[i:i + 8], 2)
                for i in range(0, len(binary), 8)
            )
            detected = "Binary"

    elif all(c in string.hexdigits for c in text) and len(text) % 2 == 0:
        data = bytes.fromhex(text)
        detected = "Hex"

    elif all(c.isdigit() or c.isspace() for c in text) and " " in text:
        values = [int(x) for x in text.split()]
        if all(0 <= x <= 255 for x in values):
            data = bytes(values)
            detected = "Decimal"

    else:
        try:
            decoded = base64.b64decode(text, validate=True)
            if decoded:
                data = decoded
                detected = "Base64"
        except ValueError:
            pass

        if detected == "Text":
            try:
                decoded = base64.b32decode(text, casefold=True)
                if decoded:
                    data = decoded
                    detected = "Base32"
            except Exception:
                pass

        if detected == "Text":
            decoded = unquote(text)
            if decoded != text:
                data = decoded.encode("utf-8")
                detected = "URL"

except (ValueError, OverflowError):
    pass


# Original / decoded text
try:
    decoded_text = data.decode("utf-8")
except UnicodeDecodeError:
    decoded_text = data.decode("latin-1")

print("Detected: ", detected)
print("Text:     ", decoded_text)

# Bytes
print("Bytes:    ", data)

# Length
print("Length:   ", len(data), "bytes")

# ASCII / Decimal
print("Decimal:  ", " ".join(str(b) for b in data))

# Hex
print("Hex:      ", data.hex())

# Binary
print("Binary:   ", " ".join(format(b, "08b") for b in data))

# Integer
print("Integer:  ", int.from_bytes(data, "big"))

# Base64
print("Base64:   ", base64.b64encode(data).decode())

# Base32
print("Base32:   ", base64.b32encode(data).decode())

# Base85
print("Base85:   ", base64.b85encode(data).decode())

# URL encoding
print("URL:      ", quote(decoded_text))

# ROT13
print("ROT13:    ", codecs.encode(decoded_text, "rot_13"))

print("============================")

