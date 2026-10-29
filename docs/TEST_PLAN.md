# Tasks 9–12 — Test plan and manual results

**Important:** Automated results are recorded in `evidence/automated_tests.txt`. The manual results below are intentionally **NOT RUN** until a tester performs these steps on a computer with PyQt6 installed. Fill in actual results, date, platform and screenshots.

| ID | Requirement | Test / input and conditions | Expected result | Actual result | Pass/fail |
|---|---|---|---|---|---|
| MT01 | FR01 | Browse and select an existing directory | Folder path shown | NOT RUN | Pending |
| MT02 | FR02 | Scan known folder with 5 files; repeat with subfolders disabled | Correct files shown in each case | NOT RUN | Pending |
| MT03 | FR03 | Click Size table heading twice | Table sorts by numeric file size | NOT RUN | Pending |
| MT04 | FR04 | Search mixed-case partial name, then filter Images | Only matching image files shown | NOT RUN | Pending |
| MT05 | FR05 | Select PNG, TXT and unsupported ZIP | Image/text preview or sensible unsupported message | NOT RUN | Pending |
| MT06 | FR06 | Select supported WAV, press Play/Pause/Stop | Audio responds without crashing; codec errors reported | NOT RUN | Pending |
| MT07 | FR07 | Scan directory with many files, then Cancel | Scan stops; UI remains responsive | NOT RUN | Pending |
| MT08 | FR07 | After Cancel, immediately start another scan | New scan starts and completes safely | NOT RUN | Pending |
| MT09 | FR08 | Filter Images and export to CSV | CSV contains the currently visible records | NOT RUN | Pending |
| MT10 | FR09 | Scan invalid/removed folder and try export to protected location | Clear warning; no app crash | NOT RUN | Pending |
| MT11 | FR03 | Scan an empty folder (boundary) | Empty table, 0 files, no crash | NOT RUN | Pending |
| MT12 | FR09 | Remove a file between discovery and metadata reading (exception) | Error counted; other files still shown | NOT RUN | Pending |
| MT13 | FR07 | Close window during a large scan (exception) | Safe cancellation and exit, no QThread warning | NOT RUN | Pending |
| MT14 | FR02 | Scan large folder (e.g., >1000 files) | Progress advances and GUI still responds | NOT RUN | Pending |

## Automated tests

Run `python -m unittest discover -s tests -v` and retain `evidence/automated_tests.txt` plus terminal screenshots. Tests cover normal, boundary, invalid and exceptional inputs, as well as safe CSV export.

## Defect / correction record — fill from actual work

| Date | Problem and reproduction | Probable cause | Fix / commit ID | Retest and result |
|---|---|---|---|---|
| — | No verified GUI defects recorded yet | — | — | Pending GUI testing |

### Tester details

- Tester:
- Date:
- Operating system and Python version:
- PyQt6 version:
- Evidence screenshots: (place them in `evidence/`)
