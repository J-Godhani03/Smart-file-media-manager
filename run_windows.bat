@echo off
setlocal
cd /d "%~dp0"
where py >nul 2>&1
if not errorlevel 1 (set "PY=py -3") else (set "PY=python")
if not exist ".venv\Scripts\python.exe" (
  echo Creating Python environment...
  %PY% -m venv .venv
  if errorlevel 1 goto :fail
)
if not exist ".venv\installed.ok" (
  echo Installing PyQt6 (internet connection needed for first run)...
  ".venv\Scripts\python.exe" -m pip install -r requirements.txt
  if errorlevel 1 goto :fail
  echo installed > ".venv\installed.ok"
)
".venv\Scripts\python.exe" main.py
if errorlevel 1 goto :fail
exit /b 0
:fail
echo.
echo Startup failed. Check that Python 3.11+ is installed and PyQt6 installation succeeded.
pause
exit /b 1
