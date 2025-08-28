import json
import src.state as state
from src.data.items import ITEM_TEMPLATES as items
from src.battle import battle
from src.types.types import Progress, Stage, Results
from src.data.characters import Character
from src.data.characters import CHARACTER_TEMPLATES as characters
from src.data.monsters import Monster
from src.data.stages import stages
from src.data.levels import levels
from typing import Tuple, Optional, Union
from src.utils.database import get_database
from src.utils.get_equipped import get_equipped

first_run = True

conn = get_database()


def find_level_from_xp(xp: int) -> int | None:
    for key, data in levels.items():
        if data["xp_required"] <= xp and levels[key + 1]["xp_required"] > xp:
            return key
    return None


def xp_until_next_level(xp: int) -> int:
    current_level = find_level_from_xp(xp)
    if current_level is not None:
        next_level = current_level + 1
    else:
        next_level = None
    if next_level is not None and next_level in levels:
        next_level_xp_required = levels[next_level]["xp_required"]
    else:
        next_level_xp_required = None
    return next_level_xp_required - xp if next_level_xp_required is not None else 0


def parse_command(raw: str) -> Tuple[Optional[str], Optional[str]]:
    """
    Splits raw input into a command_key and argument string.
    Returns (None, None) if input is empty.
    """

    from src.commands.commands import COMMAND_REGISTRY as commands

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


def handle_command(raw_command: str) -> None:
    from src.commands.commands import COMMAND_REGISTRY as commands

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


def command_loop() -> None:
    data = load_progress()
    if not data:
        print("Could not load player data")
        return

    setup_player(data)

    while True:
        cmd = input("\n> ")
        handle_command(cmd)


def load_progress() -> Progress:
    c = get_database().cursor()
    data = c.execute("SELECT * FROM progress").fetchone()
    if not data:
        c.execute("INSERT INTO progress (first_time) VALUES (?)", ("1"))
        conn.commit()

    return c.execute("SELECT * FROM progress").fetchone()


def setup_player(data: Progress) -> Character:
    character = Character(data["character"])
    state.character = character

    equipped = get_equipped()
    for item_type, item in equipped.items():  # type: ignore
        if item:
            item_data = items.get(item)
            if not item_data:
                print(f"Could not find item data for equipped item '{item}'")
                continue

            if item_type == "weapon":
                character.attack += item_data.get("attack", 0)
            elif item_type == "armor":
                character.defense += item_data.get("defense", 0)

    return character


def run_stage_battles(player: Character, stage_data: Stage) -> Results:
    results: Results = {}
    for enemy, amount in stage_data["enemies"].items():
        results[enemy] = []
        for i in range(1, amount + 1):
            print(f"\n{enemy} - {i}/{amount}")
            enemy_instance = Monster(enemy)
            result = battle(player, enemy_instance)
            results[enemy].append(result)
            if not result:  # stop if failed
                break
    return results


def handle_stage_completion(data, stage, stage_data, results) -> None:
    if state.character is None:
        raise ValueError("No character in state")

    char_key = data["character"]
    if char_key not in characters:
        raise KeyError(f"Character {char_key} not found")

    state.character.health = characters[char_key]["health"]
    state.character.defense = characters[char_key]["defense"]  # TODO add the buffs from armor

    if not all(all(outcomes) for outcomes in results.values()):
        return

    stage_rewards = stage_data["rewards"]
    current_level = find_level_from_xp(data["xp"])
    new_level = find_level_from_xp(data["xp"] + stage_rewards["xp"])

    if not stage_rewards or current_level is None or new_level is None:
        return

    print(
        f"\nYou passed stage {stage}\nrewards:\n    "
        + "\n    ".join(f"{reward}: {value}" for reward, value in stage_rewards.items())
    )

    if current_level != new_level:
        level_rewards = levels[new_level]["rewards"]
        print(f"\nNew level reached!\n    Level {current_level} -> Level {new_level}")
        print(
            "\n    rewards:\n        "
            + "\n        ".join(
                f"{reward}: {value}" for reward, value in level_rewards.items()
            )
        )

    print(
        f"\nLevel progress: \n    Level: {new_level}\n    {data['xp'] + stage_rewards['xp']} / {levels[new_level + 1]['xp_required']}"
    )

    current_inventory = json.loads(data["inventory"])
    new_items = (
        levels[new_level]["rewards"]["items"] if new_level != current_level else []
    )

    merged_inventory = list(set(current_inventory + new_items))

    inventory_str = json.dumps(merged_inventory)

    c = conn.cursor()
    c.execute(
        "UPDATE progress SET gold = ?, xp = ?, stage = ?, inventory = ?",
        (
            (
                data["gold"]
                + stage_rewards["gold"]
                + levels[new_level]["rewards"]["gold"]
                if new_level != current_level
                else data["gold"] + stage_rewards["gold"]
            ),
            data["xp"] + stage_rewards["xp"],
            stage + 1,
            inventory_str,
        ),
    )

    conn.commit()


def start() -> None:
    data = load_progress()
    stage_value = data["stage"]
    if isinstance(stage_value, dict):
        raise ValueError(f"Invalid stage value: {stage_value}")
    stage = int(stage_value)
    stage_data: Stage = stages[stage]

    player = setup_player(data)

    if data["first_time"] == 1:
        print("Welcome to the super duper good RPG Game!")
        print(f"You will be starting with the {data['character']} character")

        results = run_stage_battles(player, stage_data)

        if all(all(outcomes) for outcomes in results.values()):
            print(
                "\nNicely done, you passed the first stage and earned 50 xp and 10 gold! Time for a little break"
            )
            print(
                "You can type 'shop' and 'shop buy <character_name | character_position>' to use the shop and upgrade your character."
            )
            print("When you feel ready, type 'start' to resume the game.")

            c = conn.cursor()
            c.execute(
                "UPDATE progress SET gold = 10, xp = 50, first_time = 0, stage = 2"
            )

            conn.commit()
    else:
        results = run_stage_battles(player, stage_data)
        handle_stage_completion(data, stage, stage_data, results)


if __name__ == "__main__":
    print("Welcome! Type 'start' to begin or other commands.")
    command_loop()
