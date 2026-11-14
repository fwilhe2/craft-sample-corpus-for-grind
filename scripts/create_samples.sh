#!/usr/bin/env bash
set -euo pipefail
exec python3 "$(dirname "$0")/create_samples.py" "${1:-samples/compatibility}"