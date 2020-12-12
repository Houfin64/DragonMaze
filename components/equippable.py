class Equippable:
    def __init__(self, slot, power_bonus = 0, defence_bonus = 0, max_hp_bonus = 0, intelligence_bonus = 0,
                 dexterity_bonus = 0, ice_resist = False, fire_resist = False, poison_resist = False):

        self.slot = slot
        self.power_bonus = power_bonus
        self.defence_bonus = defence_bonus
        self.max_hp_bonus = max_hp_bonus
        self.intelligence_bonus = intelligence_bonus
        self.dexterity_bonus = dexterity_bonus
        self.ice_resist = ice_resist
        self.fire_resist = fire_resist
        self.poison_resist = poison_resist
