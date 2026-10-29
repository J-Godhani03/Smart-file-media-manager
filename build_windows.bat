@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
 echo Run run_windows.bat once before building.
 pause
 exit /b 1
)
".venv\Scripts\python.exe" -m pip install -r requirements-build.txt
if errorlevel 1 goto :fail
".venv\Scripts\python.exe" -m PyInstaller --noconfirm --clean --windowed --name SmartFileMediaManager --add-data "assets\complete.wav;assets" main.py
if errorlevel 1 goto :fail
echo Build complete. Run dist\SmartFileMediaManager\SmartFileMediaManager.exe
pause
exit /b 0
:fail
echo Build failed. See errors above.
pause
exit /b 1
