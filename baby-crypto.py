#!/usr/bin/env python3

import base64
import hashlib
import hmac
import secrets


HASHES = [
    "md5",
    "sha1",
    "sha224",
    "sha256",
    "sha384",
    "sha512",
]


def hash_data(data):
    print("\n---------- HASHING ----------")

    for algorithm in HASHES:
        digest = hashlib.new(algorithm, data).hexdigest()
        print(f"{algorithm.upper():8} {digest}")


def hmac_data(data, key):
    print("\n---------- HMAC ----------")

    for algorithm in ["sha256", "sha512"]:
        mac = hmac.new(
            key,
            data,
            getattr(hashlib, algorithm),
        ).hexdigest()

        print(f"HMAC-{algorithm.upper()}: {mac}")


def xor_data(data, key):
    return bytes(
        byte ^ key[i % len(key)]
        for i, byte in enumerate(data)
    )


def base64_data(data):
    print("\n---------- BASE64 ----------")

    standard = base64.b64encode(data)
    url_safe = base64.urlsafe_b64encode(data)

    print("Encoded:     ", standard.decode())
    print("URL-safe:    ", url_safe.decode())

    decoded = base64.b64decode(standard)

    print("Decoded:     ", decoded.decode("utf-8", errors="replace"))


def random_data():
    print("\n---------- RANDOM ----------")

    random_bytes = secrets.token_bytes(16)

    print("Random bytes:", random_bytes.hex())
    print("Random hex:  ", secrets.token_hex(16))
    print("Random URL:  ", secrets.token_urlsafe(16))


def xor_demo(data):
    print("\n---------- XOR ----------")

    key = secrets.token_bytes(1)
    encrypted = xor_data(data, key)
    decrypted = xor_data(encrypted, key)

    print("Key:         ", key.hex())
    print("XOR result:  ", encrypted.hex())
    print("Recovered:   ", decrypted.decode("utf-8", errors="replace"))


def compare_demo(data, key):
    print("\n---------- HMAC CHECK ----------")

    correct = hmac.new(
        key,
        data,
        hashlib.sha256,
    ).digest()

    test = hmac.new(
        key,
        data,
        hashlib.sha256,
    ).digest()

    print("Valid:       ", hmac.compare_digest(correct, test))


def main():
    text = input("Input: ")

    if not text:
        print("Input cannot be empty.")
        return

    data = text.encode("utf-8")
    key = secrets.token_bytes(32)

    print("\n========== CRYPTO ==========")
    print("Input:       ", text)
    print("Bytes:       ", len(data))

    hash_data(data)
    hmac_data(data, key)
    base64_data(data)
    random_data()
    xor_demo(data)
    compare_demo(data, key)

    print("==============================")


if __name__ == "__main__":
    main()
