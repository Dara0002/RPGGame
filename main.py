from battle import battle
import sqlite3
import uuid
from schemas import create_tables
from gameTypes import Stage
from characters import Character, characters
from monsters import Monster, monsters
from stages import stages
from level import levels

first_run = True

def find_level_from_xp(xp):
    for key, data in levels.items():
        if data['xp_required'] <= xp and levels[key + 1]['xp_required'] > xp:
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
    

def handle_command(command: str):
    from command_registry import commands

    split_command = command.split(" ")
    if len(split_command) >= 2:
        command_key = f"{split_command[0]} {split_command[1]}"
        argument = " ".join(split_command[2:])
        if command_key in commands:
            commands[command_key](argument)
        else:
            print(f"Unknown command: {command_key}")
    elif len(split_command) == 1:
        if command in commands:
            commands[command]()
        else:
            print(f"Unknown command: {command}")

def command_loop():
    while True:
        cmd = input("\n> ")
        handle_command(cmd)

def init_db():
    conn = sqlite3.connect('data.db')
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
    stage = int(data['stage'])
    stage_data: Stage = stages[stage]
    results = {}

    player = Character(data['character'])

    if data['first_time'] == 1:
        print("Welcome to the super duper good RPG Game!")
        print("You will be starting with the " + data['character'] + " character")
        
        for enemy, amount in stage_data['enemies'].items():
            results[enemy] = []
            for i in range(1, amount + 1):
                print(f"\n{enemy} - {i}/{amount}")
                enemy_instance = Monster(enemy)
                result = battle(player, enemy_instance)
                results[enemy].append(result)

        if all(all(outcomes) for outcomes in results.values()):
            print("\nNicely done, you passed the first stage and earned 50 xp and 10 gold! Time for a little break")
            print("You can type 'shop' and 'shop buy <character_name>' to use the shop and upgrade your character.")
            print("When you feel ready, type 'start' to resume the game.")
            c.execute("UPDATE progress SET gold = ?, xp = ?, first_time = 0, stage = 2 WHERE id = ?", (10, 50, data['id']))
            conn.commit()

    else:
        for enemy, amount in stage_data['enemies'].items():
            results[enemy] = []
            for i in range(1, amount + 1):
                print(f"\n{enemy} - {i}/{amount}")
                enemy_instance = Monster(enemy)
                result = battle(player, enemy_instance)
                results[enemy].append(result)
                if not result:
                    break
        
        if all(all(outcomes) for outcomes in results.values()):
            stage_rewards = stage_data['rewards']
            current_level = find_level_from_xp(data['xp'])
            new_level = find_level_from_xp(data['xp'] + stage_rewards['xp'])

            if not stage_rewards or current_level is None or new_level is None:
                return

            print(f"\nYou passed stage {stage}\nrewards:\n    " + "\n    ".join(f"{reward}: {value}" for reward, value in stage_rewards.items()))

            if current_level != new_level:
                level_rewards = levels[new_level]['rewards']
                print(f"New level reached!\n    Level {current_level} -> Level {new_level}")
                print(f"\n    rewards:\n        " + "\n        ".join(f"{key}: {value}" for key, value in level_rewards.items()))

            print(f"Level progress: \n    Level: {new_level}\n    {data['xp'] + stage_rewards['xp']} / {levels[new_level + 1]['xp_required']}")

            c.execute("UPDATE progress SET gold = ?, xp = ?, stage = ? WHERE id = ?", (data['gold'] + stage_rewards['gold'] + levels[new_level]['rewards']['gold'] if not new_level == current_level else 0, data['xp'] + stage_rewards['xp'], stage + 1, data['id']))
            conn.commit()

if __name__ == "__main__":
    print("Welcome! Type 'start' to begin or other commands.")
    command_loop()