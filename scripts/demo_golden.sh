#!/bin/sh
# Run from the repository root with Python 3.12, dependencies and both images ready.
set -eu
demo_output="${1:-artifacts/golden-demo}"
if [ "$#" -gt 0 ]; then shift; fi
exec "${PYTHON:-python3}" scripts/run_pipeline.py --project golden_ledger --output "$demo_output" "$@"
