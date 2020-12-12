import shelve
from game_states import GameStates

def save_game(player, entities, game_map, message_log, game_state, poison_turns, turns, burned_turns, frozen_turns):
    with shelve.open('savegame.dat', 'n') as data_file:
        data_file['player_index'] = entities.index(player)
        data_file['entities'] = entities
        data_file['game_map'] = game_map
        data_file['message_log'] = message_log
        data_file['game_state'] = game_state
        data_file['poison_turns'] = poison_turns
        data_file['turns'] = turns
        data_file['burned_turns'] = burned_turns
        data_file['frozen_turns'] = frozen_turns

def load_game():

    with shelve.open('savegame.dat', 'r') as data_file:
        player_index = data_file['player_index']
        entities = data_file['entities']
        game_map = data_file['game_map']
        message_log = data_file['message_log']
        game_state = data_file['game_state']
        poison_turns = data_file['poison_turns']
        turns = data_file['turns']
        burned_turns = data_file['burned_turns']
        frozen_turns = data_file['frozen_turns']

    if game_state == GameStates.PLAYER_DEAD:
        raise FileNotFoundError

    else:
        player = entities[player_index]

        return player, entities, game_map, message_log, game_state, poison_turns, turns, burned_turns, frozen_turns
