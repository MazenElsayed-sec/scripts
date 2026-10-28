#!/usr/bin/env bash

set -o pipefail

if [[ $# -lt 1 || $# -gt 2 ]]; then
    echo "Usage: $0 <log_file> [output_file]"
    exit 1
fi

LOG_FILE="$1"
OUTPUT_FILE="${2:-log_analysis.txt}"

if [[ ! -f "$LOG_FILE" ]]; then
    echo "Error: Log file does not exist."
    exit 1
fi

if [[ ! -r "$LOG_FILE" ]]; then
    echo "Error: Log file is not readable."
    exit 1
fi

if [[ -e "$OUTPUT_FILE" && ! -w "$OUTPUT_FILE" ]]; then
    echo "Error: Output file is not writable."
    exit 1
fi

if [[ ! -e "$OUTPUT_FILE" ]]; then
    OUTPUT_DIR="$(dirname -- "$OUTPUT_FILE")"

    if [[ ! -d "$OUTPUT_DIR" || ! -w "$OUTPUT_DIR" ]]; then
        echo "Error: Output directory is not writable."
        exit 1
    fi
fi

TOTAL_LINES=$(wc -l < "$LOG_FILE")
FAILED_COUNT=$(grep -Eic 'failed password|authentication failure|failed login|invalid user' "$LOG_FILE" || true)

{
    echo "========== Linux Log Analyzer =========="
    echo "Log File: $LOG_FILE"
    echo "Analysis Date: $(date)"
    echo "Total Log Lines: $TOTAL_LINES"
    echo "Failed Login Events: $FAILED_COUNT"
    echo
    echo "========== Failed Login Events =========="

    grep -Ein 'failed password|authentication failure|failed login|invalid user' "$LOG_FILE" || true

    echo
    echo "========== Frequent Source IPs =========="

    grep -Ei 'failed password|authentication failure|failed login|invalid user' "$LOG_FILE" |
        grep -Eo '([0-9]{1,3}\.){3}[0-9]{1,3}' |
        sort |
        uniq -c |
        sort -nr || true

} > "$OUTPUT_FILE"

if [[ $? -ne 0 ]]; then
    echo "Error: Failed to write analysis results."
    exit 1
fi

echo "Analysis completed successfully."
echo "Total Log Lines: $TOTAL_LINES"
echo "Failed Login Events: $FAILED_COUNT"
echo "Results saved to: $OUTPUT_FILE"
