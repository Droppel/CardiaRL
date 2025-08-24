import typing
import random
from .player import Player
from ..cards import Card

class RandomCPU(Player):
    def __init__(self, name, id):
        super().__init__(name, id)

    def choose(self, choice_list):
        return random.choice(choice_list)

    def play_card(self) -> Card:
        if self.hand:
            card = random.choice(self.hand)
            self.hand.remove(card)
            return card
        else:
            print(f"{self.name} has no cards to play.")
            return None