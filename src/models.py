from dataclasses import dataclass
from typing import List


@dataclass
class DifficultyStats:
    difficulty: str
    solved: int
    total: int

@dataclass
class ProfileStats:
    total_solved: int
    total_all: int
    difficulties: List[DifficultyStats]

@dataclass
class CompetitionInfo:
    name: str
    solved: int
    total: int
    score: int
    place: int
    participants: int
