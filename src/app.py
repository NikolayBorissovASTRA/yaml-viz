"""Dynamic YAML Form Generator - Clean, production-ready implementation."""

import re
import streamlit as st
import yaml
from pathlib import Path
from typing import Any, Dict, List, Optional

import settings


class DynamicFormGenerator:
    """Generates dynamic forms from YAML templates with zero hardcoded assumptions."""

    def __init__(self):
        self.template: Optional[Dict] = None
        self.root_key: Optional[str] = None
        self.key_order: List[str] = []
        self.form_data: Dict = {}

    def load_template(self, content: str) -> bool:
        """Load and parse YAML template, detecting structure dynamically."""
        try:
            self.template = yaml.safe_load(content)
            if not isinstance(self.template, dict):
                return False

            # Auto-detect structure: single root with nested data or direct data
            values = list(self.template.values())
            if len(self.template) == 1 and isinstance(values[0], dict):
                self.root_key = list(self.template.keys())[0]
                project_data = values[0]
            else:
                self.root_key = None
                project_data = self.template

            self.key_order = list(project_data.keys())
            return True

        except yaml.YAMLError:
            return False

    def render_form(self) -> Dict:
        """Render dynamic form based on template structure."""
        if not self.template:
            st.info(settings.LOAD_TEMPLATE_INFO)
            return {}

        project_data = self.template[self.root_key] if self.root_key else self.template
        self.form_data = {}

        for key, value in project_data.items():
            self._render_field(key, value)

        return self.form_data

    def _render_field(self, key: str, value: Any) -> None:
        """Render appropriate field type based on value type."""
        label = key.replace("_", " ").title()

        if isinstance(value, str):
            result = st.text_input(
                label,
                value="" if value == settings.DEFAULT_PLACEHOLDER else value,
                key=f"{settings.FIELD_PREFIX}{key}",
            )
            if result:
                self.form_data[key] = result

        elif isinstance(value, bool):
            self.form_data[key] = st.checkbox(
                label, value=value, key=f"{settings.BOOL_PREFIX}{key}"
            )

        elif isinstance(value, (int, float)):
            self.form_data[key] = st.number_input(
                label, value=value, key=f"{settings.NUM_PREFIX}{key}"
            )

        elif isinstance(value, list) and all(isinstance(x, str) for x in value):
            result = st.multiselect(label, value, key=f"{settings.MULTI_PREFIX}{key}")
            if result:
                self.form_data[key] = result

        elif isinstance(value, dict) and self._is_category_structure(value):
            self._render_category_tabs(key, value, label)

        elif isinstance(value, dict):
            self._render_nested_object(key, value, label)

    def _render_category_tabs(self, key: str, value: Dict, label: str) -> None:
        """Render tabbed interface for category structures."""
        st.subheader(label)
        tabs = st.tabs([self._format_tab_name(k) for k in value.keys()])
        category_data = {}

        for i, (cat_key, items) in enumerate(value.items()):
            with tabs[i]:
                options = [self._format_item_display(item) for item in items]
                selected = st.multiselect(
                    f"Select from {self._format_tab_name(cat_key)}",
                    options,
                    key=f"{settings.CAT_PREFIX}{key}_{cat_key}",
                )
                if selected:
                    category_data[cat_key] = selected

        if category_data:
            self.form_data[key] = category_data

    def _render_nested_object(self, key: str, value: Dict, label: str) -> None:
        """Render nested objects using expandable sections."""
        with st.expander(label, expanded=settings.EXPANDER_EXPANDED):
            nested_data = {}
            for nested_key, nested_value in value.items():
                nested_field_key = f"{key}_{nested_key}"
                self._render_field(nested_field_key, nested_value)
                if nested_field_key in self.form_data:
                    nested_data[nested_key] = self.form_data.pop(nested_field_key)

            if nested_data:
                self.form_data[key] = nested_data

    def _is_category_structure(self, obj: Dict) -> bool:
        """Detect if object represents a category structure with named items."""
        list_values = [v for v in obj.values() if isinstance(v, list)]
        return len(list_values) >= 2 and any(
            arr and isinstance(arr[0], dict) and "name" in arr[0] for arr in list_values
        )

    def _format_tab_name(self, name: str) -> str:
        """Extract clean tab name by removing parenthetical content."""
        return name.split("(")[0].strip()

    def _format_item_display(self, item: Any) -> str:
        """Format item for display in multiselect options."""
        if isinstance(item, dict) and "name" in item:
            code_suffix = f" ({item['code']})" if "code" in item else ""
            return f"{item['name']}{code_suffix}"
        return str(item)

    def export_yaml(self) -> str:
        """Export form data as clean YAML with preserved key order."""
        if not self.form_data:
            return settings.NO_DATA_TEXT

        # Preserve original key order
        ordered_data = {
            key: self.form_data[key] for key in self.key_order if key in self.form_data
        }
        ordered_data.update(
            {k: v for k, v in self.form_data.items() if k not in ordered_data}
        )

        # Use original root structure or create minimal wrapper
        root_data = (
            {self.root_key: ordered_data}
            if self.root_key
            else (
                {settings.DEFAULT_ROOT_KEY: ordered_data}
                if ordered_data
                else ordered_data
            )
        )

        # Generate clean YAML output
        yaml_output = yaml.dump(
            root_data,
            default_flow_style=settings.YAML_FLOW_STYLE,
            indent=settings.YAML_INDENT,
            allow_unicode=settings.YAML_UNICODE,
            sort_keys=settings.YAML_SORT_KEYS,
        )
        return self._clean_yaml_quotes(yaml_output)

    def _clean_yaml_quotes(self, yaml_str: str) -> str:
        """Remove unnecessary quotes from YAML output."""
        yaml_str = re.sub(r'''(['"])(.*?)\1''', r"\2", yaml_str)
        return yaml_str

    def export_csv(self) -> str:
        """Export form data as CSV with minimal quoting."""
        if not self.form_data:
            return ""

        rows = [["key_path", "value"]]
        self._flatten_data(self.form_data, rows)

        return "\n".join(
            ",".join(self._quote_if_needed(str(cell)) for cell in row) for row in rows
        )

    def _flatten_data(self, data: Dict, rows: List, prefix: str = "") -> None:
        """Recursively flatten nested data structure."""
        for key, value in data.items():
            path = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                self._flatten_data(value, rows, path)
            elif isinstance(value, list):
                for item in value:
                    rows.append([path, item])
            else:
                rows.append([path, value])

    def _quote_if_needed(self, cell: str) -> str:
        """Only quote CSV cells that require it."""
        needs_quotes = "," in cell or '"' in cell or "\n" in cell
        if needs_quotes:
            escaped = cell.replace('"', '""')
            return f'"{escaped}"'
        return cell


def get_template_files() -> List[str]:
    """Get list of template files from the templates directory."""
    templates_dir = Path(__file__).parent.parent / "templates"
    if not templates_dir.exists():
        return []

    template_files = []
    for file_path in templates_dir.glob("*.yml"):
        template_files.append(file_path.name)
    for file_path in templates_dir.glob("*.yaml"):
        template_files.append(file_path.name)

    return sorted(template_files)


def load_template_file(filename: str) -> Optional[str]:
    """Load template file content by filename."""
    templates_dir = Path(__file__).parent.parent / "templates"
    file_path = templates_dir / filename

    if file_path.exists() and file_path.suffix.lower() in [".yml", ".yaml"]:
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                return f.read()
        except Exception:
            return None
    return None


def load_css():
    """Load external CSS styles."""
    css_file = Path(__file__).parent / "styles.css"
    if css_file.exists():
        with open(css_file) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    else:
        # Fallback inline styles if CSS file not found
        st.markdown(
            """
        <style>
        .main > div { padding-top: 0.5rem; }
        .block-container { padding: 1rem 0 0; }
        </style>
        """,
            unsafe_allow_html=True,
        )


def main():
    """Main application entry point."""
    st.set_page_config(
        page_title=settings.PAGE_TITLE,
        layout=settings.PAGE_LAYOUT,
        initial_sidebar_state=settings.SIDEBAR_STATE,
    )

    # Load external CSS
    load_css()

    # Initialize session state
    if "form_generator" not in st.session_state:
        st.session_state.form_generator = DynamicFormGenerator()

    # Initialize placeholders if not present
    if "upload_placeholder" not in st.session_state:
        st.session_state.upload_placeholder = None
    if "message_placeholder" not in st.session_state:
        st.session_state.message_placeholder = None
    if "uploaded_file" not in st.session_state:
        st.session_state.uploaded_file = None
    if "file_uploader_key" not in st.session_state:
        st.session_state.file_uploader_key = 0
    if "selected_template" not in st.session_state:
        st.session_state.selected_template = None

    app = st.session_state.form_generator

    # Header section
    st.title(settings.APP_TITLE)
    col1, col2 = st.columns([3, 1])

    with col1:
        # Create placeholders for upload form and messages
        if st.session_state.upload_placeholder is None:
            st.session_state.upload_placeholder = st.empty()
        if st.session_state.message_placeholder is None:
            st.session_state.message_placeholder = st.empty()

        # Only show upload form if no template is loaded
        if not app.template:
            # Show upload form
            with st.session_state.upload_placeholder.container():
                # Get available template files
                template_files = get_template_files()

                # Create vertical layout with dropdown first, then file uploader
                if template_files:
                    st.write("**Select Template:**")
                    selected_template = st.selectbox(
                        "Choose a template",
                        [""] + template_files,
                        key=f"template_selector_{st.session_state.file_uploader_key}",
                        label_visibility="collapsed",
                    )

                    st.write("**OR Upload File:**")
                    uploaded = st.file_uploader(
                        settings.UPLOAD_LABEL,
                        type=settings.ALLOWED_FILE_TYPES,
                        label_visibility="collapsed",
                        key=f"file_uploader_{st.session_state.file_uploader_key}",
                    )
                else:
                    # No templates available, show only file uploader
                    uploaded = st.file_uploader(
                        settings.UPLOAD_LABEL,
                        type=settings.ALLOWED_FILE_TYPES,
                        label_visibility=settings.FILE_UPLOAD_LABEL_VISIBILITY,
                        key=f"file_uploader_{st.session_state.file_uploader_key}",
                    )
                    selected_template = None

            # Handle template selection from dropdown
            if (
                selected_template
                and selected_template != st.session_state.selected_template
            ):
                st.session_state.selected_template = selected_template
                template_content = load_template_file(selected_template)
                if template_content and app.load_template(template_content):
                    # Hide upload form after successful load
                    st.session_state.upload_placeholder.empty()
                    with st.session_state.message_placeholder.container():
                        st.success(
                            f"Template '{selected_template}' loaded successfully"
                        )
                    st.rerun()

            # Handle file upload and show success message
            elif uploaded and uploaded != st.session_state.uploaded_file:
                st.session_state.uploaded_file = uploaded
                if app.load_template(uploaded.read().decode("utf-8")):
                    # Hide upload form after successful load
                    st.session_state.upload_placeholder.empty()
                    with st.session_state.message_placeholder.container():
                        pass #st.success(settings.SUCCESS_MESSAGE)
                    st.rerun()
            elif uploaded is None and st.session_state.uploaded_file is not None:
                # File was removed
                st.session_state.uploaded_file = None
                st.session_state.message_placeholder.empty()
        else:
            # Template is loaded, keep upload section hidden but show success message if needed
            if st.session_state.uploaded_file:
                with st.session_state.message_placeholder.container():
                    pass #st.success(settings.SUCCESS_MESSAGE)

        # Show Clear Form button below upload section (always in the same position)
        if app.template:
            if st.button(
                settings.CLEAR_BUTTON_TEXT,
                use_container_width=settings.USE_CONTAINER_WIDTH,
                type="secondary",
                key="clear_form_main",
            ):
                # Clear all cached data
                st.session_state.form_generator = DynamicFormGenerator()
                st.session_state.uploaded_file = None
                st.session_state.selected_template = None

                # Increment the file uploader key to force a complete reset
                st.session_state.file_uploader_key += 1

                # Clear all form field widgets that might be cached
                keys_to_delete = [
                    key
                    for key in st.session_state.keys()
                    if key.startswith(
                        (
                            settings.FIELD_PREFIX,
                            settings.BOOL_PREFIX,
                            settings.NUM_PREFIX,
                            settings.MULTI_PREFIX,
                            settings.CAT_PREFIX,
                            "file_uploader_",  # Clear all file uploader instances
                            "template_selector_",  # Clear all template selector instances
                        )
                    )
                ]
                for key in keys_to_delete:
                    del st.session_state[key]

                # Clear placeholders and recreate them
                if st.session_state.upload_placeholder:
                    st.session_state.upload_placeholder.empty()
                if st.session_state.message_placeholder:
                    st.session_state.message_placeholder.empty()

                # Reset placeholders to None so they get recreated
                st.session_state.upload_placeholder = None
                st.session_state.message_placeholder = None

                st.rerun()

    with col2:
        pass  # Clear Form button moved to below the form

    # Main content area
    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.subheader(settings.FORM_SECTION_TITLE)
        form_data = app.render_form()

        # Debug output if enabled
        if settings.SHOW_DEBUG:
            with st.expander("Debug Info"):
                st.json(form_data)

    with col2:
        st.subheader(settings.PREVIEW_SECTION_TITLE)
        preview = app.export_yaml()
        st.code(preview, language="yaml", line_numbers=settings.SHOW_LINE_NUMBERS)

        if form_data:
            col_yaml, col_csv = st.columns(2)
            with col_yaml:
                st.download_button(
                    settings.DOWNLOAD_YAML_TEXT,
                    preview,
                    settings.YAML_EXPORT_FILENAME,
                    settings.YAML_EXPORT_MIME,
                    use_container_width=settings.USE_CONTAINER_WIDTH,
                )
            with col_csv:
                st.download_button(
                    settings.DOWNLOAD_CSV_TEXT,
                    app.export_csv(),
                    settings.CSV_EXPORT_FILENAME,
                    settings.CSV_EXPORT_MIME,
                    use_container_width=settings.USE_CONTAINER_WIDTH,
                )


if __name__ == "__main__":
    main()
