#!/usr/bin/env python3
"""Password Tool - High-performance Password Generator, Wordlist Toolkit & Secure Vault.

GitHub: https://github.com/ibehii
Telegram: https://t.me/dr_xz
"""

from __future__ import annotations

import sys
from pathlib import Path

# Ensure project root is in Python sys.path
PROJECT_ROOT = Path(__file__).resolve().parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from lib.cli import handle_cli_execution
from lib.initializer import initializer
from lib.ui import run_interactive_menu


def main() -> int:
    """Application main entrypoint."""
    initializer()
    cli_arguments = sys.argv[1:]
    if not cli_arguments:
        run_interactive_menu()
        return 0
    return handle_cli_execution(cli_arguments)


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\nOperation canceled by user.")
        sys.exit(0)