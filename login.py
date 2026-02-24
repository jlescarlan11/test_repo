#!/usr/bin/env python3
"""Simple local login utility for repository file protection."""

from __future__ import annotations

import argparse
import base64
import getpass
import hashlib
import hmac
import json
import os
from pathlib import Path

DEFAULT_CREDENTIALS_FILE = ".login_auth.json"
DEFAULT_ITERATIONS = 200_000


def _read_password(prompt: str, provided: str | None) -> str:
    if provided is not None:
        return provided
    return getpass.getpass(prompt)


def _derive_hash(password: str, salt: bytes, iterations: int) -> bytes:
    return hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations)


def setup_credentials(credentials_path: Path, password: str, confirm_password: str) -> None:
    if password != confirm_password:
        raise ValueError("Passwords do not match.")
    if len(password) < 8:
        raise ValueError("Password must be at least 8 characters.")

    salt = os.urandom(16)
    password_hash = _derive_hash(password, salt, DEFAULT_ITERATIONS)

    payload = {
        "iterations": DEFAULT_ITERATIONS,
        "salt": base64.b64encode(salt).decode("ascii"),
        "password_hash": base64.b64encode(password_hash).decode("ascii"),
    }

    credentials_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    os.chmod(credentials_path, 0o600)


def verify_login(credentials_path: Path, password: str) -> bool:
    if not credentials_path.exists():
        raise FileNotFoundError(
            f"Credentials file not found: {credentials_path}. Run 'setup' first."
        )

    payload = json.loads(credentials_path.read_text(encoding="utf-8"))
    iterations = int(payload["iterations"])
    salt = base64.b64decode(payload["salt"])
    expected_hash = base64.b64decode(payload["password_hash"])

    actual_hash = _derive_hash(password, salt, iterations)
    return hmac.compare_digest(actual_hash, expected_hash)


def secure_paths(root: Path, credentials_path: Path) -> tuple[int, int]:
    file_count = 0
    dir_count = 0

    for path in root.rglob("*"):
        if ".git" in path.parts:
            continue
        if path.resolve() == credentials_path.resolve():
            continue

        if path.is_dir():
            os.chmod(path, 0o700)
            dir_count += 1
        elif path.is_file():
            os.chmod(path, 0o600)
            file_count += 1

    return file_count, dir_count


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a login file and optionally harden permissions in this repository."
    )
    parser.add_argument(
        "--credentials-file",
        default=DEFAULT_CREDENTIALS_FILE,
        help=f"Path for stored login credentials (default: {DEFAULT_CREDENTIALS_FILE}).",
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    setup_parser = subparsers.add_parser("setup", help="Create login credentials.")
    setup_parser.add_argument("--password", help="Password value (optional; prompt if omitted).")
    setup_parser.add_argument(
        "--confirm-password",
        help="Confirmation password value (optional; prompt if omitted).",
    )

    login_parser = subparsers.add_parser("login", help="Verify login credentials.")
    login_parser.add_argument("--password", help="Password value (optional; prompt if omitted).")

    secure_parser = subparsers.add_parser(
        "secure", help="Verify login, then set strict file permissions across a target path."
    )
    secure_parser.add_argument("--password", help="Password value (optional; prompt if omitted).")
    secure_parser.add_argument(
        "--target",
        default=".",
        help="Directory to secure (default: current directory).",
    )

    return parser.parse_args()


def main() -> int:
    args = parse_args()
    credentials_path = Path(args.credentials_file).resolve()

    try:
        if args.command == "setup":
            password = _read_password("Create password: ", args.password)
            confirm_password = _read_password("Confirm password: ", args.confirm_password)
            setup_credentials(credentials_path, password, confirm_password)
            print(f"Created login file: {credentials_path}")
            return 0

        if args.command == "login":
            password = _read_password("Password: ", args.password)
            if verify_login(credentials_path, password):
                print("Login successful.")
                return 0
            print("Login failed.")
            return 1

        if args.command == "secure":
            password = _read_password("Password: ", args.password)
            if not verify_login(credentials_path, password):
                print("Login failed.")
                return 1
            file_count, dir_count = secure_paths(Path(args.target).resolve(), credentials_path)
            print(f"Secured {file_count} file(s) and {dir_count} directories.")
            return 0

        return 2
    except (ValueError, FileNotFoundError, PermissionError, json.JSONDecodeError) as exc:
        print(f"Error: {exc}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
