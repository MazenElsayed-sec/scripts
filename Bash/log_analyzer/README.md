# Linux Log Analyzer

A simple Bash-based cybersecurity tool that analyzes Linux log files to identify potential failed login activity, extract related log events, and summarize frequently occurring source IP addresses.

## Features

- **Log Analysis:** Counts the total number of lines in a log file.
- **Failed Login Detection:** Searches for log entries containing common indicators such as `Failed password`, `authentication failure`, `failed login`, and `invalid user`.
- **Source IP Analysis:** Extracts IPv4-like addresses from matching events and counts their occurrences.
- **Detailed Reports:** Displays matching log entries and frequently occurring source IP addresses.
- **Output File:** Saves the analysis report to a specified file.
- **Input Validation:** Checks whether the input file exists and is readable.
- **Error Handling:** Detects common input and output permission issues.

## Requirements

- Linux operating system
- Bash
- Standard Linux utilities:
  - `grep`
  - `wc`
  - `sort`
  - `uniq`
  - `date`
  - `dirname`

## Installation

Clone the repository:

```bash
git clone <YOUR_REPOSITORY_URL>
```

Navigate to the project directory:

```bash
cd <YOUR_PROJECT_DIRECTORY>
```

Make the script executable:

```bash
chmod +x log_analyzer.sh
```

## Usage

### Basic Usage

Run the tool with a log file:

```bash
./log_analyzer.sh sample.log
```

By default, the report is saved to:

```text
log_analysis.txt
```

### Specify an Output File

Provide a custom output filename:

```bash
./log_analyzer.sh sample.log results.txt
```

The analysis report will be saved to `results.txt`.

## Example Log File

Create a sample log file for testing:

```text
Oct 28 10:01:12 server sshd: Failed password for root from 192.168.1.10 port 2222 ssh2
Oct 28 10:02:15 server sshd: Failed password for admin from 192.168.1.10 port 2223 ssh2
Oct 28 10:03:20 server sshd: Accepted password for user from 192.168.1.20 port 2224 ssh2
Oct 28 10:04:30 server sshd: Invalid user test from 192.168.1.30 port 2225
```

## Example Terminal Output

Running:

```bash
./log_analyzer.sh sample.log
```

Produces output similar to:

```text
Analysis completed successfully.
Total Log Lines: 4
Failed Login Events: 3
Results saved to: log_analysis.txt
```

## Example Report

The generated report will contain sections similar to the following:

```text
========== Linux Log Analyzer ==========
Log File: sample.log
Analysis Date: [Current date and time]
Total Log Lines: 4
Failed Login Events: 3

========== Failed Login Events ==========
1:Oct 28 10:01:12 server sshd: Failed password for root from 192.168.1.10 port 2222 ssh2
2:Oct 28 10:02:15 server sshd: Failed password for admin from 192.168.1.10 port 2223 ssh2
4:Oct 28 10:04:30 server sshd: Invalid user test from 192.168.1.30 port 2225

========== Frequent Source IPs ==========
      2 192.168.1.10
      1 192.168.1.30
```

The line numbers shown above are provided by `grep -n`. The exact report date and time will depend on when the script is executed.

## Error Handling

The tool displays an error and exits when:

- The number of arguments is incorrect.
- The specified log file does not exist.
- The log file cannot be read.
- The output file or its directory is not writable.

Example:

```text
Error: Log file does not exist.
```

## How It Works

1. Validates the command-line arguments.
2. Checks whether the input log file exists and is readable.
3. Validates output file permissions.
4. Counts the total number of log lines.
5. Searches for common failed-login indicators.
6. Extracts IPv4-like addresses from matching entries.
7. Sorts and counts the extracted addresses.
8. Writes the results to the output report.

## Limitations

- Detection relies on predefined text patterns and may miss other authentication failure formats.
- The IP extraction pattern does not validate whether an IPv4 address is mathematically valid.
- The tool does not establish whether a failed login represents a real attack.
- The script analyzes the supplied file only; it does not automatically monitor logs in real time.
- Log formats differ across Linux distributions and authentication services.
