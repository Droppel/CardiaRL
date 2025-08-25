import typing
import random
import copy
from .player import Player
from .randomcpu import RandomCPU
from ..cards import Card
from ..game import KnownGameState, Game

class Evaluator(Player):
    def __init__(self, name, id):
        super().__init__(name, id)

    def evaluate_game_state(self, game: 'Game') -> float:
        hand_size_weight = 0.5
        deck_size_weight = 0.0
        has_judge_weight = 0.0
        sigils_weight = 4.0

        deck_size_diff = len(self.deck) - len(game.players[1].deck)
        hand_size_diff = len(self.hand) - len(game.players[1].hand)
        has_judge = any(enc.cards[0] == "Judge" for enc in game.encounters) - any(enc.cards[1] == "Judge" for enc in game.encounters)
        player1_sigils, player2_sigils = game.get_current_sigils()
        sigils_diff = player1_sigils - player2_sigils

        score = (hand_size_weight * hand_size_diff +
                 deck_size_weight * deck_size_diff +
                 has_judge_weight * has_judge +
                 sigils_weight * sigils_diff)
        return score

    def create_possible_games(self, known_state: 'KnownGameState') -> typing.List['Game']:
        # Create new game based on known_state
        other_id = self.id ^ 1

        players: typing.List[Player] = [RandomCPU("SimPlayer1", 0), RandomCPU("SimPlayer2", 1)]
        players[0].setup_deck()
        players[1].setup_deck()
        simulated_game = Game([RandomCPU("SimPlayer1", 0), RandomCPU("SimPlayer2", 1)], render=False)
        simulated_game.players = players
        simulated_game.current_encounter = known_state.current_encounter
        simulated_game.playopen = known_state.playopen.copy()
        simulated_game.encounters = copy.deepcopy(known_state.encounters)
        simulated_game.drawwinner = known_state.drawwinner

        for card in self.hand:
            card_name = card.name
            card = next((c for c in players[0].deck if c.name == card_name), None)
            players[0].hand.append(card)
            players[0].deck.remove(card)
        for card in self.discard:
            card_name = card.name
            card = next((c for c in players[0].deck if c.name == card_name), None)
            players[0].discard.append(card)
            players[0].deck.remove(card)

        for card in known_state.discards[other_id]:
            card_name = card.name
            card = next((c for c in players[1].deck if c.name == card_name), None)
            if card is not None:
                players[1].discard.append(card)
                players[1].deck.remove(card)

        # Create a game for each possible card the opponent could have in hand
        games = []
        for card in players[1].deck:
            new_game = copy.deepcopy(simulated_game)
            new_card = next((c for c in new_game.players[1].deck if c.name == card.name), None)
            new_game.players[1].hand = [new_card]
            new_game.players[1].deck.remove(new_card)
            games.append(new_game)
        return games

    def choose(self, name, choice_list, known_state: 'KnownGameState'):
        if name != "PlayCard" and name != "PlayFirst" and name != "PlaySecond":
            return random.choice(choice_list)

        # Create new games based on known_state
        games = self.create_possible_games(known_state)

        # For each possible choice, evaluate the resulting game states
        best_choice = None
        best_score = float('-inf')
        for choice in choice_list:
            total_score = 0.0
            for g in games:
                game = copy.deepcopy(g)

                # Simulate playing the chosen card
                chosen_card = next((c for c in game.players[0].hand if c.name == choice.name), None)
                encounter = game.get_encounter(game.current_encounter)
                encounter.cards[0] = chosen_card
                game.players[0].hand.remove(chosen_card)

                # Let the opponent play a random card
                opponent_choice = game.players[1].hand[0]
                encounter.cards[1] = opponent_choice
                game.players[1].hand.remove(opponent_choice)

                # Resolve the encounter
                sigil = encounter.get_sigil(game.drawwinner)
                if sigil == -1:
                    game.print("Not possible to evaluate sigil.")
                elif sigil == 0:
                    game.print("Both players played cards with equal influence. No sigils awarded.")
                elif sigil == 1:
                    opponent_choice.effect(game, game.players[1].id)
                else:
                    choice.effect(game, game.players[0].id)

                # Evaluate the game state after this round
                score = self.evaluate_game_state(game)
                total_score += score

            average_score = total_score / len(games) if games else 0
            if average_score > best_score:
                best_score = average_score
                best_choice = choice

        # Use known_state to make a more informed decision
        return best_choice