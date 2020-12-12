import tcod as libtcod

from components.fighter import Fighter
from components.inventory import Inventory
from components.level import Level
from components.equipment import Equipment
from components.equippable import Equippable
from components.item import Item
from item_functions import shoot
from game_messages import Message
from entity import Entity
from equipment_slots import EquipmentSlots
from game_messages import MessageLog
from game_states import GameStates
from map_objects.game_map import GameMap
from render_functions import RenderOrder

def get_constants():
    window_title = 'Dragon Maze'

    screen_width = 80
    screen_height = 50

    bar_width = 20
    panel_height = 7
    panel_y = screen_height - panel_height

    message_x = bar_width + 2
    message_width = screen_width - bar_width - 2
    message_height = panel_height - 1

    map_width = 80
    map_height = 43

    room_max_size = 10
    room_min_size = 6
    max_rooms = 30

    fov_algorithm = 0
    fov_light_walls = True
    fov_radius = 5

    constants = {
        'window_title': window_title,
        'screen_width': screen_width,
        'screen_height': screen_height,
        'bar_width': bar_width,
        'panel_height': panel_height,
        'panel_y': panel_y,
        'message_x': message_x,
        'message_width': message_width,
        'message_height': message_height,
        'map_width': map_width,
        'map_height': map_height,
        'room_max_size': room_max_size,
        'room_min_size': room_min_size,
        'max_rooms': max_rooms,
        'fov_algorithm': fov_algorithm,
        'fov_light_walls': fov_light_walls,
        'fov_radius': fov_radius,
    }

    return constants


def get_game_variables(constants):

    fighter_component = Fighter(hp=100, defence=1, power=2, intelligence=2, dexterity=2)
    inventory_component = Inventory(100)
    level_component = Level()
    equipment_component = Equipment()
    player = Entity(0, 0, '@', libtcod.white, 'Player', blocks=True, render_order=RenderOrder.PLAYER,
                    fighter=fighter_component, inventory=inventory_component, level = level_component,
                    equipment=equipment_component, monster_class = '')

    entities = [player]
    player.items = []

    equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=2, dexterity_bonus=1)
    dagger = Entity(0, 0, '-', libtcod.sky, 'Dagger', equippable=equippable_component, item_class = '(Equipment)')
    player.inventory.add_item(dagger)
    player.equipment.toggle_equip(dagger)

    fighter_component = Fighter(hp=50, defence = 1, power = 1)
    pet = Entity(0, 0, '0', 0, 'Pet', fighter=fighter_component, monster_class = '(Pet)')

    item_component = Item(use_function = shoot, arrow_targeting=True, targeting_message=Message(
                    'Use arrow keys or numpad to shoot in a direction.', libtcod.light_cyan))
    bow = Entity(0, 0, '{', libtcod.orange, 'Bow', item=item_component, item_class = '(Bow)')

    player.inventory.add_item(bow)

    item_component = Item(use_function=None)
    Arrow = Entity(0, 0, '|', libtcod.sepia, 'Arrow', item=item_component, item_class = '(Arrow)')
    for i in range(0, 10):
        player.inventory.add_item(Arrow)

    game_map = GameMap(constants['map_width'], constants['map_height'])
    game_map.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['map_width'], constants['map_height'], player, entities, pet, 'down')

    message_log = MessageLog(constants['message_x'], constants['message_width'], constants['message_height'])

    game_state = GameStates.PLAYERS_TURN

    turns = 0

    poison_turns = -42

    burned_turns = -42

    frozen_turns = -42

    return player, entities, game_map, message_log, game_state, poison_turns, turns, burned_turns, frozen_turns
