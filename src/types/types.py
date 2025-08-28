from typing import TypedDict, Dict, List, Protocol


class Stage(TypedDict):
    enemies: Dict[str, int]
    rewards: Dict[str, int]


class Progress(TypedDict):
    id: str
    stage: int
    xp: int
    gold: int
    character: str
    inventory: List[str]
    equipped: Dict[str, str]
    first_time: int


class Level(TypedDict):
    xp_required: int
    rewards: Dict[str, int | List[str]]


class Target(Protocol):
    name: str
    id: str
    health: int
    attack: int
    defense: int


Results = Dict[str, List[bool]]
