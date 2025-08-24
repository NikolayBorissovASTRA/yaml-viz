"""YAML and CSV export utilities with validation."""

import re
import yaml
from typing import Dict, List, Tuple

import settings


class ExportUtils:
    """Handles data export and validation operations."""

    @staticmethod
    def export_yaml(data: Dict) -> str:
        """Export data as clean YAML with proper formatting."""
        if not data:
            return settings.NO_DATA_TEXT

        # Generate clean YAML output
        yaml_output = yaml.dump(
            data,
            default_flow_style=settings.YAML_FLOW_STYLE,
            indent=settings.YAML_INDENT,
            allow_unicode=settings.YAML_UNICODE,
            sort_keys=settings.YAML_SORT_KEYS,
        )
        return ExportUtils._clean_yaml_quotes(yaml_output)

    @staticmethod
    def _clean_yaml_quotes(yaml_str: str) -> str:
        """Remove unnecessary quotes from YAML output."""
        yaml_str = re.sub(r"""(['"])(.*?)\1""", r"\2", yaml_str)
        return yaml_str

    @staticmethod
    def validate_yaml(data: Dict) -> Tuple[bool, str]:
        """Validate YAML data and return status with message."""
        if not data:
            return False, "No data to validate"

        try:
            yaml_output = ExportUtils.export_yaml(data)
            if yaml_output == settings.NO_DATA_TEXT:
                return False, "No data to validate"

            # Try to parse the generated YAML
            yaml.safe_load(yaml_output)
            return True, "YAML is valid"
        except yaml.YAMLError as e:
            return False, f"YAML validation error: {str(e)}"
        except Exception as e:
            return False, f"Validation error: {str(e)}"

    @staticmethod
    def export_csv(data: Dict) -> str:
        """Export data as CSV with minimal quoting."""
        if not data:
            return ""

        rows = [["key_path", "value"]]
        ExportUtils._flatten_data(data, rows)

        return "\n".join(
            ",".join(ExportUtils._quote_if_needed(str(cell)) for cell in row)
            for row in rows
        )

    @staticmethod
    def _flatten_data(data: Dict, rows: List, prefix: str = "") -> None:
        """Recursively flatten nested data structure."""
        for key, value in data.items():
            path = f"{prefix}.{key}" if prefix else key
            if isinstance(value, dict):
                ExportUtils._flatten_data(value, rows, path)
            elif isinstance(value, list):
                for item in value:
                    rows.append([path, item])
            else:
                rows.append([path, value])

    @staticmethod
    def _quote_if_needed(cell: str) -> str:
        """Only quote CSV cells that require it."""
        needs_quotes = "," in cell or '"' in cell or "\n" in cell
        if needs_quotes:
            escaped = cell.replace('"', '""')
            return f'"{escaped}"'
        return cell
