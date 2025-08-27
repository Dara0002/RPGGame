from battle import battle
import sqlite3
import uuid
from schemas import create_tables
from gameTypes import Stage
from characters import Character
from monsters import Monster
from stages import stages
from level import levels
from typing import Tuple, Optional, Union

first_run = True


def find_level_from_xp(xp):
    for key, data in levels.items():
        if data["xp_required"] <= xp and levels[key + 1]["xp_required"] > xp:
            return key
    return None


def xp_until_next_level(xp):
    current_level: int | None = find_level_from_xp(xp)
    if current_level is not None:
        next_level = current_level + 1
    else:
        next_level = None
    if next_level is not None and next_level in levels:
        next_level_xp = levels[next_level]
    else:
        next_level_xp = None
    return next_level_xp - xp


def parse_command(raw: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Splits raw input into a command_key and argument string.
    Returns (None, None) if input is empty.
    """

    from commands import COMMAND_REGISTRY as commands

    raw = raw.strip()
    if not raw:
        return None, None

    parts = raw.split()
    for i in range(len(parts), 0, -1):
        key = " ".join(parts[:i]).lower()
        if key in commands:
            argument = " ".join(parts[i:]) if i < len(parts) else None
            return key, argument
    return parts[0].lower(), " ".join(parts[1:]) if len(parts) > 1 else None


def convert_argument(arg: Optional[str]) -> Union[str, int, None]:
    """
    Converts the argument to an int if possible, otherwise returns string or None.
    Handles negative integers as well.
    """
    if arg is None:
        return None
    arg = arg.strip()
    try:
        return int(arg)
    except ValueError:
        return arg


def handle_command(raw_command: str):
    from commands import COMMAND_REGISTRY as commands

    command_key, argument = parse_command(raw_command)

    if command_key is None:
        return

    func = commands.get(command_key)
    if not func:
        print(f"Unknown command: {command_key}")
        return

    arg = convert_argument(argument)

    try:
        if arg is not None:
            func(arg)
        else:
            func()
    except TypeError as e:
        print(f"Error executing command '{command_key}': {e}")
    except Exception as e:
        print(f"An error occurred while executing '{command_key}': {e}")


def command_loop():
    while True:
        cmd = input("\n> ")
        handle_command(cmd)


def init_db():
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row

    create_tables(conn)

    c = conn.cursor()
    c.execute("SELECT * FROM progress")
    data = c.fetchone()

    if data is None:
        c.execute("INSERT INTO progress (id) VALUES (?)", (str(uuid.uuid4()),))
        conn.commit()

    return conn


def start():
    conn = init_db()
    c = conn.cursor()
    c.execute("SELECT * FROM progress")
    data = c.fetchone()
    stage = int(data["stage"])
    stage_data: Stage = stages[stage]
    results = {}

    player = Character(data["character"])

    if data["first_time"] == 1:
        print("Welcome to the super duper good RPG Game!")
        print(f"You will be starting with the {data["character"]} character")

        for enemy, amount in stage_data["enemies"].items():
            results[enemy] = []
            for i in range(1, amount + 1):
                print(f"\n{enemy} - {i}/{amount}")
                enemy_instance = Monster(enemy)
                result = battle(player, enemy_instance)
                results[enemy].append(result)

        if all(all(outcomes) for outcomes in results.values()):
            print(
                "\nNicely done, you passed the first stage and earned 50 xp and 10 gold! Time for a little break"
            )
            print(
                "You can type 'shop' and 'shop buy <character_name | character_position>' to use the shop and upgrade your character."
            )
            print("When you feel ready, type 'start' to resume the game.")
            c.execute(
                "UPDATE progress SET gold = ?, xp = ?, first_time = 0, stage = 2 WHERE id = ?",
                (10, 50, data["id"]),
            )
            conn.commit()

    else:
        for enemy, amount in stage_data["enemies"].items():
            results[enemy] = []
            for i in range(1, amount + 1):
                print(f"\n{enemy} - {i}/{amount}")
                enemy_instance = Monster(enemy)
                result = battle(player, enemy_instance)
                results[enemy].append(result)
                if not result:
                    break

        if all(all(outcomes) for outcomes in results.values()):
            stage_rewards = stage_data["rewards"]
            current_level = find_level_from_xp(data["xp"])
            new_level = find_level_from_xp(data["xp"] + stage_rewards["xp"])

            if not stage_rewards or current_level is None or new_level is None:
                return

            print(
                f"\nYou passed stage {stage}\nrewards:\n    "
                + "\n    ".join(
                    f"{reward}: {value}" for reward, value in stage_rewards.items()
                )
            )

            if current_level != new_level:
                level_rewards = levels[new_level]["rewards"]
                print(
                    f"New level reached!\n    Level {current_level} -> Level {new_level}"
                )
                print(
                    "\n    rewards:\n        "
                    + "\n        ".join(
                        f"{key}: {value}" for key, value in level_rewards.items()
                    )
                )

            print(
                f"Level progress: \n    Level: {new_level}\n    {data['xp'] + stage_rewards['xp']} / {levels[new_level + 1]['xp_required']}"
            )

            c.execute(
                "UPDATE progress SET gold = ?, xp = ?, stage = ? WHERE id = ?",
                (
                    (
                        data["gold"]
                        + stage_rewards["gold"]
                        + levels[new_level]["rewards"]["gold"]
                        if not new_level == current_level
                        else 0
                    ),
                    data["xp"] + stage_rewards["xp"],
                    stage + 1,
                    data["id"],
                ),
            )
            conn.commit()


if __name__ == "__main__":
    print("Welcome! Type 'start' to begin or other commands.")
    command_loop()
