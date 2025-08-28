import src.state as state
import sys
import json
from pyclbr import Function
from typing import Callable, NoReturn
from src.utils.database import get_database
from src.data.characters import CHARACTER_TEMPLATES as characters
from src.data.items import ITEM_TEMPLATES as items
from src.main import start as start_game
from src.utils.get_equipped import get_equipped

COMMAND_REGISTRY = {}


def command_name(name: str) -> Callable[..., object]:
    """
    Decorator to register a function with a custom command name.
    """

    def decorator(func) -> Function:
        COMMAND_REGISTRY[name.lower()] = func
        return func

    return decorator


@command_name("shop")
def shop() -> None:
    for char, data in characters.items():
        print(
            f"{char}:\n    "
            + "\n    ".join(
                f"{attr}: {stat}" for attr, stat in data.items() if attr[0] != "_"
            )
            + "\n"
        )


@command_name("shop buy")
def shop_buy(identifier: str | int) -> None:
    c = get_database().cursor()
    c.execute("SELECT gold FROM progress")
    data = c.fetchone()

    gold = data["gold"]
    name: str | None = None
    character: dict | None = None

    if isinstance(identifier, int):
        if identifier > (len(characters)):
            print(
                f"Position {identifier} exceeds maximum range of {len(characters)}. (invalid position)"
            )
            return

        for character_name, character_data in characters.items():
            if character_data["_position"] == identifier:
                name = character_name
                character = character_data
                break

        if name is None or character is None:
            print(f"Could not find character with position {identifier}")
            return

    elif isinstance(identifier, str):
        name = identifier.title()
        character = characters.get(name)
        if character is None:
            print(f"Character '{name}' not found.")
            return
    else:
        print("Invalid character identifier, must be the character's name or position")
        return

    if gold >= character["price"]:
        gold -= character["price"]
        c.execute(
            "UPDATE progress SET gold = ?, character = ?",
            (gold, name),
        )
        conn.commit()
        print(f"Successfully bought {name}\n    Remaining gold: {gold}")
    else:
        print(
            f"Not enough gold to buy {name}. You have {gold}, need {character['price']}."
        )


@command_name("item")
def item(identifier: str) -> None:
    name = identifier.title()
    item = items.get(name)
    if not item:
        print(f"Item '{name}' not found.")
        return

    print(
        f"{name}:\n    "
        + "\n    ".join(f"{key}: {value}" for key, value in items[name].items())
    )


def get_inventory() -> set[str]:
    c = get_database().cursor()
    c.execute("SELECT inventory FROM progress")
    row = c.fetchone()
    inventory = row["inventory"]
    return set(json.loads(inventory))


def toggle_item(identifier: str, equip: bool) -> None:
    equipped: dict[str, str | None] = get_equipped()  # type: ignore
    json_equipped = ""

    item = items.get(identifier)
    if item is None:
        print(f"Item '{identifier}' not found.")
        return

    item_type = item.get("type")
    if not isinstance(item_type, str):
        print(f"Item '{identifier}' does not have a valid type.")
        return

    if equip:
        equipped[item_type] = identifier
    else:
        equipped[item_type] = None

    json_equipped = json.dumps(equipped)

    c = conn.cursor()
    c.execute("UPDATE progress SET equipped = ?", (json_equipped,))
    conn.commit()


@command_name("inventory")
def inventory() -> None:
    parsed_inventory = get_inventory()
    equipped: dict[str, str] = get_equipped()  # type: ignore
    if parsed_inventory:
        print(", ".join(item for item in parsed_inventory))
    else:
        print("Empty")

    print(
        f"Equipped:\n    Armor: {equipped.get("armor")}\n    Weapon: {equipped.get("weapon")}"
    )


@command_name("equip")
def equip(identifier: str) -> None:
    name = identifier.title()
    item_data = items.get(name)

    if not item_data:
        print(f"Item '{name}' not found.")
        return

    inventory = get_inventory()
    if name not in inventory:
        print(f"You do not have '{name}' in your inventory.")
        return

    if item_data.get("type") == "potion":
        print("Can't equip potions.")
        return

    equipped_item = get_equipped(item_data.get("type"))

    if equipped_item == name:
        print(f"You already have {name} equipped")
        return

    if equipped_item:
        print(
            f"You currently have {equipped_item} equipped. "
            f"Unequip it first using 'unequip {equipped_item}'"
        )
        return

    toggle_item(name, True)
    print(f"Equiped {name}")

    character = state.character
    if not character:
        print("Could not find character")
        return

    if item_data.get("type") == "weapon":
        character.attack += item_data.get("attack", 0)
    elif item_data.get("type") == "armor":
        character.defense += item_data.get("defense", 0)


@command_name("unequip")
def unequip(identifier: str) -> None:

    name = identifier.title()
    item_data = items.get(name)

    if not item_data:
        print(f"Item '{name}' not found.")
        return

    if item_data.get("type") == "potion":
        print("You can't unequip potions")

    equipped_item = get_equipped(item_data.get("type"))

    if not equipped_item:
        print(f"You dont have {name} equipped")
        return

    toggle_item(name, False)
    print(f"Unequiped {name}")


@command_name("start")
def start() -> None:
    start_game()


@command_name("profile")
def profile() -> None:
    c = conn.cursor()
    c.execute("SELECT * FROM progress")
    data = c.fetchone()
    for key, value in dict(data).items():
        print(f"{key}: {value}")


@command_name("character")
def character() -> None:
    character = state.character
    if not character:
        print("Could not find character")
        return

    print(
        "Your character:\n    "
        + "\n    ".join(
            f"{attribute}: {value}"
            for attribute, value in vars(character).items()
            if not attribute.startswith("_")
        )
    )


@command_name("help")
def help() -> None:
    print("Commands:\n    " + "\n    ".join(command for command in COMMAND_REGISTRY))


@command_name("exit")
def exit() -> NoReturn:
    print("Goodbye!")
    conn.close()
    sys.exit()
