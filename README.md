
# Dynamic YAML Form Generator

A clean, modular Streamlit application that generates dynamic forms from YAML templates with built-in validation and export capabilities.

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

1. **Clone or download the project**
2. **Install uv** (if not already installed):
```sh
   curl -LsSf https://astral.sh/uv/install.sh | sh
```

3. **Run the application**:
```sh
   ./run.sh
```

The application will automatically:
- Install dependencies via uv
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

### Key Benefits

1. **Modularity**: Each module has a single, well-defined responsibility
2. **Testability**: Business logic separated from UI makes unit testing easier
3. **Maintainability**: Changes in one module minimally impact others
4. **Reusability**: Core logic can be reused in different contexts
5. **Clarity**: Clear separation of concerns makes code easier to understand
6. **Scalability**: Easy to extend with new features or modify existing ones
