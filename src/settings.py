"""Application settings and configuration constants."""

# Page configuration
PAGE_TITLE = "Dynamic YAML Form"
PAGE_LAYOUT = "wide"
SIDEBAR_STATE = "collapsed"

# Application strings
APP_TITLE = "Dynamic YAML Form Generator"
UPLOAD_LABEL = "Upload YAML Template"
CLEAR_BUTTON_TEXT = "Clear Form"
FORM_SECTION_TITLE = "Configuration Form"
PREVIEW_SECTION_TITLE = "Live Preview"
LOAD_TEMPLATE_INFO = "Load a YAML template to start"
NO_DATA_TEXT = "No data"
SUCCESS_MESSAGE = "Template loaded successfully"

# File upload settings
ALLOWED_FILE_TYPES = ["yaml", "yml"]
FILE_UPLOAD_LABEL_VISIBILITY = "collapsed"
DRAG_DROP_TEXT = "Drag and drop file here"
BROWSE_FILES_TEXT = "Browse files"

# Export settings
YAML_EXPORT_FILENAME = "config.yaml"
YAML_EXPORT_MIME = "text/yaml"
CSV_EXPORT_FILENAME = "config.csv"
CSV_EXPORT_MIME = "text/csv"
DOWNLOAD_YAML_TEXT = "Download YAML"
DOWNLOAD_CSV_TEXT = "Download CSV"
VALIDATE_YAML_TEXT = "Validate YAML"


# Form field settings
FIELD_PREFIX = "field_"
BOOL_PREFIX = "bool_"
NUM_PREFIX = "num_"
MULTI_PREFIX = "multi_"
CAT_PREFIX = "cat_"

# UI settings
EXPANDER_EXPANDED = True
USE_CONTAINER_WIDTH = True
SHOW_LINE_NUMBERS = False
SHOW_DEBUG = False  # Set to True to enable debug output

# YAML export settings
YAML_FLOW_STYLE = False
YAML_INDENT = 2
YAML_UNICODE = True
YAML_SORT_KEYS = False
