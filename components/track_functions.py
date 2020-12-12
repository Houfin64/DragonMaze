class Scent:
    def set_scent(game_map, x, y, turns):
        if game_map.tiles[x][y].water == False:
            game_map.tiles[x][y].turn = turns

    def get_scent(game_map, mx, my, turns):
        highscent = 0
        move_direction = []
        for x in range(-1, 1):
            for y in range(-1, 1):
                a = game_map.tiles[mx+x][my+y].turn

                if a > highscent and a > turns - 25:
                        highscent = a
                        move_direction = [x, y]
        return move_direction
