# Windows Testing Guide

This document provides testing instructions for Windows batch files.

## Testing run-pip.bat

On Windows Command Prompt or PowerShell:

```cmd
# Test basic execution (should show startup message)
run-pip.bat

# Should create .venv directory and install dependencies
# Then start Streamlit application
```

## Testing gif-demo/demo.bat

```cmd
# Test help command
gif-demo\demo.bat help

# Test status check
gif-demo\demo.bat status

# Test setup (creates virtual environment and installs Playwright)
gif-demo\demo.bat setup

# Test pipeline (requires manual ffmpeg installation)
gif-demo\demo.bat pipeline
```

## Expected Behavior

### run-pip.bat
1. Checks Python 3.10+ availability
2. Creates `.venv` virtual environment if not exists
3. Activates virtual environment
4. Installs dependencies from requirements.txt
5. Starts Streamlit application

### gif-demo/demo.bat
1. **help**: Shows usage information
2. **status**: Checks Python, pip, virtual environment, ffmpeg
3. **setup**: Installs Python dependencies and Playwright browsers
4. **pipeline**: Limited functionality, recommends WSL/Git Bash for full features

## Limitations on Windows

1. **ffmpeg**: Must be installed manually on Windows
2. **Bash features**: Some advanced shell features not available in .bat
3. **Recommended**: Use WSL (Windows Subsystem for Linux) or Git Bash for full functionality

## WSL Alternative

For full functionality on Windows, use WSL:

```bash
# In WSL
./run.sh                     # uv version
./run-pip.sh                 # pip version  
./gif-demo/demo.sh pipeline  # Full demo generation
```