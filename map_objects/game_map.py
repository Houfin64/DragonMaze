import tcod as libtcod

from components.fighter import Fighter
from components.ai import BasicMonster, BasicPet
from components.stairs import Stairs
from game_messages import Message
from map_objects.place_entities import place_entities

from render_functions import RenderOrder
from map_objects.tile import Tile
from entity import Entity, get_blocking_entities_at_location
from map_objects.rectangle import Rect
from random import randint


class GameMap:
    def __init__(self, width, height, dungeon_level=1):
        self.width = width
        self.height = height
        self.tiles = self.initialize_tiles()

        self.dungeon_level = dungeon_level
        self.biome = 0

    def initialize_tiles(self):
        tiles = [[Tile(True) for y in range(self.height)] for x in range(self.width)]

        return tiles

    def make_map(self, max_rooms, room_min_size, room_max_size, map_width, map_height, player, entities, pet, direction):
        rooms = []
        num_rooms = 0

        if self.dungeon_level < 6:
            self.biome = 'The Dungeon'
        elif self.dungeon_level < 11:
            self.biome = 'The Icebleak Cavern'
        elif self.dungeon_level < 16:
            self.biome = 'The Underglade'
        elif self.dungeon_level < 21:
            self.biome = 'The Hadalrealm'
        elif self.dungeon_level < 24:
            self.biome = 'Dragonroost'
        elif self.dungeon_level == 24:
            self.biome = 'Oblivion\'s Gate'
        elif self.dungeon_level == 25:
            self.biome = 'The Vault'

        center_of_last_room_x = None
        center_of_last_room_y = None
        if self.dungeon_level < 24:
            for r in range(max_rooms):
                # random width and height
                w = libtcod.random_get_int(0, room_min_size, room_max_size)
                h = libtcod.random_get_int(0, room_min_size, room_max_size)
                # random position without going out of the boundaries of the map
                x = libtcod.random_get_int(0, 0, map_width - w - 1)
                y = libtcod.random_get_int(0, 0, map_height - h - 1)

                # "Rect" class makes rectangles easier to work with
                new_room = Rect(x, y, w, h)

                # run through the other rooms and see if they intersect with this one
                for other_room in rooms:
                    if new_room.intersect(other_room):
                        break
                else:
                    # this means there are no intersections, so this room is valid

                    # "paint" it to the map's tiles
                    self.create_room(new_room)

                    # center coordinates of new room, will be useful later
                    (new_x, new_y) = new_room.center()

                    center_of_last_room_x = new_x
                    center_of_last_room_y = new_y

                    if num_rooms == 0:
                        # this is the first room, where the player starts at
                        player.x = new_x
                        player.y = new_y
                        player_room = new_room
                    else:
                        # all rooms after the first:
                        # connect it to the previous room with a tunnel

                        # center coordinates of previous room
                        (prev_x, prev_y) = rooms[num_rooms - 1].center()

                        self.create_tunnel(prev_x, new_x, prev_y, new_y)

                    if new_room != player_room:
                        place_entities(self, new_room, entities)

                    # finally, append the new room to the list
                    rooms.append(new_room)
                    num_rooms += 1
        else:
            for i in range(0, 3):
                room = Rect(int(i*(map_width/4)), 0, int(map_width/4), map_height - 1)
                room2 = Rect(0, int(i*(map_height/3)), map_width - 1, int(map_height/3))
                self.create_room(room)
                self.create_room(room2)
                player.x, player.y = 10, 10
                num_rooms += 2
                rooms.append(room)
                rooms.append(room2)
            room = Rect(int(3 * (map_width / 4)), 0, int(map_width / 4) - 1, map_height - 1)
            self.create_room(room)
            num_rooms += 1
            rooms.append(room)
            center_of_last_room_x, center_of_last_room_y = 40, 21
        if direction == 'down':
            stairs_component = Stairs(self.dungeon_level + 1)
            down_stairs = Entity(center_of_last_room_x, center_of_last_room_y, '>', libtcod.white, 'Down Stairs',
                                 render_order=RenderOrder.STAIRS, stairs=stairs_component)
            stairs_component = Stairs(self.dungeon_level - 1)
            up_stairs = Entity(player.x, player.y, '<', libtcod.white, 'Up Stairs',
                                 render_order=RenderOrder.STAIRS, stairs=stairs_component)
        if direction == 'up':
            stairs_component = Stairs(self.dungeon_level + 1)
            down_stairs = Entity(player.x, player.y, '>', libtcod.white, 'Down Stairs',
                                 render_order=RenderOrder.STAIRS, stairs=stairs_component)
            stairs_component = Stairs(self.dungeon_level - 1)
            up_stairs = Entity(center_of_last_room_x, center_of_last_room_y, '<', libtcod.white, 'Up Stairs',
                               render_order=RenderOrder.STAIRS, stairs=stairs_component)
        if self.dungeon_level != 25:
            entities.append(down_stairs)
        if self.dungeon_level != 1:
            entities.append(up_stairs)
        if self.dungeon_level == 24:
            fighter_component = Fighter(hp=300, defence=50, power=30)
            ai_component = BasicMonster()
            monster = Entity(40, 21, 'W', libtcod.white, 'DragonLord', blocks=True,
                             render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                             poisons_chance=100, burns_chance=100, freezes_chance=25, monster_class='(Dragon)')
            entities.append(monster)

        if pet:

            ai_component = BasicPet()
            fighter_component = Fighter(hp=pet.fighter.hp + 50, power=self.dungeon_level, defence=int(self.dungeon_level/2))
            pet = Entity(player.x - 1, player.y, 'P', libtcod.blue, 'Pet', render_order=RenderOrder.ACTOR, fighter=fighter_component,
                         ai=ai_component, blocks=True, monster_class='(Pet)')
            entities.append(pet)
            return pet

    def create_room(self, room):
        # go through the tiles in the rectangle and make them passable
        for x in range(room.x1 + 1, room.x2):
            for y in range(room.y1 + 1, room.y2):
                self.tiles[x][y].blocked = False
                self.tiles[x][y].block_sight = False

    def create_tunnel(self, x1, x2, y1, y2):
        x_left = abs(x1 - x2)
        y_left = abs(y1 - y2)
        x = min(x1, x2)
        if x == x1:
            y, true_y = y1, y2
        else:
            y, true_y = y2, y1

        while x_left != 0 or y_left != 0:
            x_distance = randint(0, x_left)
            self.create_h_tunnel(x, x + x_distance, y)
            x_left -= x_distance
            x += x_distance
            if true_y - y < 0:
                y_distance = randint(0, y_left)
                y_distance *= -1
            else:
                y_distance = randint(0, y_left)
            self.create_v_tunnel(y, y + y_distance, x)
            y_left -= abs(y_distance)
            y += y_distance

    def create_h_tunnel(self, x1, x2, y):
        for x in range(min(x1, x2), max(x1, x2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False

    def create_v_tunnel(self, y1, y2, x):
        for y in range(min(y1, y2), max(y1, y2) + 1):
            self.tiles[x][y].blocked = False
            self.tiles[x][y].block_sight = False
            if randint(0, 20) == 1:
                self.tiles[x][y].water = True

    def is_blocked(self, x, y):
        if self.tiles[x][y].blocked:
            return True

        return False

    def next_floor(self, player, message_log, constants, entities, direction):
        if direction == 'down':
            self.dungeon_level += 1
            message_log.add_message(
                Message('You take a nap on the bottom step, this seems more comfortable than your bed at home!',
                        libtcod.light_violet))
        else:
            self.dungeon_level -= 1
            message_log.add_message(
                Message('You take a nap on the top step, this seems more comfortable than your bed at home!',
                        libtcod.light_violet))
        pet = 0
        for entity in entities:
            if entity.name == 'Pet':
                pet = entity
        entities = [player]

        self.tiles = self.initialize_tiles()
        pet = self.make_map(constants['max_rooms'], constants['room_min_size'], constants['room_max_size'],
                      constants['map_width'], constants['map_height'], player, entities, pet, direction)

        return pet, entities

    def add_entity(self, message_log, entities, fov_map):
        space = False
        x, y = 0, 0
        name = ''
        colour = libtcod.black
        while not space:
            x = randint(10, self.width - 10)
            y = randint(10, self.height - 10)
            if not self.is_blocked(x, y) and not get_blocking_entities_at_location(entities, x, y) and not libtcod.map_is_in_fov(fov_map, x, y):
                space = True
        ailment = randint(1, 3)
        poison_chance, burn_chance, cold_chance = 0, 0, 0
        if ailment == 1:
            poison_chance, name, colour = 50, 'poisonous', libtcod.green
        if ailment == 2:
            burn_chance, name, colour = 50, 'fiery', libtcod.flame
        if ailment == 3:
            cold_chance, name, colour = 10, 'icy', libtcod.lighter_blue
        ai_component = BasicMonster()
        fighter_component = Fighter(hp=(self.dungeon_level * 8), defence=int(self.dungeon_level * 0.5), power=int(self.dungeon_level * 1.5), xp = self.dungeon_level * 30)
        monster = Entity(x, y, 'G', colour, (name + ' Gelatinous Blob'), blocks=True, render_order=RenderOrder.ACTOR,
                         ai=ai_component, fighter=fighter_component, poisons_chance=poison_chance,
                         burns_chance=burn_chance, freezes_chance=cold_chance, monster_class='(GOO)')
        entities.append(monster)
