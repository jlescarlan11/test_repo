#!/usr/bin/env bash
set -euo pipefail

AUTH_FILE=".login_auth"

usage() {
  cat <<'USAGE'
Usage: ./login.sh <command>

Commands:
  init      Create or reset the login password.
  login     Verify password (non-interactive via LOGIN_PASSWORD env var).
  protect   Verify password, then restrict file permissions in this repo.
  status    Show whether login is configured.
  help      Show this help.

Environment variables (optional):
  LOGIN_PASSWORD          Password for non-interactive use.
  LOGIN_PASSWORD_CONFIRM  Confirm password for non-interactive init.
USAGE
}

read_secret() {
  local prompt="$1"
  local env_value="${2-}"

  if [[ -n "$env_value" ]]; then
    printf '%s' "$env_value"
    return 0
  fi

  local input
  read -r -s -p "$prompt" input
  echo
  printf '%s' "$input"
}

extract_salt() {
  local hash="$1"
  # openssl passwd -6 output format: $6$salt$hash
  printf '%s' "$hash" | awk -F'$' '{print $3}'
}

hash_password() {
  local password="$1"
  local salt="$2"
  openssl passwd -6 -salt "$salt" "$password"
}

is_configured() {
  [[ -f "$AUTH_FILE" ]]
}

cmd_init() {
  local first second salt hash
  first="$(read_secret 'New password: ' "${LOGIN_PASSWORD-}")"
  second="$(read_secret 'Confirm password: ' "${LOGIN_PASSWORD_CONFIRM-${LOGIN_PASSWORD-}}")"

  if [[ -z "$first" ]]; then
    echo "Password cannot be empty."
    exit 1
  fi

  if [[ "$first" != "$second" ]]; then
    echo "Passwords do not match."
    exit 1
  fi

  salt="$(openssl rand -hex 16)"
  hash="$(hash_password "$first" "$salt")"
  umask 077
  printf '%s\n' "$hash" > "$AUTH_FILE"
  chmod 600 "$AUTH_FILE"
  echo "Login password configured in $AUTH_FILE"
}

verify_password() {
  local provided stored salt candidate

  if ! is_configured; then
    echo "Login not configured. Run: ./login.sh init"
    return 1
  fi

  provided="$(read_secret 'Password: ' "${LOGIN_PASSWORD-}")"
  stored="$(cat "$AUTH_FILE")"
  salt="$(extract_salt "$stored")"

  if [[ -z "$salt" ]]; then
    echo "Stored login file is invalid. Re-run: ./login.sh init"
    return 1
  fi

  candidate="$(hash_password "$provided" "$salt")"
  if [[ "$candidate" == "$stored" ]]; then
    return 0
  fi

  return 1
}

cmd_login() {
  if verify_password; then
    echo "Login successful."
  else
    echo "Login failed."
    exit 1
  fi
}

cmd_protect() {
  if ! verify_password; then
    echo "Authentication failed. Files were not modified."
    exit 1
  fi

  # Restrict access to owner only, excluding .git internals.
  find . -mindepth 1 -type d ! -path './.git*' -exec chmod 700 {} +
  find . -mindepth 1 -type f ! -path './.git*' ! -name 'login.sh' ! -name 'run_login_tests.sh' -exec chmod 600 {} +

  chmod 700 login.sh
  if [[ -f run_login_tests.sh ]]; then
    chmod 700 run_login_tests.sh
  fi

  echo "Protection applied: directories=700, files=600 (owner-only), excluding .git internals."
}

cmd_status() {
  if is_configured; then
    echo "Login is configured ($AUTH_FILE exists)."
  else
    echo "Login is not configured."
  fi
}

main() {
  local command="${1-help}"
  case "$command" in
    init) cmd_init ;;
    login) cmd_login ;;
    protect) cmd_protect ;;
    status) cmd_status ;;
    help|-h|--help) usage ;;
    *)
      echo "Unknown command: $command"
      usage
      exit 1
      ;;
  esac
}

main "$@"
