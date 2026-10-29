# Smart File & Media Manager

Advanced Programming — Assessment 2 (70%): Python/PyQt6 desktop application.

## Quick start on Windows 10/11

1. Extract **the whole ZIP** to a normal folder (do not open source files inside the ZIP).
2. Install **Python 3.11 or later** from https://www.python.org/downloads/ and enable Python on PATH.
3. Double-click **`run_windows.bat`**. On the first run, it creates `.venv` and installs the `PyQt6` dependency from PyPI. An internet connection is needed for this first setup.
4. The application opens. Choose **Browse…**, select a folder, then click **Scan Folder**.

If Windows opens the `.bat` in an editor, launch Command Prompt in the extracted directory and run `run_windows.bat`.

### Alternative: manual terminal installation

```powershell
py -3 -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python main.py
```

Linux / macOS equivalents: `python3 -m venv .venv`; `.venv/bin/python -m pip install -r requirements.txt`; `.venv/bin/python main.py`.

## Using the application

- Browse and scan a local folder; tick **Include subfolders** for a recursive scan.
- Metadata appears in a sortable table: filename, extension, category, size, modification date, location.
- Use **Search** and the **Category** dropdown to filter the results.
- Select a file to see details and a preview when the file type is supported.
- Image: preview using Qt image support. Text: read-only first 8,000 characters. Audio: Play / Pause / Stop using **QtMultimedia**; actual codecs depend on the operating system.
- Use **Export CSV** to save the currently visible table. The exported filenames are protected from spreadsheet formula interpretation.
- Long scans run in a background **QThread**. Progress is displayed, and **Cancel** safely requests cancellation. A short bundled sound plays when scanning completes, if audio is available.

**Privacy / safety:** Data stays on the machine. The app reads file metadata and limited previews, and never modifies, deletes or uploads selected files. It skips hidden dot-files, dot-folders and symbolic links during scans.

## Run automated tests

Tests use the Python standard library (no extra test framework needed):

```powershell
py -3 -m unittest discover -s tests -v
```

Use the `.venv` interpreter if `py -3` points at a different Python environment. Test results are also summarised in `docs/Technical_Report.pdf` and `evidence/automated_tests.txt`.

## Performance investigation

```powershell
py -3 benchmarks\benchmark.py --demo --repeats 3 --workers 4
```

To benchmark an existing folder (note: file metadata, not contents):

```powershell
py -3 benchmarks\benchmark.py --path "C:\Users\YOURNAME\Documents" --repeats 3 --workers 4
```

The script prints per-run times and averages for sequential vs threaded metadata inspection, plus an Amdahl's Law example. It does **not** assume threads are automatically faster.

## Build a Windows executable

Double-click `build_windows.bat` (Windows + internet access required). It installs PyInstaller into `.venv` and builds the `dist/SmartFileMediaManager/` application directory. Run `SmartFileMediaManager.exe` in that directory; retain the entire directory when distributing it.

The supplied ZIP includes build scripts and an asset but **not** a precompiled Windows `.exe`. Packaging must be built and tested on a Windows computer; see `docs/BUILD_AND_VERIFICATION.md`.

## Folder structure

- `main.py`: application entry point
- `app/models.py`: file data model and filtering/formatting
- `app/scanner.py`: filesystem discovery/metadata/limited preview
- `app/workers.py`: background QThread worker and signals
- `app/view.py`: Qt widgets, file table and previews
- `app/controller.py`: event handling, worker lifecycle, export
- `app/resources.py`, `app/style.py`, `assets/`: resources and UI styling
- `tests/`: Python automated tests
- `benchmarks/`: reproducible sequential vs threaded investigation
- `docs/`: technical report, test plan, evidence templates, architecture/design notes
- `presentation/`: editable PowerPoint presentation
- `distribution/`: packaging notes

## Git

The package includes an example `.git` history and a demonstration of branch/merge development created while assembling this package. This is **not evidence of the student's personal work**. The student should make further meaningful commits while developing and testing their own submission. See `docs/GIT_WORKFLOW.md` for commands and steps to document a genuine conflict resolution and remote workflow.

## Known limitations

- Qt multimedia codec support varies by OS; previewed audio is read-only.
- The interface shows a table, not image thumbnails. Very large directories may use substantial memory because metadata is stored for all files and shown using `QTableWidget`.
- Only common extensions are categorised; unknown extensions appear as Other.
- Initial scan discovery counts files before the determinate progress bar begins.
- An actual Windows executable, Windows GUI test screenshots, Git remote activity, and the student's in-class presentation **must be completed and evidenced locally**. They are not falsely claimed as complete in this starter package.

## Technical sources

- Qt 6 `QMainWindow`: https://doc.qt.io/qt-6/qmainwindow.html
- Qt 6 threads and worker objects: https://doc.qt.io/qt-6/qthread.html
- Qt 6 `QMediaPlayer`: https://doc.qt.io/qt-6/qmediaplayer.html
- Python `concurrent.futures`: https://docs.python.org/3/library/concurrent.futures.html
- Python `unittest`: https://docs.python.org/3/library/unittest.html
- Python `time.perf_counter`: https://docs.python.org/3/library/time.html#time.perf_counter
- PyInstaller docs: https://pyinstaller.org/en/stable/
