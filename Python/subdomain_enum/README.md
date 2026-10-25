# Python Scripts

A collection of Python scripts for cybersecurity, automation, and utility tasks.

## Scripts

### 1. Subdomain Enumeration (`subdomain_enum.py`)

**Description**

A passive subdomain enumeration tool that retrieves potential subdomains from publicly available certificate records using [crt.sh](https://crt.sh/).

**Features**
- Retrieves subdomain names from public certificate data.
- Removes duplicate results.
- Sorts results alphabetically.
- Saves results to a text file when requested.

**Requirements**
- Python 3.9 or later
- Internet connection

**Usage**

Run the script:

```bash
python subdomain_enum.py example.com
```

Save results to a file:

```bash
python subdomain_enum.py example.com -o results.txt
```

Display help:

```bash
python subdomain_enum.py --help
```

**Limitations**

Results depend on publicly available certificate records and may not include every subdomain. The tool does not check whether discovered subdomains are currently active.

**Disclaimer:** Only use this tool on domains you own or have permission to assess.
