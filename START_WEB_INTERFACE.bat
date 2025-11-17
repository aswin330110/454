@echo off
echo ================================================================================
echo           ADVANCED GIT ZIP EXTRACTOR - WEB INTERFACE
echo ================================================================================
echo.
echo Starting web server...
echo.
echo Once started, open your browser and go to:
echo.
echo    http://localhost:5000
echo.
echo Press Ctrl+C to stop the server when done
echo.
echo ================================================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.7 or higher from https://www.python.org
    pause
    exit /b 1
)

REM Check if dependencies are installed
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo Installing required dependencies...
    echo.
    pip install -r requirements.txt
    echo.
)

REM Start the web application
python web_app.py

pause
