"""Core form generation logic separated from UI concerns."""

import streamlit as st
import yaml
from typing import Any, Dict, List, Optional

import settings


class FormGenerator:
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
                value=value,
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
                    # Map selected display strings back to original objects
                    selected_objects = self._map_display_to_objects(selected, items)
                    category_data[cat_key] = selected_objects

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

    def _map_display_to_objects(self, selected_displays: List[str], original_items: List) -> List:
        """Map selected display strings back to original objects."""
        if not selected_displays:
            return []
        
        result = []
        for display_str in selected_displays:
            # Find matching original item
            for item in original_items:
                if self._format_item_display(item) == display_str:
                    # For objects with name/code, preserve original structure
                    if isinstance(item, dict):
                        result.append(item)
                    else:
                        # For simple strings, just add the string
                        result.append(item)
                    break
        
        return result

    def get_structured_data(self) -> Dict:
        """Get form data with preserved key order and original structure."""
        if not self.form_data:
            return {}

        # Preserve original key order
        ordered_data = {
            key: self.form_data[key] for key in self.key_order if key in self.form_data
        }
        ordered_data.update(
            {k: v for k, v in self.form_data.items() if k not in ordered_data}
        )

        # Use original root structure or return data directly
        if self.root_key:
            return {self.root_key: ordered_data}
        return ordered_data
