#!/usr/bin/env python3

import base64
import json
import time


def decode_base64url(value):
    padding = "=" * (-len(value) % 4)

    try:
        return base64.urlsafe_b64decode(value + padding)
    except Exception:
        return None


def decode_json(value):
    data = decode_base64url(value)

    if data is None:
        return None

    try:
        return json.loads(data.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError):
        return None


def print_json(title, data):
    print(f"\n---------- {title} ----------")

    if data is None:
        print("Invalid or undecodable.")
        return

    print(json.dumps(data, indent=2))


def show_claims(payload):
    if not isinstance(payload, dict):
        return

    print("\n---------- CLAIMS ----------")

    for name, value in payload.items():
        print(f"{name:8} {value}")

    if "exp" in payload:
        try:
            expires = int(payload["exp"])
            current = int(time.time())

            if expires < current:
                print("Status:   Expired")
            else:
                print("Status:   Not expired")
        except (ValueError, TypeError):
            print("Status:   Invalid exp claim")


def main():
    token = input("JWT: ").strip()

    parts = token.split(".")

    print("\n========== JWT TOOL ==========")
    print("Parts:     ", len(parts))

    if len(parts) != 3:
        print("Status:     Invalid JWT structure")
        print("Expected:   HEADER.PAYLOAD.SIGNATURE")
        print("==============================")
        return

    header_part, payload_part, signature_part = parts

    header = decode_json(header_part)
    payload = decode_json(payload_part)
    signature = decode_base64url(signature_part)

    print("Structure:  Header.Payload.Signature")

    print_json("HEADER", header)
    print_json("PAYLOAD", payload)

    print("\n---------- SIGNATURE ----------")

    if signature is None:
        print("Invalid or undecodable.")
    elif not signature:
        print("Empty signature.")
    else:
        print("Bytes:      ", len(signature))
        print("Hex:        ", signature.hex())

    show_claims(payload)

    print("\n---------- INFORMATION ----------")

    if isinstance(header, dict):
        print("Algorithm:  ", header.get("alg", "Unknown"))
        print("Type:       ", header.get("typ", "Unknown"))
        print("Key ID:     ", header.get("kid", "None"))

    print("================================")


if __name__ == "__main__":
    main()
