"""Worker: does file I/O away from the GUI thread and sends Qt signals."""

from threading import Event

from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot
from .scanner import discover_files, scan_paths


class ScanWorker(QObject):
    progress = pyqtSignal(int, int)
    message = pyqtSignal(str)
    completed = pyqtSignal(object, object, bool)  # records, errors, cancelled
    finished = pyqtSignal()

    def __init__(self, folder: str, recursive: bool):
        super().__init__()
        self.folder = folder
        self.recursive = recursive
        self._stop = Event()  # Thread-safe flag; GUI never accesses worker collections.

    def request_cancel(self) -> None:
        self._stop.set()

    @pyqtSlot()
    def run(self) -> None:
        records = []
        errors = []
        was_cancelled = False
        try:
            self.message.emit("Discovering files...")
            paths, discovery_errors = discover_files(self.folder, self.recursive, self._stop.is_set)
            errors.extend(discovery_errors)
            self.progress.emit(0, len(paths))
            if not self._stop.is_set():
                self.message.emit(f"Reading metadata for {len(paths):,} files...")
                records, processing_errors, was_cancelled = scan_paths(
                    paths, self._stop.is_set, lambda i, total: self.progress.emit(i, total)
                )
                errors.extend(processing_errors)
            was_cancelled = was_cancelled or self._stop.is_set()
        except Exception as exc:  # Protect the GUI if unexpected filesystem errors occur.
            errors.append(f"Scanning failed: {exc}")
        finally:
            self.completed.emit(records, errors, was_cancelled)
            self.finished.emit()
