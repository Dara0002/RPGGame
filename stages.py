from typing import TypedDict, Dict

class Stage(TypedDict):
    enemies: Dict[str, int]
    rewards: Dict[str, int]

stages: Dict[int, Stage] = {
    1:  {"enemies": {"Goblin": 2},                      "rewards": {"xp": 50,   "gold": 10}},
    2:  {"enemies": {"Skeleton": 1},                    "rewards": {"xp": 75,   "gold": 25}},
    3:  {"enemies": {"Goblin": 3, "Skeleton": 1},       "rewards": {"xp": 125,  "gold": 45}},
    4:  {"enemies": {"Orc Warrior": 2},                 "rewards": {"xp": 200,  "gold": 60}},
    5:  {"enemies": {"Troll": 1, "Orc Warrior": 2},     "rewards": {"xp": 300,  "gold": 90}},
    6:  {"enemies": {"Dark Wolf": 2, "Skeleton": 2},    "rewards": {"xp": 400,  "gold": 120}},
    7:  {"enemies": {"Wraith": 1, "Goblin": 4},         "rewards": {"xp": 500,  "gold": 140}},
    8:  {"enemies": {"Giant Spider": 2},                "rewards": {"xp": 600,  "gold": 180}},
    9:  {"enemies": {"Harpy": 2, "Skeleton": 3},        "rewards": {"xp": 750,  "gold": 210}},
    10:  {"enemies": {"Wyvern": 1, "Orc Warrior": 3},    "rewards": {"xp": 900,  "gold": 250}},
    11: {"enemies": {"Demon Lord": 1, "Dark Wolf": 3},  "rewards": {"xp": 1200, "gold": 350}},
    12: {"enemies": {"Troll": 3, "Goblin": 5},          "rewards": {"xp": 1400, "gold": 400}},
    13: {"enemies": {"Wraith": 2, "Skeleton": 4},       "rewards": {"xp": 1650, "gold": 450}},
    14: {"enemies": {"Giant Spider": 3, "Orc Warrior": 3}, "rewards": {"xp": 1900, "gold": 500}},
    15: {"enemies": {"Harpy": 3, "Goblin": 6},          "rewards": {"xp": 2200, "gold": 570}},
    16: {"enemies": {"Wyvern": 2, "Skeleton": 5},       "rewards": {"xp": 2500, "gold": 630}},
    17: {"enemies": {"Demon Lord": 1, "Troll": 4},      "rewards": {"xp": 2900, "gold": 700}},
    18: {"enemies": {"Dark Wolf": 4, "Orc Warrior": 5}, "rewards": {"xp": 3300, "gold": 770}},
    19: {"enemies": {"Wraith": 3, "Giant Spider": 4},   "rewards": {"xp": 3700, "gold": 840}},
    20: {"enemies": {"Harpy": 4, "Wyvern": 3},          "rewards": {"xp": 4100, "gold": 900}},
    21: {"enemies": {"Demon Lord": 2, "Troll": 5},      "rewards": {"xp": 4600, "gold": 1000}},
}
