import tcod as libtcod
from game_messages import Message
from random import randint


class Fighter:
    def __init__(self, hp, defence, power, intelligence=0, dexterity=0, xp=0, poison_resist = False, fire_resist = False, ice_resist = False):
        self.base_max_hp = hp
        self.hp = hp
        self.base_defence = defence
        self.base_power = power
        self.base_intelligence = intelligence
        self.base_dexterity = dexterity
        self.fire_resist = fire_resist
        self.poison_resist = poison_resist
        self.ice_resist = ice_resist
        self.xp = xp

    @property
    def max_hp(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.max_hp_bonus
        else:
            bonus = 0

        return self.base_max_hp + bonus

    @property
    def power(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.power_bonus
        else:
            bonus = 0

        return self.base_power + bonus

    @property
    def defence(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.defence_bonus
        else:
            bonus = 0

        return self.base_defence + bonus

    @property
    def intelligence(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.intelligence_bonus
        else:
            bonus = 0

        return self.base_intelligence + bonus

    @property
    def dexterity(self):
        if self.owner and self.owner.equipment:
            bonus = self.owner.equipment.dexterity_bonus
        else:
            bonus = 0

        return self.base_dexterity + bonus

    @property
    def ice_resistance(self):
        if self.owner and self.owner.equipment:
            self.ice_resist = self.owner.equipment.ice_resist
        else:
            self.ice_resist = False

        return self.ice_resist

    @property
    def fire_resistance(self):
        if self.owner and self.owner.equipment:
            self.fire_resist = self.owner.equipment.fire_resist
        else:
            self.fire_resist = False

        return self.fire_resist

    @property
    def poison_resistance(self):
        if self.owner and self.owner.equipment:
            self.poison_resist = self.owner.equipment.poison_resist
        else:
            self.poison_resist = False

        return self.poison_resist

    def take_damage(self, amount):
        results = []

        self.hp -= int(amount)

        if self.hp <= 0:
            results.append({'dead': self.owner})
        return results

    def heal(self, amount):
        if self.hp > 0:
            self.hp += amount

            if self.hp > self.max_hp:
                self.hp = self.max_hp

    def attack(self, target):
        results = []
        miss = randint(0, 100)
        if miss < 95:
            damage = self.power - target.fighter.defence * 2

            damage = randint(damage - 1, damage + 1)

            crit = randint(0, 100)
            if crit < 10:
                damage = damage * 2
                results.append({'message': Message('Critical Hit!', libtcod.fuchsia)})

            if damage > 0:
                results.append({'message': Message('The {0} attacks {1} for {2} hit points.'.format(
                    self.owner.name.capitalize(), target.name, str(int(damage))), libtcod.white)})
                results.extend(target.fighter.take_damage(damage))
            else:
                damage = randint(1, 3)
                results.append({'message': Message('The {0} attacks {1} for {2} hit points.'.format(
                    self.owner.name.capitalize(), target.name, str(int(damage))), libtcod.white)})
                results.extend(target.fighter.take_damage(int(damage)))

            if target.fighter.hp <= 0 and self.owner.name == 'Player':
                levelup = self.owner.level.add_fight_xp(1)
                if levelup:
                    results.append({'message': Message('You have honed your fighting skills farther.  Keep practicing', libtcod.fuchsia)})
                    self.base_power += 1
                    self.base_defence += 1
        else:
            results.append({'message': Message('The {0} misses'.format(self.owner.name.capitalize()), libtcod.white)})

        if self.owner.name == 'Player':
            self.owner.sound = 30
        return results
