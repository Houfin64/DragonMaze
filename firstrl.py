import tcod as libtcod
from random import randint

from death_functions import kill_monster, kill_player, kill_pet, kill_boss
from entity import get_blocking_entities_at_location, Entity
from fov_functions import initialize_fov, recompute_fov
from game_messages import Message, MessageLog
from game_states import GameStates
from components.track_functions import Scent
from components.item import Item
from input_handler import handle_keys, handle_mouse, handle_main_menu
from loader_functions.initialize_new_game import get_constants, get_game_variables
from loader_functions.data_loaders import load_game, save_game
from menus import main_menu, message_box
from render_functions import clear_all, render_all


def main():
    constants = get_constants()

    libtcod.console_set_custom_font('arial10x10.png', libtcod.FONT_TYPE_GREYSCALE | libtcod.FONT_LAYOUT_TCOD)

    libtcod.console_init_root(constants['screen_width'], constants['screen_height'], constants['window_title'], False)

    con = libtcod.console_new(constants['screen_width'], constants['screen_height'])
    panel = libtcod.console_new(constants['screen_width'], constants['panel_height'])

    player = None
    entities = []
    game_map = None
    message_log = None
    game_state = None
    turns = None
    poison_turns = None
    burned_turns = None
    frozen_turns = None

    show_main_menu = True
    show_load_error_message = False

    main_menu_background_image = libtcod.image_load('menu_background1.png')

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        if show_main_menu:
            main_menu(con, main_menu_background_image, constants['screen_width'], constants['screen_height'])

            if show_load_error_message:
                message_box(con, 'No save game to load', 50, constants['screen_width'], constants['screen_height'])

            libtcod.console_flush()

            action = handle_main_menu(key)

            new_game = action.get('new_game')
            load_saved_game = action.get('load_game')
            exit_game = action.get('exit')

            if show_load_error_message and (new_game or load_saved_game or exit_game):
                show_load_error_message = False
            elif new_game:
                player, entities, game_map, message_log, game_state, poison_turns, turns, burned_turns, frozen_turns = get_game_variables(constants)
                game_state = GameStates.PLAYERS_TURN

                show_main_menu = False
            elif load_saved_game:
                try:
                    player, entities, game_map, message_log, game_state, poison_turns, turns, burned_turns, frozen_turns = load_game()
                    show_main_menu = False
                except FileNotFoundError:
                    show_load_error_message = True
            elif exit_game:
                break

        else:
            libtcod.console_clear(con)

            play_game(player, entities, game_map, message_log, game_state, con, panel, constants, turns, poison_turns, burned_turns, frozen_turns)

            show_main_menu = True


def play_game(player, entities, game_map, message_log, game_state, con, panel, constants, turns, poison_turns, burned_turns, frozen_turns):

    fov_recompute = True
    pet = 0
    boss = None
    for entity in entities:
        if entity.name == 'Pet':
            pet = entity
            break
    for entity  in entities:
        if entity.name == 'Dragonlord':
            boss = entity
            break

    fov_map = initialize_fov(game_map)

    key = libtcod.Key()
    mouse = libtcod.Mouse()

    game_state = GameStates.PLAYERS_TURN
    previous_game_state = game_state

    targeting_item = None
    arrow_targeting_item = None

    while not libtcod.console_is_window_closed():
        libtcod.sys_check_for_event(libtcod.EVENT_KEY_PRESS | libtcod.EVENT_MOUSE, key, mouse)

        if fov_recompute:
            recompute_fov(fov_map, player.x, player.y, constants['fov_radius'], constants['fov_light_walls'],
                          constants['fov_algorithm'])

        if game_map.biome == 'The Dungeon':
            colors = {
                'dark_wall': libtcod.darkest_grey,
                'dark_ground': libtcod.darker_grey,
                'light_wall': libtcod.grey,
                'light_ground': libtcod.white,
                'dark_water': libtcod.blue,
                'light_water': libtcod.light_blue
            }
        elif game_map.biome == 'The Icebleak Cavern':
            colors = {
                'dark_wall': libtcod.darkest_cyan,
                'dark_ground': libtcod.darker_cyan,
                'light_wall': libtcod.dark_cyan,
                'light_ground': libtcod.white,
                'dark_water': libtcod.blue,
                'light_water': libtcod.light_blue
            }
        elif game_map.biome == 'The Underglade':
            colors = {
                'dark_wall': libtcod.darker_green,
                'dark_ground': libtcod.darkest_green,
                'light_wall': libtcod.desaturated_green,
                'light_ground': libtcod.brass,
                'dark_water': libtcod.blue,
                'light_water': libtcod.light_blue
            }
        elif game_map.biome == 'The Hadalrealm':
            colors = {
                'dark_wall': libtcod.darkest_red,
                'dark_ground': libtcod.darker_red,
                'light_wall': libtcod.dark_red,
                'light_ground': libtcod.white,
                'dark_water': libtcod.blue,
                'light_water': libtcod.light_blue
            }
        elif game_map.biome == 'Dragonroost':
            colors = {
                'dark_wall': libtcod.darkest_grey,
                'dark_ground': libtcod.darker_grey,
                'light_wall': libtcod.dark_grey,
                'light_ground': libtcod.grey,
                'dark_water': libtcod.blue,
                'light_water': libtcod.light_blue
            }
        elif game_map.biome == 'Oblivion\'s Gate':
            colors = {
                'dark_wall': libtcod.darkest_grey,
                'dark_ground': libtcod.darker_grey,
                'light_wall': libtcod.dark_grey,
                'light_ground': libtcod.white,
                'dark_water': libtcod.blue,
                'light_water': libtcod.light_blue
            }
        elif game_map.biome == 'The Vault':
            colors = {
                'dark_wall': libtcod.darker_yellow,
                'dark_ground': libtcod.dark_yellow,
                'light_wall': libtcod.yellow,
                'light_ground': libtcod.white,
                'dark_water': libtcod.blue,
                'light_water': libtcod.light_blue
            }

        render_all(turns, con, panel, entities, player, game_map, fov_map, fov_recompute, message_log,
                   constants['screen_width'], constants['screen_height'], constants['bar_width'],
                   constants['panel_height'], constants['panel_y'], mouse, colors, game_state)

        fov_recompute = False

        libtcod.console_flush()

        clear_all(con, entities)

        action = handle_keys(key, game_state)
        mouse_action = handle_mouse(mouse)

        player.sound = 0
        Scent.set_scent(game_map, player.x, player.y, turns)

        move = action.get('move')
        pickup = action.get('pickup')
        show_inventory = action.get('show_inventory')
        drop_inventory = action.get('drop_inventory')
        inventory_index = action.get('inventory_index')
        exit = action.get('exit')
        fullscreen = action.get('fullscreen')
        wait = action.get('wait')
        take_up_stairs = action.get('take_up_stairs')
        take_down_stairs = action.get('take_down_stairs')
        level_up = action.get('level_up')
        show_character_screen = action.get('show_character_screen')
        show_help_screen = action.get('show_help_screen')

        left_click = mouse_action.get('left_click')
        right_click = mouse_action.get('right_click')

        up = action.get('up')
        down = action.get('down')
        left = action.get('left')
        right = action.get('right')

        player_turn_results = []

        if player.frozen and frozen_turns > 0:
            game_state = GameStates.ENEMY_TURN

        if player.frozen == False:
            frozen_turns = -42

        if player.burned == False:
            burned_turns= -42

        if player.poisoned == False:
            poison_turns = -42

        if poison_turns == 0:
            player_turn_results.append({'message': Message('You feel a lot better', libtcod.light_cyan)})
            poison_turns = -42
            player.poisoned = False

        if burned_turns == 0:
            player_turn_results.append({'message': Message('Your burn feels a lot better', libtcod.light_cyan)})
            burned_turns = -42
            player.burned = False

        if frozen_turns == 0:
            player_turn_results.append({'message': Message('You defrost', libtcod.light_cyan)})
            frozen_turns = -42
            player.frozen = False

        if wait:
            game_state = GameStates.ENEMY_TURN
            d = randint(0, 100)
            if d < 25:
                message_log.add_message(Message('You stand around doing nothing', libtcod.brass))
            elif d < 50:
                message_log.add_message(Message('You lean on your sword', libtcod.brass))
            elif d < 75:
                message_log.add_message(Message('You stand around looking like a lemon', libtcod.brass))
            else:
                message_log.add_message(Message('You examine your surroundings intensely', libtcod.light_amber))

        if move and game_state == GameStates.PLAYERS_TURN:
            dx, dy = move
            destination_x = player.x + dx
            destination_y = player.y + dy

            if not game_map.is_blocked(destination_x, destination_y):
                target = get_blocking_entities_at_location(entities, destination_x, destination_y)
                if target:
                    if target.name == 'Pet':
                        target = None
                if target:
                    attack_results = player.fighter.attack(target)
                    player_turn_results.extend(attack_results)
                else:

                    if game_map.tiles[player.x][player.y].water == True:
                        if randint(0, 10) == 1:
                            game_map.tiles[destination_x][destination_y].water = True
                            player_turn_results.append({'message': Message('You splash water all over the dry bit of floor', libtcod.cyan)})
                    player.move(dx, dy)
                    player.sound = 10

                    if turns % randint(9, 11) == 0:
                        player.fighter.heal(1)

                    levelup = player.level.add_con_xp(1)
                    if levelup:
                        player.fighter.hp += 20
                        player.fighter.base_max_hp += 20
                        player_turn_results.append({'message': Message('You feel healthy, you must have been very active', libtcod.fuchsia)})

                    fov_recompute = True

                game_state = GameStates.ENEMY_TURN

        elif pickup and game_state == GameStates.PLAYERS_TURN:
            here = 0
            for entity in entities:
                if entity.name != 'Player' and not entity.stairs and not entity.monster_class == '(Pet)':
                    if (entity.item or entity.equippable) and entity.x == player.x and entity.y == player.y:
                        here = 1
                        player.sound = 5
                        pickup_results = player.inventory.add_item(entity)
                        player_turn_results.extend(pickup_results)
            else:
                if here == 0:
                    message_log.add_message(Message('There is nothing here to pick up.', libtcod.yellow))

        if show_inventory:
            previous_game_state = game_state
            game_state = GameStates.SHOW_INVENTORY

        if drop_inventory:
            previous_game_state = game_state
            player.sound = 5
            game_state = GameStates.DROP_INVENTORY

        if inventory_index is not None and previous_game_state != GameStates.PLAYER_DEAD and inventory_index < len(player.items):
            item = player.items[inventory_index]
            if type(item) != str:
                if game_state == GameStates.SHOW_INVENTORY:
                    success = True
                    if item.item_class == '(Scroll)':
                        difficulty = randint(0, 10)
                        if difficulty > player.fighter.intelligence:
                            success = False
                        else:
                            levelup = player.level.add_int_xp(1)
                            if levelup:
                                message_log.add_message(Message('Your reading grows more accurate!', libtcod.fuchsia))
                                player.fighter.base_intelligence += 1

                    player_turn_results.extend(player.inventory.use(success, item, entities=entities, fov_map=fov_map))
                elif game_state == GameStates.DROP_INVENTORY:
                    player_turn_results.extend(player.inventory.drop_item(item))
            else:
                message_log.add_message(Message('You can\'t use Headers', libtcod.yellow))

        if take_up_stairs and game_state == GameStates.PLAYERS_TURN and not boss:
            for entity in entities:
                if entity.stairs and entity.x == player.x and entity.y == player.y:
                    pet, entities = game_map.next_floor(player, message_log, constants, entities, 'up')
                    fov_map = initialize_fov(game_map)
                    fov_recompute = True
                    player.sound = 10
                    libtcod.console_clear(con)

                    break
            else:
                message_log.add_message(Message('You can\'t go up here.', libtcod.yellow))

        if take_down_stairs and game_state == GameStates.PLAYERS_TURN and not boss:
            for entity in entities:
                if entity.stairs and entity.x == player.x and entity.y == player.y:
                    pet, entities = game_map.next_floor(player, message_log, constants, entities, 'down')
                    fov_map = initialize_fov(game_map)
                    fov_recompute = True
                    player.sound = 10
                    libtcod.console_clear(con)

                    break
            else:
                message_log.add_message(Message('You can\'t go down here.', libtcod.yellow))

        if level_up:
            if level_up == 'hp':
                player.fighter.base_max_hp += 20
                player.fighter.hp += 20
            elif level_up == 'str':
                player.fighter.base_power += 1
            elif level_up == 'def':
                player.fighter.base_defence += 1
            elif level_up == 'int':
                player.fighter.base_intelligence += 1
            elif level_up == 'dex':
                player.fighter.base_dexterity += 1

            game_state = previous_game_state

        if show_character_screen:
            previous_game_state = game_state
            game_state = GameStates.CHARACTER_SCREEN

        if show_help_screen:
            previous_game_state = game_state
            game_state = GameStates.HELP_SCREEN

        if game_state == GameStates.TARGETING:
            if left_click:
                target_x, target_y = left_click
                item_use_results = player.inventory.use(success, targeting_item, entities=entities, fov_map=fov_map,
                                                        target_x=target_x, target_y=target_y)
                player_turn_results.extend(item_use_results)
            elif right_click:
                player_turn_results.append({'targeting_cancelled': True})

        if game_state == GameStates.ARROW_TARGETING:
            direction = None
            if up:
                direction = 'up'
            elif down:
                direction = 'down'
            elif left:
                direction = 'left'
            elif right:
                direction = 'right'
            if direction:
                item_use_results = player.inventory.use(success, arrow_targeting_item, entities=entities, fov_map=fov_map,
                                                        direction = direction)

                player_turn_results.extend(item_use_results)

        if exit:
            if game_state in (GameStates.SHOW_INVENTORY, GameStates.DROP_INVENTORY, GameStates.CHARACTER_SCREEN, GameStates.HELP_SCREEN):
                game_state = previous_game_state
            elif game_state == GameStates.TARGETING or game_state == GameStates.ARROW_TARGETING:
                player_turn_results.append({'targeting_cancelled': True})
            else:
                save_game(player, entities, game_map, message_log, game_state, poison_turns, turns, burned_turns, frozen_turns)
                return True

        if fullscreen:
            libtcod.console_set_fullscreen(not libtcod.console_is_fullscreen())

        for player_turn_result in player_turn_results:
            message = player_turn_result.get('message')
            dead_entity = player_turn_result.get('dead')
            item_added = player_turn_result.get('item_added')
            item_consumed = player_turn_result.get('consumed')
            arrow_consumed = player_turn_result.get('arrow_consumed')
            item_dropped = player_turn_result.get('item_dropped')
            equip = player_turn_result.get('equip')
            targeting = player_turn_result.get('targeting')
            arrow_targeting = player_turn_result.get('arrow_targeting')
            targeting_cancelled = player_turn_result.get('targeting_cancelled')
            player_burned = player_turn_result.get('burned')
            enemy_turn = player_turn_result.get('pass')

            if enemy_turn:
                game_state = GameStates.ENEMY_TURN

            if player_burned:
                player_turn_results.append({'message': Message('You get Burned', libtcod.flame)})
                burned_turns = randint(5, 10)
                message = player_turn_result.get('message')

            if message:
                message_log.add_message(message)

            if dead_entity:
                if dead_entity == player:
                    message, game_state = kill_player(dead_entity)
                else:
                    message = kill_monster(dead_entity, game_map, entities)
                    arrows = 0
                    for i in range(0, dead_entity.arrows):
                        arrow_break = randint(0, 1)
                        if not arrow_break:
                            item_component = Item(use_function=None)
                            arrow = Entity(dead_entity.x, dead_entity.y, '|', libtcod.sepia, 'Arrow', item=item_component, item_class = '(Arrow)')
                            entities.append(arrow)
                        else:
                            arrows += 1
                    if arrows == 1:
                        MessageLog.add_message(self=message_log, message=Message('The arrow stuck in the {0} breaks as it falls over'.format(dead_entity.name), libtcod.red))
                    elif arrows:
                        MessageLog.add_message(self=message_log, message=Message(
                            'The {0} arrows stuck in the {1} breaks as it falls over'.format(arrows, dead_entity.name), libtcod.red))

                message_log.add_message(message)

            if item_added:
                entities.remove(item_added)

                game_state = GameStates.ENEMY_TURN

            if item_consumed:
                game_state = GameStates.ENEMY_TURN

            if arrow_consumed:
                game_state = GameStates.ENEMY_TURN

            if item_dropped:
                entities.append(item_dropped)

                game_state = GameStates.ENEMY_TURN

            if equip:
                player.sound = 10
                equip_results = player.equipment.toggle_equip(equip)

                for equip_result in equip_results:
                    equipped = equip_result.get('equipped')
                    dequipped = equip_result.get('dequipped')

                    if equipped:
                        message_log.add_message(Message('You equipped the {0}'.format(equipped.name)))

                    if dequipped:
                        message_log.add_message(Message('You dequipped the {0}'.format(dequipped.name)))

                game_state = GameStates.ENEMY_TURN

            if targeting:
                previous_game_state = GameStates.PLAYERS_TURN
                game_state = GameStates.TARGETING

                targeting_item = targeting

                message_log.add_message(targeting_item.item.targeting_message)

            if arrow_targeting:
                player.sound = 5
                previous_game_state = GameStates.PLAYERS_TURN
                game_state = GameStates.ARROW_TARGETING

                arrow_targeting_item = arrow_targeting

                message_log.add_message(arrow_targeting_item.item.targeting_message)

            if targeting_cancelled:
                game_state = previous_game_state

                message_log.add_message(Message('Targeting cancelled'))

        if game_state == GameStates.ENEMY_TURN:
            if turns % int((300 - (game_map.dungeon_level*2)) / 2) == 0 and turns != 0:
                game_map.add_entity(message_log, entities, fov_map)

            if burned_turns >= 0 and player.burned:
                dead_entity = False
                burned_results = player.fighter.take_damage(4)
                for burned_result in burned_results:
                    dead_entity = burned_result.get('dead')
                if dead_entity:
                    if dead_entity.name == 'Player':
                        message, game_state = kill_player(dead_entity)
                        message_log.add_message(message)
                burned_turns -= 1

            if poison_turns >= 0 and player.poisoned:
                dead_entity = False
                poison_results = player.fighter.take_damage(1)
                for poison_result in poison_results:
                    dead_entity = poison_result.get('dead')
                if dead_entity:
                    if dead_entity.name == 'Player':
                        message, game_state = kill_player(dead_entity)
                        message_log.add_message(message)
                poison_turns -= 1

            if frozen_turns >= 0 and player.frozen:
                frozen_turns -= 1
                if frozen_turns == 0:
                    player.frozen = False

            for entity in entities:
                if entity.ai:
                    pet_there = 0
                    if pet:
                        if entity.distance_to(player) >= entity.distance_to(pet) and entity.name != 'Pet':
                            pet_there = 1
                            enemy_turn_results = entity.ai.take_turn(pet, fov_map, game_map, entities, turns)
                        else:
                            enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities, turns)
                    else:
                        enemy_turn_results = entity.ai.take_turn(player, fov_map, game_map, entities, turns)

                    for enemy_turn_result in enemy_turn_results:
                        if burned_turns >= 0:
                            burned_results = entity.fighter.take_damage(4)
                            for burned_result in burned_results:
                                dead_entity = burned_result.get('dead')
                                if dead_entity.name == 'Player':
                                    message, game_state = kill_player(dead_entity)
                                    message_log.add_message(message)
                            burned_turns -= 1
                        poisoned, player_burned, frozen = False, False, False
                        if not player.fighter.poison_resistance and not pet_there:
                            poisoned = enemy_turn_result.get('poisoned')
                        if not player.fighter.fire_resistance and not pet_there:
                            player_burned =  enemy_turn_result.get('burned')
                        if not player.fighter.poison_resistance and not pet_there:
                            frozen = enemy_turn_result.get('frozen')

                        if player_burned:
                            enemy_turn_results.append({'message': Message('You get Burned', libtcod.flame)})
                            burned_turns = randint(5, 10)
                            player.burned = True
                        if poisoned:
                            enemy_turn_results.append({'message': Message('you start to feel ill', libtcod.green)})
                            poison_turns = randint(20, 50)
                            player.poisoned = True
                        if frozen:
                            enemy_turn_results.append({'message': Message('you stop being able to move!', libtcod.light_blue)})
                            frozen_turns = randint(2, 5)
                            player.frozen = True

                    for enemy_turn_result in enemy_turn_results:
                        message = enemy_turn_result.get('message')
                        dead_entity = enemy_turn_result.get('dead')

                        if message:
                            message_log.add_message(message)

                        if dead_entity:
                            if dead_entity == player:
                                message, game_state = kill_player(dead_entity)
                            elif dead_entity == pet:
                                pet = 0
                                message = kill_pet(dead_entity)
                            elif dead_entity == boss:
                                game_state = GameStates.WINNING
                                message = kill_boss(dead_entity)
                            else:
                                message = kill_monster(dead_entity, pet, game_map)

                            message_log.add_message(message)

                            if game_state == GameStates.PLAYER_DEAD:
                                break

                    if game_state == GameStates.PLAYER_DEAD:
                        break
            else:

                turns += 1

                game_state = GameStates.PLAYERS_TURN


if __name__ == '__main__':
    main()


'''What happened in each version?
V1:  Got a game.  Tutorial complete, with additions of turn counter, poison, burning and extra weapons, armour, scrolls and enemies

V2:  Added enemy movement outside FoV

V3:  Added ranged weaponry and inventory stacking, as well as losing arrows when shooting

V4:  Added Scent tracking and Arrow recovery, as well as a large bug fix to stabilise V3, and an extra ring slot

V5:  Added Dexterity and Intelligence as new stats, as well as implementing them for ranged weaponry and scrolls.
     Also added being able to upgrade stats at certain levels only (dex, con, int every level; str, def every 3)

V6:  Added half a million new items/equipment/enemies, and a few new ailments from enemy attacks

V7:  Added Hearing and a pet.  

V8:  Added item and enemy classes, and general debugging

V8.1: Converted everything to laptop world, and made it all work, new base of operations is laptop. fun!

V9:  Adding a new leveling up system, where using an item makes you better at it

'''