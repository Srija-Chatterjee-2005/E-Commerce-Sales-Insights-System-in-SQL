@echo off
cd /d "%~dp0"
python app.py
if errorlevel 1 (
 echo.
 echo Python was not found. Install Python 3, then run this file again.
 pause
)
