"""Locate bundled resources in development or a PyInstaller build."""

import sys
from pathlib import Path


def asset_path(filename: str) -> Path:
    base = Path(getattr(sys, "_MEIPASS", Path(__file__).resolve().parent.parent))
    return base / "assets" / filename
