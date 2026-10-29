# Assessment 2 — All 15 tasks mapped to evidence

This checklist is based on the 7-page Advanced Programming Assessment 2 brief. "Code provided" is **not** the same as "tested and verified on Windows".

| Task | Project evidence | Status before student testing |
|---|---|---|
| 1. Requirements and design | `docs/DESIGN.md`; `docs/Technical_Report.pdf` sections 1–3 | Written |
| 2. PyQt application | `main.py`; `app/view.py`; menus, widgets, status bar, dialogs, table | Code provided; GUI verification pending |
| 3. Events and signals | `app/controller.py`; `app/workers.py` | Code provided; GUI verification pending |
| 4. MVC separation | `app/models.py`, `scanner.py`, `view.py`, `controller.py`; report | Designed and implemented; GUI verification pending |
| 5. Multimedia | `QMediaPlayer`, `QAudioOutput`, `QSoundEffect`, `assets/complete.wav` | Code provided; media playback verification pending |
| 6. Concurrency | `ScanWorker`, `QThread`, background status/progress/cancellation | Code provided; GUI responsiveness verification pending |
| 7. Thread safety | `threading.Event` cancellation; worker→controller Qt signals; main-thread GUI ownership | Code and explanation provided; GUI verification pending |
| 8. Performance/parallelism | `benchmarks/benchmark.py`; `evidence/benchmark_results.*`; Amdahl analysis in report | Performed on 800 demo files in Linux assembly environment; repeat on your PC |
| 9. Formal test plan | `docs/TEST_PLAN.md`; `docs/Test_Plan.pdf` | Prepared |
| 10. Manual testing | 14 written test cases, with expected result and blank actual outcome | **Pending Windows GUI manual runs and screenshots** |
| 11. Automated tests | `tests/`; `evidence/automated_tests.txt` | **30 automated non-GUI tests passed** |
| 12. Debugging | Defect/correction log in test plan | **Actual GUI defects/fixes to document when found** |
| 13. Git | included `.git` history, `docs/GIT_WORKFLOW.md`, `evidence/git_conflict_demo.txt` | Example local commits/branch/merge/conflict; **student development and remote activity pending** |
| 14. Distribution | `build_windows.bat`; `requirements-build.txt`; `docs/BUILD_AND_VERIFICATION.md` | Build scripts provided; **Windows executable and deployment verification pending** |
| 15. Documentation and presentation | `docs/Technical_Report.pdf`; `presentation/Project_Presentation.pptx` | Materials prepared; **in-class live presentation pending** |

## Official deliverables

1. Full code (`main.py` + `app/`).
2. Git history (`.git/`) plus additional lecturer-approved Git submission proof.
3. Automated test scripts (`tests/`).
4. Test plan and results (`docs/Test_Plan.pdf`, `docs/TEST_PLAN.md`, `evidence/`).
5. Technical report (`docs/Technical_Report.pdf`).
6. Performance investigation (`benchmarks/`, `evidence/benchmark_results.*`, report).
7. Build configuration (`build_windows.bat`, `requirements-build.txt`) plus successful Windows packaging evidence after local testing.
8. README (`README.md`).

Extra Task 15 requirement: presentation slides (`presentation/Project_Presentation.pptx`) and in-class project demonstration.

## Suggested first real local check

1. Extract ZIP on Windows and run `run_windows.bat` with an internet connection.
2. Choose a folder with several known files and start a scan.
3. Search, filter, preview text/image/audio, export CSV, cancel and restart.
4. Capture actual results/screenshots and update the test plan.
5. Build executable with `build_windows.bat` and verify it outside the source folder.
