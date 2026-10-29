"""Reproducible Task 8 comparison: sequential vs threaded file metadata I/O.

Usage: python benchmarks/benchmark.py --demo --repeats 3 --workers 4
       python benchmarks/benchmark.py --path /some/folder --repeats 3
"""

import argparse
import csv
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from statistics import mean
from tempfile import TemporaryDirectory
from time import perf_counter
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from app.scanner import discover_files, get_file_record


def inspect(paths: list[Path], threaded: bool = False, workers: int = 4) -> int:
    if threaded:
        with ThreadPoolExecutor(max_workers=workers) as pool:
            return sum(rec.size for rec in pool.map(get_file_record, paths))
    return sum(get_file_record(path).size for path in paths)


def benchmark(paths: list[Path], repeats: int, workers: int) -> list[dict]:
    if repeats < 1 or workers < 1:
        raise ValueError("repeats and workers must be positive")
    observations: list[dict] = []
    for run in range(1, repeats + 1):
        for approach in ("sequential", "threaded"):
            start = perf_counter()
            total = inspect(paths, threaded=approach == "threaded", workers=workers)
            seconds = perf_counter() - start
            observations.append({"run": run, "approach": approach,
                                 "seconds": round(seconds, 6), "files": len(paths),
                                 "total_bytes": total, "workers": workers if approach == "threaded" else 1})
    return observations


def main():
    parser = argparse.ArgumentParser(description="Measure metadata scanning approaches.")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--demo", action="store_true", help="Create temporary sample files")
    group.add_argument("--path", type=Path, help="Folder containing real sample files")
    parser.add_argument("--repeats", type=int, default=3)
    parser.add_argument("--workers", type=int, default=4)
    parser.add_argument("--output", type=Path, help="Write rows to CSV (optional)")
    args = parser.parse_args()
    if args.repeats < 1 or args.workers < 1:
        parser.error("--repeats and --workers must be positive")
    temp = TemporaryDirectory() if args.demo else None
    try:
        if args.demo:
            root = Path(temp.name)
            for i in range(800):
                (root / f"sample_{i:04d}.txt").write_bytes((f"Sample {i}: " * 16).encode())
            print("Demo: 800 temporary local files")
        else:
            root = args.path
        paths, errors = discover_files(str(root), recursive=True)
        if errors:
            print(f"Warning: {len(errors)} directory access errors")
        if not paths:
            parser.error("No files found. Choose a folder containing files.")
        rows = benchmark(paths, args.repeats, args.workers)
        for row in rows:
            print(f"Run {row['run']}: {row['approach']:10s} {row['seconds']:.6f}s  {row['files']} files  {row['total_bytes']} bytes")
        sequential = mean(r["seconds"] for r in rows if r["approach"] == "sequential")
        threaded = mean(r["seconds"] for r in rows if r["approach"] == "threaded")
        print(f"Average sequential: {sequential:.6f}s | threaded: {threaded:.6f}s | speedup (sequential/threaded): {sequential/threaded:.2f}x")
        # Example: 85% parallelisable on 4 processors; this is an illustrative
        # hypothetical fraction, NOT a measurement of the code above.
        p, n = 0.85, 4
        print(f"Amdahl illustration (p={p}, N={n}): 1/((1-p)+p/N) = {1/((1-p)+p/n):.2f}x theoretical maximum")
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            with open(args.output, "w", encoding="utf-8", newline="") as handle:
                writer = csv.DictWriter(handle, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)
            print(f"Raw benchmark CSV saved to {args.output}")
    finally:
        if temp:
            temp.cleanup()


if __name__ == "__main__":
    main()
