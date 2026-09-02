#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$ROOT"

run_expect_failure() {
  local playbook="$1"
  local label="$2"
  set +e
  ansible-playbook "$playbook" >/tmp/server-bootstrap-synthetic.out 2>&1
  local rc=$?
  set -e
  if [[ "$rc" -eq 0 ]]; then
    echo "FAIL: expected $label to fail, but playbook succeeded" >&2
    cat /tmp/server-bootstrap-synthetic.out >&2
    exit 1
  fi
  echo "PASS: $label failed as expected (exit ${rc})"
}

run_expect_success() {
  local playbook="$1"
  local label="$2"
  ansible-playbook "$playbook"
  echo "PASS: $label succeeded"
}

run_expect_failure \
  tests/synthetic/playbooks/test_missing_admin_user.yml \
  "missing bootstrap_admin_user preflight"

run_expect_failure \
  tests/synthetic/playbooks/test_unsupported_platform.yml \
  "unsupported platform preflight"

run_expect_failure \
  tests/synthetic/playbooks/test_root_admin_user.yml \
  "root bootstrap_admin_user rejection"

run_expect_failure \
  tests/synthetic/playbooks/test_missing_authorized_keys.yml \
  "missing authorized keys users preflight"

run_expect_failure \
  tests/synthetic/playbooks/test_invalid_ssh_port.yml \
  "invalid bootstrap_ssh_port rejection"

run_expect_failure \
  tests/synthetic/playbooks/test_missing_control_node_identity.yml \
  "missing control node SSH identity rejection"

run_expect_success \
  tests/synthetic/playbooks/test_ssh_dropin_content.yml \
  "ssh drop-in content rendering"

run_expect_failure \
  tests/synthetic/playbooks/test_invalid_firewall_port.yml \
  "invalid bootstrap_firewall_allowed_tcp_ports rejection"

run_expect_success \
  tests/synthetic/playbooks/test_firewall_classify_fresh.yml \
  "fresh firewall classification"

run_expect_success \
  tests/synthetic/playbooks/test_firewall_classify_project_owned.yml \
  "project-owned firewall classification"

run_expect_success \
  tests/synthetic/playbooks/test_docker_classify_absent.yml \
  "absent Docker classification"

run_expect_success \
  tests/synthetic/playbooks/test_docker_classify_official_compatible.yml \
  "official-compatible Docker classification"

run_expect_success \
  tests/synthetic/playbooks/test_docker_classify_partial.yml \
  "partial Docker classification"

run_expect_success \
  tests/synthetic/playbooks/test_docker_classify_conflicting.yml \
  "conflicting Docker classification"

run_expect_success \
  tests/synthetic/playbooks/test_docker_classify_ambiguous.yml \
  "ambiguous Docker classification"

run_expect_failure \
  tests/synthetic/playbooks/test_docker_preflight_conflicting.yml \
  "conflicting Docker preflight rejection"

run_expect_failure \
  tests/synthetic/playbooks/test_docker_downgrade_rejection.yml \
  "Docker downgrade rejection"

run_expect_success \
  tests/synthetic/playbooks/test_system_uid_classification.yml \
  "system UID classification"

run_expect_success \
  tests/synthetic/playbooks/test_summary_component_warnings.yml \
  "summary component opt-out warnings"

run_expect_success \
  tests/synthetic/playbooks/test_metadata_content.yml \
  "target metadata content"

echo "All synthetic preflight tests passed."
