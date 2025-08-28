import uuid
from src.utils.randomDamage import random_damage
from typing import Optional

MONSTER_TEMPLATES: dict[str, dict[str, int]] = {
    "Goblin": {"health": 50, "attack": 8, "defense": 5},
    "Skeleton": {"health": 60, "attack": 10, "defense": 7},
    "Orc Warrior": {"health": 80, "attack": 14, "defense": 10},
    "Troll": {"health": 100, "attack": 18, "defense": 12},
    "Dark Wolf": {"health": 120, "attack": 22, "defense": 15},
    "Wraith": {"health": 130, "attack": 25, "defense": 17},
    "Giant Spider": {"health": 150, "attack": 28, "defense": 20},
    "Harpy": {"health": 170, "attack": 30, "defense": 22},
    "Wyvern": {"health": 190, "attack": 33, "defense": 25},
    "Demon Lord": {"health": 220, "attack": 38, "defense": 30},
}


class Monster:
    monsters = {}

    def __init__(
        self,
        name: str = "Unknown",
        id: Optional[str] = None,
        health: Optional[int] = None,
        attack: Optional[int] = None,
        defense: Optional[int] = None,
    ):
        self.id = id or str(uuid.uuid4())
        self.name = name

        if name not in MONSTER_TEMPLATES:
            raise ValueError(f"Monster template '{name}' not found in monsters_data.")

        template = MONSTER_TEMPLATES[name]
        self.health = health if health is not None else template["health"]
        self.attack = attack if attack is not None else template["attack"]
        self.defense = defense if defense is not None else template["defense"]

        Monster.monsters[self.id] = self

    def attack_target(self, target) -> tuple[int, int, int]:
        damage, health, defense = random_damage(
            self.attack, target.health, target.defense
        )
        target.health = health
        target.defense = defense
        return damage, target.health, target.defense

    def __str__(self) -> str:
        return f"Monster(ID: {self.id}, Name: {self.name}, HP: {self.health}, Attack: {self.attack}, Defense: {self.defense})"
