@echo off
setlocal enabledelayedexpansion

if "%1"=="" goto help
if "%1"=="help" goto help
if "%1"=="status" goto status
if "%1"=="setup" goto setup
if "%1"=="pipeline" goto pipeline
goto help

:help
echo GIF Demo Generator (Windows)
echo Usage: %0 [COMMAND]
echo.
echo Commands:
echo   setup     Install dependencies (Playwright, ffmpeg)
echo   pipeline  Complete pipeline (setup, start app, generate, cleanup)
echo   status    Check installation and dependencies
echo   help      Show this help
echo.
echo Note: This Windows version supports basic commands.
echo For full functionality, use WSL or git-bash with demo.sh
echo.
echo Environment Variables (Configuration):
echo   SET GIF_NAME=demo.gif
echo   SET SIZE_LIMIT_MB=1.0
echo   SET PROJECT_NAME=Highway Construction Demo
echo.
echo Examples:
echo   %0 status                              # Check dependencies
echo   SET GIF_NAME=custom.gif ^& %0 pipeline  # Custom GIF name
goto end

:status
echo 🔍 Checking installation status...
echo.

REM Check Python
python --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=*" %%i in ('python --version 2^>^&1') do echo ✅ %%i
) else (
    echo ❌ Python not found
)

REM Check pip
pip --version >nul 2>&1
if %errorlevel% equ 0 (
    for /f "tokens=1,2" %%i in ('pip --version 2^>^&1') do echo ✅ pip found: %%i %%j
) else (
    echo ❌ pip not found
)

REM Check virtual environment
if exist "..\\.venv" (
    echo ✅ Virtual environment found (.venv)
) else (
    echo ⚠️  Virtual environment not found (run: run-pip.bat)
)

REM Check ffmpeg
ffmpeg -version >nul 2>&1
if %errorlevel% equ 0 (
    echo ✅ ffmpeg found
) else (
    echo ❌ ffmpeg not found (install from https://ffmpeg.org/)
)

echo.
echo 💡 Package manager: pip
echo    Use: run-pip.bat to start the app
echo    Note: For full demo features, consider using WSL or git-bash
goto end

:setup
echo Setting up dependencies for Windows...
echo.

if not exist "..\\.venv" (
    echo Creating virtual environment...
    cd ..
    python -m venv .venv
    cd gif-demo
)

echo Activating virtual environment and installing dependencies...
cd ..
call .venv\\Scripts\\activate.bat
python -m pip install --upgrade pip
pip install -r requirements.txt
pip install playwright
python -m playwright install chromium

echo.
echo ⚠️  Note: You need to install ffmpeg separately:
echo    1. Download from: https://ffmpeg.org/download.html#build-windows
echo    2. Extract and add to PATH
echo    3. Or use chocolatey: choco install ffmpeg

cd gif-demo
echo Setup complete (except ffmpeg)
goto end

:pipeline
echo Starting GIF demo pipeline (Windows)...
echo.
echo ⚠️  Limited Windows support. For full functionality:
echo    - Install ffmpeg manually
echo    - Consider using WSL or git-bash
echo    - Or run: demo.sh pipeline (in git-bash/WSL)
echo.

if not exist "..\\.venv" (
    echo Virtual environment not found. Running setup first...
    call :setup
)

echo Checking if Streamlit app is running...
curl -s http://localhost:8501 >nul 2>&1
if %errorlevel% neq 0 (
    echo Starting Streamlit app...
    cd ..
    call .venv\\Scripts\\activate.bat
    start /B python -m streamlit run src\\app.py
    cd gif-demo
    
    echo Waiting for app to start...
    timeout /t 10 /nobreak >nul
)

echo.
echo ⚠️  Manual steps required:
echo 1. Ensure Streamlit app is running at http://localhost:8501
echo 2. Ensure ffmpeg is installed and in PATH
echo 3. Run: python create-interactive-gif.py
echo.
echo For automated pipeline, use WSL: ./demo.sh pipeline

:end