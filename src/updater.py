import logging
from pathlib import Path
from typing import Dict, Any

logger = logging.getLogger(__name__)


class Updater:
    def __init__(self, config: Dict[str, Any]):
        self.svg_output = config["svg_output"]
        self.readme_path = config["readme_path"]

    def save_svg(self, svg_content: str) -> None:
        """Сохраняет SVG-файл, создавая при необходимости родительскую папку."""
        output_path = Path(self.svg_output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(svg_content, encoding="utf-8")
        logger.info(f"SVG сохранён в {output_path}")

    def update_readme(self) -> bool:
        """Вставляет ссылку на SVG в README между маркерами."""
        readme_path = Path(self.readme_path)
        if not readme_path.exists():
            logger.error(f"Файл {readme_path} не найден")
            return False

        content = readme_path.read_text(encoding="utf-8")
        start_marker = "<!-- CODE_RUN_STATS_START -->"
        end_marker = "<!-- CODE_RUN_STATS_END -->"

        if start_marker not in content or end_marker not in content:
            logger.error("Маркеры в README не найдены")
            return False

        svg_block = f'<div align="center">\n  <img src="./{self.svg_output}" alt="CodeRun statistics" width="720"/>\n</div>'

        start_idx = content.find(start_marker) + len(start_marker)
        end_idx = content.find(end_marker)
        new_content = (
            content[:start_idx] + "\n" + svg_block + "\n" + content[end_idx:]
        )
        readme_path.write_text(new_content, encoding="utf-8")
        logger.info("README успешно обновлён")
        return True