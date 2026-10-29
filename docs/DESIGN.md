# Task 1 — Requirements and application design

## 1.1 Application purpose

Smart File & Media Manager helps a user organise information about files on their computer without opening each file individually. Users can scan a folder, see file names, types, sizes and modification dates, search the results and preview supported images, text and audio. The application is intended for ordinary computer users with a large collection of mixed files. It does not modify or upload the selected files.

## 1.2 Functional requirements

| ID | Requirement | Verification |
|---|---|---|
| FR01 | The user shall be able to choose an existing local folder. | MT01, AT01 |
| FR02 | The user shall be able to scan the selected folder, optionally including subfolders. | MT02, AT02 |
| FR03 | The application shall show metadata for discovered files in a sortable table. | MT03, AT03 |
| FR04 | The user shall be able to search filenames/paths and filter by file category. | MT04, AT04 |
| FR05 | The application shall show limited text and image previews for supported items. | MT05, AT05 |
| FR06 | The application shall support audio playback for suitable audio files using QtMultimedia. | MT06 |
| FR07 | The user shall be able to cancel a background scan and see progress/status safely. | MT07, MT08, AT06 |
| FR08 | The user shall be able to export the currently filtered file list to CSV. | MT09, AT07 |
| FR09 | The application shall warn the user if a folder cannot be accessed or an export fails. | MT10, AT08 |

## 1.3 Initial GUI wireframe

```
+---------------------------------------------------------------------+
| File menu: Open Folder | Export CSV | Exit     Help: About           |
| SMART FILE & MEDIA MANAGER                                          |
| Folder: [C:\...                                    ] [Browse]         |
| [x] Include subfolders      [Scan Folder] [Cancel]                   |
| Search: [................]  Category: [All Files v]                  |
|                                                                     |
| +---------------------------------------+ +-----------------------+ |
| | NAME  TYPE CATEGORY SIZE DATE  FOLDER | | Preview               | |
| | file...                               | | details / image /     | |
| |                                       | | text / audio controls | |
| +---------------------------------------+ +-----------------------+ |
| 0 files | 0 B total    [===========progress===========]             |
| Status: Ready.                                                       |
+---------------------------------------------------------------------+
```

## 1.4 Architecture

- **Model:** `app/models.py` and `app/scanner.py` contain immutable file records, validation, filtering and file processing.
- **View:** `app/view.py` builds Qt widgets, shows file records, displays previews and updates progress and status.
- **Controller:** `app/controller.py` connects UI signals to operations, handles validation and CSV export, and manages the background scan lifecycle.
- **Worker:** `app/workers.py` runs slow file discovery/metadata reading on a `QThread`. A `threading.Event` communicates cancellation. The worker emits Qt signals, and the controller is the sole owner of GUI state.

Data flow: **User action → View signal → Controller → Scanner/Model (in QThread for scanning) → Qt signal → Controller → View**.
