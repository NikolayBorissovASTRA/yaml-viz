@echo off
echo Starting Dynamic YAML Form Generator (pip version)...

REM Check Python version
python -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)" >nul 2>&1
if %errorlevel% neq 0 (
    echo Python 3.10+ required
    echo Please install Python from https://python.org/downloads/
    pause
    exit /b 1
)

REM Create virtual environment if it doesn't exist
if not exist ".venv" (
    echo Creating virtual environment...
    python -m venv .venv
)

REM Activate virtual environment
echo Activating virtual environment...
call .venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip
pip install -r requirements.txt

REM Start Streamlit app
echo Starting Streamlit application...
echo Access the app at: http://localhost:8501
echo Press Ctrl+C to stop

python -m streamlit run src/app.py

pause