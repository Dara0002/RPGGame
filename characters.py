from utils.randomDamage import random_damage
import uuid
from typing import Optional

characters = {
    "Novice Squire":          {"health": 90,  "attack": 12, "defense": 14, "price": 0},
    "Apprentice Mage":        {"health": 100, "attack": 14, "defense": 16, "price": 10},
    "Rusty Spearman":         {"health": 110, "attack": 16, "defense": 18, "price": 32},
    "Forest Scout":           {"health": 120, "attack": 18, "defense": 20, "price": 42},
    "Storm Initiate":         {"health": 130, "attack": 20, "defense": 22, "price": 54},
    "Shadow Adept":           {"health": 140, "attack": 22, "defense": 24, "price": 70},
    "Ironblade Warrior":      {"health": 150, "attack": 24, "defense": 26, "price": 91},
    "Moonlit Ranger":         {"health": 160, "attack": 26, "defense": 28, "price": 119},
    "Stoneheart Defender":    {"health": 170, "attack": 28, "defense": 30, "price": 155},
    "Dawnbringer Paladin":    {"health": 180, "attack": 30, "defense": 32, "price": 202},
    "Ironclaw Berserker":     {"health": 190, "attack": 32, "defense": 34, "price": 263},
    "Swiftstrike Assassin":   {"health": 195, "attack": 33, "defense": 35, "price": 342},
    "Shadowbane Duelist":     {"health": 200, "attack": 34, "defense": 36, "price": 445},
    "Lightbringer Cleric":    {"health": 205, "attack": 35, "defense": 37, "price": 579},
    "Stormrider Elemental":   {"health": 210, "attack": 36, "defense": 38, "price": 752},
    "Nightfall Sorcerer":     {"health": 215, "attack": 37, "defense": 39, "price": 978},
    "Fireheart Champion":     {"health": 220, "attack": 38, "defense": 40, "price": 1272},
    "Frostveil Archmage":     {"health": 225, "attack": 39, "defense": 41, "price": 1655},
    "Blackthorn Warlord":     {"health": 230, "attack": 40, "defense": 42, "price": 1953},
    "Celeste Dawnseer":       {"health": 235, "attack": 41, "defense": 43, "price": 2599},
}

class Character:
    characters = {}

    def __init__(
        self,
        name: str = "Unknown",
        given_uuid: Optional[str] = None,
        health: Optional[int] = None,
        attack: Optional[int] = None,
        defense: Optional[int] = None
    ):
        self.uuid = given_uuid or str(uuid.uuid4())
        self.name = name
        self.health = health if health is not None else characters[name]["health"]
        self.attack = attack if attack is not None else characters[name]["attack"]
        self.defense = defense if defense is not None else characters[name]["defense"]

        Character.characters[self.uuid] = self

    def attack_target(self, target):
        damage, health, defense = random_damage(self.attack, target.defense, target.health)
        target.health = health
        target.defense = defense
        return damage, target.health, target.defense
    
    def __str__(self):
        return (f"Character(UUID: {self.uuid}, Name: {self.name}, HP: {self.health}, Attack: {self.attack}, Defense: {self.defense})")
    
    @classmethod
    def get_character(cls, uuid):
        return cls.characters.get(uuid)
