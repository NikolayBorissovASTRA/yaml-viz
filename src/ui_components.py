"""Streamlit UI components and layout management."""

import streamlit as st
from pathlib import Path
from typing import Dict
from packaging import version

import settings
from form_generator import FormGenerator
from export_utils import ExportUtils
from template_manager import TemplateManager


def _supports_label_visibility() -> bool:
    """Check if current Streamlit version supports label_visibility parameter."""
    return version.parse(st.__version__) >= version.parse("1.16.0")


def _supports_line_numbers() -> bool:
    """Check if current Streamlit version supports line_numbers parameter in st.code()."""
    return version.parse(st.__version__) >= version.parse("1.28.0")


def _supports_rerun() -> bool:
    """Check if current Streamlit version supports st.rerun() (vs st.experimental_rerun())."""
    return version.parse(st.__version__) >= version.parse("1.18.0")


def _supports_use_container_width() -> bool:
    """Check if current Streamlit version supports use_container_width parameter for buttons."""
    return version.parse(st.__version__) >= version.parse("1.13.0")


def _get_selectbox_kwargs(label: str, options: list, key: str = None, label_visibility: str = None) -> dict:
    """Get selectbox kwargs compatible with current Streamlit version."""
    kwargs = {
        "label": label,
        "options": options
    }
    if key:
        kwargs["key"] = key
    if label_visibility and _supports_label_visibility():
        kwargs["label_visibility"] = label_visibility
    return kwargs


def _get_file_uploader_kwargs(label: str, type: list = None, key: str = None, label_visibility: str = None) -> dict:
    """Get file_uploader kwargs compatible with current Streamlit version."""
    kwargs = {
        "label": label
    }
    if type:
        kwargs["type"] = type
    if key:
        kwargs["key"] = key
    if label_visibility and _supports_label_visibility():
        kwargs["label_visibility"] = label_visibility
    return kwargs


def _get_code_kwargs(body: str, language: str = None, line_numbers: bool = None) -> dict:
    """Get st.code kwargs compatible with current Streamlit version."""
    kwargs = {
        "body": body
    }
    if language:
        kwargs["language"] = language
    if line_numbers is not None and _supports_line_numbers():
        kwargs["line_numbers"] = line_numbers
    return kwargs


def _rerun_app() -> None:
    """Rerun the Streamlit app using compatible method."""
    if _supports_rerun():
        st.rerun()
    else:
        st.experimental_rerun()


def _get_button_kwargs(label: str, key: str = None, help: str = None, 
                      on_click=None, args=None, kwargs=None, type: str = "secondary", 
                      disabled: bool = False, use_container_width: bool = None) -> dict:
    """Get st.button kwargs compatible with current Streamlit version."""
    button_kwargs = {
        "label": label
    }
    if key:
        button_kwargs["key"] = key
    if help:
        button_kwargs["help"] = help
    if on_click:
        button_kwargs["on_click"] = on_click
    if args:
        button_kwargs["args"] = args
    if kwargs:
        button_kwargs["kwargs"] = kwargs
    if type != "secondary":
        button_kwargs["type"] = type
    if disabled:
        button_kwargs["disabled"] = disabled
    if use_container_width is not None and _supports_use_container_width():
        button_kwargs["use_container_width"] = use_container_width
    return button_kwargs


def _get_download_button_kwargs(label: str, data, file_name: str = None, mime: str = None,
                               key: str = None, help: str = None, on_click=None, args=None, 
                               kwargs=None, disabled: bool = False, use_container_width: bool = None) -> dict:
    """Get st.download_button kwargs compatible with current Streamlit version."""
    download_kwargs = {
        "label": label,
        "data": data
    }
    if file_name:
        download_kwargs["file_name"] = file_name
    if mime:
        download_kwargs["mime"] = mime
    if key:
        download_kwargs["key"] = key
    if help:
        download_kwargs["help"] = help
    if on_click:
        download_kwargs["on_click"] = on_click
    if args:
        download_kwargs["args"] = args
    if kwargs:
        download_kwargs["kwargs"] = kwargs
    if disabled:
        download_kwargs["disabled"] = disabled
    if use_container_width is not None and _supports_use_container_width():
        download_kwargs["use_container_width"] = use_container_width
    return download_kwargs


class UIComponents:
    """Handles Streamlit UI components and interactions."""

    @staticmethod
    def load_css() -> None:
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

    @staticmethod
    def initialize_session_state() -> None:
        """Initialize all session state variables."""
        session_defaults = {
            "form_generator": FormGenerator(),
            "upload_placeholder": None,
            "message_placeholder": None,
            "uploaded_file": None,
            "file_uploader_key": 0,
            "selected_template": None,
            "yaml_validation_status": None,
            "yaml_is_valid": False,
        }

        for key, default_value in session_defaults.items():
            if key not in st.session_state:
                st.session_state[key] = default_value

    @staticmethod
    def render_template_loader() -> None:
        """Render template loading interface."""
        app = st.session_state.form_generator

        if not app.template:
            UIComponents._render_upload_form()
        else:
            UIComponents._show_success_message()
            UIComponents._render_clear_button()

    @staticmethod
    def _render_upload_form() -> None:
        """Render file upload and template selection form."""
        if st.session_state.upload_placeholder is None:
            st.session_state.upload_placeholder = st.empty()
        if st.session_state.message_placeholder is None:
            st.session_state.message_placeholder = st.empty()

        with st.session_state.upload_placeholder.container():
            template_files = TemplateManager.get_template_files()

            if template_files:
                st.write("**Select Template:**")
                selectbox_kwargs = _get_selectbox_kwargs(
                    label="Choose a template",
                    options=[""] + template_files,
                    key=f"template_selector_{st.session_state.file_uploader_key}",
                    label_visibility="collapsed"
                )
                selected_template = st.selectbox(**selectbox_kwargs)

                st.write("**OR Upload File:**")
                uploader_kwargs = _get_file_uploader_kwargs(
                    label=settings.UPLOAD_LABEL,
                    type=settings.ALLOWED_FILE_TYPES,
                    key=f"file_uploader_{st.session_state.file_uploader_key}",
                    label_visibility="collapsed"
                )
                uploaded = st.file_uploader(**uploader_kwargs)
            else:
                uploader_kwargs = _get_file_uploader_kwargs(
                    label=settings.UPLOAD_LABEL,
                    type=settings.ALLOWED_FILE_TYPES,
                    key=f"file_uploader_{st.session_state.file_uploader_key}",
                    label_visibility=settings.FILE_UPLOAD_LABEL_VISIBILITY
                )
                uploaded = st.file_uploader(**uploader_kwargs)
                selected_template = None

        UIComponents._handle_template_selection(selected_template, uploaded)

    @staticmethod
    def _handle_template_selection(selected_template: str, uploaded) -> None:
        """Handle template selection and file upload."""
        app = st.session_state.form_generator

        # Handle template selection from dropdown
        if (
            selected_template
            and selected_template != st.session_state.selected_template
        ):
            st.session_state.selected_template = selected_template
            template_content = TemplateManager.load_template_file(selected_template)
            if template_content and app.load_template(template_content):
                UIComponents._on_template_loaded(
                    f"Template '{selected_template}' loaded successfully"
                )

        # Handle file upload
        elif uploaded and uploaded != st.session_state.uploaded_file:
            st.session_state.uploaded_file = uploaded
            if app.load_template(uploaded.read().decode("utf-8")):
                UIComponents._on_template_loaded()

        elif uploaded is None and st.session_state.uploaded_file is not None:
            st.session_state.uploaded_file = None
            st.session_state.message_placeholder.empty()

    @staticmethod
    def _on_template_loaded(message: str = None) -> None:
        """Handle successful template loading."""
        st.session_state.upload_placeholder.empty()
        if message:
            with st.session_state.message_placeholder.container():
                st.success(message)
        _rerun_app()

    @staticmethod
    def _show_success_message() -> None:
        """Show success message for loaded template."""
        if st.session_state.uploaded_file and st.session_state.message_placeholder:
            with st.session_state.message_placeholder.container():
                pass  # Keep placeholder for consistency

    @staticmethod
    def _render_clear_button() -> None:
        """Render clear form button."""
        button_kwargs = _get_button_kwargs(
            label=settings.CLEAR_BUTTON_TEXT,
            use_container_width=settings.USE_CONTAINER_WIDTH,
            type="secondary",
            key="clear_form_main"
        )
        if st.button(**button_kwargs):
            UIComponents._clear_form()

    @staticmethod
    def _clear_form() -> None:
        """Clear form and reset all state."""
        # Reset core state
        st.session_state.form_generator = FormGenerator()
        st.session_state.uploaded_file = None
        st.session_state.selected_template = None
        st.session_state.yaml_validation_status = None
        st.session_state.yaml_is_valid = False

        # Increment file uploader key to force reset
        st.session_state.file_uploader_key += 1

        # Clear form field widgets
        prefixes = (
            settings.FIELD_PREFIX,
            settings.BOOL_PREFIX,
            settings.NUM_PREFIX,
            settings.MULTI_PREFIX,
            settings.CAT_PREFIX,
            "file_uploader_",
            "template_selector_",
        )

        keys_to_delete = [
            key for key in st.session_state.keys() if key.startswith(prefixes)
        ]
        for key in keys_to_delete:
            del st.session_state[key]

        # Clear and reset placeholders
        if st.session_state.upload_placeholder:
            st.session_state.upload_placeholder.empty()
        if st.session_state.message_placeholder:
            st.session_state.message_placeholder.empty()

        st.session_state.upload_placeholder = None
        st.session_state.message_placeholder = None
        _rerun_app()

    @staticmethod
    def render_preview_section(form_data: Dict) -> None:
        """Render preview section with export controls."""
        st.subheader(settings.PREVIEW_SECTION_TITLE)

        app = st.session_state.form_generator
        structured_data = app.get_structured_data()
        preview = ExportUtils.export_yaml(structured_data)

        code_kwargs = _get_code_kwargs(
            body=preview,
            language="yaml", 
            line_numbers=settings.SHOW_LINE_NUMBERS
        )
        st.code(**code_kwargs)

        if form_data:
            UIComponents._render_export_controls(preview, structured_data)

    @staticmethod
    def _render_export_controls(preview: str, data: Dict) -> None:
        """Render validation and export buttons."""
        # Validate YAML button
        button_kwargs = _get_button_kwargs(
            label=settings.VALIDATE_YAML_TEXT,
            use_container_width=settings.USE_CONTAINER_WIDTH,
            type="secondary"
        )
        if st.button(**button_kwargs):
            is_valid, message = ExportUtils.validate_yaml(data)
            st.session_state.yaml_is_valid = is_valid
            st.session_state.yaml_validation_status = message
            _rerun_app()

        # Show validation status message
        if st.session_state.yaml_validation_status:
            if st.session_state.yaml_is_valid:
                st.success(st.session_state.yaml_validation_status)
            else:
                st.error(st.session_state.yaml_validation_status)

        # Download YAML button
        download_kwargs = _get_download_button_kwargs(
            label=settings.DOWNLOAD_YAML_TEXT,
            data=preview,
            file_name=settings.YAML_EXPORT_FILENAME,
            mime=settings.YAML_EXPORT_MIME,
            use_container_width=settings.USE_CONTAINER_WIDTH,
            disabled=not st.session_state.yaml_is_valid
        )
        st.download_button(**download_kwargs)

        # Download CSV button
        download_kwargs = _get_download_button_kwargs(
            label=settings.DOWNLOAD_CSV_TEXT,
            data=ExportUtils.export_csv(data),
            file_name=settings.CSV_EXPORT_FILENAME,
            mime=settings.CSV_EXPORT_MIME,
            use_container_width=settings.USE_CONTAINER_WIDTH
        )
        st.download_button(**download_kwargs)
