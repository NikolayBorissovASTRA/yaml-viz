"""Dynamic YAML Form Generator - Clean, modular main application."""

import streamlit as st

import settings
from ui_components import UIComponents


def main():
    """Main application entry point."""
    # Configure page
    st.set_page_config(
        page_title=settings.PAGE_TITLE,
        layout=settings.PAGE_LAYOUT,
        initial_sidebar_state=settings.SIDEBAR_STATE,
    )

    # Load styling and initialize state
    UIComponents.load_css()
    UIComponents.initialize_session_state()

    # Render main application
    st.title(settings.APP_TITLE)

    # Template loading section
    col1, col2 = st.columns([3, 1])
    with col1:
        UIComponents.render_template_loader()

    # Main content area
    col1, col2 = st.columns([1.5, 1])

    with col1:
        st.subheader(settings.FORM_SECTION_TITLE)
        form_data = st.session_state.form_generator.render_form()

        # Debug output if enabled
        if settings.SHOW_DEBUG and form_data:
            with st.expander("Debug Info"):
                st.json(form_data)

    with col2:
        UIComponents.render_preview_section(form_data)


if __name__ == "__main__":
    main()
