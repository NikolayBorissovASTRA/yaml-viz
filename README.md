
# Dynamic YAML Form Generator

A clean, modular Streamlit application that generates dynamic forms from YAML templates with built-in validation and export capabilities.


![Dynamic YAML Form Generator Demo](demo.gif)


## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Either [uv](https://docs.astral.sh/uv/) (recommended) or pip package manager

### Installation

Choose one of the following methods:

#### Option A: Using uv (Recommended)

1. **Clone or download the project**
2. **Install uv**:
```sh
curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. **Run the application**:
```sh
./run.sh
```

#### Option B: Using pip

1. **Clone or download the project**
2. **Run the application**:

**Linux/macOS:**
```sh
./run-pip.sh
```

**Windows:**
```cmd
run-pip.bat
```

Both methods will automatically:
- Install dependencies (in virtual environment)
- Start the Streamlit server  
- Open in your browser at `http://localhost:8501`

## 🏗️ Architecture

### System Overview

```mermaid
graph TB
    %% Main Application Layer
    subgraph "Main Application"
        APP[app.py<br/>Main Orchestrator<br/>47 lines]
    end

    %% Configuration Layer
    subgraph "Configuration"
        SETTINGS[settings.py<br/>App Settings<br/>Constants & Config]
    end

    %% UI Layer
    subgraph "UI Components"
        UI[ui_components.py<br/>UIComponents Class<br/>Streamlit UI Logic]
    end

    %% Business Logic Layer
    subgraph "Business Logic"
        FORM[form_generator.py<br/>FormGenerator Class<br/>Core Form Logic]
        EXPORT[export_utils.py<br/>ExportUtils Class<br/>YAML/CSV Export & Validation]
        TEMPLATE[template_manager.py<br/>TemplateManager Class<br/>File Operations]
    end

    %% External Dependencies
    subgraph "External"
        ST[Streamlit Framework]
        YAML[PyYAML Library]
        FILES[Template Files<br/>templates/*.yml]
    end

    %% Main Flow
    APP --> UI
    APP --> SETTINGS
    
    %% UI Dependencies
    UI --> FORM
    UI --> EXPORT
    UI --> TEMPLATE
    UI --> SETTINGS
    UI --> ST
    
    %% Business Logic Dependencies
    FORM --> YAML
    FORM --> SETTINGS
    FORM --> ST
    
    EXPORT --> YAML
    EXPORT --> SETTINGS
    
    TEMPLATE --> FILES
    
    %% Styling
    classDef mainApp fill:#e1f5fe
    classDef config fill:#f3e5f5
    classDef ui fill:#e8f5e8
    classDef business fill:#fff3e0
    classDef external fill:#fce4ec
    
    class APP mainApp
    class SETTINGS config
    class UI ui
    class FORM,EXPORT,TEMPLATE business
    class ST,YAML,FILES external
```

### Module Structure

- **`app.py`** (47 lines) - Clean main orchestration layer
- **`form_generator.py`** - Core form generation logic (separated from UI)  
- **`export_utils.py`** - YAML/CSV export and validation utilities
- **`template_manager.py`** - Template file loading and management
- **`ui_components.py`** - All Streamlit UI logic and components
- **`settings.py`** - Cleaned up configuration constants

### Automated GIF Demo Generation

Generate a professional demo GIF automatically using Playwright. Works with both uv and pip installations:

**Linux/macOS:**
```sh
# Complete pipeline (auto-detects uv or pip)
./gif-demo/demo.sh pipeline

# Individual commands
./gif-demo/demo.sh setup     # One-time setup
./gif-demo/demo.sh status    # Check dependencies
./gif-demo/demo.sh generate  # Generate GIF (requires running app)

# Custom configuration
GIF_NAME=highway-demo.gif SIZE_LIMIT_MB=0.8 ./gif-demo/demo.sh pipeline
```

**Windows:**
```cmd
REM Basic Windows support
gif-demo\demo.bat status    
gif-demo\demo.bat setup     
gif-demo\demo.bat pipeline  

REM For full functionality, use WSL or Git Bash:
bash gif-demo/demo.sh pipeline
```

The demo script automatically detects whether you're using uv or pip and adapts accordingly.

**Platform Notes:**
- **Linux/macOS**: Full functionality with automatic dependency detection
- **Windows**: Basic support via .bat files, full features available via WSL/Git Bash
- **Dependencies**: Automatically installs Playwright and Python packages, ffmpeg installation varies by platform

See `./gif-demo/demo.sh help` or `gif-demo\demo.bat help` for configuration options.


