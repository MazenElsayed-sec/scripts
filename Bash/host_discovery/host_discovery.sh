#!/usr/bin/env bash

set -u

TIMEOUT=2
COUNT=1
OUTPUT_FILE=""
HOST_FILE=""
HOSTS=()

ALIVE=0
NO_RESPONSE=0
ERRORS=0

usage() {
    echo "Usage:"
    echo "  $0 <host> [host2 ...]"
    echo "  $0 -f <hosts_file> [-o <output_file>]"
    echo "  $0 -o <output_file> <host> [host2 ...]"
    echo "  $0 -h"
}

show_help() {
    echo "Host Discovery Tool"
    echo
    echo "Options:"
    echo "  -f <file>   Read hosts from a file"
    echo "  -o <file>   Save results to a file"
    echo "  -h          Display help"
    echo
    echo "Examples:"
    echo "  $0 192.168.1.1"
    echo "  $0 192.168.1.1 192.168.1.10"
    echo "  $0 -f hosts.txt"
    echo "  $0 -f hosts.txt -o results.txt"
}

log() {
    printf '%s\n' "$1"

    if [[ -n "$OUTPUT_FILE" ]]; then
        if ! printf '%s\n' "$1" >> "$OUTPUT_FILE"; then
            echo "[ERROR] Could not write to output file." >&2
            exit 1
        fi
    fi
}

if ! command -v ping >/dev/null 2>&1; then
    echo "[ERROR] The 'ping' command is not installed." >&2
    exit 1
fi

while [[ $# -gt 0 ]]; do
    case "$1" in
        -f)
            if [[ $# -lt 2 || -z "$2" ]]; then
                echo "[ERROR] Missing hosts file after -f." >&2
                usage
                exit 1
            fi
            HOST_FILE="$2"
            shift 2
            ;;
        -o)
            if [[ $# -lt 2 || -z "$2" ]]; then
                echo "[ERROR] Missing output file after -o." >&2
                usage
                exit 1
            fi
            OUTPUT_FILE="$2"
            shift 2
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        -*)
            echo "[ERROR] Unknown option: $1" >&2
            usage
            exit 1
            ;;
        *)
            HOSTS+=("$1")
            shift
            ;;
    esac
done

if [[ -n "$HOST_FILE" ]]; then
    if [[ ! -f "$HOST_FILE" || ! -r "$HOST_FILE" ]]; then
        echo "[ERROR] Hosts file does not exist or is not readable: $HOST_FILE" >&2
        exit 1
    fi

    while IFS= read -r line || [[ -n "$line" ]]; do
        line="${line#"${line%%[![:space:]]*}"}"
        line="${line%"${line##*[![:space:]]}"}"

        [[ -z "$line" || "$line" == \#* ]] && continue

        HOSTS+=("$line")
    done < "$HOST_FILE"
fi

if [[ ${#HOSTS[@]} -eq 0 ]]; then
    echo "[ERROR] No hosts provided." >&2
    usage
    exit 1
fi

if [[ -n "$OUTPUT_FILE" ]]; then
    if [[ -d "$OUTPUT_FILE" ]]; then
        echo "[ERROR] Output path is a directory." >&2
        exit 1
    fi

    if ! : > "$OUTPUT_FILE"; then
        echo "[ERROR] Cannot create or write to output file: $OUTPUT_FILE" >&2
        exit 1
    fi
fi

log "================================"
log "       Host Discovery Tool"
log "================================"
log "Total hosts to check: ${#HOSTS[@]}"
log "Ping attempts per host: $COUNT"
log "Timeout: ${TIMEOUT}s"
log "--------------------------------"

for host in "${HOSTS[@]}"; do
    if [[ -z "$host" || "$host" =~ [[:space:]] ]]; then
        log "[ERROR] Invalid host entry: $host"
        ((ERRORS+=1))
        continue
    fi

    ping -n -c "$COUNT" -W "$TIMEOUT" "$host" >/dev/null 2>&1
    ping_status=$?

    case "$ping_status" in
        0)
            log "[+] $host : ALIVE"
            ((ALIVE+=1))
            ;;
        1)
            log "[-] $host : NO RESPONSE"
            ((NO_RESPONSE+=1))
            ;;
        *)
            log "[ERROR] $host : PING FAILED (exit code: $ping_status)"
            ((ERRORS+=1))
            ;;
    esac
done

log "--------------------------------"
log "Scan completed."
log "Total hosts: ${#HOSTS[@]}"
log "Alive: $ALIVE"
log "No response: $NO_RESPONSE"
log "Errors: $ERRORS"
log "================================"
