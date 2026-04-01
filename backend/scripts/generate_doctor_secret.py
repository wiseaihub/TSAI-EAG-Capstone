"""Generate a strong DOCTOR_PROVISION_SECRET for local or production use.

Usage:
  python backend/scripts/generate_doctor_secret.py
  python backend/scripts/generate_doctor_secret.py --bytes 48
"""

from __future__ import annotations

import argparse
import secrets


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate DOCTOR_PROVISION_SECRET")
    parser.add_argument(
        "--bytes",
        type=int,
        default=32,
        help="Entropy bytes for token_urlsafe (default: 32, recommended >= 32)",
    )
    args = parser.parse_args()

    if args.bytes < 16:
        raise SystemExit("--bytes must be >= 16")

    token = secrets.token_urlsafe(args.bytes)
    print(f"DOCTOR_PROVISION_SECRET={token}")


if __name__ == "__main__":
    main()
