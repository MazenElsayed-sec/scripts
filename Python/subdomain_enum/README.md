# Subdomain Enumeration Tool

A Python-based passive subdomain enumeration tool that retrieves potential subdomains from publicly available certificate records using [crt.sh](https://crt.sh/).

## Features

- Retrieves subdomain names from public certificate records.
- Removes duplicate results.
- Displays results in alphabetical order.
- Saves discovered subdomains to a text file.
- Uses Python's built-in libraries without requiring external packages.

## Requirements

- Python 3.9 or later
- Internet connection

## Installation

Clone the repository or download `subdomain_enum.py` to your local machine.

No additional Python packages are required.

## Usage

### 1. Enumerate Subdomains

Run the script with a target domain:

```bash
python subdomain_enum.py example.com
```

Replace `example.com` with the domain you are authorized to assess.

### 2. Save Results to a File

Use the `-o` or `--output` option:

```bash
python subdomain_enum.py example.com -o results.txt
```

The results will be saved to `results.txt`.

### 3. Display Help

View the available arguments and options:

```bash
python subdomain_enum.py --help
```

## How It Works

1. Accepts a target domain as a command-line argument.
2. Queries crt.sh for publicly available certificate records associated with the domain.
3. Extracts matching subdomain names.
4. Removes duplicate entries and sorts the results.
5. Prints the discovered subdomains and optionally saves them to a file.

## Limitations

- Results depend on publicly available certificate records.
- Some subdomains may not appear in the results.
- The tool does not verify whether discovered subdomains are currently active.

