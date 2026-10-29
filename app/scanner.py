"""Filesystem discovery and metadata processing, independent of the GUI."""

import os
from pathlib import Path
from typing import Callable

from .models import FileRecord, category_for

CancelCheck = Callable[[], bool]
ProgressFn = Callable[[int, int], None]


def discover_files(root: str, recursive: bool = True,
                   cancelled: CancelCheck | None = None) -> tuple[list[Path], list[str]]:
    path = Path(root).expanduser()
    if not path.is_dir():
        raise ValueError("Please choose an existing folder.")

    items: list[Path] = []
    errors: list[str] = []
    stop = cancelled or (lambda: False)

    def on_error(exc: OSError) -> None:
        errors.append(f"Folder access error: {exc}")

    if recursive:
        for folder, dirs, files in os.walk(path, followlinks=False, onerror=on_error):
            if stop():
                break
            # Do not follow symlinked folders or include hidden dot-folders.
            dirs[:] = [d for d in dirs if not d.startswith(".") and not (Path(folder) / d).is_symlink()]
            for name in files:
                if stop():
                    break
                candidate = Path(folder) / name
                if not name.startswith(".") and not candidate.is_symlink():
                    items.append(candidate)
    else:
        try:
            with os.scandir(path) as it:
                for entry in it:
                    if stop():
                        break
                    try:
                        if not entry.name.startswith(".") and entry.is_file(follow_symlinks=False):
                            items.append(Path(entry.path))
                    except OSError as exc:
                        errors.append(f"Cannot inspect {entry.path}: {exc}")
        except OSError as exc:
            errors.append(f"Cannot read folder: {exc}")
    return items, errors


def get_file_record(path: Path) -> FileRecord:
    info = path.stat()
    if not path.is_file():
        raise OSError(f"Not a regular file: {path}")
    return FileRecord(
        path=str(path.absolute()), name=path.name,
        extension=path.suffix.lower() or "—",
        category=category_for(path.name),
        size=info.st_size, modified_ts=info.st_mtime,
    )


def scan_paths(paths: list[Path], cancelled: CancelCheck | None = None,
               progress: ProgressFn | None = None) -> tuple[list[FileRecord], list[str], bool]:
    stop = cancelled or (lambda: False)
    results: list[FileRecord] = []
    errors: list[str] = []
    total = len(paths)
    for i, path in enumerate(paths, start=1):
        if stop():
            return results, errors, True
        try:
            results.append(get_file_record(path))
        except OSError as exc:
            errors.append(f"{path.name}: {exc}")
        if progress is not None and (i == total or i % 20 == 0):
            progress(i, total)
    return results, errors, bool(stop())


def load_text_preview(path: str, max_chars: int = 8000) -> str:
    """Read a limited amount of text so huge files do not block the interface."""
    if max_chars < 1:
        raise ValueError("max_chars must be positive")
    with open(path, "r", encoding="utf-8", errors="replace") as handle:
        text = handle.read(max_chars + 1)
    if len(text) > max_chars:
        return text[:max_chars] + "\n\n[Preview shortened]"
    return text
