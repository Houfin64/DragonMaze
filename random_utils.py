from random import randint


def from_dungeon_level(table, dungeon_level):
    for (value, level) in reversed(table):
        if dungeon_level >= level:
            return value

    return 0


def random_choice_index(chances):
    random_chance = randint(1, sum(chances))

    running_sum = 0
    choice = 0
    for w in chances:
        running_sum += w

        if random_chance <= running_sum:
            return choice
        choice += 1


def random_choice_from_dict(choice_dict):
    choices = list(choice_dict.keys())
    chances = list(choice_dict.values())

    return choices[random_choice_index(chances)]


def tail_off_probability(dungeon_level, base_percent, base_level, biome_start, biome_end):

    if dungeon_level > biome_start and dungeon_level < biome_end:

        dif = abs(int(dungeon_level - base_level))

        value = (1 / (dif+1)) * base_percent

        return int(value)
    else:
        return 0
