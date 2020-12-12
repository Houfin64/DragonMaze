import tcod as libtcod

from render_functions import RenderOrder
from components.item import Item
from game_messages import Message
from item_functions import feed
from game_states import GameStates


def kill_player(player):
    player.char = '%'
    player.color = libtcod.dark_red

    return Message('You died. Oh Well. Esc to exit.', libtcod.red), GameStates.PLAYER_DEAD

def kill_boss(boss):
    boss.char = '%'
    boss.color = libtcod.darkest_red
    boss.blocks = False
    boss.fighter = None
    boss.ai = None
    boss.name = boss.name + ' Corpse'
    boss.render_order = RenderOrder.CORPSE
    boss.item_class = '(Corpse)'

    return Message('You have vanquished the foul beast at the bottom of these Pits.  Go onward to claim your prize, Great Hero', libtcod.fuchsia)


def kill_monster(monster, game_map, entities):
    death_message = Message('The {0} is dead!'.format(monster.name.capitalize()), libtcod.orange)

    monster.item = Item(use_function=feed, sound = 10, health = int(monster.fighter.hp / 2), game_map = game_map, entities = entities)
    monster.char = '%'
    monster.color = libtcod.dark_red
    monster.blocks = False
    monster.fighter = None
    monster.ai = None
    monster.name = monster.name + ' Corpse'
    monster.render_order = RenderOrder.CORPSE
    monster.item_class = '(Corpse)'

    return death_message

def kill_pet(pet):
    death_message = Message('You feel a moment of extreme sadness, then it passes', libtcod.fuchsia)

    pet.char = '%'
    pet.color = libtcod.blue
    pet.blocks = False
    pet.fighter = None
    pet.ai = None
    pet.name = 'remains of ' + pet.name
    pet.render_order = RenderOrder.CORPSE

    return death_message