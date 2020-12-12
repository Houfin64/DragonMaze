import tcod as libtcod
from random import randint
from components.track_functions import Scent
from game_messages import Message

class NPC:
    def take_turn(self, player, fov_map, game_map, entities, turns):
        npc = self.owner
        results = []
        move_results = npc.move_random
        results.extend(move_results)
        return results

class BasicPet:
    def take_turn(self, player, fov_map, game_map, entities, turns):
        results = []
        close = 10
        target = None
        pet = self.owner
        move_results = None
        attack_results = None
        for entity in entities:
            if (pet.distance_to(entity) < close) and (entity.ai) and (entity.name != 'Pet') and (libtcod.map_is_in_fov(fov_map, entity.x, entity.y)):
                target = entity
                close = pet.distance_to(entity)
        if target and pet.distance_to(target) >= 2:
            move_results = pet.move_towards(target.x, target.y, game_map, entities)
            results.extend(move_results)
        elif target and target.fighter.hp > 0:
            attack_results = pet.fighter.attack(target)
            results.extend(attack_results)
        if not move_results and not attack_results and pet.distance_to(player) < 4:
            move_results = pet.move_random(entities, game_map)
            results.extend(move_results)
        elif not move_results and not attack_results:
            move_results = pet.move_astar(player, entities, game_map)
            results.extend(move_results)
        return results

class BasicMonster:
    def take_turn(self, target, fov_map, game_map, entities, turns):
        results = []
        monster = self.owner
        if libtcod.map_is_in_fov(fov_map, monster.x, monster.y):

            if monster.distance_to(target) >= 2:
                move_results = monster.move_astar(target, entities, game_map)
                results.extend(move_results)

            elif target.fighter.hp > 0:
                attack_results = monster.fighter.attack(target)
                poison = randint(0, 100)
                burn = randint(0, 100)
                freeze = randint(0, 100)
                if monster.poisons_chance > poison:
                    results.append({'poisoned': True})
                elif monster.burns_chance > burn:
                    results.append({'burned': True})
                elif monster.freezes_chance > freeze:
                    results.append({'frozen': True})
                results.extend(attack_results)

        else:
            if monster.distance_to(target) < target.sound:
                move_results = monster.move_astar(target, entities, game_map)
                results.extend(move_results)
            else:
                move_direction = Scent.get_scent(game_map, monster.x, monster.y, turns)
                if move_direction == []:
                    move_results = monster.move_random(entities, game_map)
                    results.extend(move_results)
                else:
                    monster.move_scent(move_direction)
        return results


class ConfusedMonster:
    def __init__(self, previous_ai, number_of_turns=10):
        self.previous_ai = previous_ai
        self.number_of_turns = number_of_turns

    def take_turn(self, target, fov_map, game_map, entities, turns):
        results = []

        if self.number_of_turns > 0:
            random_x = self.owner.x + randint(0, 2) - 1
            random_y = self.owner.y + randint(0, 2) - 1

            if random_x != self.owner.x and random_y != self.owner.y:
                self.owner.move_towards(random_x, random_y, game_map, entities)

            self.number_of_turns -= 1
        else:
            self.owner.ai = self.previous_ai
            results.append({'message': Message('The {0} is no longer confused!'.format(self.owner.name), libtcod.red)})

        return results

class FrozenMonster:
    def __init__(self, previous_ai, number_of_turns = 10):
        self.previous_ai = previous_ai
        self.number_of_turns = number_of_turns

    def take_turn(self, target, fov_map, game_map, entities, turns):
        results = []

        if self.number_of_turns > 0:
            self.number_of_turns -= 1

        else:
            self.owner.ai = self.previous_ai
            results.append({'message': Message('The {0} is no longer frozen!'.format(self.owner.name), libtcod.red)})

        return results