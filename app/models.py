"""Pure data types and formatting/filter helpers (no PyQt dependencies)."""

from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Iterable

IMAGE_EXT = {".png", ".jpg", ".jpeg", ".gif", ".bmp", ".webp"}
AUDIO_EXT = {".mp3", ".wav", ".ogg", ".flac", ".m4a"}
VIDEO_EXT = {".mp4", ".mov", ".avi", ".mkv", ".webm"}
DOCUMENT_EXT = {".pdf", ".doc", ".docx", ".txt", ".rtf", ".md"}
DATA_EXT = {".csv", ".json", ".xml", ".xlsx", ".xls", ".tsv"}
ARCHIVE_EXT = {".zip", ".rar", ".7z", ".tar", ".gz"}
TEXT_PREVIEW_EXT = {".txt", ".md", ".csv", ".json", ".xml", ".tsv", ".log", ".py"}
CATEGORIES = ("All Files", "Images", "Audio", "Video", "Documents", "Data", "Archives", "Other")


@dataclass(frozen=True)
class FileRecord:
    path: str
    name: str
    extension: str
    category: str
    size: int
    modified_ts: float

    @property
    def folder(self) -> str:
        return str(Path(self.path).parent)


def category_for(filename: str) -> str:
    ext = Path(filename).suffix.lower()
    for category, extensions in (
        ("Images", IMAGE_EXT), ("Audio", AUDIO_EXT), ("Video", VIDEO_EXT),
        ("Documents", DOCUMENT_EXT), ("Data", DATA_EXT), ("Archives", ARCHIVE_EXT),
    ):
        if ext in extensions:
            return category
    return "Other"


def format_size(value: int) -> str:
    if value < 0:
        raise ValueError("File size cannot be negative")
    if value < 1024:
        return f"{value} B"
    amount = float(value)
    for unit in ("KB", "MB", "GB", "TB", "PB"):
        amount /= 1024
        if amount < 1024 or unit == "PB":
            return f"{amount:.1f} {unit}"
    return "0 B"


def format_modified(ts: float) -> str:
    return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M")


def filter_records(records: Iterable[FileRecord], text: str = "", category: str = "All Files") -> list[FileRecord]:
    term = text.strip().casefold()
    return [rec for rec in records if
            (category == "All Files" or rec.category == category)
            and (not term or term in rec.name.casefold() or term in rec.path.casefold())]


def csv_safe(value: str) -> str:
    """Prevent spreadsheet applications from interpreting untrusted names as formulas."""
    if value and value.lstrip().startswith(("=", "+", "-", "@")):
        return "'" + value
    return value
