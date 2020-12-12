import tcod as libtcod
from game_messages import Message


class Inventory:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = []

    def add_item(self, item):
        results = []
        add = False

        for thing in self.owner.items:
            if type(thing)!= str:
                if thing.name == item.name:
                    add = True
                    break

        if (len(self.items) >= self.capacity) or (len(self.owner.items) == 26 and add != True):
            results.append({
                'item_added': None,
                'message': Message('You cannot carry any more, your inventory is full', libtcod.yellow)
            })
        else:
            results.append({
                'item_added': item,
                'message': Message('You pick up the {0}!'.format(item.name), libtcod.lighter_blue)
            })

            self.items.append(item)

            self.owner.items.append(item)

            for each in self.owner.items:
                if type(each) != str:
                    add = 0
                    for this in self.owner.items:
                        if type(this) != str:
                            if each.name == this.name:
                                if add == 1:
                                    self.owner.items.remove(item)
                                    add = 0
                                else:
                                    add = 1

        return results

    def use(self, success, item_entity, **kwargs):
        results = []

        item_component = item_entity.item

        if item_component.use_function is None:
            equippable_component = item_entity.equippable

            if equippable_component:
                results.append({'equip': item_entity})
            else:
                results.append({'message': Message('The {0} cannot be used'.format(item_entity.name), libtcod.yellow)})
        else:
            if success:
                if item_component.targeting and not (kwargs.get('target_x') or kwargs.get('target_y')):
                    results.append({'targeting': item_entity})

                elif item_component.arrow_targeting and not kwargs.get('direction'):
                    results.append({'arrow_targeting': item_entity})

                else:
                    kwargs = {**item_component.function_kwargs, **kwargs}
                    item_use_results = item_component.use_function(self.owner, **kwargs)

                    for item_use_result in item_use_results:
                        if item_use_result.get('consumed'):
                            self.remove_item(item_entity)
                        arrow = item_use_result.get('arrow_consumed')
                        if arrow:
                            self.remove_item(arrow)

                    results.extend(item_use_results)
            else:
                results.append({'pass': True, 'message': Message('Your reading is not good enough to decifer the text', libtcod.yellow)})

        self.owner.sound = item_component.sound
        return results

    def remove_item(self, item_entity):
        remove = 1

        for item in self.items:
            if remove == 1 and item.name == item_entity.name:
                remove = 0
                item_entity = item
                self.items.remove(item)

        remove = 1
        for item in self.items:
            if item.name  == item_entity.name:
                remove = 0
                break
                
        if remove:
            for thing in self.owner.items:
                if type(thing) != str:
                    if thing.name == item_entity.name:
                        self.owner.items.remove(thing)
                        break



    def drop_item(self, item):
        results = []
        toggle = 0
        for equip in self.items:
            if equip.name == item.name:
                toggle += 1

        if toggle == 1:
            if self.owner.equipment.main_hand == item or self.owner.equipment.off_hand == item or self.owner.equipment.head == item or \
                    self.owner.equipment.body == item or self.owner.equipment.legs == item or self.owner.equipment.feet == item or \
                    self.owner.equipment.right_finger == item or self.owner.equipment.left_finger == item or self.owner.equipment.back == item:
                self.owner.equipment.toggle_equip(item)

        item.x = self.owner.x
        item.y = self.owner.y

        self.remove_item(item)
        results.append({'item_dropped': item, 'message': Message('You dropped the {0}'.format(item.name),
                                                                 libtcod.yellow)})

        return results