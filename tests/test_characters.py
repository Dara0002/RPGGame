import pytest
from src.data.characters import Character
from src.data.monsters import Monster


test_character = "Celeste Dawnseer"
test_monster = "Demon Lord"


def test_character_initialization_defaults():
    c = Character(test_character)
    assert c.name == test_character
    assert c.health > 0
    assert hasattr(c, "attack")
    assert isinstance(c.id, str)


def test_character_initialization_custom():
    c = Character(test_character, health=500, attack=99, defense=77, id="12345")
    assert c.health == 500
    assert c.attack == 99
    assert c.defense == 77
    assert c.id == "12345"


def test_character_invalid_template():
    with pytest.raises(ValueError):
        Character("NotARealCharacter")


def test_character_attack_reduces_health_and_defense():
    attacker = Character(test_character)
    defender = Monster(test_monster)
    start_health = defender.health
    start_defense = defender.defense

    damage, new_health, new_defense = attacker.attack_target(defender)

    assert damage > 0
    assert new_health <= start_health
    assert new_defense < start_defense


def test_character_multiple_attacks():
    attacker = Character(test_character)
    defender = Monster(test_monster)

    for _ in range(10):
        attacker.attack_target(defender)

    assert defender.health >= 0


def test_character_self_attack():
    c = Character(test_character)
    damage, new_health, _ = c.attack_target(c)
    assert damage >= 0
    assert new_health <= c.health


def test_character_str_representation():
    c = Character(test_character)
    rep = str(c)
    assert "Character" in rep
    assert test_character in rep
    assert "HP:" in rep


def test_character_added_to_class_dict():
    c = Character(test_character)
    assert c.id in Character.characters
    assert Character.characters[c.id] is c


def test_character_unique_ids():
    c1 = Character(test_character)
    c2 = Character(test_character)
    assert c1.id != c2.id


def test_attack_target_returns_tuple():
    attacker = Character(test_character)
    defender = Monster(test_monster)
    result = attacker.attack_target(defender)
    assert isinstance(result, tuple)
    assert len(result) == 3
    assert all(isinstance(x, int) for x in result)


def test_character_stat_override_does_not_use_template():
    template_health = Character(test_character).health
    c = Character(test_character, health=template_health + 100)
    assert c.health == template_health + 100


def test_attack_with_zero_attack_does_no_damage():
    attacker = Character(test_character, attack=0)
    defender = Monster(test_monster)
    damage, _, _ = attacker.attack_target(defender)
    assert damage == 0
