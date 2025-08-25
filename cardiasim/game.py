import copy
import typing

from .cards import *
if typing.TYPE_CHECKING:
    from .players.player import Player

class Encounter():
    def __init__(self):
        self.cards: typing.List[Card] = [None, None]
        self.permanent: typing.List[bool] = [False, False]
        self.modifiers: typing.List[int] = [0, 0]

    def get_sigil(self, draw_winner):
        if self.cards[0] is None or self.cards[1] is None:
            return -1 # Not possible to evaluate
        if self.cards[0].name == "Mediator" and self.permanent[0]:
            return draw_winner
        if self.cards[1].name == "Mediator" and self.permanent[1]:
            return draw_winner

        if self.cards[0].influence + self.modifiers[0] > self.cards[1].influence + self.modifiers[1]:
            return 1
        elif self.cards[0].influence + self.modifiers[0] < self.cards[1].influence + self.modifiers[1]:
            return 2

        return draw_winner  # Tie

    def __str__(self):
        return f" - {self.cards[0].name} ({self.cards[0].influence+self.modifiers[0]}) vs {self.cards[1].name} ({self.cards[1].influence+self.modifiers[1]})"
class KnownGameState():
    def __init__(self):
        self.handsizes = [0, 0]
        self.decksizes = [0, 0]
        self.discards = [[], []]  # List of cards in each player's discard pile
        self.playopen = [False, False]
        self.encounters: typing.List[Encounter] = []
        self.current_encounter = 0
        self.drawwinner = 0  # 0 for draw, 1 for player1, 2 for player2, 3 for both

class Game():
    def __init__(self, players: typing.List['Player'], render=True):
        self.render = render
        self.players: typing.List['Player'] = players
        self.players[0].setup_player()
        self.players[1].setup_player()

        self.playopen = [False, False]
        self.current_encounter = 0
        self.encounters: typing.List[Encounter] = []
        self.drawwinner = 0  # 0 for draw, 1 for player1, 2 for player2, 3 for both
        self.winner = 0 # 0 for no winner, 1 for player1, 2 for player2
        pass

    def get_encounter(self, index) -> Encounter:
        if index < len(self.encounters):
            return self.encounters[index]
        new_enc = Encounter()
        self.encounters.append(new_enc)
        return new_enc

    def get_gamestate(self) -> KnownGameState:
        state = KnownGameState()
        state.handsizes[0] = len(self.players[0].hand)
        state.handsizes[1] = len(self.players[1].hand)
        state.decksizes[0] = len(self.players[0].deck)
        state.decksizes[1] = len(self.players[1].deck)
        state.discards[0] = copy.deepcopy(self.players[0].discard)
        state.discards[1] = copy.deepcopy(self.players[1].discard)
        state.playopen = copy.deepcopy(self.playopen)
        state.encounters = copy.deepcopy(self.encounters)
        state.current_encounter = self.current_encounter
        state.drawwinner = self.drawwinner
        return state

    def print(self, msg):
        if self.render:
            print(msg)

    def print_state(self):
        if not self.render:
            return
        print(f"{self.players[0].name} Handcards: {len(self.players[0].hand)}")
        print(f"{self.players[0].name} Deck: {len(self.players[0].deck)}")
        player1_discard = f"{self.players[0].name} Discard: "
        for card in self.players[0].discard:
            player1_discard += card.name + ", "
        print(player1_discard)
        print("-----")
        print(f"{self.players[1].name} Handcards: {len(self.players[1].hand)}")
        print(f"{self.players[1].name} Deck: {len(self.players[1].deck)}")
        player2_discard = f"{self.players[1].name} Discard: "
        for card in self.players[1].discard:
            player2_discard += card.name + ", "
        print(player2_discard)
        print("-----")
        print("Encounters:")
        for encounter in self.encounters:
            if encounter.cards[0] and encounter.cards[1]:
                print(encounter)
        print("-----")

    def get_current_sigils(self):
        player1_sigils = 0
        player2_sigils = 0
        treasurer_bonus = 0
        for enc in reversed(self.encounters):
            winner = enc.get_sigil(self.drawwinner)
            if winner == 1:
                player1_sigils += 1 + treasurer_bonus
            elif winner == 2:
                player2_sigils += 1 + treasurer_bonus
            elif winner == 3:
                player1_sigils += 1 + treasurer_bonus
                player2_sigils += 1 + treasurer_bonus
            treasurer_bonus = 0
            if enc.cards[0] and enc.cards[0].name == "Treasurer" and enc.permanent[0]:
                treasurer_bonus += 1
            if enc.cards[1] and enc.cards[1].name == "Treasurer" and enc.permanent[1]:
                treasurer_bonus += 1
        return player1_sigils, player2_sigils

    def turn(self) -> typing.Tuple[bool, KnownGameState]:
        self.print("Starting turn")
        self.print_state()

        player1_card: Card = None
        player2_card: Card = None
        player1_card_choices = [card for card in self.players[0].hand]
        player2_card_choices = [card for card in self.players[1].hand]
        if not player1_card_choices and not player2_card_choices:
            self.print("No cards left! The game ends in a draw.")
            return 0, self.get_gamestate()
        if not player1_card_choices:
            self.print(f"{self.players[0].name} has no cards to play. Player 2 wins!")
            return 2, self.get_gamestate()
        if not player2_card_choices:
            self.print(f"{self.players[1].name} has no cards to play. Player 1 wins!")
            return 1, self.get_gamestate()

        encounter = self.get_encounter(self.current_encounter)
        if self.playopen[0]:
            player1_card = self.players[0].choose("PlayFirst", player1_card_choices, self.get_gamestate())
            encounter.cards[0] = player1_card
            self.print(f"{self.players[0].name} played {player1_card.name}")
            player2_card = self.players[1].choose("PlaySecond", player2_card_choices, self.get_gamestate())
            encounter.cards[1] = player2_card
            self.print(f"{self.players[1].name} played {player2_card.name}")
        elif self.playopen[1]:
            player2_card = self.players[1].choose("PlayFirst", player2_card_choices, self.get_gamestate())
            encounter.cards[1] = player2_card
            self.print(f"{self.players[1].name} played {player2_card.name}")
            player1_card = self.players[0].choose("PlaySecond", player1_card_choices, self.get_gamestate())
            encounter.cards[0] = player1_card
            self.print(f"{self.players[0].name} played {player1_card.name}")
        else:
            cur_game_state = self.get_gamestate()
            player1_card = self.players[0].choose("PlayCard", player1_card_choices, cur_game_state)
            player2_card = self.players[1].choose("PlayCard", player2_card_choices, cur_game_state)
            encounter.cards[0] = player1_card
            encounter.cards[1] = player2_card
            self.print(f"{self.players[0].name} played {player1_card.name}")
            self.print(f"{self.players[1].name} played {player2_card.name}")

        self.players[0].hand.remove(player1_card)
        self.players[1].hand.remove(player2_card)
        # Reset playopen states
        self.playopen = [False, False]
        
        # Play cards
        self.print(f"{self.players[0].name} plays {player1_card.name}: Influence {player1_card.influence}")
        self.print(f"{self.players[1].name} plays {player2_card.name}: Influence {player2_card.influence}")
        sigil = encounter.get_sigil(self.drawwinner)
        if sigil == -1:
            self.print("Not possible to evaluate sigil.")
        elif sigil == 0:
            self.print("Both players played cards with equal influence. No sigils awarded.")
        elif sigil == 1:
            player2_card.effect(self, self.players[1].id)
        else:
            player1_card.effect(self, self.players[0].id)

        if self.winner != 0:
            self.print(f"Player {self.winner} has already won the game.")
            return self.winner, self.get_gamestate()

        self.players[0].draw_card()
        self.players[1].draw_card()

        # Check Judge
        self.drawwinner = 0
        for enc in self.encounters:
            if enc.cards[0] and enc.cards[0].name == "Judge" and enc.permanent[0]:
                self.drawwinner += 1
            if enc.cards[1] and enc.cards[1].name == "Judge" and enc.permanent[1]:
                self.drawwinner += 2

        # Check winner
        player1_sigils, player2_sigils = self.get_current_sigils()
        
        if player1_sigils == player2_sigils:
            pass
        elif player1_sigils >= 5 and player1_sigils > player2_sigils:
            self.print(f"{self.players[0].name} wins!")
            return 1, self.get_gamestate()
        elif player2_sigils >= 5 and player2_sigils > player1_sigils:
            self.print(f"{self.players[1].name} wins!")
            return 2, self.get_gamestate()

        self.print(f"End of turn. Sigils - {self.players[0].name}: {player1_sigils}, {self.players[1].name}: {player2_sigils}")

        self.current_encounter += 1
        return -1, self.get_gamestate()