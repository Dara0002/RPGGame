from src.types.types import Item

ITEM_TEMPLATES: dict[str, Item] = {
    # Armors
    "Chainmail Armor": {
        "type": "armor",
        "defense": 20,
        "description": "A sturdy chainmail that offers basic protection.",
    },
    "Leather Armor": {
        "type": "armor",
        "defense": 25,
        "description": "Light armor made from toughened leather, allows mobility.",
    },
    "Plate Armor": {
        "type": "armor",
        "defense": 35,
        "description": "Heavy plate armor providing excellent protection.",
    },
    "Dragon Scale Armor": {
        "type": "armor",
        "defense": 50,
        "description": "Armor forged from dragon scales, extremely durable.",
    },
    "Mythril Armor": {
        "type": "armor",
        "defense": 70,
        "description": "A legendary armor that is both light and incredibly strong.",
    },
    # Swords
    "Iron Sword": {
        "type": "weapon",
        "attack": 15,
        "description": "A basic iron sword, reliable for new adventurers.",
    },
    "Steel Sword": {
        "type": "weapon",
        "attack": 20,
        "description": "A sword forged from steel, sharper and stronger than iron.",
    },
    "Silver Sword": {
        "type": "weapon",
        "attack": 30,
        "description": "A sword with a silver blade, effective against magical creatures.",
    },
    "Knight Sword": {
        "type": "weapon",
        "attack": 40,
        "description": "A finely crafted sword favored by knights.",
    },
    "Excalibur Sword": {
        "type": "weapon",
        "attack": 50,
        "description": "The legendary sword of kings, unmatched in power.",
    },
    # Potions
    "Minor Potion": {
        "type": "potion",
        "heal": 25,
        "description": "A small potion that restores a little health.",
    },
    "Greater Potion": {
        "type": "potion",
        "heal": 75,
        "description": "A strong potion that restores a significant amount of health.",
    },
    "Superior Potion": {
        "type": "potion",
        "heal": 150,
        "description": "A powerful potion that fully restores health.",
    },
}
