from characters import characters
import sqlite3
import uuid
from main import start as start_game

def init_db():
    conn = sqlite3.connect('data.db')
    conn.row_factory = sqlite3.Row

    return conn

def shop():
    for char, data in characters.items():
        print(f"{char}:\n    " + "\n    ".join(f"{attr}: {stat}" for attr, stat in data.items()) + "\n")    

def shop_buy(name):
    conn = init_db()
    c = conn.cursor()

    c.execute("SELECT id, gold FROM progress")
    data = c.fetchone()

    if not data:
        print("No progress data found.")
        conn.close()
        return

    gold = data['gold']
    row_id = data['id']

    character = characters.get(name)
    if character is None:
        print(f"Character '{name}' not found.")
        conn.close()
        return

    if gold >= character['price']:
        gold -= character['price']
        c.execute("UPDATE progress SET gold = ?, character = ? WHERE id = ?", (gold, name, row_id))
        conn.commit()
        print(f"Successfully bought {name}\n    Remaining gold: {gold}")
    else:
        print(f"Not enough gold to buy {name}. You have {gold}, need {character['price']}.")

    conn.close()

def start():
    start_game()

def profile():
    conn = init_db()
    c = conn.cursor()
    c.execute("SELECT * FROM progress")
    data = c.fetchone()
    for key, value in dict(data).items():
        print(f"{key}: {value}")