#!/usr/bin/env bash
set -euo pipefail

# Prove the secret gate rejects an unapproved synthetic secret.
# Uses a temporary file outside the repository; nothing is committed.
TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT

# Build a representative AWS access key pattern at runtime (documented example
# prefix/suffix split so the literal key is not stored in a tracked file).
PART_A='AKIA'
PART_B='IOSFODNN7EXAMPLE'
printf '%s\n' "aws_secret_access_key = \"${PART_A}${PART_B}\"" >"$TMP"

set +e
detect-secrets-hook --baseline .secrets.baseline "$TMP"
RC=$?
set -e

if [[ "$RC" -eq 0 ]]; then
  echo "FAIL: secret gate did not reject synthetic secret" >&2
  exit 1
fi

echo "PASS: secret gate rejected synthetic secret (exit ${RC})"
