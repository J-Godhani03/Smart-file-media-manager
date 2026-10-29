"""Check benchmark validates its settings and both modes agree on results."""

import tempfile
import unittest
from pathlib import Path
from benchmarks.benchmark import inspect, benchmark


class BenchmarkTests(unittest.TestCase):
    def test_sequential_and_threaded_agree(self):
        with tempfile.TemporaryDirectory() as folder:
            files = [Path(folder) / f"file_{i}.txt" for i in range(12)]
            for i, path in enumerate(files):
                path.write_bytes(b"x" * (i + 1))
            self.assertEqual(inspect(files, False), inspect(files, True, 4))

    def test_benchmark_generates_rows(self):
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "test.txt"
            path.write_bytes(b"123")
            observations = benchmark([path], repeats=2, workers=2)
            self.assertEqual(len(observations), 4)
            self.assertEqual({r["approach"] for r in observations}, {"sequential", "threaded"})

    def test_invalid_workers_rejected(self):
        with self.assertRaises(ValueError):
            benchmark([], repeats=1, workers=0)

    def test_invalid_repeats_rejected(self):
        with self.assertRaises(ValueError):
            benchmark([], repeats=0, workers=4)


if __name__ == "__main__":
    unittest.main()
