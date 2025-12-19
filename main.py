from torch import rand
from engine.game import Game, trigger_card
import copy
import itertools

def generate_next_turn_options(game: Game):
    moves = []
    for card in game.hands[0]:
        moves.append(card)
    
    return running, options, winner

if __name__ == "__main__":
    # ==================== Input ====================
    hand_0 = [2, 4, 12, 13, 16]
    hand_1_size = 4
    discard_0 = [1,8]
    discard_1 = [1,4,5,12,15]
    state = [5,0,0,6,0,0,10,0,0,7,0,0,7,0,0,11,0,0,15,0,0,2,0,0,3,0,0,10,0,0,14,0,0,14,0,0,9,0,0,9,0,0]
    next_modifier = [0, 0]
    # ==================== Input ====================

    games = []

    initial_decks = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
             [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]]
    for i in range(0, len(state), 6):
        initial_decks[0].remove(state[i])
    for i in range(3, len(state), 6):
        initial_decks[1].remove(state[i])
    for card in hand_0:
        initial_decks[0].remove(card)
    for card in discard_0:
        initial_decks[0].remove(card)
    for card in discard_1:
        initial_decks[1].remove(card)

    for deck_permutation in itertools.permutations(initial_decks[0]):
        for deck_permutation_1 in itertools.permutations(initial_decks[1]):
            decks = [list(deck_permutation), list(deck_permutation_1)]
            game = Game()
            game.decks = decks
            game.hands[0] = hand_0
            for _ in range(hand_1_size):
                game.hands[1].append(game.decks[1].pop(0))
            game.discards = [discard_0, discard_1]
            game.state = state
            game.next_modifier = next_modifier
            games.append(game)

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