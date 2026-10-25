import argparse
import time
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen


def parse_args():
    parser = argparse.ArgumentParser(
        description="Basic directory and path discovery tool."
    )

    parser.add_argument(
        "-u", "--url",
        required=True,
        help="Base URL to scan (e.g. http://127.0.0.1:8000)"
    )

    parser.add_argument(
        "-w", "--wordlist",
        required=True,
        help="Path to a wordlist file"
    )

    parser.add_argument(
        "-o", "--output",
        help="Save results to a file"
    )

    parser.add_argument(
        "--timeout",
        type=float,
        default=5.0,
        help="Request timeout in seconds (default: 5)"
    )

    return parser.parse_args()


def validate_url(url):
    parsed = urlparse(url)

    if parsed.scheme not in ("http", "https") or not parsed.netloc:
        raise ValueError("Please provide a valid HTTP or HTTPS URL.")

    if parsed.username or parsed.password:
        raise ValueError("URLs containing credentials are not supported.")

    return url if url.endswith("/") else url + "/"


def load_wordlist(path):
    wordlist_path = Path(path)

    if not wordlist_path.is_file():
        raise FileNotFoundError(
            f"Wordlist file not found: {wordlist_path}"
        )

    with wordlist_path.open("r", encoding="utf-8-sig") as file:
        words = [
            line.strip()
            for line in file
            if line.strip() and not line.lstrip().startswith("#")
        ]

    if not words:
        raise ValueError("The wordlist is empty.")

    return words


def check_path(url, timeout):
    request = Request(
        url,
        headers={"User-Agent": "BasicDirectoryScanner/1.0"}
    )

    try:
        with urlopen(request, timeout=timeout) as response:
            return response.status, None

    except HTTPError as error:
        # HTTP errors such as 403 and 404 are valid scan results.
        return error.code, None

    except (URLError, TimeoutError, OSError) as error:
        return None, str(error)


def main():
    args = parse_args()
    start_time = time.time()

    try:
        base_url = validate_url(args.url)

        if args.timeout <= 0:
            raise ValueError("Timeout must be greater than zero.")

        words = load_wordlist(args.wordlist)

    except (ValueError, FileNotFoundError, OSError) as error:
        print(f"[!] Error: {error}")
        return 1

    results = []
    errors = 0

    print(f"[*] Target: {base_url}")
    print(f"[*] Wordlist entries: {len(words)}")
    print("[*] Starting scan...\n")

    for word in words:
        # Ignore absolute URLs and restrict entries to simple paths.
        path = word.lstrip("/")

        if (
            not path
            or "://" in path
            or "?" in path
            or "#" in path
            or "\\" in path
            or any(part == ".." for part in path.split("/"))
        ):
            print(f"[!] Skipping invalid path: {word}")
            continue

        target_url = urljoin(base_url, path)

        status, error = check_path(target_url, args.timeout)

        if error:
            errors += 1
            print(f"[!] Connection error: {target_url} ({error})")
            continue

        result = f"[{status}] {target_url}"
        print(result)
        results.append(result)

    elapsed = time.time() - start_time

    print("\n[*] Scan completed.")
    print(f"[*] Responses: {len(results)}")
    print(f"[*] Connection errors: {errors}")
    print(f"[*] Elapsed time: {elapsed:.2f} seconds")

    if args.output:
        try:
            output_path = Path(args.output)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_text(
                "\n".join(results) + ("\n" if results else ""),
                encoding="utf-8"
            )
            print(f"[*] Results saved to: {output_path}")

        except OSError as error:
            print(f"[!] Could not save results: {error}")
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
