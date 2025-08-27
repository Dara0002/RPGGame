from characters import Character
from monsters import Monster

test_character = "Celeste Dawnseer"
test_monster = "Demon Lord"


def test_character_initialization():
    c = Character(test_character)
    assert c.name == test_character
    assert c.health > 0
    assert hasattr(c, "attack")


def test_character_attack():
    attacker = Character(test_character)
    defender = Monster(test_monster)
    starting_hp = defender.health

    attacker.attack_target(defender)

    assert defender.health < starting_hp
