#!/usr/bin/env python3

import hashlib
import re


algorithms = [
    "md5",
    "sha1",
    "sha224",
    "sha256",
    "sha384",
    "sha512",
    "sha3_224",
    "sha3_256",
    "sha3_384",
    "sha3_512",
    "blake2b",
    "blake2s",
]


hash_lengths = {
    32: ["MD5"],
    40: ["SHA-1"],
    56: ["SHA-224"],
    64: ["SHA-256", "SHA3-256", "BLAKE2s"],
    96: ["SHA-384", "SHA3-384"],
    128: ["SHA-512", "SHA3-512", "BLAKE2b"],
}


def identify(value):
    value = value.strip()

    if re.fullmatch(r"[0-9a-fA-F]+", value):
        return hash_lengths.get(len(value), ["Hexadecimal string"])

    patterns = {
        r"\$2[aby]\$\d{2}\$[./A-Za-z0-9]{53}": ["bcrypt"],
        r"\$1\$[^$]+\$[./A-Za-z0-9]{22}": ["MD5-crypt"],
        r"\$5\$[^$]+\$[./A-Za-z0-9]{43}": ["SHA-256 crypt"],
        r"\$6\$[^$]+\$[./A-Za-z0-9]{86}": ["SHA-512 crypt"],
    }

    for pattern, name in patterns.items():
        if re.fullmatch(pattern, value):
            return name

    return []


def main():
    text = input("Input: ")
    matches = identify(text)

    print("\n========== HASH TOOL ==========")
    print("Input:   ", text)
    print("Length:  ", len(text), "characters")

    print("\n---------- IDENTIFICATION ----------")

    if matches:
        print("Detected:", ", ".join(matches))
    else:
        data = text.encode("utf-8")

        print("Detected: Unknown")

        print("\n------------- HASHES ---------------")
        print("Bytes:   ", data)
        print("Length:  ", len(data), "bytes")

        for algorithm in algorithms:
            digest = hashlib.new(algorithm, data).hexdigest()
            print(f"{algorithm.upper():10} {digest}")

if __name__ == "__main__":
    main()
