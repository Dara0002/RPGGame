from typing import TypedDict, Dict

class Stage(TypedDict):
    enemies: Dict[str, int]
    rewards: Dict[str, int]