import tcod as libtcod


def menu(con, header, options, width, screen_width, screen_height):
    if len(options) > 26: raise ValueError('Cannot have a menu with more than 26 options')

    # Calculate total height for the header (after auto-wrap) ane one line per option
    header_height = libtcod.console_get_height_rect(con, 0, 0, width, screen_height, header)
    height = len(options) + header_height

    # Create an off-screen menu console
    window = libtcod.console_new(width, height)

    # Print the header, with auto-wrap
    libtcod.console_set_default_foreground(window, libtcod.white)
    libtcod.console_print_rect_ex(window, 0, 0, width, height, libtcod.BKGND_NONE, libtcod.LEFT, header)

    # Print all the options
    y = header_height
    letter_index = ord('a')
    for option_text in options:
        text = '(' + chr(letter_index) + ')' + option_text
        libtcod.console_print_ex(window, 0, y, libtcod.BKGND_NONE, libtcod.LEFT, text)
        y += 1
        letter_index += 1

    # Blit the comntents of 'window' to the root console
    x = int(screen_width / 2 - width / 2)
    y = int(screen_height / 2 - height / 2)
    libtcod.console_blit(window, 0, 0, width, height, 0, x, y, 1.0, 0.7)


def inventory_menu(con, header, player, inventory_width, screen_width, screen_height):
    if len(player.inventory.items) == 0:
        options = ['Inventory is empty.']
    else:
        player.scrolls = []
        player.potions = []
        player.rings = []
        player.items_equipment = []
        player.bows = []
        player.arrows = []
        player.corpses = []
        scrolls = []
        potions = []
        rings = []
        equipment = []
        bows = []
        arrows = []
        corpses = []

        options = []
        inv = player.inventory.items

        for items in player.items:
            if type(items) != str:
                this_item = items.name

                num = 0
                for item in inv:
                    if this_item == item.name:
                        num += 1
                if num == 1:

                    if player.equipment.main_hand == items:
                        item_disp = ' 1' + ' ' + this_item + ' (in main hand)'
                    elif player.equipment.off_hand == items:
                        item_disp = ' 1' + ' ' + this_item + ' (in off hand)'
                    elif player.equipment.head == items:
                        item_disp = ' 1' + ' ' + this_item + ' (on head)'
                    elif player.equipment.body == items:
                        item_disp = ' 1' + ' ' + this_item + ' (on torso)'
                    elif player.equipment.legs == items:
                        item_disp = ' 1' + ' ' + this_item + ' (on legs)'
                    elif player.equipment.feet == items:
                        item_disp = ' 1' + ' ' + this_item + ' (on feet)'
                    elif player.equipment.right_finger == items:
                        item_disp = ' 1' + ' ' + this_item + ' (on right finger)'
                    elif player.equipment.left_finger == items:
                        item_disp = ' 1' + ' ' + this_item + ' (on left finger)'
                    elif player.equipment.back == items:
                        item_disp = ' 1' + ' ' + this_item + ' (on back)'
                    else:
                        item_disp = ' 1' + ' ' + this_item
                else:

                    if player.equipment.main_hand == items:
                        item_disp = ' ' + str(num) + ' ' + this_item + 's (1 in main hand)'
                    elif player.equipment.off_hand == items:
                        item_disp = ' ' + str(num) + ' ' + this_item + 's (1 in off hand)'
                    elif player.equipment.head == items:
                        item_disp = ' ' + str(num) + ' ' + this_item + 's (1 on head)'
                    elif player.equipment.body == items:
                        item_disp = ' ' + str(num) + ' ' + this_item + 's (1 on torso)'
                    elif player.equipment.legs == items:
                        item_disp = ' ' + str(num) + ' ' + this_item + 's (1 on legs)'
                    elif player.equipment.feet == items:
                        item_disp = ' ' + str(num) + ' ' + this_item + 's (1 on feet)'
                    elif player.equipment.right_finger == items:
                        item_disp = ' ' + str(num) + ' ' + this_item + 's (1 on right finger)'
                    elif player.equipment.left_finger == items:
                        item_disp = ' ' + str(num) + ' ' + this_item + 's (1 on left finger)'
                    elif player.equipment.back == items:
                        item_disp = ' ' + str(num) + ' ' + this_item + 's (1 on back)'
                    else:
                        item_disp = ' ' + str(num) + ' ' + this_item + 's'

                if items.item_class == '(Scroll)':
                    scrolls.append(item_disp)
                    player.scrolls.append(items)
                elif items.item_class == '(Potion)':
                    potions.append(item_disp)
                    player.potions.append(items)
                elif items.item_class == '(Equipment)':
                    equipment.append(item_disp)
                    player.items_equipment.append(items)
                elif items.item_class == '(Ring)':
                    rings.append(item_disp)
                    player.rings.append(items)
                elif items.item_class == '(Bow)':
                    bows.append(item_disp)
                    player.bows.append(items)
                elif items.item_class == '(Arrow)':
                    arrows.append(item_disp)
                    player.arrows.append(items)
                elif items.item_class == '(Corpse)':
                    corpses.append(item_disp)
                    player.corpses.append(items)

        options.append('Equipment:')
        options.extend(equipment)
        options.append('Bows:')
        options.extend(bows)
        options.append('Arrows:')
        options.extend(arrows)
        options.append('Rings:')
        options.extend(rings)
        options.append('Potions:')
        options.extend(potions)
        options.append('Scrolls:')
        options.extend(scrolls)
        options.append('Corpses:')
        options.extend(corpses)

        player.items = []
        player.items.append('Equipment:')
        player.items.extend(player.items_equipment)
        player.items.append('Bows:')
        player.items.extend(player.bows)
        player.items.append('Arrows:')
        player.items.extend(player.arrows)
        player.items.append('Rings:')
        player.items.extend(player.rings)
        player.items.append('Potions:')
        player.items.extend(player.potions)
        player.items.append('Scrolls:')
        player.items.extend(player.scrolls)
        player.items.append('Corpses')
        player.items.extend(player.corpses)

    menu(con, header, options, inventory_width, screen_width, screen_height)


def main_menu(con, background_image, screen_width, screen_height):

    libtcod.image_blit_2x(background_image, 0, 0, 0)

    libtcod.console_set_default_foreground(0, libtcod.light_yellow)
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height / 2) - 4, libtcod.BKGND_NONE, libtcod.CENTER,
                             'THE DUNGEONS OF NOT REALLY VERY MUCH DOOM')
    libtcod.console_print_ex(0, int(screen_width / 2), int(screen_height - 2), libtcod.BKGND_NONE, libtcod.CENTER,
                             'By Andrew')

    menu(con, '', ['Play a new game', 'Continue last game', 'Quit'], 24, screen_width, screen_height)


def character_screen(player, character_screen_width, character_screen_height, screen_width, screen_height):
    window = libtcod.console_new(character_screen_width, character_screen_height)

    libtcod.console_set_default_foreground(window, libtcod.white)

    libtcod.console_print_rect_ex(window, 0, 1, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Character Information')
    libtcod.console_print_rect_ex(window, 0, 3, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Maximum HP: {0}'.format(player.fighter.max_hp))
    libtcod.console_print_rect_ex(window, 0, 4, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Attack: {0}'.format(player.fighter.power))
    libtcod.console_print_rect_ex(window, 0, 5, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Defence: {0}'.format(player.fighter.defence))
    libtcod.console_print_rect_ex(window, 0, 6, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Intelligence: {0}'.format(player.fighter.intelligence))
    libtcod.console_print_rect_ex(window, 0, 7, character_screen_width, character_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Dexterity: {0}'.format(player.fighter.dexterity))

    x = screen_width // 2 - character_screen_width // 2
    y = screen_height // 2 - character_screen_height // 2
    libtcod.console_blit(window, 0, 0, character_screen_width, character_screen_height, 0, x, y, 1.0, 0.7)


def help_screen(help_screen_width, help_screen_height, screen_width, screen_height):
    window = libtcod.console_new(help_screen_width, help_screen_height)

    libtcod.console_set_default_foreground(window, libtcod.white)

    libtcod.console_print_rect_ex(window, 0, 1, help_screen_width, help_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'List of Game Commands')
    libtcod.console_print_rect_ex(window, 0, 3, help_screen_width, help_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Pick up: comma')
    libtcod.console_print_rect_ex(window, 0, 5, help_screen_width, help_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Move: arrow keys, num pad')
    libtcod.console_print_rect_ex(window, 0, 7, help_screen_width, help_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Wait: full stop / 5 on num pad')
    libtcod.console_print_rect_ex(window, 0, 9, help_screen_width, help_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Down stairs: space')
    libtcod.console_print_rect_ex(window, 0, 11, help_screen_width, help_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Help menu: \'h\'')
    libtcod.console_print_rect_ex(window, 0, 13, help_screen_width, help_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Inventory menu: \'i\'')
    libtcod.console_print_rect_ex(window, 0, 15, help_screen_width, help_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Drop menu: \'d\'')
    libtcod.console_print_rect_ex(window, 0, 17, help_screen_width, help_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Character screen: \'c\'')
    libtcod.console_print_rect_ex(window, 0, 19, help_screen_width, help_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Cancel/exit anything: esc')
    libtcod.console_print_rect_ex(window, 0, 21, help_screen_width, help_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Full screen: Alt-Enter')
    libtcod.console_print_rect_ex(window, 0, 23, help_screen_width, help_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Using menus: a-z(signified beside the option)')
    libtcod.console_print_rect_ex(window, 0, 25, help_screen_width, help_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'What\'s that?: hover with mouse')
    libtcod.console_print_rect_ex(window, 0, 27, help_screen_width, help_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'If an item is a piece of armour or weapon(excluding bows): select it in inventory menu to (d)equip')
    libtcod.console_print_rect_ex(window, 0, 31, help_screen_width, help_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Any other item is instant use')
    libtcod.console_print_rect_ex(window, 0, 33, help_screen_width, help_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Most items are fairly self-explanatory(antidotes), but scrolls can make monsters move randomly(confusion), hit the nearest monster(lightning), deal AOE damage(fireball) or freeze a monster(freeze)')
    libtcod.console_print_rect_ex(window, 0, 40, help_screen_width, help_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'If in doubt: read the message bar/ask me!!')
    libtcod.console_print_rect_ex(window, 0, 42, help_screen_width, help_screen_height, libtcod.BKGND_NONE,
                                  libtcod.LEFT, 'Game automatically saves with esc')

    x = screen_width // 2 - help_screen_width // 2
    y = screen_height // 2 - help_screen_width // 2
    libtcod.console_blit(window, 0, 0, help_screen_width, help_screen_height, 0, x, y, 1.0, 0.7)


def message_box(con, header, width, screen_width, screen_height):

    menu(con, header, [], width, screen_width, screen_height)
