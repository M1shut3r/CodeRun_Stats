import math
from typing import Any, Dict, Optional

from .models import CompetitionInfo, ProfileStats


class Renderer:
    def __init__(self, config: Dict[str, Any]):
        self.colors = config.get("colors", {
            "EASY": "#3fb950",
            "MEDIUM": "#d29922",
            "HARD": "#f85149"
        })

    def render(self, stats: ProfileStats, comp: Optional[CompetitionInfo]) -> str:
        total_solved = stats.total_solved
        total_all = stats.total_all

        diff_map = {d.difficulty: d for d in stats.difficulties}

        # Круговой индикатор
        r = 58
        C = 2 * math.pi * r
        frac = min(total_solved / total_all, 1) if total_all else 0
        dash = frac * C

        # Прогресс-бары по сложностям
        rows = ""
        y = 78
        for key, label in [("EASY", "Easy"), ("MEDIUM", "Medium"), ("HARD", "Hard")]:
            d = diff_map.get(key)
            if d:
                s, t = d.solved, d.total
            else:
                s, t = 0, 0
            bar_w = 480
            fill_w = max(round(s / t * bar_w), 6) if t and s else 0
            rows += f'''
  <text x="210" y="{y}" fill="#e6edf3" font-size="19" font-weight="600">{label}</text>
  <text x="690" y="{y}" fill="#e6edf3" font-size="17" font-weight="600" text-anchor="end">{s} / {t}</text>
  <rect x="210" y="{y + 14}" width="{bar_w}" height="6" rx="3" fill="#2d333b"/>
  <rect x="210" y="{y + 14}" width="{fill_w}" height="6" rx="3" fill="{self.colors[key]}"/>'''
            y += 66

        # Блок соревнований
        if comp is None:
            comp_block = '''
  <text x="30" y="338" fill="#8b949e" font-size="18" font-weight="400">Нет активных соревнований</text>
  <text x="30" y="380" fill="#8b949e" font-size="14">Попробуйте другой сезон или участвуйте в будущих</text>'''
        else:
            comp_block = f'''
  <text x="30" y="338" fill="#e6edf3" font-size="20" font-weight="700">{comp.name}</text>
  <text x="30" y="380" fill="#ffffff" font-size="22" font-weight="700">{comp.solved} / {comp.total}</text>
  <text x="30" y="402" fill="#8b949e" font-size="14">Solved</text>
  <text x="280" y="380" fill="#ffffff" font-size="22" font-weight="700">{comp.score}</text>
  <text x="280" y="402" fill="#8b949e" font-size="14">Points</text>
  <text x="480" y="380" fill="#ffffff" font-size="22" font-weight="700">#{comp.place} / {comp.participants:,}</text>
  <text x="480" y="402" fill="#8b949e" font-size="14">Place</text>'''

        # Собираем итоговый SVG
        svg = f'''<svg width="720" height="420" viewBox="0 0 720 420" xmlns="http://www.w3.org/2000/svg" font-family="Segoe UI, Helvetica, Arial, sans-serif">
  <rect width="720" height="420" rx="16" fill="#0d1117"/>
  <circle cx="110" cy="120" r="{r}" fill="none" stroke="#2d333b" stroke-width="10"/>
  <circle cx="110" cy="120" r="{r}" fill="none" stroke="#f0883e" stroke-width="10" stroke-linecap="round" stroke-dasharray="{dash:.1f} {C:.1f}" transform="rotate(-90 110 120)"/>
  <text x="110" y="120" fill="#ffffff" font-size="42" font-weight="700" text-anchor="middle" dominant-baseline="central">{total_solved}</text>
  {rows}
  <line x1="30" y1="268" x2="690" y2="268" stroke="#2d333b" stroke-width="1"/>
  <text x="30" y="305" fill="#8b949e" font-size="14" font-weight="700" letter-spacing="3">COMPETITIONS</text>
  {comp_block}
</svg>'''
        return svg
