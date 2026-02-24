#!/usr/bin/env python3
import argparse
import getpass
import hashlib
import hmac
import os
import secrets
import sys
from pathlib import Path
from typing import Optional, Tuple

AUTH_FILE = Path('.login_auth')
PBKDF2_ITERATIONS = 200_000


def read_secret(prompt: str, env_value: Optional[str] = None) -> str:
    if env_value:
        return env_value
    return getpass.getpass(prompt)


def hash_password(password: str, salt_hex: str, iterations: int = PBKDF2_ITERATIONS) -> str:
    dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), bytes.fromhex(salt_hex), iterations)
    return dk.hex()


def is_configured() -> bool:
    return AUTH_FILE.is_file()


def parse_stored_hash(content: str) -> Optional[Tuple[int, str, str]]:
    parts = content.strip().split('$')
    if len(parts) != 4 or parts[0] != 'pbkdf2_sha256':
        return None
    try:
        iterations = int(parts[1])
    except ValueError:
        return None
    return iterations, parts[2], parts[3]


def cmd_init() -> int:
    first = read_secret('New password: ', os.getenv('LOGIN_PASSWORD'))
    second = read_secret('Confirm password: ', os.getenv('LOGIN_PASSWORD_CONFIRM', os.getenv('LOGIN_PASSWORD')))

    if not first:
        print('Password cannot be empty.')
        return 1
    if first != second:
        print('Passwords do not match.')
        return 1

    salt = secrets.token_hex(16)
    digest = hash_password(first, salt)
    line = f'pbkdf2_sha256${PBKDF2_ITERATIONS}${salt}${digest}\n'

    old_umask = os.umask(0o177)
    try:
        AUTH_FILE.write_text(line, encoding='utf-8')
    finally:
        os.umask(old_umask)

    os.chmod(AUTH_FILE, 0o600)
    print(f'Login password configured in {AUTH_FILE}')
    return 0


def verify_password() -> bool:
    if not is_configured():
        print('Login not configured. Run: ./login.py init')
        return False

    provided = read_secret('Password: ', os.getenv('LOGIN_PASSWORD'))
    parsed = parse_stored_hash(AUTH_FILE.read_text(encoding='utf-8'))
    if parsed is None:
        print('Stored login file is invalid. Re-run: ./login.py init')
        return False

    iterations, salt, stored_digest = parsed
    candidate = hash_password(provided, salt, iterations)
    return hmac.compare_digest(candidate, stored_digest)


def _protect_permissions(base: Path) -> None:
    for path in sorted(base.rglob('*')):
        if any(part == '.git' for part in path.parts):
            continue
        if path.is_dir():
            os.chmod(path, 0o700)
        elif path.is_file():
            if path.name in {'login.sh', 'run_login_tests.sh', 'login.py', 'run_login_py_tests.sh'}:
                os.chmod(path, 0o700)
            else:
                os.chmod(path, 0o600)


def cmd_login() -> int:
    if verify_password():
        print('Login successful.')
        return 0

    print('Login failed.')
    return 1


def cmd_protect() -> int:
    if not verify_password():
        print('Authentication failed. Files were not modified.')
        return 1

    _protect_permissions(Path('.'))
    print('Protection applied: directories=700, files=600 (owner-only), excluding .git internals.')
    return 0


def cmd_status() -> int:
    if is_configured():
        print(f'Login is configured ({AUTH_FILE} exists).')
    else:
        print('Login is not configured.')
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description='Local password gate and permissions hardener.')
    parser.add_argument('command', nargs='?', default='help', choices=['init', 'login', 'protect', 'status', 'help'])
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == 'init':
        return cmd_init()
    if args.command == 'login':
        return cmd_login()
    if args.command == 'protect':
        return cmd_protect()
    if args.command == 'status':
        return cmd_status()
    if args.command == 'help':
        parser.print_help()
        return 0

    return 1


if __name__ == '__main__':
    sys.exit(main())
