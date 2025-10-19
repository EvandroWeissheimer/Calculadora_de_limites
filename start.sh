#!/usr/bin/env bash
set -euo pipefail

# If a virtualenv exists in .venv, activate it
if [ -f .venv/bin/activate ]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
fi

python3 main.py
