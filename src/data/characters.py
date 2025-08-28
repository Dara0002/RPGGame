import uuid
from src.utils.randomDamage import random_damage
from typing import Optional
from src.types.types import Target

CHARACTER_TEMPLATES = {
    "Novice Squire": {
        "health": 90,
        "attack": 12,
        "defense": 14,
        "price": 0,
        "_position": 1,
    },
    "Apprentice Mage": {
        "health": 100,
        "attack": 14,
        "defense": 16,
        "price": 10,
        "_position": 2,
    },
    "Rusty Spearman": {
        "health": 110,
        "attack": 16,
        "defense": 18,
        "price": 32,
        "_position": 3,
    },
    "Forest Scout": {
        "health": 120,
        "attack": 18,
        "defense": 20,
        "price": 42,
        "_position": 4,
    },
    "Storm Initiate": {
        "health": 130,
        "attack": 20,
        "defense": 22,
        "price": 54,
        "_position": 5,
    },
    "Shadow Adept": {
        "health": 140,
        "attack": 22,
        "defense": 24,
        "price": 70,
        "_position": 6,
    },
    "Ironblade Warrior": {
        "health": 150,
        "attack": 24,
        "defense": 26,
        "price": 91,
        "_position": 7,
    },
    "Moonlit Ranger": {
        "health": 160,
        "attack": 26,
        "defense": 28,
        "price": 119,
        "_position": 8,
    },
    "Stoneheart Defender": {
        "health": 170,
        "attack": 28,
        "defense": 30,
        "price": 155,
        "_position": 9,
    },
    "Dawnbringer Paladin": {
        "health": 180,
        "attack": 30,
        "defense": 32,
        "price": 202,
        "_position": 10,
    },
    "Ironclaw Berserker": {
        "health": 190,
        "attack": 32,
        "defense": 34,
        "price": 263,
        "_position": 11,
    },
    "Swiftstrike Assassin": {
        "health": 195,
        "attack": 33,
        "defense": 35,
        "price": 342,
        "_position": 12,
    },
    "Shadowbane Duelist": {
        "health": 200,
        "attack": 34,
        "defense": 36,
        "price": 445,
        "_position": 13,
    },
    "Lightbringer Cleric": {
        "health": 205,
        "attack": 35,
        "defense": 37,
        "price": 579,
        "_position": 14,
    },
    "Stormrider Elemental": {
        "health": 210,
        "attack": 36,
        "defense": 38,
        "price": 752,
        "_position": 15,
    },
    "Nightfall Sorcerer": {
        "health": 215,
        "attack": 37,
        "defense": 39,
        "price": 978,
        "_position": 16,
    },
    "Fireheart Champion": {
        "health": 220,
        "attack": 38,
        "defense": 40,
        "price": 1272,
        "_position": 17,
    },
    "Frostveil Archmage": {
        "health": 225,
        "attack": 39,
        "defense": 41,
        "price": 1655,
        "_position": 18,
    },
    "Blackthorn Warlord": {
        "health": 230,
        "attack": 40,
        "defense": 42,
        "price": 1953,
        "_position": 19,
    },
    "Celeste Dawnseer": {
        "health": 235,
        "attack": 41,
        "defense": 43,
        "price": 2599,
        "_position": 20,
    },
}


class Character:
    characters = {}

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

        if name not in CHARACTER_TEMPLATES:
            raise ValueError(f"Character template '{name}' not found in characters_data.")

        template = CHARACTER_TEMPLATES[name]
        self.health = health if health is not None else template["health"]
        self.attack = attack if attack is not None else template["attack"]
        self.defense = defense if defense is not None else template["defense"]

        Character.characters[self.id] = self

    def attack_target(self, target: Target) -> tuple[int, int, int]:
        damage, health, defense = random_damage(
            self.attack,
            target.health,
            target.defense
        )
        target.health = health
        target.defense = defense
        return damage, target.health, target.defense

    def __str__(self) -> str:
        return f"Character(ID: {self.id}, Name: {self.name}, HP: {self.health}, Attack: {self.attack}, Defense: {self.defense})"
