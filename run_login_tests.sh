#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(pwd)"
TMP_DIR="$(mktemp -d)"
trap 'rm -rf "$TMP_DIR"' EXIT

cp "$ROOT_DIR/login.sh" "$TMP_DIR/login.sh"
chmod 700 "$TMP_DIR/login.sh"

cd "$TMP_DIR"

echo "Running login.sh tests in $TMP_DIR"

# Test 1: init should create auth file
LOGIN_PASSWORD='pass123' LOGIN_PASSWORD_CONFIRM='pass123' ./login.sh init >/dev/null
[[ -f .login_auth ]] || { echo 'FAIL: .login_auth not created'; exit 1; }

# Test 2: login succeeds with correct password
LOGIN_PASSWORD='pass123' ./login.sh login >/dev/null || { echo 'FAIL: login should succeed'; exit 1; }

# Test 3: login fails with wrong password
if LOGIN_PASSWORD='wrong' ./login.sh login >/dev/null 2>&1; then
  echo 'FAIL: login should fail with wrong password'
  exit 1
fi

# Prepare sample files for permission test
mkdir docs
printf 'hello\n' > docs/a.txt
printf 'hello\n' > b.txt

# Test 4: protect should harden permissions
LOGIN_PASSWORD='pass123' ./login.sh protect >/dev/null

[[ "$(stat -c '%a' docs)" == "700" ]] || { echo 'FAIL: docs dir perms not 700'; exit 1; }
[[ "$(stat -c '%a' b.txt)" == "600" ]] || { echo 'FAIL: b.txt perms not 600'; exit 1; }
[[ "$(stat -c '%a' docs/a.txt)" == "600" ]] || { echo 'FAIL: docs/a.txt perms not 600'; exit 1; }

echo "All tests passed."
