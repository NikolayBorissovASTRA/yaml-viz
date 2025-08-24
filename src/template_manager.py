"""Template loading and management utilities."""

from pathlib import Path
from typing import List, Optional


class TemplateManager:
    """Handles template file operations and management."""

    @staticmethod
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

    @staticmethod
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
