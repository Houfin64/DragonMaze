import tcod as libtcod

from enum import Enum

from game_states import GameStates

from menus import inventory_menu, character_screen, help_screen


class RenderOrder(Enum):
    CORPSE = 1
    ITEM = 2
    STAIRS = 3
    ACTOR = 4
    PLAYER = 5


def get_names_under_mouse(mouse, entities, fov_map):
    (x, y) = (mouse.cx, mouse.cy)

    names = [entity.name + ' ' + entity.monster_class + entity.item_class for entity in entities
             if entity.x == x and entity.y == y and libtcod.map_is_in_fov(fov_map, entity.x, entity.y)]
    names = ', '.join(names)

    return names.capitalize()


def render_turn_bar(panel, x, y, total_width, name, value, color):

    libtcod.console_set_default_background(panel, color)

    libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_foreground(panel, libtcod.white)
    libtcod.console_print_ex(panel, int(x + total_width / 2), y, libtcod.BKGND_NONE, libtcod.CENTER,
                             '{0}: {1}'.format(name, value))


def render_bar(panel, x, y, total_width, name, value, maximum, bar_color, back_color):
    bar_width = int(float(value) / maximum * total_width)

    libtcod.console_set_default_background(panel, back_color)
    libtcod.console_rect(panel, x, y, total_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_background(panel, bar_color)
    if bar_width > 0:
        libtcod.console_rect(panel, x, y, bar_width, 1, False, libtcod.BKGND_SCREEN)

    libtcod.console_set_default_foreground(panel, libtcod.white)
    libtcod.console_print_ex(panel, int(x + total_width / 2), y, libtcod.BKGND_NONE, libtcod.CENTER,
                             '{0}: {1}/{2}'.format(name, value, maximum))


def render_all(turns, con, panel, entities, player, game_map, fov_map, fov_recompute, message_log, screen_width, screen_height,
               bar_width, panel_height, panel_y, mouse, colors, game_state):

    if fov_recompute:
        # Draw all the tiles in the game map
        for y in range(game_map.height):
            for x in range(game_map.width):
                visible = libtcod.map_is_in_fov(fov_map, x, y)
                wall = game_map.tiles[x][y].block_sight
                water = game_map.tiles[x][y].water

                if visible:
                    if water:
                        libtcod.console_set_default_foreground(con, colors.get('light_water'))
                        libtcod.console_put_char(con, x, y, '~', libtcod.BKGND_NONE)
                    elif wall:
                        libtcod.console_set_default_foreground(con, colors.get('light_wall'))
                        libtcod.console_put_char(con, x, y, '#', libtcod.BKGND_NONE)
                    else:
                        libtcod.console_set_default_foreground(con, colors.get('light_ground'))
                        libtcod.console_put_char(con, x, y, '.', libtcod.BKGND_NONE)

                    game_map.tiles[x][y].explored = True
                elif game_map.tiles[x][y].explored:
                    if water:
                        libtcod.console_set_default_foreground(con, colors.get('dark_water'))
                        libtcod.console_put_char(con, x, y, '~', libtcod.BKGND_NONE)
                    elif wall:
                        libtcod.console_set_default_foreground(con, colors.get('dark_wall'))
                        libtcod.console_put_char(con, x, y, '#', libtcod.BKGND_NONE)
                    else:
                        libtcod.console_set_default_foreground(con, colors.get('dark_ground'))
                        libtcod.console_put_char(con, x, y, '.', libtcod.BKGND_NONE)

    entities_in_render_order = sorted(entities, key=lambda x: x.render_order.value)

    # Draw all entities in the list
    for entity in entities_in_render_order:
        draw_entity(con, entity, fov_map, game_map)

    libtcod.console_blit(con, 0, 0, screen_width, screen_height, 0, 0, 0)

    libtcod.console_set_default_background(panel, libtcod.black)
    libtcod.console_clear(panel)

    # Print the same message, 1 line at a time
    y = 1
    for message in message_log.messages:
        libtcod.console_set_default_foreground(panel, message.color)
        libtcod.console_print_ex(panel, message_log.x, y, libtcod.BKGND_NONE, libtcod.LEFT, message.text)
        y += 1

    render_bar(panel, 1, 1, bar_width, 'HP', player.fighter.hp, player.fighter.max_hp,
               libtcod.light_red, libtcod.darker_red)
    ailments = None
    color = libtcod.black
    render_turn_bar(panel, 1, 2, bar_width, 'Biome', game_map.biome, color)
    render_turn_bar(panel, 1, 3, bar_width, 'Dungeon level', game_map.dungeon_level, color)
    render_turn_bar(panel, 1, 4, bar_width, 'Turns', turns, color)
    if player.poisoned or player.burned:
        if player.burned:
            ailments = 'Burned'
        if player.poisoned:
            ailments = 'Poisoned'
            if player.burned:
                ailments = ailments + ', \nBurned'
    if ailments:
        render_turn_bar(panel, 1, 5, bar_width, 'Ailments', ailments, color)

    libtcod.console_set_default_foreground(panel, libtcod.light_gray)
    libtcod.console_print_ex(panel, 1, 0, libtcod.BKGND_NONE, libtcod.LEFT,
                             get_names_under_mouse(mouse, entities, fov_map))

    libtcod.console_blit(panel, 0, 0, screen_width, panel_height, 0, 0, panel_y)

    if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY):
        inventory_title = 'Press the key next to a menu to select it, or Esc to cancel.\n'

        inventory_menu(con, inventory_title, player, 50, screen_width, screen_height)

    elif game_state == GameStates.CHARACTER_SCREEN:
        character_screen(player, 30, 12, screen_width, screen_height)

    elif game_state == GameStates.HELP_SCREEN:
        help_screen(50, 45, screen_width, screen_height)

def clear_all(con, entities):
    for entity in entities:
        clear_entity(con, entity)

def draw_entity(con, entity, fov_map, game_map):
    if libtcod.map_is_in_fov(fov_map, entity.x, entity.y) or (entity.stairs and game_map.tiles[entity.x][entity.y].explored):
        libtcod.console_set_default_foreground(con, entity.color)
        libtcod.console_put_char(con, entity.x, entity.y, entity.char, libtcod.BKGND_NONE)

def clear_entity(con, entity):
    # erase the character that represents this object
    libtcod.console_put_char(con, entity.x, entity.y, ' ', libtcod.BKGND_NONE)