"""Handle user actions and worker lifecycle without blocking the GUI."""

import csv
from pathlib import Path

from PyQt6.QtCore import QThread
from PyQt6.QtWidgets import QFileDialog

from .models import FileRecord, filter_records, TEXT_PREVIEW_EXT, csv_safe, format_modified
from .scanner import load_text_preview
from .workers import ScanWorker


class AppController:
    def __init__(self, view):
        self.view = view
        self.records: list[FileRecord] = []
        self._by_path: dict[str, FileRecord] = {}
        self.thread: QThread | None = None
        self.worker: ScanWorker | None = None
        self._running = False
        self._close_pending = False
        view.close_handler = self.safe_close
        view.browse_button.clicked.connect(self.choose_folder)
        view.open_action.triggered.connect(self.choose_folder)
        view.scan_button.clicked.connect(self.start_scan)
        view.cancel_button.clicked.connect(self.cancel_scan)
        view.search_input.textChanged.connect(self.refresh)
        view.category_combo.currentTextChanged.connect(self.refresh)
        view.table.itemSelectionChanged.connect(self.preview_selection)
        view.export_action.triggered.connect(self.export_csv)
        view.audio_play.clicked.connect(view.audio_player.play)
        view.audio_pause.clicked.connect(view.audio_player.pause)
        view.audio_stop.clicked.connect(view.audio_player.stop)

    def choose_folder(self):
        selected = QFileDialog.getExistingDirectory(self.view, "Choose a folder to scan", str(Path.home()))
        if selected:
            self.view.folder_input.setText(selected)
            self.view.notify(f"Selected folder: {selected}")

    def start_scan(self):
        if self._running:
            return
        folder = self.view.folder_input.text().strip()
        if not folder or not Path(folder).is_dir():
            self.view.warning("Invalid folder", "Please browse to an existing folder first.")
            return
        self.records = []
        self._by_path = {}
        self.view.show_records([])
        self.view.set_busy(True)
        self.view.notify("Starting background scan...")
        self._running = True
        self.thread = QThread(self.view)
        self.worker = ScanWorker(folder, self.view.recursive_check.isChecked())
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        self.worker.progress.connect(self.view.update_progress)
        self.worker.message.connect(self.view.notify)
        self.worker.completed.connect(self.scan_finished)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread_finished)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.start()

    def cancel_scan(self):
        if self._running and self.worker is not None:
            self.worker.request_cancel()  # Sets only a thread-safe Event.
            self.view.cancel_button.setEnabled(False)
            self.view.notify("Cancellation requested. Finishing the current file...")

    def scan_finished(self, records: list[FileRecord], errors: list[str], was_cancelled: bool):
        self.records = records
        self._by_path = {rec.path: rec for rec in records}
        self.refresh()
        if was_cancelled:
            self.view.notify(f"Scan cancelled. {len(records):,} files processed before cancellation.", 12000)
        else:
            self.view.progress.setValue(self.view.progress.maximum())
            self.view.notify(f"Scan complete: {len(records):,} files. {len(errors)} errors.", 12000)
            self.view.play_completion_sound()
        if errors and not self._close_pending:
            examples = "\n".join(errors[:5])
            more = f"\n... plus {len(errors)-5} more." if len(errors) > 5 else ""
            self.view.warning("Some files could not be processed", examples + more)

    def thread_finished(self):
        self._running = False
        self.worker = None
        self.thread = None
        self.view.set_busy(False)
        if self._close_pending:
            self.view.close()

    def refresh(self, *_args):
        matches = filter_records(self.records,
            self.view.search_input.text(), self.view.category_combo.currentText())
        self.view.show_records(matches)

    def preview_selection(self):
        path = self.view.selected_path()
        rec = self._by_path.get(path) if path else None
        if rec is None:
            return
        text = None
        if Path(rec.path).suffix.lower() in TEXT_PREVIEW_EXT:
            try:
                text = load_text_preview(rec.path)
            except OSError as exc:
                text = f"Cannot read preview: {exc}"
        self.view.display_preview(rec, text)

    def export_csv(self):
        if not self.view._displayed:
            self.view.warning("Nothing to export", "Scan or filter to at least one file first.")
            return
        output_path, _ = QFileDialog.getSaveFileName(
            self.view, "Export file list", "file_inventory.csv", "CSV Files (*.csv)")
        if not output_path:
            return
        try:
            with open(output_path, "w", encoding="utf-8-sig", newline="") as stream:
                writer = csv.writer(stream)
                writer.writerow(["Name", "Extension", "Category", "Size (bytes)", "Modified", "Folder", "Full path"])
                for rec in self.view._displayed:
                    writer.writerow([
                        csv_safe(rec.name), csv_safe(rec.extension), rec.category, rec.size,
                        format_modified(rec.modified_ts), csv_safe(rec.folder), csv_safe(rec.path),
                    ])
        except OSError as exc:
            self.view.warning("Export failed", str(exc))
            return
        self.view.notify(f"CSV exported: {output_path}", 12000)

    def safe_close(self) -> bool:
        if not self._running:
            return True
        self._close_pending = True
        self.cancel_scan()
        self.view.notify("Cancelling background scan before closing...")
        return False
