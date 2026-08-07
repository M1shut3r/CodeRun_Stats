import logging
from typing import Any, Dict, Optional

import requests

from .models import CompetitionInfo, DifficultyStats, ProfileStats

logger = logging.getLogger(__name__)

class Fetcher:
    def __init__(self, config: Dict[str, Any]):
        self.config = config
        self.session = requests.Session()
        self.session.timeout = config["timeout"]

    def _get_stats_url(self) -> str:
        return f"{self.config['base_url']}/profile/statistics/{self.config['profile']}/problems/solved/dynamic"

    def _get_comp_url(self) -> str:
        season = self.config.get("season", "")
        if not season:
            return None  # или пустая строка, но мы не будем вызывать
        return f"{self.config['base_url']}/profile/{self.config['profile']}/season-results/{season}"

    def fetch_stats(self) -> Optional[ProfileStats]:
        try:
            resp = self.session.get(self._get_stats_url())
            resp.raise_for_status()
            data = resp.json()
            result = data["result"]

            total_solved = result["totalSolved"]
            difficulties = []
            total_all = 0
            for item in result["statistic"]:
                diff = item["literalDifficulty"]
                solved = item["solved"]
                total = item["total"]
                total_all += total
                difficulties.append(DifficultyStats(diff, solved, total))

            return ProfileStats(total_solved, total_all, difficulties)
        except (requests.RequestException, KeyError, ValueError) as e:
            logger.error(f"Ошибка получения статистики: {e}")
            return None

    def fetch_competition(self) -> Optional[CompetitionInfo]:
        try:
            resp = self.session.get(self._get_comp_url())
            resp.raise_for_status()
            data = resp.json()
            result = data["result"]
            tracks = result.get("tracks", [])
            if not tracks:
                logger.info("Нет данных о соревнованиях (tracks пуст)")
                return None
            track = tracks[0]  # берём первый трек

            return CompetitionInfo(
                name=result.get("name", "Без названия"),
                solved=track["problemSolved"],
                total=track["problemTotal"],
                score=track["score"],
                place=track["place"],
                participants=track["totalParticipants"]
            )
        except (requests.RequestException, KeyError, ValueError) as e:
            logger.error(f"Ошибка получения соревнования: {e}")
            return None
