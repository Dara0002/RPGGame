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
    equipped: Dict[str, str | None]
    first_time: int


class Level(TypedDict):
    xp_required: int
    rewards: Dict[str, int | List[str]]


class Item(TypedDict, total=False):
    type: str
    defense: int
    attack: int
    heal: int
    description: str


class Target(Protocol):
    name: str
    id: str
    health: int
    attack: int
    defense: int


Results = Dict[str, List[bool]]
