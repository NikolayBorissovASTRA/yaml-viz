# Dynamic YAML Form Generator

A professional Python/Streamlit application that generates dynamic forms from YAML templates with real-time preview and export capabilities.

## ✨ Features

- **Dynamic Form Generation**: Automatically creates forms from any YAML structure
- **Real-time Preview**: Live YAML output with syntax highlighting
- **Multiple Export Formats**: Download as YAML or CSV
- **Nested Objects Support**: Handles complex hierarchical structures with expandable sections
- **All Data Types**: Supports strings, numbers, booleans, arrays, and nested objects
- **Clean UI**: Professional, responsive design with uniform styling
- **Zero Hardcoded Logic**: Works with any YAML template structure

## 📁 Project Structure

```
python-form-clean/
├── src/
│   ├── app.py          # Main application
│   ├── settings.py     # Configuration constants
│   └── styles.css      # UI styling
├── tests/
│   ├── test-flat.yml   # Simple flat structure test
│   ├── test-nested.yml # Complex nested test
│   └── ...             # Additional test files
├── run.sh              # Application launcher
├── README.md           # This file
└── pyproject.toml      # Dependencies
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- [uv](https://docs.astral.sh/uv/) package manager

### Installation

1. **Clone or download the project**
2. **Install uv** (if not already installed):
   ```bash
   curl -LsSf https://astral.sh/uv/install.sh | sh
   ```
3. **Run the application**:
   ```bash
   ./run.sh
   ```

The application will automatically:
- Install dependencies via uv
- Start the Streamlit server
- Open in your browser at `http://localhost:8501`

## 📖 Usage

### Basic Workflow

1. **Upload YAML Template**: Drag & drop or browse for a `.yaml`/`.yml` file
2. **Configure Fields**: Fill out the generated form fields
3. **Preview Changes**: See real-time YAML output in the preview panel  
4. **Export Data**: Download as YAML or CSV format

### Example YAML Templates

**Simple Configuration:**
```yaml
SimpleConfig:
  app_name: "My Application"
  version: "1.0.0"
  debug: true
  port: 8080
  features:
    - "authentication"
    - "logging"
```

**Complex Nested Structure:**
```yaml
WebApp:
  metadata:
    name: "E-commerce Platform"
    description: "Online shopping platform"
    version: "3.0"
  server:
    host: "0.0.0.0"
    port: 3000
    ssl_enabled: true
  database:
    host: "db.example.com"
    credentials:
      username: "admin"
      password: ""
```

## ⚙️ Configuration

### Settings

Edit `src/settings.py` to customize:

- **UI Settings**: Page title, layout, button text
- **Export Settings**: Default filenames, formats
- **Debug Mode**: Enable/disable debug output
- **Field Behavior**: Default values, prefixes

### Styling

Modify `src/styles.css` to customize:

- Form field appearance
- Spacing and layout
- Colors and fonts
- Responsive behavior

## 🧪 Testing

Test files are provided in the `tests/` directory:

- `test-flat.yml`: Simple flat structure
- `test-nested.yml`: Complex nested objects
- `test-mixed.yml`: Mixed data types
- `test-hierarchical.yml`: Deep hierarchical structure

Upload any test file to verify functionality.

## 🔧 Development

### Manual Installation

```bash
# Install dependencies
uv sync

# Run directly
cd src
uv run streamlit run app.py
```

### Debug Mode

Enable debug output in `src/settings.py`:

```python
SHOW_DEBUG = True
```

This adds a debug panel showing the raw form data structure.

## 📝 Technical Details

### Supported Data Types

- **Strings**: Text inputs with placeholder support
- **Numbers**: Numeric spinners with validation
- **Booleans**: Checkboxes
- **Arrays**: Multi-select dropdowns
- **Objects**: Expandable nested sections
- **Complex Structures**: Category tabs for structured data

### Key Features

- **Dynamic Structure Detection**: Automatically identifies root keys and nesting
- **Key Order Preservation**: Maintains original YAML key ordering in exports
- **Quote Removal**: Clean YAML output without unnecessary quotes
- **CSV Flattening**: Hierarchical data flattened to dot-notation paths
- **Session Management**: Form state preserved during browser session

## 🛠️ Architecture

The application follows a modular design:

- **DynamicFormGenerator**: Core form generation engine
- **Settings Module**: Centralized configuration
- **External CSS**: Separated styling concerns
- **Type-based Rendering**: Field types determined by value analysis

## 📄 License

This project is provided as-is for educational and professional use.

## 🤝 Contributing

To contribute:

1. Follow the existing code patterns
2. Update tests for new features
3. Maintain the clean, professional design
4. Document any configuration changes

---

**Professional Dynamic Form Generator** - Built with Python, Streamlit, and modern development practices.