import tcod as libtcod
from random import randint

from game_messages import Message
from entity import get_blocking_entities_at_location
from components.ai import ConfusedMonster, FrozenMonster


def feed(*args, **kwargs):
    results = []
    pet = False
    close = 3
    player = args[0]
    entities = kwargs.get('entities')
    health = kwargs.get('health')

    for entity in entities:
        if entity.monster_class == '(Pet)' or ('remains' in entity.name and 'pet' in entity.name):
            distance = player.distance_to(entity)
            if distance < close:
                close = distance
                pet = entity
    if pet:
        if pet.fighter.hp > 0:
                pet.fighter.hp += health
                results.append({'consumed': True, 'message': Message('Your pet growls happily', libtcod.green)})

        else:
            results.append({'consumed': False, 'message': Message('You can\'t feed a dead pet!', libtcod.yellow)})
    else:
        results.append({'message': Message('You don\'t have a pet close enough', libtcod.yellow)})

    return results


def shoot(*args, **kwargs):
    shooter = args[0]
    damage = kwargs.get('damage')
    direction = kwargs.get('direction')
    entities = kwargs.get('entities')
    target = None
    arrow = False

    for item in shooter.inventory.items:
        if item.name == 'Arrow':
            arrow = True
            break
    if arrow:

        for i in range(1, 11):
            damage = (shooter.fighter.dexterity * 2) + 2
            if direction == 'up':
                if get_blocking_entities_at_location(entities, shooter.x, shooter.y - i):
                    if get_blocking_entities_at_location(entities, shooter.x + i, shooter.y).monster_class != '(Pet)':
                        target = get_blocking_entities_at_location(entities, shooter.x, shooter.y - i)

            elif direction == 'down':
                if get_blocking_entities_at_location(entities, shooter.x, shooter.y + i):
                    if get_blocking_entities_at_location(entities, shooter.x + i, shooter.y).monster_class != '(Pet)':
                        target = get_blocking_entities_at_location(entities, shooter.x, shooter.y + i)

            elif direction == 'left':
                if get_blocking_entities_at_location(entities, shooter.x - i, shooter.y):
                    if get_blocking_entities_at_location(entities, shooter.x + i, shooter.y).monster_class != '(Pet)':
                        target = get_blocking_entities_at_location(entities, shooter.x - i, shooter.y)

            elif direction == 'right':
                if get_blocking_entities_at_location(entities, shooter.x + i, shooter.y):
                    if get_blocking_entities_at_location(entities, shooter.x + i, shooter.y).monster_class != '(Pet)':
                        target = get_blocking_entities_at_location(entities, shooter.x + i, shooter.y)

            if target:
                break

        results = []
        for item in shooter.inventory.items:
            if item.name == 'Arrow':
                arrow = item

        miss = randint(0, 100)
        if miss < 5:
            miss = True
        else:
            miss = False

        if miss or not target:
            results.append({'arrow_consumed': arrow, 'consumed': False, 'message': Message('You miss everything, and the arrow disappears into the dark', libtcod.fuchsia)})

            return results
        else:
            results.append({'consumed': False, 'message': Message('You shoot the {0}!'.format(target.name),libtcod.orange)})
            levelup = shooter.level.add_bow_xp(1)
            if levelup:
                shooter.fighter.dexterity += 1
                results.append({'message': Message('You get better at wielding your bow, you must have been practicing', libtcod.fuchsia)})
            results.append({'arrow_consumed': arrow, 'consumed': False, 'message': Message('The {0} takes {1} damage!'.format(target.name, damage), libtcod.orange)})
            damage_results = target.fighter.take_damage(damage)
            for damage_result in damage_results:
                dead = damage_result.get('dead')
                xp = damage_result.get('xp')
                results.append({'dead': dead, 'xp': xp})
            target.arrows += 1
        return results

    else:
        results = []
        results.append({'consumed': False, 'message': Message('You reach into your quiver, and have a sudden feeling of dread...', libtcod.yellow)})
        return results


def big_shoot(*args, **kwargs):
    shooter = args[0]
    damage = kwargs.get('damage')
    direction = kwargs.get('direction')
    entities = kwargs.get('entities')
    target = None
    arrow = False

    for item in shooter.inventory.items:
        if item.name == 'Arrow':
            arrow = True
            break
    if arrow:

        for i in range(1, 11):
            damage = (shooter.fighter.dexterity * 3)
            if direction == 'up':
                if get_blocking_entities_at_location(entities, shooter.x, shooter.y - i):
                    if get_blocking_entities_at_location(entities, shooter.x + i, shooter.y).monster_class != '(Pet)':
                        target = get_blocking_entities_at_location(entities, shooter.x, shooter.y - i)

            elif direction == 'down':
                if get_blocking_entities_at_location(entities, shooter.x, shooter.y + i):
                    if get_blocking_entities_at_location(entities, shooter.x + i, shooter.y).monster_class != '(Pet)':
                        target = get_blocking_entities_at_location(entities, shooter.x, shooter.y + i)

            elif direction == 'left':
                if get_blocking_entities_at_location(entities, shooter.x - i, shooter.y):
                    if get_blocking_entities_at_location(entities, shooter.x + i, shooter.y).monster_class != '(Pet)':
                        target = get_blocking_entities_at_location(entities, shooter.x - i, shooter.y)

            elif direction == 'right':
                if get_blocking_entities_at_location(entities, shooter.x + i, shooter.y):
                    if get_blocking_entities_at_location(entities, shooter.x + i, shooter.y).monster_class != '(Pet)':
                        target = get_blocking_entities_at_location(entities, shooter.x + i, shooter.y)

            if target:
                break

        results = []
        for item in shooter.inventory.items:
            if item.name == 'Arrow':
                arrow = item

        miss = randint(0, 100)
        if miss < 5:
            miss = True
        else:
            miss = False

        if miss or not target:
            results.append({'arrow_consumed': arrow, 'consumed': False, 'message': Message('You miss everything, and the arrow disappears into the dark', libtcod.fuchsia)})

            return results
        else:
            results.append({'consumed': False, 'message': Message('You shoot the {0}!'.format(target.name),libtcod.orange)})
            levelup = shooter.level.add_bow_xp(1)
            if levelup:
                shooter.fighter.dexterity += 1
                results.append({'message': Message('You get better at wielding your bow, you must have been practicing', libtcod.fuchsia)})
            results.append({'arrow_consumed': arrow, 'consumed': False, 'message': Message('The {0} takes {1} damage!'.format(target.name, damage), libtcod.orange)})
            damage_results = target.fighter.take_damage(damage)
            for damage_result in damage_results:
                dead = damage_result.get('dead')
                xp = damage_result.get('xp')
                results.append({'dead': dead, 'xp': xp})
            target.arrows += 1
        return results

    else:
        results = []
        results.append({'consumed': False, 'message': Message('You reach into your quiver, and have a sudden feeling of dread...', libtcod.yellow)})
        return results


def antidote(*args, **kwargs):
    player = args[0]
    results = []

    if player.poisoned:
        player.poisoned = False
        results.append({'consumed': True, 'message': Message('you feel a lot better', libtcod.light_cyan)})

    else:
        results.append({'consumed': False, 'message': Message('you aren\'t poisoned', libtcod.yellow)})

    return results


def burn_salve(*args, **kwargs):
    player = args[0]
    results = []

    if player.burned:
        player.burned = False
        results.append({'consumed': True, 'message': Message('you feel a lot better', libtcod.light_cyan)})

    else:
        results.append({'consumed': False, 'message': Message('you aren\'t burning', libtcod.yellow)})

    return results


def heal(*args, **kwargs):
    entity = args[0]
    amount = kwargs.get('amount')

    results = []

    if entity.fighter.hp == entity.fighter.max_hp:
        results.append({'consumed': False, 'message': Message('You are already at full health', libtcod.yellow)})
    else:
        entity.fighter.heal(amount)
        results.append({'consumed': True, 'message': Message('Your wounds start to feel better!', libtcod.green)})
    return results


def cast_lightning(*args, **kwargs):
    caster = args[0]
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    maximum_range = kwargs.get('maximum_range')

    results = []

    target = None
    closest_distance = maximum_range + 1

    for entity in entities:
        if entity.fighter and entity != caster and libtcod.map_is_in_fov(fov_map, entity.x, entity.y):
            distance = caster.distance_to(entity)

            if distance < closest_distance and entity.monster_class != '(Pet)':
                target = entity
                closest_distance = distance

    if target:
        results.append({'consumed': True, 'target': target, 'message': Message('A lighting bolt strikes the {0} with a loud thunder for {1} hp!'.format(target.name, damage))})
        results.extend(target.fighter.take_damage(damage))
    else:
        results.append({'consumed': False, 'target': None, 'message': Message('No enemy is close enough to strike.', libtcod.red)})

    return results


def cast_fireball(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    damage = kwargs.get('damage')
    radius = kwargs.get('radius')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False, 'message': Message('You cannot target a tile outside your field of view.', libtcod.yellow)})
        return results

    results.append({'consumed': True, 'message': Message('The fireball explodes, burning everything within {0} tiles!'.format(radius), libtcod.orange)})

    for entity in entities:
        if entity.distance(target_x, target_y) <= radius and entity.fighter:
                results.append({'message': Message('The {0} gets burned for {1} hit points.'.format(entity.name, damage), libtcod.orange)})
                results.extend(entity.fighter.take_damage(damage))

    return results


def cast_confuse(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False, 'message': Message('You cannot target a tile outside your field of view.', libtcod.yellow)})
        return results

    for entity in entities:
        if entity.x == target_x and entity.y == target_y and entity.ai:
            confused_ai = ConfusedMonster(entity.ai, 10)

            confused_ai.owner = entity
            entity.ai = confused_ai

            results.append({'consumed': True, 'message': Message('The eyes of the {0} look vacant, as he starts to stumble around!'.format(entity.name), libtcod.light_green)})

            break
    else:
        results.append({'consumed': False, 'message': Message('There is no targetable enemy at that location.', libtcod.red)})

    return results


def cast_freeze(*args, **kwargs):
    entities = kwargs.get('entities')
    fov_map = kwargs.get('fov_map')
    target_x = kwargs.get('target_x')
    target_y = kwargs.get('target_y')

    results = []

    if not libtcod.map_is_in_fov(fov_map, target_x, target_y):
        results.append({'consumed': False, 'message': Message('You cannot target a tile outside your field of view.', libtcod.red)})
        return results

    for entity in entities:
        if entity.x == target_x and entity.y == target_y and entity.ai:
            frozen_ai = FrozenMonster(entity.ai, 15)

            frozen_ai.owner = entity
            entity.ai = frozen_ai

            results.append({'consumed': True, 'message': Message('The {0} starts to turn blue, and stops moving!'.format(entity.name), libtcod.light_cyan)})

            break
    else:
        results.append({'consumed': False, 'message': Message('There is no targetable enemy at that location.', libtcod.red)})

    return results