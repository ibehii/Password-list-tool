"""Pyfiglet font installer and fallback helper."""

from __future__ import annotations

import shutil
from pathlib import Path
from typing import Optional

try:
    import pyfiglet
except ImportError:
    pyfiglet = None

ROOT_PROJECT_PATH: Path = Path(__file__).resolve().parent.parent
LOCAL_LIB_PATH: Path = Path(__file__).resolve().parent


def get_pyfiglet_fonts_dir() -> Optional[Path]:
    """Locate pyfiglet fonts directory."""
    if not pyfiglet:
        return None
    try:
        fonts_dir = Path(pyfiglet.__file__).resolve().parent / "fonts"
        fonts_dir.mkdir(parents=True, exist_ok=True)
        return fonts_dir
    except Exception:
        return None


def figlet_font_downloader() -> bool:
    """Ensure ANSI Shadow.flf is available to pyfiglet."""
    if not pyfiglet:
        return False

    fonts_dir = get_pyfiglet_fonts_dir()
    if not fonts_dir:
        return False

    target_font_path = fonts_dir / "ANSI Shadow.flf"
    if target_font_path.exists():
        return True

    # Check root project directory and lib directory for bundled font
    candidate_locations = [
        ROOT_PROJECT_PATH / "ANSI Shadow.flf",
        LOCAL_LIB_PATH / "ANSI Shadow.flf",
        Path.cwd() / "ANSI Shadow.flf",
    ]

    for candidate_path in candidate_locations:
        if candidate_path.is_file():
            try:
                shutil.copy2(candidate_path, target_font_path)
                return True
            except Exception:
                continue

    # Attempt network download if local font file not found
    try:
        import requests
        download_url = "https://github.com/xero/figlet-fonts/raw/master/ANSI%20Shadow.flf"
        response = requests.get(download_url, timeout=5)
        if response.status_code == 200:
            target_font_path.write_bytes(response.content)
            return True
    except Exception:
        pass

    return False


def render_figlet_banner(text: str, preferred_font: str = "ANSI Shadow") -> str:
    """Render figlet banner with graceful fallback to standard font."""
    if not pyfiglet:
        return text

    try:
        return pyfiglet.figlet_format(text, font=preferred_font)
    except Exception:
        try:
            return pyfiglet.figlet_format(text, font="standard")
        except Exception:
            return text
