"""Qt window and presentation. Slow scanning belongs in the worker, not here."""

from pathlib import Path

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QAction, QPixmap
from PyQt6.QtMultimedia import QAudioOutput, QMediaPlayer, QSoundEffect
from PyQt6.QtWidgets import (
    QCheckBox, QComboBox, QFrame, QGroupBox, QHBoxLayout, QLabel,
    QLineEdit, QMainWindow, QMessageBox, QProgressBar, QPushButton,
    QSplitter, QStatusBar, QTableWidget, QTableWidgetItem, QTextEdit,
    QVBoxLayout, QWidget, QHeaderView, QAbstractItemView,
)

from .models import CATEGORIES, FileRecord, IMAGE_EXT, AUDIO_EXT, TEXT_PREVIEW_EXT, format_size, format_modified
from .resources import asset_path
from .style import STYLE


class SizeItem(QTableWidgetItem):
    """Sort Size column using numeric byte counts rather than formatted text."""
    def __init__(self, value: int):
        super().__init__(format_size(value))
        self.bytes_value = value
        self.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

    def __lt__(self, other: QTableWidgetItem) -> bool:
        if isinstance(other, SizeItem):
            return self.bytes_value < other.bytes_value
        return super().__lt__(other)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.controller = None
        self.close_handler = None
        self.setWindowTitle("Smart File & Media Manager")
        self.resize(1260, 780)
        self.setMinimumSize(930, 620)
        self.setStyleSheet(STYLE)
        self._displayed: list[FileRecord] = []
        self.audio_output = QAudioOutput(self)
        self.audio_player = QMediaPlayer(self)
        self.audio_player.setAudioOutput(self.audio_output)
        self.audio_output.setVolume(0.65)
        self.audio_player.errorOccurred.connect(self._on_audio_error)
        self.complete_sound = QSoundEffect(self)
        sound = asset_path("complete.wav")
        if sound.is_file():
            self.complete_sound.setSource(QUrl.fromLocalFile(str(sound)))
            self.complete_sound.setVolume(0.18)
        self._create_menu()
        self._create_interface()
        self.setStatusBar(QStatusBar(self))
        self.statusBar().showMessage("Ready — choose a folder to begin.")

    def _create_menu(self):
        file_menu = self.menuBar().addMenu("&File")
        self.open_action = QAction("Open Folder...", self)
        self.export_action = QAction("Export Visible Files to CSV...", self)
        self.export_action.setEnabled(False)
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(self.open_action)
        file_menu.addAction(self.export_action)
        file_menu.addSeparator()
        file_menu.addAction(exit_action)
        help_menu = self.menuBar().addMenu("&Help")
        about_action = QAction("About", self)
        about_action.triggered.connect(self._about)
        help_menu.addAction(about_action)

    def _create_interface(self):
        root = QWidget()
        self.setCentralWidget(root)
        layout = QVBoxLayout(root)
        layout.setContentsMargins(20, 16, 20, 14)
        layout.setSpacing(12)

        title = QLabel("Smart File & Media Manager")
        title.setStyleSheet("font-size: 22pt; font-weight: 700; color: #183c6d; background: transparent;")
        layout.addWidget(title)
        desc = QLabel("Browse your local files, inspect their details and preview supported media — without editing them.")
        desc.setStyleSheet("color: #62748c; background: transparent;")
        layout.addWidget(desc)

        folder_row = QHBoxLayout()
        folder_row.setSpacing(8)
        folder_row.addWidget(QLabel("Folder:"))
        self.folder_input = QLineEdit()
        self.folder_input.setReadOnly(True)
        self.folder_input.setPlaceholderText("No folder selected")
        folder_row.addWidget(self.folder_input, 1)
        self.browse_button = QPushButton("Browse...")
        folder_row.addWidget(self.browse_button)
        layout.addLayout(folder_row)

        actions = QHBoxLayout()
        self.recursive_check = QCheckBox("Include subfolders")
        self.recursive_check.setChecked(True)
        actions.addWidget(self.recursive_check)
        actions.addStretch(1)
        self.scan_button = QPushButton("Scan Folder")
        self.scan_button.setObjectName("primary")
        actions.addWidget(self.scan_button)
        self.cancel_button = QPushButton("Cancel Scan")
        self.cancel_button.setEnabled(False)
        actions.addWidget(self.cancel_button)
        layout.addLayout(actions)

        filters = QHBoxLayout()
        filters.addWidget(QLabel("Search:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search file names or paths...")
        self.search_input.setClearButtonEnabled(True)
        filters.addWidget(self.search_input, 1)
        filters.addWidget(QLabel("Category:"))
        self.category_combo = QComboBox()
        self.category_combo.addItems(CATEGORIES)
        filters.addWidget(self.category_combo)
        layout.addLayout(filters)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        self.table = QTableWidget(0, 6)
        self.table.setHorizontalHeaderLabels(["Name", "Ext.", "Category", "Size", "Modified", "Folder"])
        self.table.setSortingEnabled(True)
        self.table.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SelectionMode.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.EditTrigger.NoEditTriggers)
        self.table.setAlternatingRowColors(True)
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Interactive)
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.setColumnWidth(0, 235)
        self.table.setColumnWidth(1, 67)
        self.table.setColumnWidth(2, 92)
        self.table.setColumnWidth(3, 86)
        self.table.setColumnWidth(4, 137)
        splitter.addWidget(self.table)

        preview_group = QGroupBox("File Details & Preview")
        detail_layout = QVBoxLayout(preview_group)
        detail_layout.setSpacing(9)
        self.details_label = QLabel("Select a file from the list to view its details.")
        self.details_label.setWordWrap(True)
        self.details_label.setTextFormat(Qt.TextFormat.PlainText)
        self.details_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.details_label.setStyleSheet("font-weight: normal; font-size: 9pt; line-height: 1.5;")
        detail_layout.addWidget(self.details_label)
        self.image_label = QLabel("No preview selected")
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.image_label.setMinimumHeight(170)
        self.image_label.setStyleSheet("background: #f2f5fa; border: 1px solid #e0e7f0; border-radius: 6px; color: #64758b;")
        detail_layout.addWidget(self.image_label, 1)
        self.text_preview = QTextEdit()
        self.text_preview.setReadOnly(True)
        self.text_preview.setVisible(False)
        detail_layout.addWidget(self.text_preview, 1)
        audio_row = QHBoxLayout()
        self.audio_play = QPushButton("Play")
        self.audio_pause = QPushButton("Pause")
        self.audio_stop = QPushButton("Stop")
        for button in (self.audio_play, self.audio_pause, self.audio_stop):
            button.setEnabled(False)
            audio_row.addWidget(button)
        detail_layout.addLayout(audio_row)
        detail_layout.addStretch(0)
        splitter.addWidget(preview_group)
        splitter.setSizes([810, 330])
        layout.addWidget(splitter, 1)

        info_row = QHBoxLayout()
        self.count_label = QLabel("0 files")
        self.size_label = QLabel("0 B total")
        info_row.addWidget(self.count_label)
        info_row.addWidget(QLabel("•"))
        info_row.addWidget(self.size_label)
        info_row.addStretch()
        self.progress = QProgressBar()
        self.progress.setMinimumWidth(260)
        self.progress.setRange(0, 100)
        self.progress.setValue(0)
        info_row.addWidget(self.progress)
        layout.addLayout(info_row)

    def set_busy(self, busy: bool):
        self.scan_button.setEnabled(not busy)
        self.browse_button.setEnabled(not busy)
        self.open_action.setEnabled(not busy)
        self.recursive_check.setEnabled(not busy)
        self.cancel_button.setEnabled(busy)
        if busy:
            self.progress.setRange(0, 0)  # Indeterminate during path discovery.
        else:
            self.progress.setRange(0, 100)

    def update_progress(self, processed: int, total: int):
        self.progress.setRange(0, max(total, 1))
        self.progress.setValue(processed)
        self.progress.setFormat(f"{processed:,} / {total:,}")

    def show_records(self, records: list[FileRecord]):
        self._displayed = records
        self.table.setSortingEnabled(False)
        self.table.setRowCount(len(records))
        for row, rec in enumerate(records):
            values: list[QTableWidgetItem] = [
                QTableWidgetItem(rec.name),
                QTableWidgetItem(rec.extension),
                QTableWidgetItem(rec.category),
                SizeItem(rec.size),
                QTableWidgetItem(format_modified(rec.modified_ts)),
                QTableWidgetItem(rec.folder),
            ]
            for col, item in enumerate(values):
                item.setData(Qt.ItemDataRole.UserRole, rec.path)
                if col == 0:
                    item.setToolTip(rec.path)
                self.table.setItem(row, col, item)
        self.table.setSortingEnabled(True)
        self.count_label.setText(f"{len(records):,} files")
        self.size_label.setText(f"{format_size(sum(x.size for x in records))} total")
        self.export_action.setEnabled(bool(records))
        self.clear_preview()

    def selected_path(self) -> str | None:
        row = self.table.currentRow()
        item = self.table.item(row, 0) if row >= 0 else None
        return str(item.data(Qt.ItemDataRole.UserRole)) if item is not None else None

    def clear_preview(self):
        self.audio_player.stop()
        self.audio_player.setSource(QUrl())
        self.details_label.setText("Select a file from the list to view its details.")
        self.image_label.setText("No preview selected")
        self.image_label.setPixmap(QPixmap())
        self.image_label.show()
        self.text_preview.hide()
        for button in (self.audio_play, self.audio_pause, self.audio_stop):
            button.setEnabled(False)

    def display_preview(self, rec: FileRecord, text: str | None = None):
        self.clear_preview()
        # Use setText with plain strings and escaped file details; never render file content as HTML.
        self.details_label.setText(
            f"Name: {rec.name}\nType: {rec.category} ({rec.extension})\n"
            f"Size: {format_size(rec.size)}\nModified: {format_modified(rec.modified_ts)}\n"
            f"Location: {rec.folder}"
        )
        ext = Path(rec.path).suffix.lower()
        if ext in IMAGE_EXT:
            pixmap = QPixmap(rec.path)
            if pixmap.isNull():
                self.image_label.setText("Image could not be decoded.")
            else:
                self.image_label.setPixmap(pixmap.scaled(300, 270,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation))
        elif ext in TEXT_PREVIEW_EXT:
            self.image_label.hide()
            self.text_preview.setPlainText(text if text is not None else "Preview is not available.")
            self.text_preview.show()
        elif ext in AUDIO_EXT:
            self.image_label.setText("Audio file selected. Use Play / Pause / Stop below.")
            self.audio_player.setSource(QUrl.fromLocalFile(rec.path))
            for button in (self.audio_play, self.audio_pause, self.audio_stop):
                button.setEnabled(True)
        else:
            self.image_label.setText("Preview not supported for this file type.\nMetadata is available above.")

    def play_completion_sound(self):
        if self.complete_sound.isLoaded():
            self.complete_sound.play()

    def notify(self, message: str, timeout: int = 5000):
        self.statusBar().showMessage(message, timeout)

    def warning(self, title: str, message: str):
        QMessageBox.warning(self, title, message)

    def information(self, title: str, message: str):
        QMessageBox.information(self, title, message)

    def _on_audio_error(self, error, error_text: str):
        if error != QMediaPlayer.Error.NoError:
            self.notify(f"Audio playback problem: {error_text}", 9000)

    def _about(self):
        self.information("About", "Smart File & Media Manager\nA Python / PyQt6 desktop project.\nLocal metadata, search, preview, audio and background scanning.")

    def closeEvent(self, event):
        if self.close_handler is not None and not self.close_handler():
            event.ignore()
            return
        self.audio_player.stop()
        event.accept()
