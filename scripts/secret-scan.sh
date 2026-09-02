#!/usr/bin/env bash
set -euo pipefail

# Scan all Git-tracked files against the committed baseline.
# Fails when a newly detected secret is not already represented in the baseline.
git ls-files -z | xargs -0 --no-run-if-empty detect-secrets-hook --baseline .secrets.baseline
