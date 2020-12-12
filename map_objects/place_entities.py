import tcod as libtcod
from random import randint

from random_utils import from_dungeon_level, random_choice_from_dict, tail_off_probability
from components.ai import BasicMonster
from entity import Entity
from components.fighter import Fighter
from render_functions import RenderOrder
from equipment_slots import EquipmentSlots
from components.item import Item
from components.equippable import Equippable
from item_functions import heal, burn_salve, antidote, cast_lightning, cast_fireball, cast_freeze, cast_confuse, big_shoot
from game_messages import Message


def place_entities(self, room, entities):
    """get a random number of monsters"""
    max_monsters_per_room = from_dungeon_level([[2, 1], [3, 4], [4, 7], [1, 10]], self.dungeon_level)
    max_items_per_room = from_dungeon_level([[1, 1], [2, 4], [4, 6]], self.dungeon_level)

    number_of_monsters = randint(0, max_monsters_per_room)
    number_of_items = randint(0, max_items_per_room)

    monster_chances = {
        # Dungeon Biome
        'Fire Newt': tail_off_probability(self.dungeon_level, 50, 1, 0, 6),
        'Frost Newt': tail_off_probability(self.dungeon_level, 50, 1, 0, 6),
        'Newt': tail_off_probability(self.dungeon_level, 50, 1, 0, 6),
        'Troll': tail_off_probability(self.dungeon_level, 50, 4, 0, 6),
        'Orc': tail_off_probability(self.dungeon_level, 50, 2, 0, 6),
        'Wild Dog': tail_off_probability(self.dungeon_level, 50, 2, 0, 6),
        'Rock Golem': tail_off_probability(self.dungeon_level, 50, 5, 0, 6),
        'Eagle': tail_off_probability(self.dungeon_level, 50, 2, 0, 6),
        'Rat': tail_off_probability(self.dungeon_level, 50, 1, 0, 6),
        'Gargoyle': tail_off_probability(self.dungeon_level, 50, 3, 0, 6),
        # Ice Biome
        'Ice Golem': tail_off_probability(self.dungeon_level, 50, 7, 5, 11),
        'Ice Crab': tail_off_probability(self.dungeon_level, 50, 10, 5, 11),
        'Snow Owl': tail_off_probability(self.dungeon_level, 50, 8, 5, 11),
        'Frost Bear': tail_off_probability(self.dungeon_level, 50, 6, 5, 11),
        'Frost Serpent': tail_off_probability(self.dungeon_level, 50, 6, 5, 11),
        'Amarok': tail_off_probability(self.dungeon_level, 50, 9, 5, 11),
        # Poison Biome
        'Toxic Arachnid': tail_off_probability(self.dungeon_level, 50, 12, 10, 16),
        'Lavellan': tail_off_probability(self.dungeon_level, 50, 11, 10, 16),
        'Snake': tail_off_probability(self.dungeon_level, 50, 11, 10, 16),
        'Basilisk': tail_off_probability(self.dungeon_level, 50, 14, 10, 16),
        'Komodo': tail_off_probability(self.dungeon_level, 50, 13, 10, 16),
        'Dryad': tail_off_probability(self.dungeon_level, 50, 15, 10, 16),
        'OwlBear': tail_off_probability(self.dungeon_level, 50, 12, 10, 16),
        # Hell
        'Imp': tail_off_probability(self.dungeon_level, 50, 16, 15, 21),
        'Daemon': tail_off_probability(self.dungeon_level, 50, 17, 15, 21),
        'Devil': tail_off_probability(self.dungeon_level, 50, 4, 19, 21),
        'Flamebearer': tail_off_probability(self.dungeon_level, 50, 20, 15, 21),
        'HellHound': tail_off_probability(self.dungeon_level, 50, 16, 15, 21),
        'Chupacabra': tail_off_probability(self.dungeon_level, 50, 18, 15, 21),
        'Adarna': tail_off_probability(self.dungeon_level, 50, 3, 18, 21),
        # Dragons
        'Dragon': tail_off_probability(self.dungeon_level, 50, 22, 20, 24),
        'Black Dragon': tail_off_probability(self.dungeon_level, 50, 23, 20, 24),
        'Blue Dragon': tail_off_probability(self.dungeon_level, 50, 23, 20, 24),
        'Green Dragon': tail_off_probability(self.dungeon_level, 50, 23, 20, 24),
        'Roc': tail_off_probability(self.dungeon_level, 50, 21, 20, 24),
        'Air elemental': tail_off_probability(self.dungeon_level, 50, 23, 20, 24),
        'Amphiptere': tail_off_probability(self.dungeon_level, 50, 21, 20, 24)
        # Bosses ??
        #'Wo/u/yrm Trilogy'
        #'Orochi'
        #'Yalgoroth, Abyssal Fiend'
        #'Werdna, Lord of the Abyss'
        #'DragonLord'
    }
    item_chances = {
        'Max Potion': from_dungeon_level([[2, 4], [10, 8], [20, 10], [50, 15]], self.dungeon_level),
        'Super Potion': from_dungeon_level([[10, 4], [20, 8], [50, 10], [1, 15]], self.dungeon_level),
        'Healing Potion': from_dungeon_level([[60, 1], [50, 4], [30, 8], [10, 10], [1, 15]], self.dungeon_level),
        'Burn Salve': 30,
        'Antidote': 30,
        'Sword': from_dungeon_level([[15, 4], [20, 5], [1, 6]], self.dungeon_level),
        'Arrow': 50,
        'War Hammer': from_dungeon_level([[15, 10], [1, 12]], self.dungeon_level),
        'Quarterstaff': from_dungeon_level([[15, 8], [1, 10]], self.dungeon_level),
        'Mace': from_dungeon_level([[15, 7], [1, 9]], self.dungeon_level),
        'Flail': from_dungeon_level([[15, 6], [1, 8]], self.dungeon_level),
        'Polearm': from_dungeon_level([[15, 12]], self.dungeon_level),
        'Katana': from_dungeon_level([[15, 9], [1, 11]], self.dungeon_level),
        'Khopesh': from_dungeon_level([[15, 6], [1, 8]], self.dungeon_level),
        'Mambele': from_dungeon_level([[15, 5], [1, 7]], self.dungeon_level),
        'Greatbow': from_dungeon_level([[15, 8]], self.dungeon_level),
        'Shield': from_dungeon_level([[15, 4], [1, 6]], self.dungeon_level),
        'Sharpshield': from_dungeon_level([[15, 6], [1, 8]], self.dungeon_level),
        'Buckler': from_dungeon_level([[15, 6], [1, 8]], self.dungeon_level),
        'Heater Shield': from_dungeon_level([[15, 8], [1, 10]], self.dungeon_level),
        'Targe': from_dungeon_level([[15, 10], [1, 12]], self.dungeon_level),
        'Pelatrion': from_dungeon_level([[15, 12], [1, 15]], self.dungeon_level),
        'Aspis': from_dungeon_level([[15, 15]], self.dungeon_level),
        'Leather Helmet': from_dungeon_level([[15, 4], [1, 6]], self.dungeon_level),
        'Leather Chestplate': from_dungeon_level([[15, 4], [1, 6]], self.dungeon_level),
        'Leather Leggings': from_dungeon_level([[15, 4], [1, 6]], self.dungeon_level),
        'Leather Boots': from_dungeon_level([[15, 4], [1, 6]], self.dungeon_level),
        'Scale Helmet': from_dungeon_level([[15, 6], [1, 8]], self.dungeon_level),
        'Scale Mail': from_dungeon_level([[15, 6], [1, 8]], self.dungeon_level),
        'Scale Leggings': from_dungeon_level([[15, 6], [1, 8]], self.dungeon_level),
        'Scale Boots': from_dungeon_level([[15, 6], [1, 8]], self.dungeon_level),
        'Iron Helmet': from_dungeon_level([[15, 8], [1, 10]], self.dungeon_level),
        'Iron Chestplate': from_dungeon_level([[15, 8], [1, 10]], self.dungeon_level),
        'Iron Leggings': from_dungeon_level([[15, 8], [1, 10]], self.dungeon_level),
        'Iron Boots': from_dungeon_level([[15, 8], [1, 10]], self.dungeon_level),
        'Stone Helmet': from_dungeon_level([[15, 10], [1, 12]], self.dungeon_level),
        'Stone Chestplate': from_dungeon_level([[15, 10], [1, 12]], self.dungeon_level),
        'Stone Leggings': from_dungeon_level([[15, 10], [1, 12]], self.dungeon_level),
        'Stone Boots': from_dungeon_level([[15, 10], [1, 12]], self.dungeon_level),
        'Plate Helmet': from_dungeon_level([[15, 12]], self.dungeon_level),
        'Plate Mail': from_dungeon_level([[15, 12]], self.dungeon_level),
        'Plate Leggings': from_dungeon_level([[15, 12]], self.dungeon_level),
        'Plate Boots': from_dungeon_level([[15, 12]], self.dungeon_level),
        'Dragon Ring': from_dungeon_level([[10, 12]], self.dungeon_level),
        'Lion Ring': from_dungeon_level([[10, 12]], self.dungeon_level),
        'Wolf Ring': from_dungeon_level([[10, 12]], self.dungeon_level),
        'Eagle Ring': from_dungeon_level([[10, 12]], self.dungeon_level),
        'Badger Ring': from_dungeon_level([[10, 12]], self.dungeon_level),
        'Squirrel Ring': from_dungeon_level([[10, 12]], self.dungeon_level),
        'Bull Ring': from_dungeon_level([[10, 12]], self.dungeon_level),
        'Elephant Ring': from_dungeon_level([[10, 12]], self.dungeon_level),
        'Raven Ring': from_dungeon_level([[10, 12]], self.dungeon_level),
        'Turtle Ring': from_dungeon_level([[10, 12]], self.dungeon_level),
        'Hero Ring': from_dungeon_level([[10, 8], [1, 12]], self.dungeon_level),
        'Blocker Ring': from_dungeon_level([[10, 8], [1, 12]], self.dungeon_level),
        'Weaver Ring': from_dungeon_level([[10, 8], [1, 12]], self.dungeon_level),
        'Sage Ring': from_dungeon_level([[10, 8], [1, 12]], self.dungeon_level),
        'Brute Ring': from_dungeon_level([[10, 8], [1, 12]], self.dungeon_level),
        'Warrior Ring': from_dungeon_level([[10, 8], [1, 12]], self.dungeon_level),
        'Battlemage Ring': from_dungeon_level([[10, 8], [1, 12]], self.dungeon_level),
        'Thief Ring': from_dungeon_level([[10, 8], [1, 12]], self.dungeon_level),
        'Shieldmage Ring': from_dungeon_level([[10, 8], [1, 12]], self.dungeon_level),
        'Ranger Ring': from_dungeon_level([[10, 8], [1, 12]], self.dungeon_level),
        'Ring of Power': from_dungeon_level([[10, 5], [1, 8]], self.dungeon_level),
        'Ring of Toughness': from_dungeon_level([[10, 5], [1, 8]], self.dungeon_level),
        'Ring of Constitution': from_dungeon_level([[10, 5], [1, 8]], self.dungeon_level),
        'Ring of Dexterity': from_dungeon_level([[10, 5], [1, 8]], self.dungeon_level),
        'Ring of Intelligence': from_dungeon_level([[10, 5], [1, 8]], self.dungeon_level),
        'Sealskin Cloak': from_dungeon_level([[5, 5], [10, 7], [30, 9]], self.dungeon_level),
        'Lizardskin Cloak': from_dungeon_level([[5, 5], [10, 7], [30, 9]], self.dungeon_level),
        'Venombane Cloak': from_dungeon_level([[5, 5], [10, 7], [30, 9]], self.dungeon_level),
        'Scroll of Lightning Bolt': from_dungeon_level([[15, 4], [20, 5], [30, 8]], self.dungeon_level),
        'Scroll of Summon Fireball': from_dungeon_level([[10, 3], [20, 5], [20, 8]], self.dungeon_level),
        'Scroll of Confusion Ray': from_dungeon_level([[10, 3], [20, 5], [20, 8]], self.dungeon_level),
        'Scroll of Frost Blast': from_dungeon_level([[15, 4], [20, 5], [30, 8]], self.dungeon_level)

    }

    for i in range(number_of_monsters):
        'pick a random location in the room'
        x = randint(room.x1 + 1, room.x2 - 1)
        y = randint(room.y1 + 1, room.y2 - 1)

        if not any([entity for entity in entities if entity.x == x and entity.y == y]):

            monster_choice = random_choice_from_dict(monster_chances)

            # Dungeon Biome

            if monster_choice == 'Orc':
                fighter_component = Fighter(hp=20, defence=0, power=4, xp=35)
                ai_component = BasicMonster()
                monster = Entity(x, y, 'o', libtcod.desaturated_green, 'Orc', blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                                 monster_class='(Greenskin)')

            elif monster_choice == 'Troll':
                fighter_component = Fighter(hp=28, defence=2, power=7)
                ai_component = BasicMonster()
                monster = Entity(x, y, 'T', libtcod.darker_green, 'Troll', blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                                 monster_class='(Greenskin)')

            elif monster_choice == 'Eagle':
                fighter_component = Fighter(hp=10, defence=0, power=4, xp=20)
                ai_component = BasicMonster()
                monster = Entity(x, y, 'b', libtcod.brass, 'Roc', blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                                 monster_class='(Bird)')

            elif monster_choice == 'Wild Dog':
                fighter_component = Fighter(hp=10, defence=2, power=5, xp=20)
                ai_component = BasicMonster()
                monster = Entity(x, y, 'd', libtcod.brass, 'Wild Dog', blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                                 monster_class='(Canine)')

            elif monster_choice == 'Rat':
                fighter_component = Fighter(hp=5, defence=0, power=4, xp=50)
                ai_component = BasicMonster()
                monster = Entity(x, y, 'r', libtcod.brass, 'Rat', blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                                 poisons_chance=10, monster_class='(Rat)')

            elif monster_choice == 'Fire Newt':
                fighter_component = Fighter(hp=1, defence=0, power=4, xp=20)
                ai_component = BasicMonster()
                monster = Entity(x, y, 'N', libtcod.darker_flame, 'Fire Newt', blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                                 burns_chance=50, monster_class='(Newt)')

            elif monster_choice == 'Newt':
                fighter_component = Fighter(hp=1, defence=0, power=4, xp=20)
                ai_component = BasicMonster()
                monster = Entity(x, y, 'N', libtcod.light_green, 'Toxic Newt', blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                                 poisons_chance=50, monster_class='(Newt)')

            elif monster_choice == 'Frost Newt':  # 25% chance Freezes
                fighter_component = Fighter(hp=1, defence=0, power=4, xp=20)
                ai_component = BasicMonster()
                monster = Entity(x, y, 'N', libtcod.lighter_blue, 'Frost Newt', blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                                 freezes_chance=2, monster_class='(Newt)')

            elif monster_choice == 'Gargoyle':
                fighter_component = Fighter(hp=15, defence=3, power=5)
                ai_component = BasicMonster()
                monster = Entity(x, y, '@', libtcod.darker_grey, 'Gargoyle', blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                                 monster_class='(Statue)')

            elif monster_choice == 'Rock Golem':
                fighter_component = Fighter(hp=30, defence=3, power=6)
                ai_component = BasicMonster()
                monster = Entity(x, y, '@', libtcod.dark_grey, 'Rock Golem', blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                                 monster_class='(Elemental)')

            # Ice Biome

            elif monster_choice == 'Amarok':  # big wolfy
                fighter_component = Fighter(hp=32, defence=2, power=7)
                ai_component = BasicMonster()
                monster = Entity(x, y, 'd', libtcod.light_grey, 'Wolf', blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                                 freezes_chance=10, monster_class='(Canine)')

            elif monster_choice == 'Ice Golem':
                fighter_component = Fighter(hp=40, defence=4, power=7)
                ai_component = BasicMonster()
                monster = Entity(x, y, '@', libtcod.lighter_blue, 'Ice Golem', blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                                 freezes_chance=20, monster_class='(Elemental)')

            elif monster_choice == 'Ice Crab':
                fighter_component = Fighter(hp=25, defence=2, power=8)
                ai_component = BasicMonster()
                monster = Entity(x, y, 'c', libtcod.dark_blue, 'Ice Crab', blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                                 freezes_chance=12, monster_class='(Crustacean)')

            elif monster_choice == 'Snow Owl':
                fighter_component = Fighter(hp=28, defence=2, power=7)
                ai_component = BasicMonster()
                monster = Entity(x, y, 'b', libtcod.dark_blue, 'Snow Owl', blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                                 freezes_chance=5, monster_class='(Bird)')

            elif monster_choice == 'Frost Bear':
                fighter_component = Fighter(hp=26, defence=1, power=9)
                ai_component = BasicMonster()
                monster = Entity(x, y, 'B', libtcod.blue, 'Frost Bear', blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                                 freezes_chance=17, monster_class='(Ursus)')

            elif monster_choice == 'Frost Serpent':
                fighter_component = Fighter(hp=29, defence=2, power=8)
                ai_component = BasicMonster()
                monster = Entity(x, y, 'S', libtcod.blue, 'Frost Serpent', blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                                 freezes_chance=30, monster_class='(Snake)')

            # Poison Biome

            elif monster_choice == 'Toxic Arachnid':
                fighter_component = Fighter(hp=35, defence=1, power=0)
                ai_component = BasicMonster()
                monster = Entity(x, y, 'x', libtcod.crimson, 'Toxic Arachnid', blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                                 poisons_chance=50, monster_class='(Spider)')

            elif monster_choice == 'Lavellan':
                fighter_component = Fighter(hp=34, defence=2, power=6)
                ai_component = BasicMonster()
                monster = Entity(x, y, 'r', libtcod.white, 'Lavellan', blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                                 poisons_chance=90, monster_class='(Rat)')

            elif monster_choice == 'Snake':  # 10% chance of poisoning
                fighter_component = Fighter(hp=35, defence=3, power=5)
                ai_component = BasicMonster()
                monster = Entity(x, y, 's', libtcod.dark_green, 'Snake', blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                                 poisons_chance=20, monster_class='(Reptile)')

            elif monster_choice == 'Basilisk':  # 10% freezes you, 25% chance of poisoning
                fighter_component = Fighter(hp=45, defence=3, power=4)
                ai_component = BasicMonster()
                monster = Entity(x, y, 'S', libtcod.dark_green, 'Basilisk', blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                                 freezes_chance=10, poisons_chance=30, monster_class='(Reptile)')

            elif monster_choice == 'Komodo':  # 50% chance of poisoning
                fighter_component = Fighter(hp=40, defence=2, power=8)
                ai_component = BasicMonster()
                monster = Entity(x, y, 'S', libtcod.dark_red, 'Komodo', blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                                 poisons_chance=50, monster_class='(Reptile)')

            elif monster_choice == 'Dryad':
                fighter_component = Fighter(hp=50, defence=4, power=9)
                ai_component = BasicMonster()
                monster = Entity(x, y, '@', libtcod.brass, 'Dryad', blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                                 poisons_chance=98, monster_class='(Elemental)')

            elif monster_choice == 'Owlbear':
                fighter_component = Fighter(hp=36, defence=3, power=12)
                ai_component = BasicMonster()
                monster = Entity(x, y, 'B', libtcod.white, 'Owlbear', blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                                 poisons_chance=17, monster_class='(Ursus)')
            #Fire Biome

            elif monster_choice == 'Imp':  # 50% chance to burn
                fighter_component = Fighter(hp=50, defence=2, power=10)
                ai_component = BasicMonster()
                monster = Entity(x, y, 'z', libtcod.red, 'Imp', blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                                 burns_chance=10, monster_class='(Demon)')

            elif monster_choice == 'Daemon':  # 75% chance to burn
                fighter_component = Fighter(hp=55, defence=3, power=13)
                ai_component = BasicMonster()
                monster = Entity(x, y, 'Z', libtcod.red, 'Daemon', blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                                 burns_chance=50, monster_class='(Demon)')

            elif monster_choice == 'Devil':  # burns
                fighter_component = Fighter(hp=60, defence=4, power=15)
                ai_component = BasicMonster()
                monster = Entity(x, y, 'Z', libtcod.dark_flame, 'Devil', blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                                 burns_chance=75, monster_class='(Demon)')

            elif monster_choice == 'Flamebearer':
                fighter_component = Fighter(hp=70, defence=6, power=20)
                ai_component = BasicMonster()
                monster = Entity(x, y, '@', libtcod.darkest_red, 'Flamebearer', blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                                 burns_chance=98, monster_class='(Elemental)')

            elif monster_choice == 'HellHound':  # dog that burns you
                fighter_component = Fighter(hp=48, defence=3, power=10)
                ai_component = BasicMonster()
                monster = Entity(x, y, 'd', libtcod.darker_red, 'Hellhound', blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                                 burns_chance=75, monster_class='(Canine)')

            elif monster_choice == 'Chupacabra':  # vampiric dog
                fighter_component = Fighter(hp=53, defence=4, power=11)
                ai_component = BasicMonster()
                monster = Entity(x, y, 'd', libtcod.white, 'Chupacabra', blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                                 monster_class='(Canine)')

            elif monster_choice == 'Adarna':  # 5% chance Puts you to sleep (use freezing, but different text)
                fighter_component = Fighter(hp=56, defence=4, power=12)
                ai_component = BasicMonster()
                monster = Entity(x, y, 'b', libtcod.darkest_grey, 'Harpy', blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                                 freezes_chance=5, monster_class='(Bird)')

            # Dragon Biome

            elif monster_choice == 'Dragon':
                fighter_component = Fighter(hp=80, defence=4, power=18)
                ai_component = BasicMonster()
                monster = Entity(x, y, 'W', libtcod.light_red, 'Dragon', blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                                 burns_chance=50, monster_class='(Dragon)')

            elif monster_choice == 'Black Dragon':
                fighter_component = Fighter(hp=100, defence=8, power=25)
                ai_component = BasicMonster()
                monster = Entity(x, y, 'W', libtcod.flame, 'Ancient Red Dragon', blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                                 burns_chance=100, monster_class='(Dragon)')

            elif monster_choice == 'Blue Dragon':
                fighter_component = Fighter(hp=100, defence=8, power=25)
                ai_component = BasicMonster()
                monster = Entity(x, y, 'W', libtcod.blue, 'Ancient Blue Dragon', blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                                 freezes_chance=100, monster_class='(Dragon)')

            elif monster_choice == 'Green Dragon':
                fighter_component = Fighter(hp=100, defence=8, power=25)
                ai_component = BasicMonster()
                monster = Entity(x, y, 'W', libtcod.green, 'Ancient Green Dragon', blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                                 poisons_chance=100, monster_class='(Dragon)')

            elif monster_choice == 'Roc':
                fighter_component = Fighter(hp=70, defence=4, power=15)
                ai_component = BasicMonster()
                monster = Entity(x, y, 'b', libtcod.gold, 'Raptor', blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                                 monster_class='(Bird)')

            elif monster_choice == 'Air Sprite':
                fighter_component = Fighter(hp=110, defence=10, power=30)
                ai_component = BasicMonster()
                monster = Entity(x, y, '@', libtcod.light_sky, 'Air Sprite', blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                                 monster_class='(Elemental)')

            elif monster_choice == 'Amphiptere':  # 30% chance of burning, small winged legless dragon used in heraldry
                fighter_component = Fighter(hp=73, defence=1, power=19)
                ai_component = BasicMonster()
                monster = Entity(x, y, 'w', libtcod.light_red, 'Dragonling', blocks=True,
                                 render_order=RenderOrder.ACTOR, fighter=fighter_component, ai=ai_component,
                                 burns_chance=30, monster_class='(Dragon)')

            entities.append(monster)
    for i in range(number_of_items):
        x = randint(room.x1 + 1, room.x2 - 1)
        y = randint(room.y1 + 1, room.y2 - 1)

        if not any([entity for entity in entities if entity.x == x and entity.y == y]):
            item_choice = random_choice_from_dict(item_chances)

            if item_choice == 'Max Potion':
                item_component = Item(use_function=heal, amount=500)
                item = Entity(x, y, '!', libtcod.orange, 'Max Potion',
                              render_order=RenderOrder.ITEM, item=item_component, item_class='(Potion)')

            if item_choice == 'Super Potion':
                item_component = Item(use_function=heal, amount=100)
                item = Entity(x, y, '!', libtcod.fuchsia, 'Super Potion',
                              render_order=RenderOrder.ITEM, item=item_component, item_class='(Potion)')

            elif item_choice == 'Healing Potion':
                item_component = Item(use_function=heal, amount=40)
                item = Entity(x, y, '!', libtcod.violet, 'Healing Potion',
                              render_order=RenderOrder.ITEM, item=item_component, item_class='(Potion)')

            elif item_choice == 'Burn Salve':
                item_component = Item(use_function=burn_salve)
                item = Entity(x, y, '!', libtcod.red, 'Burn Salve',
                              render_order=RenderOrder.ITEM, item=item_component, item_class='(Potion)')

            elif item_choice == 'Antidote':
                item_component = Item(use_function=antidote)
                item = Entity(x, y, '!', libtcod.green, 'Antidote Potion',
                              render_order=RenderOrder.ITEM, item=item_component, item_class='(Potion)')

            elif item_choice == 'Sword':
                equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=3, dexterity_bonus=1)
                item = Entity(x, y, '/', libtcod.sky, 'Sword', equippable=equippable_component,
                              item_class='(Equipment)')

            elif item_choice == 'War Hammer':
                equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=6, dexterity_bonus=1)
                item = Entity(x, y, '/', libtcod.dark_sky, 'War Hammer', equippable=equippable_component,
                              item_class='(Equipment)')

            elif item_choice == 'Quarterstaff':
                equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=4, defence_bonus=2,
                                                  dexterity_bonus=3)
                item = Entity(x, y, '/', libtcod.brass, 'Quarterstaff', equippable=equippable_component,
                              item_class='(Equipment)')

            elif item_choice == 'Mace':
                equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=5, dexterity_bonus=1)
                item = Entity(x, y, '/', libtcod.sepia, 'Mace', equippable=equippable_component,
                              item_class='(Equipment)')

            elif item_choice == 'Flail':
                equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=4, dexterity_bonus=2)
                item = Entity(x, y, '/', libtcod.lighter_sky, 'Flail', equippable=equippable_component,
                              item_class='(Equipment)')

            elif item_choice == 'Polearm':  # freezes (smashed into ground, can't move)
                equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=8)
                item = Entity(x, y, '/', libtcod.light_sepia, 'Polearm', equippable=equippable_component,
                              item_class='(Equipment)')

            elif item_choice == 'Katana':
                equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=5, dexterity_bonus=2,
                                                  intelligence_bonus=2)
                item = Entity(x, y, '/', libtcod.darker_sepia, 'Katana', equippable=equippable_component,
                              item_class='(Equipment)')

            elif item_choice == 'Khopesh':  # poisons
                equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=3, defence_bonus=2,
                                                  dexterity_bonus=1)
                item = Entity(x, y, '/', libtcod.dark_grey, 'Khopesh', equippable=equippable_component,
                              item_class='(Equipment)')

            elif item_choice == 'Mambele':  # poisons
                equippable_component = Equippable(EquipmentSlots.MAIN_HAND, power_bonus=2, dexterity_bonus=2)
                item = Entity(x, y, '/', libtcod.green, 'Mambele', equippable=equippable_component,
                              item_class='(Equipment)')

            elif item_choice == 'Arrow':
                item_component = Item(use_function=None)
                item = Entity(x, y, '|', libtcod.sepia, 'Arrow', item=item_component, item_class='(Arrow)')

            elif item_choice == 'Greatbow':
                item_component = Item(use_function=big_shoot, arrow_targeting=True, targeting_message=Message(
                    'Use arrow keys or numpad to shoot in a direction.', libtcod.light_cyan))
                item = Entity(0, 0, '{', libtcod.dark_sepia, 'Greatbow', item=item_component, item_class='(Bow)')

            elif item_choice == 'Buckler':
                equippable_component = Equippable(EquipmentSlots.OFF_HAND, defence_bonus=1, dexterity_bonus=1)
                item = Entity(x, y, '(', libtcod.light_orange, 'Buckler', equippable=equippable_component,
                              item_class='(Equipment)')

            elif item_choice == 'Shield':
                equippable_component = Equippable(EquipmentSlots.OFF_HAND, defence_bonus=1)
                item = Entity(x, y, '(', libtcod.lighter_orange, 'Shield', equippable=equippable_component,
                              item_class='(Equipment)')

            elif item_choice == 'Sharpshield':
                equippable_component = Equippable(EquipmentSlots.OFF_HAND, defence_bonus=2, power_bonus=1)
                item = Entity(x, y, '(', libtcod.orange, 'Sharpshield', equippable=equippable_component,
                              item_class='(Equipment)')

            elif item_choice == 'Heater Shield':
                equippable_component = Equippable(EquipmentSlots.OFF_HAND, defence_bonus=3, dexterity_bonus=-1)
                item = Entity(x, y, '(', libtcod.orange, 'Heater Shield', equippable=equippable_component,
                              item_class='(Equipment)')

            elif item_choice == 'Pelatrion':
                equippable_component = Equippable(EquipmentSlots.OFF_HAND, defence_bonus=4, dexterity_bonus=-1)
                item = Entity(x, y, '(', libtcod.dark_orange, 'Pelatrion', equippable=equippable_component,
                              item_class='(Equipment)')

            elif item_choice == 'Targe':
                equippable_component = Equippable(EquipmentSlots.OFF_HAND, defence_bonus=4)
                item = Entity(x, y, '(', libtcod.darker_orange, 'Targe', equippable=equippable_component,
                              item_class='(Equipment)')

            elif item_choice == 'Aspis':
                equippable_component = Equippable(EquipmentSlots.OFF_HAND, defence_bonus=5)
                item = Entity(x, y, '(', libtcod.darkest_orange, 'Aspis', equippable=equippable_component,
                              item_class='(Equipment)')

            elif item_choice == 'Ring of Power':
                equippable_component = Equippable(EquipmentSlots.RIGHT_FINGER, power_bonus=3)
                item = Entity(x, y, '*', libtcod.brass, 'Power Ring', equippable=equippable_component,
                              item=Item(use_function=None), item_class='(Ring)')

            elif item_choice == 'Ring of Toughness':
                equippable_component = Equippable(EquipmentSlots.RIGHT_FINGER, defence_bonus=2)
                item = Entity(x, y, '*', libtcod.brass, 'Defence Ring', equippable=equippable_component,
                              item=Item(use_function=None), item_class='(Ring)')

            elif item_choice == 'Ring of Constitution':
                equippable_component = Equippable(EquipmentSlots.RIGHT_FINGER, max_hp_bonus=40)
                item = Entity(x, y, '*', libtcod.brass, 'Health Ring', equippable=equippable_component,
                              item=Item(use_function=None), item_class='(Ring)')

            elif item_choice == 'Ring of Dexterity':
                equippable_component = Equippable(EquipmentSlots.RIGHT_FINGER, dexterity_bonus=3)
                item = Entity(x, y, '*', libtcod.brass, 'Dexterity Ring', equippable=equippable_component,
                              item=Item(use_function=None), item_class='(Ring)')

            elif item_choice == 'Ring of Intelligence':
                equippable_component = Equippable(EquipmentSlots.RIGHT_FINGER, intelligence_bonus=3)
                item = Entity(x, y, '*', libtcod.brass, 'Intelligence Ring', equippable=equippable_component,
                              item=Item(use_function=None), item_class='(Ring)')

            elif item_choice == 'Hero Ring':
                equippable_component = Equippable(EquipmentSlots.RIGHT_FINGER, max_hp_bonus=40, power_bonus=3)
                item = Entity(x, y, '*', libtcod.brass, 'Hero Ring', equippable=equippable_component,
                              item_class='(Ring)')

            elif item_choice == 'Blocker Ring':
                equippable_component = Equippable(EquipmentSlots.RIGHT_FINGER, max_hp_bonus=40, defence_bonus=2)
                item = Entity(x, y, '*', libtcod.brass, 'Blocker Ring', equippable=equippable_component,
                              item_class='(Ring)')

            elif item_choice == 'Weaver Ring':
                equippable_component = Equippable(EquipmentSlots.RIGHT_FINGER, max_hp_bonus=40, dexterity_bonus=3)
                item = Entity(x, y, '*', libtcod.brass, 'Weaver Ring', equippable=equippable_component,
                              item_class='(Ring)')

            elif item_choice == 'Sage Ring':
                equippable_component = Equippable(EquipmentSlots.RIGHT_FINGER, max_hp_bonus=40,
                                                  intelligence_bonus=3)
                item = Entity(x, y, '*', libtcod.brass, 'Sage Ring', equippable=equippable_component,
                              item_class='(Ring)')

            elif item_choice == 'Brute Ring':
                equippable_component = Equippable(EquipmentSlots.RIGHT_FINGER, power_bonus=3, defence_bonus=2)
                item = Entity(x, y, '*', libtcod.brass, 'Brute Ring', equippable=equippable_component,
                              item_class='(Ring)')

            elif item_choice == 'Warrior Ring':
                equippable_component = Equippable(EquipmentSlots.RIGHT_FINGER, power_bonus=3, dexterity_bonus=3)
                item = Entity(x, y, '*', libtcod.brass, 'Warrior Ring', equippable=equippable_component,
                              item_class='(Ring)')

            elif item_choice == 'Battlemage Ring':
                equippable_component = Equippable(EquipmentSlots.RIGHT_FINGER, power_bonus=3, intelligence_bonus=3)
                item = Entity(x, y, '*', libtcod.brass, 'Battlemage Ring', equippable=equippable_component,
                              item_class='(Ring)')

            elif item_choice == 'Thief Ring':
                equippable_component = Equippable(EquipmentSlots.RIGHT_FINGER, defence_bonus=2, dexterity_bonus=3)
                item = Entity(x, y, '*', libtcod.brass, 'Thief Ring', equippable=equippable_component,
                              item_class='(Ring)')

            elif item_choice == 'Shieldmage Ring':
                equippable_component = Equippable(EquipmentSlots.RIGHT_FINGER, defence_bonus=2,
                                                  intelligence_bonus=3)
                item = Entity(x, y, '*', libtcod.brass, 'Shieldmage Ring', equippable=equippable_component,
                              item_class='(Ring)')

            elif item_choice == 'Ranger Ring':
                equippable_component = Equippable(EquipmentSlots.RIGHT_FINGER, dexterity_bonus=3,
                                                  intelligence_bonus=3)
                item = Entity(x, y, '*', libtcod.brass, 'Ranger Ring', equippable=equippable_component,
                              item_class='(Ring)')

            elif item_choice == 'Dragon Ring':
                equippable_component = Equippable(EquipmentSlots.RIGHT_FINGER, max_hp_bonus=40, power_bonus=3,
                                                  defence_bonus=2)
                item = Entity(x, y, '*', libtcod.brass, 'Dragon Ring', equippable=equippable_component,
                              item_class='(Ring)')

            elif item_choice == 'Lion Ring':
                equippable_component = Equippable(EquipmentSlots.RIGHT_FINGER, max_hp_bonus=40, power_bonus=3,
                                                  dexterity_bonus=3)
                item = Entity(x, y, '*', libtcod.brass, 'Lion Ring', equippable=equippable_component,
                              item_class='(Ring)')

            elif item_choice == 'Wolf Ring':
                equippable_component = Equippable(EquipmentSlots.RIGHT_FINGER, max_hp_bonus=40, power_bonus=3,
                                                  intelligence_bonus=3)
                item = Entity(x, y, '*', libtcod.brass, 'Wolf Ring', equippable=equippable_component,
                              item_class='(Ring)')

            elif item_choice == 'Eagle Ring':
                equippable_component = Equippable(EquipmentSlots.RIGHT_FINGER, max_hp_bonus=40, defence_bonus=2,
                                                  dexterity_bonus=3)
                item = Entity(x, y, '*', libtcod.brass, 'Eagle Ring', equippable=equippable_component,
                              item_class='(Ring)')

            elif item_choice == 'Badger Ring':
                equippable_component = Equippable(EquipmentSlots.RIGHT_FINGER, max_hp_bonus=40, defence_bonus=2,
                                                  intelligence_bonus=3)
                item = Entity(x, y, '*', libtcod.brass, 'Badger Ring', equippable=equippable_component,
                              item_class='(Ring)')

            elif item_choice == 'Squirrel Ring':
                equippable_component = Equippable(EquipmentSlots.RIGHT_FINGER, max_hp_bonus=40, dexterity_bonus=3,
                                                  intelligence_bonus=3)
                item = Entity(x, y, '*', libtcod.brass, 'Squirrel Ring', equippable=equippable_component,
                              item_class='(Ring)')

            elif item_choice == 'Bull Ring':
                equippable_component = Equippable(EquipmentSlots.RIGHT_FINGER, power_bonus=3, defence_bonus=2,
                                                  dexterity_bonus=3)
                item = Entity(x, y, '*', libtcod.brass, 'Bull Ring', equippable=equippable_component,
                              item_class='(Ring)')

            elif item_choice == 'Elephant Ring':
                equippable_component = Equippable(EquipmentSlots.RIGHT_FINGER, power_bonus=3, defence_bonus=2,
                                                  intelligence_bonus=3)
                item = Entity(x, y, '*', libtcod.brass, 'Elephant Ring', equippable=equippable_component,
                              item_class='(Ring)')

            elif item_choice == 'Raven Ring':
                equippable_component = Equippable(EquipmentSlots.RIGHT_FINGER, power_bonus=3, dexterity_bonus=3,
                                                  intelligence_bonus=3)
                item = Entity(x, y, '*', libtcod.brass, 'Raven Ring', equippable=equippable_component,
                              item_class='(Ring)')

            elif item_choice == 'Turtle Ring':
                equippable_component = Equippable(EquipmentSlots.RIGHT_FINGER, defence_bonus=2, dexterity_bonus=3,
                                                  intelligence_bonus=3)
                item = Entity(x, y, '*', libtcod.brass, 'Turtle Ring', equippable=equippable_component,
                              item_class='(Ring)')

            elif item_choice == 'Leather Helmet':
                equippable_component = Equippable(EquipmentSlots.HEAD, defence_bonus=1, dexterity_bonus=1)
                item = Entity(x, y, '[', libtcod.chartreuse, 'Leather Helmet', equippable=equippable_component,
                              item_class='(Equipment)')

            elif item_choice == 'Leather Chestplate':
                equippable_component = Equippable(EquipmentSlots.BODY, defence_bonus=1, dexterity_bonus=1)
                item = Entity(x, y, '[', libtcod.chartreuse, 'Leather Chestplate', equippable=equippable_component,
                              item_class='(Equipment)')

            elif item_choice == 'Leather Leggings':
                equippable_component = Equippable(EquipmentSlots.LEGS, defence_bonus=1, dexterity_bonus=1)
                item = Entity(x, y, '[', libtcod.chartreuse, 'Leather Leggings', equippable=equippable_component,
                              item_class='(Equipment)')

            elif item_choice == 'Leather Boots':
                equippable_component = Equippable(EquipmentSlots.FEET, defence_bonus=1, dexterity_bonus=1)
                item = Entity(x, y, '[', libtcod.chartreuse, 'Leather Boots', equippable=equippable_component,
                              item_class='(Equipment)')

            elif item_choice == 'Scale Helmet':
                equippable_component = Equippable(EquipmentSlots.HEAD, defence_bonus=2)
                item = Entity(x, y, '[', libtcod.desaturated_chartreuse, 'Scale Helmet',
                              equippable=equippable_component, item_class='(Equipment)')

            elif item_choice == 'Scale Mail':
                equippable_component = Equippable(EquipmentSlots.BODY, defence_bonus=2)
                item = Entity(x, y, '[', libtcod.desaturated_chartreuse, 'Scale Mail', equippable=equippable_component,
                              item_class='(Equipment)')

            elif item_choice == 'Scale Leggings':
                equippable_component = Equippable(EquipmentSlots.LEGS, defence_bonus=2)
                item = Entity(x, y, '[', libtcod.desaturated_chartreuse, 'Scale Leggings',
                              equippable=equippable_component, item_class='(Equipment)')

            elif item_choice == 'Scale Boots':
                equippable_component = Equippable(EquipmentSlots.FEET, defence_bonus=2)
                item = Entity(x, y, '[', libtcod.desaturated_chartreuse, 'Scale Boots', equippable=equippable_component,
                              item_class='(Equipment)')

            elif item_choice == 'Sealskin Cloak':  # defends ice
                equippable_component = Equippable(EquipmentSlots.BACK, ice_resist=True)
                item = Entity(x, y, '^', libtcod.lighter_blue, 'Sealskin Cloak', equippable=equippable_component,
                              item_class='(Equipment)')

            elif item_choice == 'Lizardskin Cloak':  # defends fire
                equippable_component = Equippable(EquipmentSlots.BACK, fire_resist=True)
                item = Entity(x, y, '^', libtcod.dark_red, 'Lizardskin Cloak', equippable=equippable_component,
                              item_class='(Equipment)')

            elif item_choice == 'Venombane Cloak':  # defends poison
                equippable_component = Equippable(EquipmentSlots.BACK, poison_resist=True)
                item = Entity(x, y, '^', libtcod.light_green, 'Venombane Cloak', equippable=equippable_component,
                              item_class='(Equipment)')

            elif item_choice == 'Iron Helmet':
                equippable_component = Equippable(EquipmentSlots.HEAD, defence_bonus=3)
                item = Entity(x, y, '[', libtcod.dark_chartreuse, 'Iron Helmet', equippable=equippable_component,
                              item_class='(Equipment)')

            elif item_choice == 'Iron Chestplate':
                equippable_component = Equippable(EquipmentSlots.BODY, defence_bonus=3)
                item = Entity(x, y, '[', libtcod.dark_chartreuse, 'Iron Chestplate', equippable=equippable_component,
                              item_class='(Equipment)')

            elif item_choice == 'Iron Leggings':
                equippable_component = Equippable(EquipmentSlots.LEGS, defence_bonus=3)
                item = Entity(x, y, '[', libtcod.dark_chartreuse, 'Iron Leggings', equippable=equippable_component,
                              item_class='(Equipment)')

            elif item_choice == 'Iron Boots':
                equippable_component = Equippable(EquipmentSlots.FEET, defence_bonus=3)
                item = Entity(x, y, '[', libtcod.dark_chartreuse, 'Iron Boots', equippable=equippable_component,
                              item_class='(Equipment)')

            elif item_choice == 'Stone Helmet':
                equippable_component = Equippable(EquipmentSlots.HEAD, defence_bonus=4, dexterity_bonus=-1)
                item = Entity(x, y, '[', libtcod.grey, 'Stone Helmet', equippable=equippable_component,
                              item_class='(Equipment)')

            elif item_choice == 'Stone Chestplate':
                equippable_component = Equippable(EquipmentSlots.BODY, defence_bonus=4, dexterity_bonus=-1)
                item = Entity(x, y, '[', libtcod.grey, 'Stone Chestplate', equippable=equippable_component,
                              item_class='(Equipment)')

            elif item_choice == 'Stone Leggings':
                equippable_component = Equippable(EquipmentSlots.LEGS, defence_bonus=4, dexterity_bonus=-1)
                item = Entity(x, y, '[', libtcod.grey, 'Stone Leggings', equippable=equippable_component,
                              item_class='(Equipment)')

            elif item_choice == 'Stone Boots':
                equippable_component = Equippable(EquipmentSlots.FEET, defence_bonus=4, dexterity_bonus=-1)
                item = Entity(x, y, '[', libtcod.grey, 'Stone Boots', equippable=equippable_component,
                              item_class='(Equipment)')

            elif item_choice == 'Plate Helmet':
                equippable_component = Equippable(EquipmentSlots.HEAD, defence_bonus=5)
                item = Entity(x, y, '[', libtcod.darker_chartreuse, 'Plate Helmet', equippable=equippable_component,
                              item_class='(Equipment)')

            elif item_choice == 'Plate Mail':
                equippable_component = Equippable(EquipmentSlots.BODY, defence_bonus=5)
                item = Entity(x, y, '[', libtcod.darker_chartreuse, 'Plate Mail', equippable=equippable_component,
                              item_class='(Equipment)')

            elif item_choice == 'Plate Leggings':
                equippable_component = Equippable(EquipmentSlots.LEGS, defence_bonus=5)
                item = Entity(x, y, '[', libtcod.darker_chartreuse, 'Plate Leggings', equippable=equippable_component,
                              item_class='(Equipment)')

            elif item_choice == 'Plate Boots':
                equippable_component = Equippable(EquipmentSlots.FEET, defence_bonus=5)
                item = Entity(x, y, '[', libtcod.darker_chartreuse, 'Plate Boots', equippable=equippable_component,
                              item_class='(Equipment)')

            elif item_choice == 'Scroll of Summon Fireball':
                item_component = Item(use_function=cast_fireball, targeting=True, targeting_message=Message(
                    'Left-click a target tile for the fireball, or right-click to cancel.', libtcod.light_cyan),
                                      sound=20,
                                      dificulty=4, damage=25, radius=3)
                item = Entity(x, y, '?', libtcod.red, 'Fireball Scroll', render_order=RenderOrder.ITEM,
                              item=item_component, item_class='(Scroll)')

            elif item_choice == 'Scroll of Confusion Ray':
                item_component = Item(use_function=cast_confuse, targeting=True, targeting_message=Message(
                    'Left-click an enemy to confuse it, or right-click to cancel.', libtcod.light_cyan), difficulty=2)
                item = Entity(x, y, '?', libtcod.light_pink, 'Confusion Scroll', render_order=RenderOrder.ITEM,
                              item=item_component, item_class='(Scroll)')

            elif item_choice == 'Scroll of Lightning Bolt':
                item_component = Item(use_function=cast_lightning, sound=15, difficulty=6, damage=40, maximum_range=5)
                item = Entity(x, y, '?', libtcod.dark_yellow, 'Lightning Scroll', render_order=RenderOrder.ITEM,
                              item=item_component, item_class='(Scroll)')

            elif item_choice == 'Scroll of Frost Blast':
                item_component = Item(use_function=cast_freeze, targeting=True, targeting_message=Message(
                    'Left-click an enemy to freeze it, or right-click to cancel.', libtcod.light_cyan), sound=5,
                                      difficulty=8)
                item = Entity(x, y, '?', libtcod.light_cyan, 'Frost Scroll', render_order=RenderOrder.ITEM,
                              item=item_component, item_class='(Scroll)')

            entities.append(item)
            return entities
