import os
import sys
import logging
from dotenv import load_dotenv
from .fetcher import Fetcher
from .renderer import Renderer
from .updater import Updater


def load_config() -> dict:
    load_dotenv()

    required = ["PROFILE", "BASE_URL", "SEASON"]
    config = {}
    missing = []
    for key in required:
        value = os.getenv(key)
        if value is None:
            missing.append(key)
        else:
            config[key.lower()] = value

    if missing:
        raise EnvironmentError(
            f"Отсутствуют обязательные переменные окружения: {', '.join(missing)}"
        )

    config["svg_output"] = os.getenv("SVG_OUTPUT", "assets/stats.svg")
    config["readme_path"] = os.getenv("README_PATH", "README.md")
    config["timeout"] = int(os.getenv("TIMEOUT", "10"))
    config["colors"] = {
        "EASY": "#3fb950",
        "MEDIUM": "#d29922",
        "HARD": "#f85149"
    }
    return config


def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )


def main():
    setup_logging()
    logger = logging.getLogger(__name__)

    try:
        config = load_config()
    except EnvironmentError as e:
        logger.error(str(e))
        sys.exit(1)

    fetcher = Fetcher(config)
    renderer = Renderer(config)
    updater = Updater(config)

    logger.info("Загрузка статистики...")
    stats = fetcher.fetch_stats()
    comp = fetcher.fetch_competition()

    if stats is None:
        logger.error("Не удалось получить статистику, завершение.")
        sys.exit(1)

    logger.info("Генерация SVG...")
    svg_content = renderer.render(stats, comp)

    updater.save_svg(svg_content)
    success = updater.update_readme()
    if success:
        logger.info("Готово!")
    else:
        logger.warning("README не обновлён, но SVG сохранён.")


if __name__ == "__main__":
    main()