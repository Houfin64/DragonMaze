from equipment_slots import EquipmentSlots

class Equipment:
    def __init__(self, main_hand = None, off_hand = None, right_finger=None,
                 feet = None, legs = None, body = None, head = None, left_finger = None, back = None):
        self.main_hand = main_hand
        self.off_hand = off_hand
        self.body = body
        self.head = head
        self.legs = legs
        self.feet = feet
        self.right_finger = right_finger
        self.left_finger = left_finger
        self.back = back

    @property
    def max_hp_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.max_hp_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.max_hp_bonus

        if self.feet and self.feet.equippable:
            bonus += self.feet.equippable.max_hp_bonus

        if self.body and self.body.equippable:
            bonus += self.body.equippable.max_hp_bonus

        if self.legs and self.legs.equippable:
            bonus += self.legs.equippable.max_hp_bonus

        if self.head and self.head.equippable:
            bonus += self.head.equippable.max_hp_bonus

        if self.right_finger and self.right_finger.equippable:
            bonus += self.right_finger.equippable.max_hp_bonus

        if self.left_finger and self.left_finger.equippable:
            bonus += self.left_finger.equippable.max_hp_bonus

        if self.back and self.back.equippable:
            bonus += self.back.equippable.max_hp_bonus

        return bonus

    @property
    def power_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.power_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.power_bonus

        if self.feet and self.feet.equippable:
            bonus += self.feet.equippable.power_bonus

        if self.body and self.body.equippable:
            bonus += self.body.equippable.power_bonus

        if self.legs and self.legs.equippable:
            bonus += self.legs.equippable.power_bonus

        if self.head and self.head.equippable:
            bonus += self.head.equippable.power_bonus

        if self.right_finger and self.right_finger.equippable:
            bonus += self.right_finger.equippable.power_bonus

        if self.left_finger and self.left_finger.equippable:
            bonus += self.left_finger.equippable.power_bonus

        if self.back and self.back.equippable:
            bonus += self.back.equippable.power_bonus

        return bonus

    @property
    def defence_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.defence_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.defence_bonus

        if self.feet and self.feet.equippable:
            bonus += self.feet.equippable.defence_bonus

        if self.body and self.body.equippable:
            bonus += self.body.equippable.defence_bonus

        if self.legs and self.legs.equippable:
            bonus += self.legs.equippable.defence_bonus

        if self.head and self.head.equippable:
            bonus += self.head.equippable.defence_bonus

        if self.right_finger and self.right_finger.equippable:
            bonus += self.right_finger.equippable.defence_bonus

        if self.left_finger and self.left_finger.equippable:
            bonus += self.left_finger.equippable.defence_bonus

        if self.back and self.back.equippable:
            bonus += self.back.equippable.defence_bonus

        return bonus

    @property
    def intelligence_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.intelligence_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.intelligence_bonus

        if self.feet and self.feet.equippable:
            bonus += self.feet.equippable.intelligence_bonus

        if self.body and self.body.equippable:
            bonus += self.body.equippable.intelligence_bonus

        if self.legs and self.legs.equippable:
            bonus += self.legs.equippable.intelligence_bonus

        if self.head and self.head.equippable:
            bonus += self.head.equippable.intelligence_bonus

        if self.right_finger and self.right_finger.equippable:
            bonus += self.right_finger.equippable.intelligence_bonus

        if self.left_finger and self.left_finger.equippable:
            bonus += self.left_finger.equippable.intelligence_bonus

        if self.back and self.back.equippable:
            bonus += self.back.equippable.intelligence_bonus

        return bonus

    @property
    def dexterity_bonus(self):
        bonus = 0

        if self.main_hand and self.main_hand.equippable:
            bonus += self.main_hand.equippable.dexterity_bonus

        if self.off_hand and self.off_hand.equippable:
            bonus += self.off_hand.equippable.dexterity_bonus

        if self.feet and self.feet.equippable:
            bonus += self.feet.equippable.dexterity_bonus

        if self.body and self.body.equippable:
            bonus += self.body.equippable.dexterity_bonus

        if self.legs and self.legs.equippable:
            bonus += self.legs.equippable.dexterity_bonus

        if self.head and self.head.equippable:
            bonus += self.head.equippable.dexterity_bonus

        if self.right_finger and self.right_finger.equippable:
            bonus += self.right_finger.equippable.dexterity_bonus

        if self.left_finger and self.left_finger.equippable:
            bonus += self.left_finger.equippable.dexterity_bonus

        if self.back and self.back.equippable:
            bonus += self.back.equippable.dexterity_bonus

        return bonus

    @property
    def ice_resist(self):
        ice_resist = False

        if self.back and self.back.equippable:
            ice_resist = self.back.equippable.ice_resist

        return ice_resist

    @property
    def fire_resist(self):
        fire_resist = False

        if self.back and self.back.equippable:
            fire_resist = self.back.equippable.fire_resist

        return fire_resist

    @property
    def poison_resist(self):
        poison_resist = False

        if self.back and self.back.equippable:
            poison_resist = self.back.equippable.poison_resist

        return poison_resist

    def toggle_equip(self, equippable_entity):
        results = []

        slot = equippable_entity.equippable.slot

        if slot == EquipmentSlots.MAIN_HAND:
            if self.main_hand == equippable_entity:
                self.main_hand = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.main_hand:
                    results.append({'dequipped': self.main_hand})

                self.main_hand = equippable_entity
                results.append({'equipped': equippable_entity})
        elif slot == EquipmentSlots.OFF_HAND:
            if self.off_hand == equippable_entity:
                self.off_hand = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.off_hand:
                    results.append({'dequipped': self.off_hand})

                self.off_hand = equippable_entity
                results.append({'equipped': equippable_entity})

        elif slot == EquipmentSlots.HEAD:
            if self.head == equippable_entity:
                self.head = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.head:
                    results.append({'dequipped': self.head})

                self.head = equippable_entity
                results.append({'equipped': equippable_entity})

        elif slot == EquipmentSlots.BODY:
            if self.body == equippable_entity:
                self.body = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.body:
                    results.append({'dequipped': self.body})

                self.body = equippable_entity
                results.append({'equipped': equippable_entity})

        elif slot == EquipmentSlots.LEGS:
            if self.legs == equippable_entity:
                self.legs = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.legs:
                    results.append({'dequipped': self.legs})

                self.legs = equippable_entity
                results.append({'equipped': equippable_entity})

        elif slot == EquipmentSlots.FEET:
            if self.feet == equippable_entity:
                self.feet = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.feet:
                    results.append({'dequipped': self.feet})

                self.feet = equippable_entity
                results.append({'equipped': equippable_entity})

        elif slot == EquipmentSlots.BACK:
            if self.back == equippable_entity:
                self.back = None
                results.append({'dequipped': equippable_entity})
            else:
                if self.back:
                    results.append({'dequipped': self.back})

                self.back = equippable_entity
                results.append({'equipped': equippable_entity})

        elif slot == EquipmentSlots.RIGHT_FINGER:
            if self.right_finger == equippable_entity:
                self.right_finger = None
                results.append({'dequipped': equippable_entity})

            elif self.left_finger == equippable_entity:
                self.left_finger = None
                results.append({'dequipped': equippable_entity})

            else:
                if self.right_finger:
                    if not self.left_finger:
                        self.left_finger = equippable_entity
                        results.append({'equipped': equippable_entity})
                    else:
                        results.append({'dequipped': self.right_finger})
                        self.right_finger = equippable_entity
                        results.append({'equipped': equippable_entity})
                else:
                    if not self.left_finger:
                        self.left_finger = equippable_entity
                        results.append({'equipped': equippable_entity})
                    else:
                        self.right_finger = equippable_entity
                        results.append({'equipped': equippable_entity})

        return results