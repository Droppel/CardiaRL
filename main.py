from torch import rand
from engine.game import Game, trigger_card
import random
import copy

def generate_next_turn_options(game: Game):
    moves = []
    for card in game.hands[0]:
        moves.append(card)
    
    return running, options, winner

if __name__ == "__main__":
    # ==================== Input ====================
    hand_0 = [1, 2, 3, 4, 5]
    discard_0 = []
    discard_1 = []
    state = []
    next_modifier = [0, 0]
    # ==================== Input ====================

    decks = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
             [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]]
    for card in hand_0:
        decks[0].remove(card)
    for card in discard_0:
        decks[0].remove(card)
    for card in discard_1:
        decks[1].remove(card)

    random.seed(42)

    moves = []

    game = Game()
    game.decks = decks
    game.eval_player_hand = hand_0
    game.discards = [discard_0, discard_1]
    game.state = state

    moves_lists = []
    moves_evals = []
    game_copy = game.copy()
    running, options, winner = game_copy.next_turn(copy.copy(moves))
    for option in options:
        moves_lists.append([option])
        moves_evals
    while True:
        game_copy = game.copy()
        running, options = game_copy.next_turn(copy.copy(moves))
        if options is not None:
            moves.append(random.choice(options))
        else:
            game = game_copy
            moves = []
        if not running:
            break