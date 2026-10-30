# HTTP Security Header Analyzer

A simple Python tool that analyzes HTTP security headers for a specified URL and reports which headers are present or missing.

## Features

- Accepts a target URL from the user.
- Automatically adds `https://` if no HTTP scheme is provided.
- Checks eight common HTTP security headers.
- Displays the values of headers that are present.
- Identifies missing security headers.
- Shows the HTTP status code and final URL after redirects.
- Handles common errors, including connection failures, timeouts, and SSL certificate verification errors.
- Provides a summary of present and missing headers.

## Requirements

- Python 3.8 or later.
- Internet connection.
- The `requests` Python library.

## Installation

Download `http-security-header-analyzer.py` to your local machine, then install the required dependency:

```bash
python -m pip install requests
```

## Usage

Run the script using:

```bash
python http-security-header-analyzer.py
```

Enter the target URL when prompted.

Example:

```text
HTTP Security Header Analyzer
-----------------------------
Enter target URL: https://example.com
```

The tool will send an HTTP GET request and analyze the security headers returned in the final HTTP response.

## Security Headers Checked

| Header | Purpose |
|---|---|
| Content-Security-Policy | Helps mitigate content injection and cross-site scripting (XSS). |
| Strict-Transport-Security | Instructs browsers to use HTTPS for future connections. |
| X-Content-Type-Options | Helps prevent MIME type sniffing. |
| X-Frame-Options | Helps protect against clickjacking. |
| Referrer-Policy | Controls the referrer information sent with requests. |
| Permissions-Policy | Controls access to browser features and APIs. |
| Cross-Origin-Opener-Policy | Helps isolate browsing contexts from cross-origin documents. |
| Cross-Origin-Resource-Policy | Controls which origins can load a resource. |

## Example Output

```text
========== Scan Results ==========
Final URL: https://example.com/
HTTP Status Code: 200

[+] Content-Security-Policy: Present
    Value: default-src 'self'

[-] Strict-Transport-Security: Missing
    Purpose: Tells browsers to use HTTPS for future connections.

========== Summary ==========
Present headers: 1
Missing headers: 7
Total checked: 8
```

*Note: This is an illustrative example. Actual results depend on the target server's HTTP response.*

## Limitations

- Analyzes the HTTP response for one specified URL only.
- Does not crawl the website or scan all its pages.
- Does not authenticate to pages that require a login.
- Does not perform a comprehensive vulnerability assessment.
- A missing header does not automatically mean that the website is vulnerable.
- Header recommendations depend on the application's architecture and security requirements.
