# Windows packaging and verification evidence — TO COMPLETE ON WINDOWS

The source package includes `run_windows.bat` and `build_windows.bat`, but a Windows EXE cannot be reliably built or tested in the Linux package assembly environment.

1. On Windows, extract the entire ZIP.
2. Run `run_windows.bat` and test scanning a folder, searching, previewing, exporting CSV and cancelling a long scan.
3. Run `build_windows.bat`. Confirm `dist/SmartFileMediaManager/SmartFileMediaManager.exe` is produced.
4. Run that EXE **from outside the source folder** (copy the entire `dist/SmartFileMediaManager` directory).
5. Verify browse/scan, progress, export and audio playback (if the machine supports the selected audio codec).
6. Add screenshots in `evidence/` and record the test results in `docs/TEST_PLAN.md`.

Do not claim a successful Windows deployment until these steps have actually been completed.
