# Streamlit Version Compatibility

This document explains the cross-platform Streamlit compatibility implemented in this project.

## Issue

The `label_visibility` parameter was introduced in Streamlit 1.16.0, but some environments (particularly Windows) may have older versions (e.g., 1.12.0) installed, causing:

```
TypeError: selectbox() got an unexpected keyword argument 'label_visibility'
```

## Solution

The project implements automatic version detection and compatibility:

### Compatibility Functions

**`_supports_label_visibility()`**
- Checks if current Streamlit version >= 1.16.0
- Returns boolean indicating support

**`_get_selectbox_kwargs()`** and **`_get_file_uploader_kwargs()`**
- Build parameter dictionaries compatible with current Streamlit version
- Include `label_visibility` only if supported

### Implementation Example

```python
# Before (incompatible with old versions)
st.selectbox("Choose", options=["A", "B"], label_visibility="collapsed")

# After (compatible with all versions)
kwargs = _get_selectbox_kwargs(
    label="Choose", 
    options=["A", "B"], 
    label_visibility="collapsed"
)
st.selectbox(**kwargs)
```

## Version Support

| Streamlit Version | Status | label_visibility | Behavior |
|------------------|--------|------------------|----------|
| 1.12.0 - 1.15.x | ✅ Supported | ❌ Ignored | Labels show normally |
| 1.16.0+ | ✅ Supported | ✅ Applied | Labels can be collapsed |

## Dependencies

- **packaging>=21.0** - Required for version comparison
- **streamlit>=1.12.0** - Minimum supported version

## Testing

The compatibility functions are automatically tested when the application runs. You can verify compatibility by:

```bash
# Check demo script status (shows Streamlit version)
./gif-demo/demo.sh status

# Run the application (uses compatibility functions)
./run.sh  # uv
./run-pip.sh  # pip
```

The application will automatically adapt to your Streamlit version without any manual intervention.

## Platform Impact

| Platform | Streamlit Version | Impact | Solution |
|----------|------------------|--------|----------|
| **macOS** | Latest (1.48+) | None | Full functionality |
| **Windows** | Often older (1.12+) | `label_visibility` ignored | UI still works, labels visible |
| **Linux** | Varies | Auto-detected | Adapts to installed version |

## Benefits

1. **Cross-platform compatibility** - Works on Windows with older Streamlit
2. **No functionality loss** - UI remains fully functional
3. **Future-proof** - Automatically uses new features when available
4. **No user action required** - Compatibility handled transparently

## Windows Testing Guide

This section provides detailed testing instructions for Windows environments.

### Testing run-pip.bat

On Windows Command Prompt or PowerShell:

```cmd
# Test basic execution (should show startup message)
run-pip.bat

# Should create .venv directory and install dependencies
# Then start Streamlit application
```

### Testing gif-demo/demo.bat

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

### Expected Behavior

#### run-pip.bat
1. Checks Python 3.10+ availability
2. Creates `.venv` virtual environment if not exists
3. Activates virtual environment
4. Installs dependencies from requirements.txt
5. Starts Streamlit application

#### gif-demo/demo.bat
1. **help**: Shows usage information
2. **status**: Checks Python, pip, virtual environment, ffmpeg
3. **setup**: Installs Python dependencies and Playwright browsers
4. **pipeline**: Limited functionality, recommends WSL/Git Bash for full features

### Windows Limitations

1. **ffmpeg**: Must be installed manually on Windows
2. **Bash features**: Some advanced shell features not available in .bat
3. **Recommended**: Use WSL (Windows Subsystem for Linux) or Git Bash for full functionality

### WSL Alternative

For full functionality on Windows, use WSL:

```bash
# In WSL
./run.sh                     # uv version
./run-pip.sh                 # pip version  
./gif-demo/demo.sh pipeline  # Full demo generation
```