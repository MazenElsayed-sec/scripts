# Host Discovery Tool

A lightweight Bash script for checking whether hosts respond to ICMP ping requests. It supports scanning a single host, multiple hosts, or a list of hosts provided in a text file.

## Features

- Check a single IP address or hostname.
- Check multiple hosts in one command.
- Read hosts from a text file.
- Display the status of each host.
- Save scan results to an output file.
- Display a summary of scan results.
- Handle missing files, invalid arguments, and common errors.
- Skip blank lines and comment lines in host lists.

## Requirements

- Linux operating system.
- Bash shell.
- `ping` command installed and available in your `PATH`.

## Installation

Clone the repository:

```bash
git clone <repository-url>
```

Navigate to the project directory:

```bash
cd <repository-directory>
```

Make the script executable:

```bash
chmod +x host_discovery.sh
```

## Usage

### 1. Display Help

```bash
./host_discovery.sh -h
```

Displays the available options and usage examples.

### 2. Scan a Single Host

```bash
./host_discovery.sh 192.168.1.1
```

You can also use a hostname:

```bash
./host_discovery.sh example.com
```

### 3. Scan Multiple Hosts

Provide multiple IP addresses or hostnames as arguments:

```bash
./host_discovery.sh 192.168.1.1 192.168.1.10 example.com
```

The tool checks each host individually and displays its result.

### 4. Scan Hosts from a File

Create a file named `hosts.txt`:

```text
192.168.1.1
192.168.1.10
192.168.1.20
example.com
# This is a comment
```

Run the tool:

```bash
./host_discovery.sh -f hosts.txt
```

Each host must be placed on a separate line. Blank lines and lines beginning with `#` are ignored.

### 5. Save Results to a File

To save the results of a host list scan:

```bash
./host_discovery.sh -f hosts.txt -o results.txt
```

You can also save results when scanning individual hosts:

```bash
./host_discovery.sh -o results.txt 192.168.1.1 192.168.1.10
```

The output file is created if it does not exist. If it already exists, its previous contents are overwritten.

## Example Output

```text
================================
       Host Discovery Tool
================================
Total hosts to check: 3
Ping attempts per host: 1
Timeout: 2s
--------------------------------
[+] 192.168.1.1 : ALIVE
[-] 192.168.1.10 : NO RESPONSE
[+] example.com : ALIVE
--------------------------------
Scan completed.
Total hosts: 3
Alive: 2
No response: 1
Errors: 0
================================
```

*The output above is an example. Actual results depend on network conditions and host configuration.*

## Status Definitions

| Status | Description |
|---|---|
| `ALIVE` | The host responded to the ping request. |
| `NO RESPONSE` | The host did not respond successfully within the configured timeout. |
| `ERROR` | The tool encountered an invalid host entry or another reported error. |

## How It Works

1. Parses command-line arguments to identify hosts, input files, and output files.
2. Loads hosts from the specified file when file mode is used.
3. Skips blank lines and comments in the host list.
4. Sends an ICMP ping request to each host.
5. Displays whether each host responded.
6. Tracks the results and prints a summary after the scan.
7. Optionally saves the displayed results to a file.

## Limitations

- The tool relies on ICMP ping responses to determine host availability.
- A host may be online but report `NO RESPONSE` if ICMP traffic is blocked by a firewall or network configuration.
- `ALIVE` indicates a successful ping response; it does not confirm that a particular service or port is available.
- The script performs one ping attempt per host by default.
- The scan is sequential, so hosts are checked one at a time.

