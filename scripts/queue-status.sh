#!/usr/bin/env bash
set -euo pipefail

queue_dir=".queue"

while [[ $# -gt 0 ]]; do
    case "$1" in
        --dir)
            if [[ $# -lt 2 ]]; then
                echo "error: --dir requires a path argument" >&2
                exit 1
            fi
            queue_dir="$2"
            shift 2
            ;;
        --dir=*)
            queue_dir="${1#--dir=}"
            shift
            ;;
        -h|--help)
            cat <<'USAGE'
Usage: queue-status.sh [--dir <path>]

Prints a read-only summary of every task JSON across the four queue
subdirectories: pending, in-progress, done, failed.

Options:
  --dir <path>   Queue root directory (default: .queue/)
  -h, --help     Show this help and exit
USAGE
            exit 0
            ;;
        *)
            echo "error: unknown argument: $1" >&2
            exit 1
            ;;
    esac
done

if [[ ! -d "$queue_dir" ]]; then
    echo "error: queue root not found: $queue_dir" >&2
    exit 1
fi

if ! command -v jq >/dev/null 2>&1; then
    echo "error: jq is required but was not found in PATH" >&2
    exit 1
fi

print_section() {
    local label="$1"
    local subdir="$2"
    local path="$queue_dir/$subdir"

    echo "=== $label ==="

    if [[ ! -d "$path" ]]; then
        echo "  (directory missing)"
        echo
        return
    fi

    local found=0
    local file
    for file in "$path"/*.json; do
        [[ -e "$file" ]] || continue
        found=1
        local base id role
        base="$(basename "$file")"
        id="$(jq -r '.id // "<missing>"' "$file" 2>/dev/null || echo "<unreadable>")"
        role="$(jq -r '.role // "<missing>"' "$file" 2>/dev/null || echo "<unreadable>")"
        printf '  %s  id=%s  role=%s\n' "$base" "$id" "$role"
    done

    if [[ "$found" -eq 0 ]]; then
        echo "  (empty)"
    fi
    echo
}

print_section "PENDING"     "pending"
print_section "IN-PROGRESS" "in-progress"
print_section "DONE"        "done"
print_section "FAILED"      "failed"
