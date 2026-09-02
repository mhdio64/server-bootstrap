#!/usr/bin/env bash
set -euo pipefail

# Scan all Git-tracked files against the committed baseline.
# Fails when a newly detected secret is not already represented in the baseline.
# graphify-out/ is excluded: generated AST/content hashes trigger false positives.
git ls-files -z -- ':!graphify-out' | xargs -0 --no-run-if-empty detect-secrets-hook --baseline .secrets.baseline
