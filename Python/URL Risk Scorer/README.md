# URL Risk Scorer

A Python-based cybersecurity tool that extracts features from URLs, assigns heuristic risk scores, and classifies URLs into different risk levels.

## Project Overview

URLs are commonly used in phishing attacks to deceive users and redirect them to potentially malicious websites.

**URL Risk Scorer** is a lightweight defensive security tool designed to identify suspicious URL characteristics using a predefined rule-based scoring system.

The tool analyzes URL structures without visiting websites or making network requests.

It supports analyzing a single URL or multiple URLs through an input file.

## Features

- URL length analysis.
- Domain dot count analysis.
- Subdomain count analysis.
- Detection of the `@` symbol.
- Detection of hyphens in hostnames.
- IP address detection.
- HTTPS usage detection.
- Suspicious keyword detection.
- Suspicious Top-Level Domain (TLD) detection.
- Basic URL validation.
- Rule-based risk scoring.
- Risk classification: Low, Medium, High, and Invalid.
- CSV report generation.
- Statistical summary using Pandas.

## How It Works

The tool processes each URL through the following steps:

1. **Input:** Reads URLs from `urls.txt`.
2. **Feature Extraction:** Extracts relevant characteristics from each URL.
3. **Risk Scoring:** Assigns points based on predefined suspicious indicators.
4. **Risk Classification:** Categorizes each URL according to its calculated score.
5. **Data Analysis:** Uses Pandas to organize and summarize the results.
6. **Report Generation:** Saves the analysis results in `results.csv`.

## Risk Scoring System

| Indicator | Risk Points |
|---|---:|
| URL length greater than 75 characters | +1 |
| More than 3 dots in hostname | +1 |
| More than 2 subdomains | +1 |
| Contains `@` in network location | +2 |
| Contains a hyphen in hostname | +1 |
| Uses an IP address as hostname | +1 |
| Contains suspicious keywords | +1 |
| Uses a listed suspicious TLD | +1 |
| Does not use HTTPS | +1 |
| Certain combinations of suspicious indicators | +2 |

The combined risk bonus is applied when one of these conditions is met:

- Suspicious keyword and suspicious TLD are both detected.
- An IP address and suspicious keyword are both detected.
- The `@` symbol and suspicious keyword are both detected.

### Risk Classification

| Risk Score | Risk Level |
|---|---|
| 0–2 | Low |
| 3–5 | Medium |
| 6 or more | High |
| Invalid URL | Invalid |

These classifications are heuristic assessments and do not confirm whether a URL is malicious or safe.

## Requirements

- Python 3
- Pandas

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/MazenElsayed-sec/scripts.git
```

### 2. Navigate to the Project Directory

```bash
cd scripts/Python/url-risk-scorer
```

### 3. Install Dependencies

```bash
py -m pip install -r requirements.txt
```

## Usage

### 1. Prepare the Input File

Open `urls.txt` and add the URLs you want to analyze.

Each URL must be placed on a separate line.

**Example: Analyzing a Single URL**

```text
https://secure-verify-account.example.xyz
```

**Example: Analyzing Multiple URLs**

```text
https://www.google.com
https://github.com
http://192.168.1.5/login
https://secure-verify-account.example.xyz
http://admin-login.example.top
```

The tool analyzes all non-empty lines in the input file.

### 2. Run the Tool

From the project directory, execute:

```bash
py url_risk_scorer.py
```

### 3. View the Results

After execution, the tool displays a statistical summary in the terminal and generates a `results.csv` file containing the analysis results.

## Example Output

The following output is from a sample execution using 28 test URLs:

```text
==================================================
          URL RISK ANALYSIS SUMMARY
==================================================

Total URLs analyzed: 28

Risk Classification:
Low: 13
Medium: 9
High: 6
Invalid: 0

Average URL length: 32.57

Most common suspicious feature(s):
has_suspicious_keyword: 17

==================================================

Results saved successfully to results.csv
```

## Output File

The tool generates a CSV report named `results.csv`.

The report contains the following columns:

| Column | Description |
|---|---|
| url | Original URL |
| url_length | Total URL length |
| dot_count | Number of dots in the hostname |
| subdomain_count | Estimated number of subdomains |
| contains_at | Whether the network location contains `@` |
| contains_hyphen | Whether the hostname contains a hyphen |
| is_ip_address | Whether the hostname is an IP address |
| uses_https | Whether the URL uses HTTPS |
| has_suspicious_keyword | Whether suspicious keywords were detected |
| has_suspicious_tld | Whether the hostname uses a listed suspicious TLD |
| is_valid_url | Basic URL validation result |
| risk_score | Calculated risk score |
| risk_level | Final risk classification |

## Project Structure

```text
url-risk-scorer/
│
├── README.md
├── url_risk_scorer.py
├── urls.txt
├── requirements.txt
└── results.csv
```

`results.csv` is generated automatically when the tool runs.

## Technologies Used

- **Python:** Main programming language.
- **Pandas:** Data organization, statistical analysis, and CSV generation.
- **urllib.parse:** URL parsing.
- **ipaddress:** IP address identification.

## Limitations

- The tool uses heuristic rules rather than Machine Learning.
- It does not visit websites or send network requests.
- It does not analyze website content.
- It does not perform DNS, WHOIS, or domain reputation checks.
- It does not inspect redirects or TLS certificates.
- Suspicious keywords and TLD lists are predefined and may produce false positives.
- The absence of HTTPS does not necessarily mean a website is malicious.
- Basic URL validation does not guarantee that a URL is reachable or fully conforms to every URL specification.
- A low-risk result does not guarantee that a URL is safe.

The tool is intended for educational purposes and preliminary URL risk assessment. It should not replace professional phishing detection or threat intelligence solutions.

## Test Data

The project includes a sample dataset of 28 manually selected URLs for testing different URL characteristics and risk indicators.

Some URLs use example domains and private IP addresses to demonstrate the tool's behavior.

The sample classifications are illustrative and do not establish that any tested URL is malicious.

## Author

**Mazen Elsayed**

GitHub: [MazenElsayed-sec](https://github.com/MazenElsayed-sec)
