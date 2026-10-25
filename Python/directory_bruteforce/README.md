# Directory Brute Force

A basic Python tool for checking paths on an authorized web target using a user-provided wordlist.

## Features

- Sequential path discovery using HTTP requests.
- Displays HTTP status codes for each tested path.
- Saves scan results to an output file.
- Handles HTTP errors, connection failures, and timeouts.
- Uses Python's standard library only.

## Requirements

- Python 3.9 or later recommended.
- A wordlist text file.
- Authorization to test the target.

## Usage

```bash
python directory_bruteforce.py -u http://127.0.0.1:8000 -w wordlist.txt
```

Save results to a file:

```bash
python directory_bruteforce.py -u http://127.0.0.1:8000 -w wordlist.txt -o results.txt
```

Set a custom timeout:

```bash
python directory_bruteforce.py -u http://127.0.0.1:8000 -w wordlist.txt --timeout 10
```

## Wordlist Format

Provide one path per line:

```text
admin
login
robots.txt
uploads
```

Blank lines and lines beginning with `#` are ignored.

## Output

The tool prints the HTTP status code and URL for each successful HTTP response, including HTTP error responses such as `403` and `404`. Connection failures are reported separately.

## Limitations

- Requests are sent sequentially.
- HTTP status codes do not always establish whether a path exists.
- Redirects and application-specific responses may affect results.

