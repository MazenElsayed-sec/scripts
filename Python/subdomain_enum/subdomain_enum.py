import argparse
import json
import urllib.error
import urllib.parse
import urllib.request


def enumerate_subdomains(domain):
    url = (
        "https://crt.sh/?q="
        + urllib.parse.quote(f"%.{domain}")
        + "&output=json"
    )

    request = urllib.request.Request(
        url,
        headers={"User-Agent": "SubdomainEnum/1.0"}
    )

    try:
        with urllib.request.urlopen(request, timeout=20) as response:
            data = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError) as error:
        print(f"[!] Request failed: {error}")
        return set()

    subdomains = set()

    for entry in data:
        for name in entry.get("name_value", "").splitlines():
            name = name.strip().lower().removeprefix("*.")

            if name == domain or name.endswith("." + domain):
                subdomains.add(name)

    return subdomains


def main():
    parser = argparse.ArgumentParser(
        description="Discover subdomains using public certificate data."
    )
    parser.add_argument("domain", help="Domain you are authorized to assess")
    parser.add_argument("-o", "--output", help="Save results to a text file")
    args = parser.parse_args()

    domain = args.domain.strip().lower().rstrip(".")

    if not domain or "." not in domain or any(c.isspace() for c in domain):
        parser.error("Please provide a valid domain name.")

    print(f"[*] Enumerating subdomains for: {domain}")
    results = enumerate_subdomains(domain)

    for subdomain in sorted(results):
        print(subdomain)

    print(f"\n[+] Found {len(results)} unique subdomains.")

    if args.output:
        with open(args.output, "w", encoding="utf-8") as file:
            file.write("\n".join(sorted(results)))
            if results:
                file.write("\n")
        print(f"[+] Results saved to {args.output}")


if __name__ == "__main__":
    main()
