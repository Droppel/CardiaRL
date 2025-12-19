import typing

# A game is just represented as a 1d array
# It's length is 6 n where n is the number of "tracked" encounters
# Each encounter is represented by 6 values in the array
# The first value is the first players card
# The second value is the first players cards modifier
# The third value is 0 or 1 depending on if the first players card has the ongoing marker
# This is repeated for the second player
class Game:
    def __init__(self, decks=None):
        self.state = []
        self.discards = [[], []]
        self.hands = [[], []]
        if decks is None:
            self.decks = [[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16],
                      [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]]
        else:
            self.decks = decks
        self.next_modifier = [0, 0]
    
    def initial_deal(self):
        for _ in range(5):
            self.hands[0].append(self.decks[0].pop())
            self.hands[1].append(self.decks[1].pop())

    def copy(self):
        new_game = Game(decks=[self.decks[0][:], self.decks[1][:]])
        new_game.state = self.state[:]
        new_game.discards = [self.discards[0][:], self.discards[1][:]]
        new_game.hands = [self.hands[0][:], self.hands[1][:]]
        new_game.next_modifier = self.next_modifier[:]
        return new_game

    def add_encounter(self, cards):
        p0_influence = cards[0] + self.next_modifier[0]
        p1_influence = cards[1] + self.next_modifier[1]
        self.state.extend([cards[0], self.next_modifier[0], 0, cards[1], self.next_modifier[1], 0])
        if p0_influence > p1_influence:
            return 0
        if p1_influence > p0_influence:
            return 1
        self.next_modifier = [0, 0]
        return 2
    
    def evaluate(self):
        judges = [0, 0]
        for i in range(0, len(self.state), 6):
            if self.state[i] == 8 and self.state[i+2] == 1:
                judges[0] = 1
            if self.state[i+3] == 8 and self.state[i+5] == 1:
                judges[1] = 1
        sigils = [0, 0]
        treasurer = 1
        for i in range(len(self.state)-6, -1, -6):
            if (self.state[i] == 12 and self.state[i+2] == 1):
                treasurer += 1
            if (self.state[i+3] == 12 and self.state[i+5] == 1):
                treasurer += 1
            if (self.state[i] == 4 and self.state[i+2] == 1) or (self.state[i+3] == 4 and self.state[i+5] == 1):
                sigils[0] += judges[0] * treasurer
                sigils[1] += judges[1] * treasurer
                treasurer = 1
                continue
            influences = [self.state[i] + self.state[i+1], self.state[i+3] + self.state[i+5]]
            if influences[0] > influences[1]:
                sigils[0] += treasurer
                treasurer = 1
            elif influences[1] > influences[0]:
                sigils[1] += treasurer
                treasurer = 1
            else:
                sigils[0] += judges[0] * treasurer
                sigils[1] += judges[1] * treasurer
                treasurer = 1
        return sigils
    
    # Returns False, None if game is over
    # Returns False, options if game is not over but we need a new move
    # Returns True, None iof turn ends
    def next_turn(self, moves: typing.List[int]):
        if len(self.hands[0]) == 0:
            print("Player 1 wins! Player 0 has no cards left.")
            return False, None
        if len(self.hands[1]) == 0:
            print("Player 0 wins! Player 1 has no cards left.")
            return False, None

        if len(moves) == 0:
            return True, list(range(len(self.hands[0])))
        card1_index = moves.pop(0)

        if len(moves) == 0:
            return True, list(range(len(self.hands[1])))
        card2_index = moves.pop(0)
        cards = [self.hands[0].pop(card1_index), self.hands[1].pop(card2_index)]
        print(f"Player 0 plays {cards[0]}, Player 1 plays {cards[1]}")
        enc_result = self.add_encounter(cards)
        if enc_result != 2:
            activating_player = 1 - enc_result
            winner, options = trigger_card(self, cards[activating_player], activating_player, moves)
            if winner == 0:
                print("Player 0 wins!")
                return False, None
            elif winner == 1:
                print("Player 1 wins!")
                return False, None
            if options is not None:
                return True, options
        
        sigils = self.evaluate()
        print(f"Sigils: {sigils}")
        if sigils[0] >= 5 and sigils[0] > sigils[1]:
            print("Player 0 wins!")
            return False, None
        elif sigils[1] >= 5 and sigils[1] > sigils[0]:
            print("Player 1 wins!")
            return False, None

        self.hands[0].append(self.decks[0].pop()) if len(self.decks[0]) > 0 else None
        self.hands[1].append(self.decks[1].pop()) if len(self.decks[1]) > 0 else None
        return True, None

# Returns winner, options
def trigger_card(game: Game, card, player, moves: typing.List[int]):
    if card == 1:
        # Remove the last encounter
        game.discards[0].append(game.state[-6])
        game.discards[1].append(game.state[-3])
        game.state = game.state[:-6]
        return -1, None
    elif card == 2:
        # Find valid targets
        valid_targets = []
        for i in range(0, len(game.state), 6):
            if game.state[i+1] != 0:  # Player 1's modifier
                valid_targets.append(i+1)
            if game.state[i+2] != 0:  # Player 2's modifier
                valid_targets.append(i+2)
            if game.state[i+4] != 0:  # Player 1's modifier
                valid_targets.append(i+4)
            if game.state[i+5] != 0:  # Player 2's modifier
                valid_targets.append(i+5)
        if len(valid_targets) == 0:
            return -1, None
        if len(moves) == 0:
            return -1, valid_targets
        choice = moves.pop(0)
        game.state[choice] = 0  # Remove a modifier
        return -1, None
    elif card == 3:
        game.next_modifier[player] -= 5
        return -1, None
    elif card == 4:
        game.state[-4 if player == 0 else -1] = 1  # Give ongoing to last played card
        return -1, None
    elif card == 5:
        opponent = 1 - player
        opponent_deck_length = len(game.decks[opponent])
        if opponent_deck_length == 0:
            return -1, None
        if opponent_deck_length == 1:
            game.discards[opponent].append(game.decks[opponent].pop())
            return -1, None
        game.discards[opponent].append(game.decks[opponent].pop())
        game.discards[opponent].append(game.decks[opponent].pop())
        return -1, None
    elif card == 6:
        return -1, None # No effect
    elif card == 7:
        opponent = 1 - player
        if len(moves) == 0:
            return -1, range(4)
        faction = moves.pop(0)
        options = [-1]
        options.extend([i for i in range(len(game.hands[opponent])) if game.hands[opponent][i] % 4 == faction])
        if len(options) == 0:
            game.state[-5 if player == 0 else -2] += 7 
            return -1, None
        if len(moves) == 0:
            return -1, options
        choice = moves.pop(0)
        if choice == -1:
            game.state[-5 if player == 0 else -2] += 7 
            return -1, None
        game.discards[opponent].append(game.hands[opponent].pop(choice))
    elif card == 8:
        game.state[-4 if player == 0 else -1] = 1  # Give ongoing to last played card
        return -1, None
    elif card == 9:
        opponent = 1 - player
        if len(moves) == 0:
            return -1, range(4)
        faction = moves.pop(0)
        for i in range(len(game.hands[opponent])-1, -1, -1):
            if game.hands[opponent][i] % 4 == faction:
                game.discards[opponent].append(game.hands[opponent].pop(i))
        return -1, None
    elif card == 10:
        opponent = 1 - player
        if len(game.hands[opponent]) == 0:
            return player, None
        game.discards[opponent].append(game.state[-3 if opponent == 0 else -6])
        if len(moves) == 0:
            return -1, range(len(game.hands[opponent]))
        new_card = moves.pop(0)
        game.state[-3 if opponent == 0 else -6] = game.hands[opponent].pop(new_card)
        return -1, None
    elif card == 11:
        if len(game.state) >= 12:
            game.state.extend([0] * (12 - len(game.state)))
        game.next_modifier[player] += 3
        return -1, None
    elif card == 12:
        game.state[-4 if player == 0 else -1] = 1  # Give ongoing to last played card
        return -1, None
    elif card == 13:
        # All previous encounters as options
        options = list(range(0, len(game.state) - 1, 6))
        if len(options) == 0:
            return -1, None
        if len(moves) == 0:
            return -1, options
        choice = moves.pop(0)
        opponent = 1 - player
        opp_card = choice + 3 if opponent == 0 else choice
        own_card = choice if opponent == 0 else choice + 3
        game.discards[opponent].append(game.state[opp_card])
        game.hands[player].append(game.state[own_card])
        for i in range(6):
            game.state.pop(choice)
        return -1, None
    elif card == 14:
        card_influence = 14 + game.state[-5 if player == 0 else -2]
        options = [i for i in range(0 if player == 0 else 3, len(game.state), 6) if game.state[i] + game.state[i+1] < card_influence]
        if len(options) == 0:
            return -1, None
        if len(moves) == 0:
            return -1, options
        choice = moves.pop(0)
        return trigger_card(game, game.state[choice], 1 - player, moves)
    elif card == 15:
        options = range(0, len(game.state), 3)
        if len(moves) == 0:
            return -1, options
        choice = moves.pop(0)
        game.state[choice + 1] += 3
        if len(moves) == 0:
            return -1, options
        choice = moves.pop(0)
        game.state[choice + 1] -= 3
        return -1, None
    elif card == 16:
        return player, None
    print("Error: Unknown card triggered")
    return -1, None
