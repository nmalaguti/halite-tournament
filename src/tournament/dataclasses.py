from dataclasses import dataclass
from typing import List, Optional

from mashumaro import DataClassDictMixin


@dataclass
class MatchResultDataClass(DataClassDictMixin):
    bot_name: str
    docker_image: str
    rank: int
    last_frame_alive: int
    error_log: Optional[str]


@dataclass
class MatchDataClass(DataClassDictMixin):
    id: str
    date: str
    replay: str
    seed: int
    width: int
    height: int
    match_results: List[MatchResultDataClass]
    workflow_run_id: int
