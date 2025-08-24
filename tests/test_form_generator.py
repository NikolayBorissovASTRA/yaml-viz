"""Unit tests for DynamicFormGenerator."""

from pathlib import Path
import sys

# Add src to Python path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from app import DynamicFormGenerator


class TestDynamicFormGenerator:
    """Test cases for DynamicFormGenerator class."""

    def setup_method(self):
        """Set up test fixtures."""
        self.generator = DynamicFormGenerator()

    def test_init(self):
        """Test generator initialization."""
        assert self.generator.template is None
        assert self.generator.root_key is None
        assert self.generator.key_order == []
        assert self.generator.form_data == {}

    def test_load_template_valid_yaml(self):
        """Test loading valid YAML template."""
        yaml_content = """
        Project:
          name: "Test Project"
          version: "1.0"
          enabled: true
        """
        result = self.generator.load_template(yaml_content)
        assert result is True
        assert self.generator.root_key == "Project"
        assert "name" in self.generator.key_order
        assert "version" in self.generator.key_order
        assert "enabled" in self.generator.key_order

    def test_load_template_flat_structure(self):
        """Test loading flat YAML structure without root key."""
        yaml_content = """
        name: "Test"
        version: "1.0"
        debug: false
        """
        result = self.generator.load_template(yaml_content)
        assert result is True
        assert self.generator.root_key is None
        assert self.generator.key_order == ["name", "version", "debug"]

    def test_load_template_invalid_yaml(self):
        """Test handling invalid YAML content."""
        invalid_yaml = "invalid: yaml: content: ["
        result = self.generator.load_template(invalid_yaml)
        assert result is False
        assert self.generator.template is None

    def test_load_template_non_dict(self):
        """Test handling non-dictionary YAML content."""
        non_dict_yaml = "- item1\n- item2"
        result = self.generator.load_template(non_dict_yaml)
        assert result is False
        # Template will contain the parsed list, but load should return False

    def test_is_category_structure_positive(self):
        """Test category structure detection for valid structure."""
        category_data = {
            "Category1": [
                {"name": "Item 1", "code": "A1"},
                {"name": "Item 2", "code": "A2"},
            ],
            "Category2": [
                {"name": "Item 3", "code": "B1"},
                {"name": "Item 4", "code": "B2"},
            ],
        }
        assert self.generator._is_category_structure(category_data) is True

    def test_is_category_structure_negative(self):
        """Test category structure detection for invalid structure."""
        non_category_data = {
            "simple_list": ["item1", "item2"],
            "nested_obj": {"key": "value"},
        }
        assert self.generator._is_category_structure(non_category_data) is False

    def test_format_tab_name(self):
        """Test tab name formatting."""
        assert self.generator._format_tab_name("Category1 (10 items)") == "Category1"
        assert self.generator._format_tab_name("Simple Name") == "Simple Name"

    def test_format_item_display_with_code(self):
        """Test item display formatting with code."""
        item = {"name": "Test Item", "code": "T1"}
        result = self.generator._format_item_display(item)
        assert result == "Test Item (T1)"

    def test_format_item_display_without_code(self):
        """Test item display formatting without code."""
        item = {"name": "Test Item"}
        result = self.generator._format_item_display(item)
        assert result == "Test Item"

    def test_format_item_display_string(self):
        """Test item display formatting for string items."""
        item = "Simple String"
        result = self.generator._format_item_display(item)
        assert result == "Simple String"

    def test_export_yaml_no_data(self):
        """Test YAML export with no form data."""
        result = self.generator.export_yaml()
        assert result == "No data"

    def test_export_csv_no_data(self):
        """Test CSV export with no form data."""
        result = self.generator.export_csv()
        assert result == ""

    def test_quote_if_needed_no_quotes(self):
        """Test CSV quoting for cells that don't need quotes."""
        result = self.generator._quote_if_needed("simple_text")
        assert result == "simple_text"

    def test_quote_if_needed_with_comma(self):
        """Test CSV quoting for cells with commas."""
        result = self.generator._quote_if_needed("text,with,commas")
        assert result == '"text,with,commas"'

    def test_quote_if_needed_with_quotes(self):
        """Test CSV quoting for cells with quotes."""
        result = self.generator._quote_if_needed('text with "quotes"')
        assert result == '"text with ""quotes"""'

    def test_clean_yaml_quotes(self):
        """Test YAML quote cleaning."""
        yaml_with_quotes = """
        test: "true"
        number: "123"
        regular: "text"
        """
        result = self.generator._clean_yaml_quotes(yaml_with_quotes)
        assert '"true"' not in result
        assert '"123"' not in result
        assert '"text"' in result  # Regular text should keep quotes


class TestComplexScenarios:
    """Test complex real-world scenarios."""

    def setup_method(self):
        """Set up test fixtures."""
        self.generator = DynamicFormGenerator()

    def test_nested_structure_processing(self):
        """Test processing of nested YAML structures."""
        yaml_content = """
        WebApp:
          metadata:
            name: "Test App"
            version: "2.0"
          database:
            host: "localhost"
            port: 5432
            ssl: true
        """

        result = self.generator.load_template(yaml_content)
        assert result is True
        assert self.generator.root_key == "WebApp"
        assert "metadata" in self.generator.key_order
        assert "database" in self.generator.key_order

    def test_mixed_data_types(self):
        """Test handling of mixed data types."""
        yaml_content = """
        Config:
          app_name: "My App"
          port: 8080
          debug: true
          features:
            - "auth"
            - "logging"
          rate_limit: 100.5
        """

        result = self.generator.load_template(yaml_content)
        assert result is True

        # Verify all keys are captured in order
        expected_keys = ["app_name", "port", "debug", "features", "rate_limit"]
        assert self.generator.key_order == expected_keys

    def test_flatten_data_complex(self):
        """Test data flattening with complex nested structure."""
        complex_data = {
            "simple": "value",
            "nested": {"key1": "value1", "key2": "value2"},
            "list_items": ["item1", "item2"],
        }

        rows = [["key_path", "value"]]
        self.generator._flatten_data(complex_data, rows)

        # Check that all data was flattened correctly
        paths = [row[0] for row in rows[1:]]  # Skip header
        assert "simple" in paths
        assert "nested.key1" in paths
        assert "nested.key2" in paths
        assert "list_items" in paths

        # Check list items are properly handled
        list_rows = [row for row in rows if row[0] == "list_items"]
        assert len(list_rows) == 2
        assert list_rows[0][1] == "item1"
        assert list_rows[1][1] == "item2"
