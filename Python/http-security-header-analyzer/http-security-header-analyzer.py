import sys
from urllib.parse import urlparse

import requests


SECURITY_HEADERS = {
    "Content-Security-Policy": (
        "Helps protect against content injection and XSS."
    ),
    "Strict-Transport-Security": (
        "Tells browsers to use HTTPS for future connections."
    ),
    "X-Content-Type-Options": (
        "Helps prevent MIME type sniffing."
    ),
    "X-Frame-Options": (
        "Helps protect against clickjacking."
    ),
    "Referrer-Policy": (
        "Controls how much referrer information is shared."
    ),
    "Permissions-Policy": (
        "Controls access to browser features and APIs."
    ),
    "Cross-Origin-Opener-Policy": (
        "Helps isolate a browsing context from cross-origin windows."
    ),
    "Cross-Origin-Resource-Policy": (
        "Controls which origins can load a resource."
    ),
}


def get_target_url():
    url = input("Enter target URL: ").strip()

    if not url:
        raise ValueError("URL cannot be empty.")

    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed_url = urlparse(url)

    if (
        parsed_url.scheme not in ("http", "https")
        or not parsed_url.hostname
        or parsed_url.username
        or parsed_url.password
    ):
        raise ValueError("Please enter a valid HTTP or HTTPS URL.")

    return url


def fetch_response(url):
    try:
        response = requests.get(
            url,
            timeout=10,
            allow_redirects=True,
            headers={"User-Agent": "HTTP-Security-Header-Analyzer/1.0"},
        )
        return response

    except requests.exceptions.SSLError:
        print("[!] SSL certificate verification failed.")
    except requests.exceptions.Timeout:
        print("[!] Request timed out.")
    except requests.exceptions.ConnectionError:
        print("[!] Could not connect to the target.")
    except requests.exceptions.RequestException as error:
        print(f"[!] Request failed: {error}")

    return None


def analyze_headers(response):
    response_headers = {
        name.lower(): value
        for name, value in response.headers.items()
    }

    print("\n========== Scan Results ==========")
    print(f"Final URL: {response.url}")
    print(f"HTTP Status Code: {response.status_code}")

    present_count = 0
    missing_count = 0

    for header, description in SECURITY_HEADERS.items():
        value = response_headers.get(header.lower())

        if value:
            present_count += 1
            print(f"\n[+] {header}: Present")
            print(f"    Value: {value}")
        else:
            missing_count += 1
            print(f"\n[-] {header}: Missing")

        print(f"    Purpose: {description}")

    print("\n========== Summary ==========")
    print(f"Present headers: {present_count}")
    print(f"Missing headers: {missing_count}")
    print(f"Total checked: {len(SECURITY_HEADERS)}")


def main():
    print("HTTP Security Header Analyzer")
    print("-----------------------------")

    try:
        target_url = get_target_url()
    except (ValueError, EOFError) as error:
        print(f"[!] Input error: {error}")
        return

    response = fetch_response(target_url)

    if response is None:
        print("[!] Scan could not be completed.")
        return

    try:
        analyze_headers(response)
    finally:
        response.close()


if __name__ == "__main__":
    main()
