class Tile:
    '''
    A tile on a map, maybe blocking movement, sight, or both
    '''
    def __init__(self, blocked, block_sight=None, turn = 0, water = False):
        self.blocked = blocked

        # By default, transparent walls do not exist
        if block_sight is None:
            block_sight = blocked

        self.block_sight = block_sight

        self.explored = False

        self.turn = turn
        self.water = water