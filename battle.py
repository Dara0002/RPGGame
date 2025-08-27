import time
import random
from characters import Character
from monsters import Monster


def attack(attacker: Monster | Character, attacked: Monster | Character):
    if isinstance(attacker, Character):
        print(f"Attacking {attacked.name}...\n")
        time.sleep(1)
        damage, health, defense = attacker.attack_target(attacked)
        print(
            f"You attacked {attacked.name} for {str(damage)} damage and left them at {str(health)} health, {str(defense)} defense"
        )
    else:
        print(f"{attacker.name} is attacking...\n")
        time.sleep(1)
        damage, health, defense = attacker.attack_target(attacked)
        print(
            f"You were attacked by {attacker.name} for {str(damage)} damage and left with {str(health)} health, {str(defense)} defense"
        )


def battle(player: Character, enemy: Monster):
    turn = 0
    first_turn = None

    while player.health > 0 and enemy.health > 0:
        turn += 1
        print("\nStarting turn " + str(turn) + "")

        if turn == 1:
            print("Randomizing who gets the first turn...")
            if random.choice([1, 2]) == 1:
                first_turn = player
                print("You get to start first!")
                time.sleep(1)
                attack(player, enemy)
            else:
                first_turn = enemy
                print("Enemy gets to start first...")
                time.sleep(1)
                attack(enemy, player)
            continue

        if turn % 2 == 0 and first_turn == enemy:
            print("Your turn!")
            attack(player, enemy)
        elif turn % 2 == 1 and first_turn == enemy:
            print("Enemy's turn!")
            attack(enemy, player)
        elif turn % 2 == 0 and first_turn == player:
            print("Enemy's turn!")
            attack(enemy, player)
        else:
            print("Your turn!")
            attack(player, enemy)

        if player.health <= 0:
            print("You lost! Better luck next time...")
            return False
        elif enemy.health <= 0:
            print("Congratulations! You won!")
            return True

        continue
