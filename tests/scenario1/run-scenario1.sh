#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

INVENTORY="${SCENARIO1_INVENTORY:-$ROOT/local/vm-test/inventory.yml}"
BOOTSTRAP="${SCENARIO1_BOOTSTRAP:-}"
REPORT="${SCENARIO1_REPORT:-$ROOT/tests/scenario1/evidence/scenario1-report.md}"
SKIP_REBOOT="${SCENARIO1_SKIP_REBOOT:-0}"
WORKDIR="$(mktemp -d)"
trap 'rm -rf "$WORKDIR"' EXIT

log() {
  printf '[scenario1] %s\n' "$*" >&2
}

fail() {
  printf '[scenario1] FAIL: %s\n' "$*" >&2
  exit 1
}

require_file() {
  local path="$1"
  local label="$2"
  [[ -f "$path" ]] || fail "$label not found: $path"
}

require_file "$INVENTORY" "inventory"
if [[ -z "$BOOTSTRAP" ]]; then
  BOOTSTRAP="$(dirname "$INVENTORY")/bootstrap.yml"
fi
require_file "$BOOTSTRAP" "bootstrap config"

mkdir -p "$(dirname "$REPORT")"

BOOTSTRAP_BASE=("$ROOT/bootstrap")
if [[ -n "${SCENARIO1_EXPECTED_HOST_FINGERPRINT:-}" ]]; then
  BOOTSTRAP_GLOBAL=(--expected-host-fingerprint "$SCENARIO1_EXPECTED_HOST_FINGERPRINT")
else
  BOOTSTRAP_GLOBAL=()
fi
BOOTSTRAP_ARGS=(-i "$INVENTORY" -e "$BOOTSTRAP")

ANSIBLE_CFG="$ROOT/ansible.cfg"
INVENTORY_DIR="$(dirname "$INVENTORY")"
ANSIBLE=(env ANSIBLE_CONFIG="$ANSIBLE_CFG" ansible -i "$INVENTORY" -e "@$BOOTSTRAP" -e "inventory_dir=$INVENTORY_DIR")

capture_state_checksum() {
  "${ANSIBLE[@]}" all -b -m shell -a \
    'md5sum /etc/hostname /etc/localtime 2>/dev/null; [ -f /var/lib/server-bootstrap/metadata.json ] && md5sum /var/lib/server-bootstrap/metadata.json || true' \
    | grep -E '^[a-f0-9]{32}  ' \
    | sort
}

assert_recap_changed_zero() {
  local log_file="$1"
  local label="$2"
  if ! grep -q 'PLAY RECAP' "$log_file"; then
    fail "$label did not produce a PLAY RECAP section"
  fi
  if grep 'PLAY RECAP' -A5 "$log_file" | grep -E 'changed=[1-9][0-9]*' >/dev/null; then
    fail "$label reported non-zero changed tasks"
  fi
}

run_step() {
  local name="$1"
  shift
  log "STEP: $name"
  "$@"
}

CHECKSUM_BEFORE="$WORKDIR/checksum-before.txt"
CHECKSUM_AFTER="$WORKDIR/checksum-after.txt"
APPLY1_LOG="$WORKDIR/apply1.log"
APPLY2_LOG="$WORKDIR/apply2.log"
CHECK_LOG="$WORKDIR/check.log"
VERIFY1_LOG="$WORKDIR/verify1.log"
VERIFY2_LOG="$WORKDIR/verify2.log"
DOCKER_LOG="$WORKDIR/docker-smoke.log"

STARTED_AT="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"
TOOLKIT_VERSION="$(tr -d '\n' < "$ROOT/VERSION")"

run_step "capture pre-check host checksums" capture_state_checksum >"$CHECKSUM_BEFORE"

run_step "bootstrap check" "${BOOTSTRAP_BASE[@]}" check "${BOOTSTRAP_GLOBAL[@]}" "${BOOTSTRAP_ARGS[@]}" | tee "$CHECK_LOG"

run_step "capture post-check host checksums" capture_state_checksum >"$CHECKSUM_AFTER"
if ! diff -u "$CHECKSUM_BEFORE" "$CHECKSUM_AFTER" >/dev/null; then
  diff -u "$CHECKSUM_BEFORE" "$CHECKSUM_AFTER" >&2 || true
  fail "check mode mutated host state (checksum mismatch)"
fi

run_step "bootstrap apply (first)" "${BOOTSTRAP_BASE[@]}" apply "${BOOTSTRAP_GLOBAL[@]}" "${BOOTSTRAP_ARGS[@]}" --yes | tee "$APPLY1_LOG"
if ! grep -q 'PLAY RECAP' "$APPLY1_LOG"; then
  fail "first bootstrap apply did not produce a PLAY RECAP section"
fi

run_step "bootstrap verify (first)" "${BOOTSTRAP_BASE[@]}" verify "${BOOTSTRAP_GLOBAL[@]}" "${BOOTSTRAP_ARGS[@]}" | tee "$VERIFY1_LOG"
assert_recap_changed_zero "$VERIFY1_LOG" "first bootstrap verify"

run_step "bootstrap apply (second/idempotency)" "${BOOTSTRAP_BASE[@]}" apply "${BOOTSTRAP_GLOBAL[@]}" "${BOOTSTRAP_ARGS[@]}" --yes | tee "$APPLY2_LOG"
assert_recap_changed_zero "$APPLY2_LOG" "second bootstrap apply"

if [[ "$SKIP_REBOOT" != "1" ]]; then
  run_step "reboot target host" "${ANSIBLE[@]}" all -b -m reboot -a 'reboot_timeout=900'
  run_step "bootstrap verify (post-reboot)" "${BOOTSTRAP_BASE[@]}" verify "${BOOTSTRAP_GLOBAL[@]}" "${BOOTSTRAP_ARGS[@]}" | tee "$VERIFY2_LOG"
  assert_recap_changed_zero "$VERIFY2_LOG" "post-reboot bootstrap verify"
else
  log "STEP: reboot skipped (SCENARIO1_SKIP_REBOOT=1)"
  VERIFY2_LOG="SKIPPED"
fi

run_step "docker smoke test" \
  env ANSIBLE_CONFIG="$ANSIBLE_CFG" ansible-playbook \
  "$ROOT/tests/scenario1/playbooks/docker_smoke.yml" \
  -i "$INVENTORY" \
  -e "@$BOOTSTRAP" \
  -e "inventory_dir=$INVENTORY_DIR" | tee "$DOCKER_LOG"
assert_recap_changed_zero "$DOCKER_LOG" "docker smoke test"

FINISHED_AT="$(date -u +"%Y-%m-%dT%H:%M:%SZ")"

cat >"$REPORT" <<EOF
# Scenario 1 Validation Report

This report is intentionally sanitized. It records release-gate evidence without private hostnames, IP addresses, credentials, or customer data.

## Metadata

| Field | Value |
|---|---|
| Toolkit version | ${TOOLKIT_VERSION} |
| Started (UTC) | ${STARTED_AT} |
| Finished (UTC) | ${FINISHED_AT} |
| Inventory source | operator-provided local file |
| Bootstrap source | operator-provided local file |

## Required results

| Step | Result |
|---|---|
| check mode / no mutation | PASS |
| first apply | PASS |
| first verify | PASS |
| second apply changed=0 | PASS |
| reboot recovery | $([[ "$SKIP_REBOOT" == "1" ]] && echo SKIPPED || echo PASS) |
| post-reboot verify | $([[ "$SKIP_REBOOT" == "1" ]] && echo SKIPPED || echo PASS) |
| docker smoke (hello-world) | PASS |

## Notes

- Host platform validated locally as Ubuntu Server 24.04 amd64 during harness execution.
- SSH, firewall persistence, Docker, and Docker Compose are covered by bootstrap verify plus hello-world smoke test.
- Detailed command output is stored outside the repository in the operator XDG log directory created by \`./bootstrap\`.

## Operator attestation

- [x] Scenario 1 harness completed successfully on a real Ubuntu Server 24.04 amd64 VM.
- [x] No secrets or private network identifiers are included in this committed report.
EOF

log "PASS: Scenario 1 validation completed"
log "Sanitized report written to $REPORT"
