#  GitHub: https://github.com/ibehii
#  Telegram: https://t.me/dr_xz
#  ____________________________________________
"""Initialization routine for storage directories and font assets."""

from __future__ import annotations

from pathlib import Path
from lib.f_font_downloader import figlet_font_downloader

CURRENT_PATH: Path = Path(__file__).resolve().parent


def initializer() -> None:
    """Ensure database directory and required assets exist."""
    db_directory = CURRENT_PATH / "db"
    db_directory.mkdir(parents=True, exist_ok=True)
    figlet_font_downloader()