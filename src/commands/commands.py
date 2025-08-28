from typing import Callable, NoReturn, Optional
from src.data.characters import CHARACTER_TEMPLATES as characters
from src.data.items import ITEM_TEMPLATES as items
import sqlite3
from src.main import start as start_game
import sys
import json

COMMAND_REGISTRY = {}


def command_name(name: str) -> Callable[..., object]:
    """
    Decorator to register a function with a custom command name.
    """

    def decorator(func):
        COMMAND_REGISTRY[name.lower()] = func
        return func

    return decorator


def init_db() -> sqlite3.Connection:
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row

    return conn


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
    conn = init_db()
    c = conn.cursor()

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
            conn.close()
            return
    else:
        print("Invalid character identifier, must be the character's name or position")
        conn.close()
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

    conn.close()


@command_name("item")
def item(identifier: str | int) -> None:
    if isinstance(identifier, str):
        name = identifier.title()
        item = items.get(name)
        if item is None:
            print(f"Item '{name}' not found.")
            return

        print(
            f"{name}:\n    "
            + "\n    ".join(f"{key}: {value}" for key, value in items[name].items())
        )

    if isinstance(identifier, int):
        # TODO add id to items
        pass


def get_inventory() -> set[str]:
    conn = init_db()
    c = conn.cursor()
    c.execute("SELECT inventory FROM progress")
    row = c.fetchone()
    inventory = row["inventory"]
    return set(json.loads(inventory))


def get_equipped(item_type: Optional[str] = None) -> dict[str, str] | str:
    conn = init_db()
    c = conn.cursor()
    c.execute("SELECT equipped FROM progress")
    row = c.fetchone()
    equipped = json.loads(row["equipped"])

    if item_type is None:
        return equipped

    return equipped.get(item_type)


def equip_item(identifier):
    conn = init_db()
    c = conn.cursor()

    equipped: dict[str, str] = get_equipped()  # type: ignore
    json_equipped = ""

    if isinstance(identifier, str):
        equipped[(items[identifier]["type"])] = identifier
        json_equipped = json.dumps(equipped)

    elif isinstance(identifier, int):
        pass

    c.execute("UPDATE progress SET equipped = ?", (json_equipped,))
    conn.commit()
    conn.close()


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

    if item_data["type"] == "potion":
        print("Can't equip potions.")
        return

    equipped_item = get_equipped(item_data["type"])
    if equipped_item:
        print(
            f"You currently have '{equipped_item}' equipped. "
            f"Unequip it first using 'unequip {equipped_item}'"
        )
        return

    equip_item(name)
    print(f"'{name}' is now equipped.")


@command_name("start")
def start() -> None:
    start_game()


@command_name("profile")
def profile() -> None:
    conn = init_db()
    c = conn.cursor()
    c.execute("SELECT * FROM progress")
    data = c.fetchone()
    for key, value in dict(data).items():
        print(f"{key}: {value}")


@command_name("help")
def help() -> None:
    print("Commands:\n    " + "\n    ".join(command for command in COMMAND_REGISTRY))


@command_name("exit")
def exit() -> NoReturn:
    print("Goodbye!")
    sys.exit()
