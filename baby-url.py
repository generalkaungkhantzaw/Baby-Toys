#!/usr/bin/env python3

from urllib.parse import (
    urlparse,
    parse_qs,
    unquote,
    quote,
    urlunparse,
)


def show_query(query):
    if not query:
        print("Query:       None")
        return

    print("Query:")

    parameters = parse_qs(query, keep_blank_values=True)

    for key, values in parameters.items():
        for value in values:
            print(f"  {key} = {value}")


def main():
    url = input("Input URL: ").strip()

    if not url:
        print("URL cannot be empty.")
        return

    parsed = urlparse(url)

    print("\n========== URL TOOL ==========")

    print("Original:    ", url)
    print("Scheme:      ", parsed.scheme or "None")
    print("Username:    ", parsed.username or "None")
    print("Password:    ", parsed.password or "None")
    print("Hostname:    ", parsed.hostname or "None")

    try:
        print("Port:        ", parsed.port or "None")
    except ValueError:
        print("Port:         Invalid")

    print("Path:        ", parsed.path or "None")
    print("Parameters:  ", parsed.params or "None")
    print("Fragment:    ", parsed.fragment or "None")

    print("\n---------- QUERY ----------")
    show_query(parsed.query)

    print("\n---------- DECODING ----------")

    decoded_path = unquote(parsed.path)
    decoded_query = unquote(parsed.query)

    print("Decoded path: ", decoded_path)
    print("Decoded query:", decoded_query)

    print("\n---------- ENCODING ----------")

    sample = input("Text to URL-encode (blank = skip): ")

    if sample:
        encoded = quote(sample, safe="")
        print("Encoded:      ", encoded)

    print("\n---------- REBUILD ----------")

    rebuilt = urlunparse(parsed)

    print("Rebuilt URL:  ", rebuilt)

    print("===============================")


if __name__ == "__main__":
    main()
