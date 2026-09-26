#!/usr/bin/env python3

import json
import re
import sys
import time
from urllib.parse import urlparse, parse_qs

import requests


SECURITY_HEADERS = {
    "strict-transport-security": "HSTS",
    "content-security-policy": "CSP",
    "x-content-type-options": "X-Content-Type-Options",
    "x-frame-options": "X-Frame-Options",
    "referrer-policy": "Referrer-Policy",
    "permissions-policy": "Permissions-Policy",
    "cross-origin-opener-policy": "COOP",
    "cross-origin-resource-policy": "CORP",
}

def parse_key_value(values):
    result = {}

    for value in values or []:
        if "=" not in value:
            print(f"[!] Ignoring invalid value: {value}")
            continue

        key, val = value.split("=", 1)
        result[key.strip()] = val.strip()

    return result


def parse_headers(values):
    return parse_key_value(values)


def parse_cookies(values):
    return parse_key_value(values)


def print_section(title):
    print(f"\n{'─' * 30}")
    print(f" {title}")
    print(f"{'─' * 30}")


def print_headers(headers):
    for key, value in headers.items():
        print(f"{key}: {value}")


def print_request(response):
    request = response.request

    print_section("REQUEST")

    print(f"Method : {request.method}")
    print(f"URL    : {request.url}")

    if request.headers:
        print("\nHeaders:")
        print_headers(request.headers)

    if request.body:
        print("\nBody:")
        body = request.body

        if isinstance(body, bytes):
            body = body.decode("utf-8", errors="replace")

        print(body)


def print_response(response, elapsed):
    print_section("RESPONSE")

    print(f"Status       : {response.status_code} {response.reason}")
    print(f"Final URL    : {response.url}")
    print(f"HTTP Version : {response.raw.version}")
    print(f"Content-Type : {response.headers.get('Content-Type', 'N/A')}")
    print(f"Size         : {len(response.content):,} bytes")
    print(f"Time         : {elapsed:.3f} seconds")


def print_redirects(response):
    if not response.history:
        return

    print_section("REDIRECT CHAIN")

    for index, item in enumerate(response.history, 1):
        location = item.headers.get("Location", "N/A")

        print(
            f"{index}. "
            f"{item.status_code} "
            f"{item.request.method} "
            f"{item.url}"
        )
        print(f"   → {location}")

    print(
        f"{len(response.history) + 1}. "
        f"{response.status_code} "
        f"{response.url}"
    )


def print_cookies(response):
    if not response.cookies:
        return

    print_section("RESPONSE COOKIES")

    for cookie in response.cookies:
        print(f"Name   : {cookie.name}")
        print(f"Value  : {cookie.value}")
        print(f"Domain : {cookie.domain or 'N/A'}")
        print(f"Path   : {cookie.path or 'N/A'}")
        print()


def analyze_security_headers(response):
    print_section("SECURITY HEADERS")

    for header, name in SECURITY_HEADERS.items():
        value = response.headers.get(header)

        if value:
            print(f"[+] {name}")
            print(f"    {value}")
        else:
            print(f"[-] {name}: not present")


def extract_html_title(text):
    match = re.search(
        r"<title[^>]*>(.*?)</title>",
        text,
        re.IGNORECASE | re.DOTALL,
    )

    if not match:
        return None

    return re.sub(r"\s+", " ", match.group(1)).strip()


def show_response_body(response, limit):
    print_section("RESPONSE BODY")

    content_type = response.headers.get("Content-Type", "").lower()

    text = response.text

    if "application/json" in content_type:
        try:
            parsed = response.json()
            text = json.dumps(parsed, indent=2, ensure_ascii=False)
        except ValueError:
            pass

    elif "text/html" in content_type:
        title = extract_html_title(text)

        if title:
            print(f"HTML Title: {title}\n")

    if len(text) > limit:
        print(text[:limit])
        print(f"\n... [{len(text) - limit:,} more characters]")
    else:
        print(text)


def show_url_info(url):
    parsed = urlparse(url)

    print_section("URL INFORMATION")

    print(f"Scheme   : {parsed.scheme}")
    print(f"Host     : {parsed.hostname or 'N/A'}")
    print(f"Port     : {parsed.port or 'default'}")
    print(f"Path     : {parsed.path or '/'}")
    print(f"Query    : {parsed.query or 'N/A'}")
    print(f"Fragment : {parsed.fragment or 'N/A'}")

    if parsed.query:
        print("\nQuery Parameters:")

        for key, values in parse_qs(parsed.query).items():
            for value in values:
                print(f"  {key} = {value}")


def send_request(args):
    headers = parse_headers(args.header)
    cookies = parse_cookies(args.cookie)

    if args.user_agent:
        headers["User-Agent"] = args.user_agent

    data = args.data

    if args.json:
        try:
            data = json.loads(args.json)
        except json.JSONDecodeError as e:
            print(f"[!] Invalid JSON: {e}")
            sys.exit(1)

    session = requests.Session()

    if args.auth:
        username, password = args.auth.split(":", 1)
        session.auth = (username, password)

    try:
        start = time.perf_counter()

        response = session.request(
            method=args.method,
            url=args.url,
            headers=headers,
            cookies=cookies,
            data=data,
            allow_redirects=args.follow,
            timeout=args.timeout,
            verify=not args.insecure,
        )

        elapsed = time.perf_counter() - start

    except requests.exceptions.SSLError:
        print("[!] TLS/SSL verification failed.")
        print("[!] Use --insecure only when you understand why.")
        sys.exit(1)

    except requests.exceptions.Timeout:
        print("[!] Request timed out.")
        sys.exit(1)

    except requests.exceptions.ConnectionError as e:
        print(f"[!] Connection failed: {e}")
        sys.exit(1)

    except requests.exceptions.RequestException as e:
        print(f"[!] Request failed: {e}")
        sys.exit(1)

    show_url_info(args.url)
    print_request(response)
    print_response(response, elapsed)

    if response.history:
        print_redirects(response)

    print_cookies(response)
    analyze_security_headers(response)

    if not args.no_body and args.method != "HEAD":
        show_response_body(response, args.max_body)


def main():

    url = input("URL: ").strip()

    if not url:
        print("[!] URL cannot be empty.")
        return

    class Args:
        pass

    args = Args()
    args.url = url
    args.method = "GET"
    args.header = []
    args.cookie = []
    args.user_agent = None
    args.data = None
    args.json = None
    args.auth = None
    args.follow = True
    args.insecure = False
    args.timeout = 10
    args.max_body = 5000
    args.no_body = False

    send_request(args)


if __name__ == "__main__":
    main()
