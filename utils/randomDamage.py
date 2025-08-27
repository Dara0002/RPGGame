import random


def random_damage(base_damage, base_defence, target_health):
    new_damage = int(random.randint(base_damage // 2, base_damage * 2))
    if base_defence > 0:
        if new_damage >= base_defence:
            new_damage -= base_defence
            base_defence = 0
            target_health -= new_damage
        else:
            base_defence -= new_damage
        return (new_damage, target_health, base_defence)
    else:
        target_health -= new_damage
        return (new_damage, max(0, target_health), base_defence)
