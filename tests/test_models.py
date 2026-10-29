"""Automated tests of normal, boundary and invalid file-model behaviour."""

import unittest
from app.models import FileRecord, category_for, format_size, filter_records, csv_safe


class ModelTests(unittest.TestCase):
    def setUp(self):
        self.records = [
            FileRecord("/tmp/Photo.JPG", "Photo.JPG", ".jpg", "Images", 1024, 1000),
            FileRecord("/tmp/notes.txt", "notes.txt", ".txt", "Documents", 0, 1000),
            FileRecord("/tmp/music.mp3", "music.mp3", ".mp3", "Audio", 2048, 1000),
        ]

    def test_category_is_case_insensitive(self):
        self.assertEqual(category_for("HOLIDAY.JPEG"), "Images")

    def test_known_categories(self):
        self.assertEqual(category_for("data.csv"), "Data")
        self.assertEqual(category_for("archive.zip"), "Archives")
        self.assertEqual(category_for("movie.mp4"), "Video")

    def test_unknown_extension(self):
        self.assertEqual(category_for("mystery.unknown"), "Other")

    def test_extensionless_file(self):
        self.assertEqual(category_for("README"), "Other")

    def test_zero_bytes_boundary(self):
        self.assertEqual(format_size(0), "0 B")

    def test_kilobytes_boundary(self):
        self.assertEqual(format_size(1024), "1.0 KB")

    def test_megabytes_boundary(self):
        self.assertEqual(format_size(1024**2), "1.0 MB")

    def test_negative_size_rejected(self):
        with self.assertRaises(ValueError):
            format_size(-1)

    def test_filter_case_insensitive(self):
        self.assertEqual(len(filter_records(self.records, "PHOTO")), 1)

    def test_filter_category_and_text(self):
        self.assertEqual([rec.name for rec in filter_records(self.records, "mp", "Audio")], ["music.mp3"])

    def test_filter_no_matches(self):
        self.assertEqual(filter_records(self.records, "missing"), [])

    def test_path_is_searchable(self):
        self.assertEqual(len(filter_records(self.records, "/tmp/")), 3)

    def test_csv_formula_injection_guard(self):
        self.assertEqual(csv_safe("=SUM(1+2)"), "'=SUM(1+2)")
        self.assertEqual(csv_safe(" @cmd"), "' @cmd")
        self.assertEqual(csv_safe("normal.txt"), "normal.txt")


if __name__ == "__main__":
    unittest.main()
