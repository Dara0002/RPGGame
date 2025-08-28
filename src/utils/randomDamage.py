import random


def random_damage(
    base_damage: int, target_health: int, target_defense: int
) -> tuple[int, int, int]:
    new_damage = int(random.randint(base_damage // 2, base_damage * 2))
    if target_defense > 0:
        if new_damage >= target_defense:
            new_damage -= target_defense
            target_defense = 0
            target_health -= new_damage
        else:
            target_defense -= new_damage
        return (new_damage, target_health, target_defense)
    else:
        target_health -= new_damage
        return (new_damage, max(0, target_health), target_defense)
