from typing import Callable
from src.data.characters import CHARACTER_TEMPLATES as characters
import sqlite3
from src.main import start as start_game
import sys

COMMAND_REGISTRY = {}


def command_name(name: str) -> Callable[..., object]:
    """
    Decorator to register a function with a custom command name.
    """

    def decorator(func):
        COMMAND_REGISTRY[name.lower()] = func
        return func

    return decorator


def init_db():
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row

    return conn


@command_name("shop")
def shop():
    for char, data in characters.items():
        print(
            f"{char}:\n    "
            + "\n    ".join(
                f"{attr}: {stat}" for attr, stat in data.items() if attr[0] != "_"
            )
            + "\n"
        )


@command_name("shop buy")
def shop_buy(identifier: str | int):
    conn = init_db()
    c = conn.cursor()

    c.execute("SELECT id, gold FROM progress")
    data = c.fetchone()

    if not data:
        print("No progress data found.")
        conn.close()
        return

    gold = data["gold"]
    progress_id = data["id"]
    name: str | None = None
    character: dict | None = None

    if isinstance(identifier, int):
        if identifier > (len(characters) + 1):
            print(
                f"Position {identifier} exceeds maximum range of {len(characters) + 1}. (invalid position)"
            )

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
            "UPDATE progress SET gold = ?, character = ? WHERE id = ?",
            (gold, name, progress_id),
        )
        conn.commit()
        print(f"Successfully bought {name}\n    Remaining gold: {gold}")
    else:
        print(
            f"Not enough gold to buy {name}. You have {gold}, need {character['price']}."
        )

    conn.close()


@command_name("start")
def start():
    start_game()


@command_name("profile")
def profile():
    conn = init_db()
    c = conn.cursor()
    c.execute("SELECT * FROM progress")
    data = c.fetchone()
    for key, value in dict(data).items():
        print(f"{key}: {value}")


@command_name("exit")
def exit():
    print("Goodbye!")
    sys.exit()
