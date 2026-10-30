import ipaddress
import pandas as pd
from urllib.parse import urlsplit

INPUT_FILE = "urls.txt"
OUTPUT_FILE = "results.csv"

SUSPICIOUS_KEYWORDS = [
    "login",
    "verify",
    "secure",
    "security",
    "account",
    "update",
    "password",
    "admin",
    "signin",
    "confirm",
    "banking",
    "payment"
]

SUSPICIOUS_TLDS = {
    "xyz", "top", "tk", "ml", "ga", "cf", "gq", "click"
}


def extract_features(url):
    features = {
        "url_length": len(url),
        "dot_count": 0,
        "subdomain_count": 0,
        "contains_at": False,
        "contains_hyphen": False,
        "is_ip_address": False,
        "uses_https": False,
        "has_suspicious_keyword": False,
        "has_suspicious_tld": False,
        "is_valid_url": False
    }

    try:
        parsed = urlsplit(url)

        if parsed.scheme.lower() not in ("http", "https"):
            raise ValueError

        if not parsed.hostname:
            raise ValueError

        hostname = parsed.hostname.lower()
        domain_parts = hostname.split(".")

        try:
            ipaddress.ip_address(hostname)
            is_ip = True
        except ValueError:
            is_ip = False

        features["dot_count"] = hostname.count(".")
        features["subdomain_count"] = (
            max(0, len(domain_parts) - 2) if not is_ip else 0
        )
        features["contains_at"] = "@" in parsed.netloc
        features["contains_hyphen"] = "-" in hostname
        features["is_ip_address"] = is_ip
        features["uses_https"] = parsed.scheme.lower() == "https"

        suspicious_text = (
            hostname + parsed.path + parsed.query
        ).lower()

        features["has_suspicious_keyword"] = any(
            keyword in suspicious_text
            for keyword in SUSPICIOUS_KEYWORDS
        )

        features["has_suspicious_tld"] = (
            domain_parts[-1] in SUSPICIOUS_TLDS
            if not is_ip and len(domain_parts) > 1
            else False
        )

        features["is_valid_url"] = True

    except ValueError:
        features["is_valid_url"] = False

    return features


def calculate_risk(features):
    score = 0

    if not features["is_valid_url"]:
        return score, "Invalid"

    if features["url_length"] > 75:
        score += 1

    if features["dot_count"] > 3:
        score += 1

    if features["subdomain_count"] > 2:
        score += 1

    if features["contains_at"]:
        score += 2

    indicators = [
        "contains_hyphen",
        "is_ip_address",
        "has_suspicious_keyword",
        "has_suspicious_tld"
    ]

    for indicator in indicators:
        if features[indicator]:
            score += 1

    if not features["uses_https"]:
        score += 1

    combined_risk = (
        (features["has_suspicious_keyword"] and
         features["has_suspicious_tld"])
        or
        (features["is_ip_address"] and
         features["has_suspicious_keyword"])
        or
        (features["contains_at"] and
         features["has_suspicious_keyword"])
    )

    if combined_risk:
        score += 2

    if score <= 2:
        risk_level = "Low"
    elif score <= 5:
        risk_level = "Medium"
    else:
        risk_level = "High"

    return score, risk_level


def analyze_urls(urls):
    results = []

    for url in urls:
        features = extract_features(url)
        score, risk_level = calculate_risk(features)

        results.append({
            "url": url,
            **features,
            "risk_score": score,
            "risk_level": risk_level
        })

    return pd.DataFrame(results)


def print_summary(df):
    print("\n" + "=" * 50)
    print("          URL RISK ANALYSIS SUMMARY")
    print("=" * 50)

    print(f"\nTotal URLs analyzed: {len(df)}")

    print("\nRisk Classification:")

    risk_counts = df["risk_level"].value_counts()

    for level in ["Low", "Medium", "High", "Invalid"]:
        print(f"{level}: {risk_counts.get(level, 0)}")

    valid_urls = df[df["is_valid_url"]]

    if not valid_urls.empty:
        print(
            f"\nAverage URL length: "
            f"{valid_urls['url_length'].mean():.2f}"
        )

        feature_columns = [
            "contains_at",
            "contains_hyphen",
            "is_ip_address",
            "has_suspicious_keyword",
            "has_suspicious_tld"
        ]

        feature_counts = valid_urls[feature_columns].sum()

        max_count = feature_counts.max()

        if max_count > 0:
            print("\nMost common suspicious feature(s):")

            for feature, count in feature_counts.items():
                if count == max_count:
                    print(f"{feature}: {count}")
        else:
            print("\nNo suspicious features detected.")

    print("\n" + "=" * 50)


def main():
    try:
        with open(INPUT_FILE, "r", encoding="utf-8") as file:
            urls = [
                line.strip()
                for line in file
                if line.strip()
            ]

        if not urls:
            print("Error: No URLs found in urls.txt.")
            return

        df = analyze_urls(urls)

        df.to_csv(
            OUTPUT_FILE,
            index=False,
            encoding="utf-8-sig"
        )

        print_summary(df)

        print(f"\nResults saved successfully to {OUTPUT_FILE}")

    except FileNotFoundError:
        print(f"Error: {INPUT_FILE} was not found.")

    except PermissionError:
        print("Error: Permission denied while accessing a file.")


if __name__ == "__main__":
    main()
