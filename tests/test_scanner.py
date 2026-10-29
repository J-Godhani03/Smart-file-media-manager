"""Automated tests for file discovery, cancellation and error handling."""

import tempfile
import unittest
from pathlib import Path

from app.scanner import discover_files, get_file_record, scan_paths, load_text_preview


class ScannerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)
        (self.root / "top.txt").write_text("Hello, world!", encoding="utf-8")
        (self.root / "photo.PNG").write_bytes(b"dummy")
        (self.root / ".secret.txt").write_text("hidden")
        self.child = self.root / "sub"
        self.child.mkdir()
        (self.child / "inside.csv").write_text("a,b\n1,2")

    def tearDown(self):
        self.temp.cleanup()

    def test_recursive_discovery(self):
        files, errors = discover_files(str(self.root), recursive=True)
        self.assertEqual(len(files), 3)
        self.assertFalse(errors)

    def test_nonrecursive_discovery(self):
        files, _ = discover_files(str(self.root), recursive=False)
        self.assertEqual(sorted(p.name for p in files), ["photo.PNG", "top.txt"])

    def test_invalid_path(self):
        with self.assertRaises(ValueError):
            discover_files(str(self.root / "missing"))

    def test_cancel_before_discovery(self):
        files, _ = discover_files(str(self.root), cancelled=lambda: True)
        self.assertEqual(files, [])

    def test_file_record_metadata(self):
        record = get_file_record(self.root / "top.txt")
        self.assertEqual(record.size, 13)
        self.assertEqual(record.category, "Documents")

    def test_missing_file_error(self):
        with self.assertRaises(OSError):
            get_file_record(self.root / "deleted.txt")

    def test_scan_paths_success(self):
        files, _ = discover_files(str(self.root))
        events = []
        records, errors, cancelled = scan_paths(files, progress=lambda a, b: events.append((a,b)))
        self.assertEqual(len(records), 3)
        self.assertFalse(errors)
        self.assertFalse(cancelled)
        self.assertEqual(events[-1], (3,3))

    def test_scan_paths_deleted_during_processing(self):
        files = [self.root / "top.txt", self.root / "deleted.txt"]
        records, errors, cancelled = scan_paths(files)
        self.assertEqual(len(records), 1)
        self.assertEqual(len(errors), 1)
        self.assertFalse(cancelled)

    def test_scan_paths_cancelled(self):
        paths = [self.root / "top.txt"] * 3
        records, errors, cancelled = scan_paths(paths, cancelled=lambda: True)
        self.assertEqual(records, [])
        self.assertTrue(cancelled)

    def test_preview_shorten(self):
        preview = load_text_preview(str(self.root / "top.txt"), max_chars=5)
        self.assertTrue(preview.startswith("Hello"))
        self.assertIn("Preview shortened", preview)

    def test_preview_full_text(self):
        self.assertEqual(load_text_preview(str(self.root / "top.txt")), "Hello, world!")

    def test_preview_invalid_limit(self):
        with self.assertRaises(ValueError):
            load_text_preview(str(self.root / "top.txt"), max_chars=0)

    def test_preview_file_not_found(self):
        with self.assertRaises(OSError):
            load_text_preview(str(self.root / "missing.txt"))


if __name__ == "__main__":
    unittest.main()
