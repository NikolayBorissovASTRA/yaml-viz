# Dynamic YAML Form Generator - Architecture

## System Architecture Diagram

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

## Class Relationships

```mermaid
classDiagram
    class UIComponents {
        +load_css() void
        +initialize_session_state() void
        +render_template_loader() void
        +render_preview_section(form_data: Dict) void
        -_render_upload_form() void
        -_handle_template_selection() void
        -_render_export_controls() void
        -_clear_form() void
    }

    class FormGenerator {
        -template: Dict
        -root_key: str
        -key_order: List[str]
        -form_data: Dict
        +load_template(content: str) bool
        +render_form() Dict
        +get_structured_data() Dict
        -_render_field() void
        -_render_category_tabs() void
        -_render_nested_object() void
        -_is_category_structure() bool
    }

    class ExportUtils {
        +export_yaml(data: Dict)$ str
        +validate_yaml(data: Dict)$ Tuple[bool, str]
        +export_csv(data: Dict)$ str
        -_clean_yaml_quotes(yaml_str: str)$ str
        -_flatten_data(data: Dict, rows: List)$ void
        -_quote_if_needed(cell: str)$ str
    }

    class TemplateManager {
        +get_template_files()$ List[str]
        +load_template_file(filename: str)$ str
    }

    class Streamlit {
        <<external>>
    }

    class PyYAML {
        <<external>>
    }

    class FileSystem {
        <<external>>
    }

    UIComponents --> FormGenerator : uses
    UIComponents --> ExportUtils : uses
    UIComponents --> TemplateManager : uses
    FormGenerator --> Streamlit : renders_UI
    ExportUtils --> PyYAML : processes
    TemplateManager --> FileSystem : reads
```

## Data Flow

```mermaid
sequenceDiagram
    participant User
    participant App as app.py
    participant UI as UIComponents
    participant TM as TemplateManager
    participant FG as FormGenerator
    participant EU as ExportUtils

    User->>App: Launch Application
    App->>UI: initialize_session_state()
    App->>UI: load_css()
    
    User->>UI: Upload/Select Template
    UI->>TM: load_template_file()
    TM-->>UI: template_content
    UI->>FG: load_template(content)
    FG-->>UI: success/failure
    
    User->>FG: Fill Form Fields
    FG->>FG: render_form()
    FG-->>UI: form_data
    
    UI->>FG: get_structured_data()
    FG-->>UI: structured_data
    UI->>EU: export_yaml(data)
    EU-->>UI: yaml_preview
    
    User->>UI: Click Validate YAML
    UI->>EU: validate_yaml(data)
    EU-->>UI: validation_result
    
    User->>UI: Download YAML/CSV
    UI->>EU: export_yaml()/export_csv()
    EU-->>User: file_download
```

## Module Dependencies

```mermaid
graph LR
    subgraph "Dependency Layers"
        L1[Layer 1: Main App]
        L2[Layer 2: UI Components]
        L3[Layer 3: Business Logic]
        L4[Layer 4: External Libraries]
    end
    
    L1 --> L2
    L2 --> L3
    L3 --> L4
    
    subgraph "Layer 1"
        app[app.py]
    end
    
    subgraph "Layer 2"
        ui[ui_components.py]
        settings[settings.py]
    end
    
    subgraph "Layer 3"
        form[form_generator.py]
        export[export_utils.py]
        template[template_manager.py]
    end
    
    subgraph "Layer 4"
        streamlit[Streamlit]
        yaml[PyYAML]
        typing[Typing]
        pathlib[Pathlib]
        re[Re]
    end
```

## Key Benefits of This Architecture

1. **Modularity**: Each module has a single, well-defined responsibility
2. **Testability**: Business logic separated from UI makes unit testing easier
3. **Maintainability**: Changes in one module minimally impact others
4. **Reusability**: Core logic can be reused in different contexts
5. **Clarity**: Clear separation of concerns makes code easier to understand
6. **Scalability**: Easy to extend with new features or modify existing ones
