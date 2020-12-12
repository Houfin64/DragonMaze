class Level:
    def __init__(self, bow_current_level=1, bow_current_xp=0, bow_level_up_base=10, bow_level_up_factor=3,
                 fight_current_level=1, fight_current_xp=0, fight_level_up_base=50, fight_level_up_factor=10,
                 int_current_level=4, int_current_xp=0, int_level_up_base=5, int_level_up_factor=1,
                 con_current_level=1, con_current_xp=0, con_level_up_base=500, con_level_up_factor=100):

        self.bow_current_level = bow_current_level
        self.bow_current_xp = bow_current_xp
        self.bow_level_up_base = bow_level_up_base
        self.bow_level_up_factor = bow_level_up_factor

        self.fight_current_level = fight_current_level
        self.fight_current_xp = fight_current_xp
        self.fight_level_up_base = fight_level_up_base
        self.fight_level_up_factor = fight_level_up_factor

        self.int_current_level = int_current_level
        self.int_current_xp = int_current_xp
        self.int_level_up_base = int_level_up_base
        self.int_level_up_factor = int_level_up_factor

        self.con_current_level = con_current_level
        self.con_current_xp = con_current_xp
        self.con_level_up_base = con_level_up_base
        self.con_level_up_factor = con_level_up_factor

    @property
    def bow_experience_to_next_level(self):
        return self.bow_level_up_base + self.bow_current_level * self.bow_level_up_factor

    @property
    def fight_experience_to_next_level(self):
        return self.fight_level_up_base + self.fight_current_level * self.fight_level_up_factor

    @property
    def con_experience_to_next_level(self):
        return self.con_level_up_base + self.con_current_level * self.con_level_up_factor

    @property
    def int_experience_to_next_level(self):
        return self.int_level_up_base + self.int_current_level * self.int_level_up_factor

    def add_bow_xp(self, xp):
        self.bow_current_xp += xp

        if self.bow_current_xp > self.bow_experience_to_next_level:
            self.bow_current_xp -= self.bow_experience_to_next_level
            self.bow_current_level += 1

            return True
        else:
            return False

    def add_fight_xp(self, xp):
        self.fight_current_xp += xp

        if self.fight_current_xp > self.fight_experience_to_next_level:
            self.fight_current_xp -= self.fight_experience_to_next_level
            self.fight_current_level += 1

            return True
        else:
            return False

    def add_int_xp(self, xp):
        self.int_current_xp += xp

        if self.int_current_xp > self.int_experience_to_next_level:
            self.int_current_xp -= self.int_experience_to_next_level
            self.int_current_level += 1

            return True
        else:
            return False

    def add_con_xp(self, xp):
        self.con_current_xp += xp

        if self.con_current_xp > self.con_experience_to_next_level:
            self.con_current_xp -= self.con_experience_to_next_level
            self.con_current_level += 1

            return True
        else:
            return False

