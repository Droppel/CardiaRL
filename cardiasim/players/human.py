import typing
from .player import Player
from ..cards import *

class Human(Player):
    def __init__(self, name, id):
        super().__init__(name, id)

    def choose(self, choice_list):
        print("Available choices:")
        for i, choice in enumerate(choice_list):
            print(f"{i + 1}: {choice}")

        choice_index = int(input("Choose an option: ")) - 1
        if 0 <= choice_index < len(choice_list):
            return choice_list[choice_index]
        return choice_list[0]

    def play_card(self) -> Card:
        if self.hand:
            self.print_hand()
            card = None
            cardname = input("Enter card to play:")
            if cardname in [c.name for c in self.hand]:
                card = self.hand[[c.name for c in self.hand].index(cardname)]
            else:
                card = self.hand[0]  # For simplicity, just play the first card in hand
            self.hand.remove(card)
            return card
        else:
            print(f"{self.name} has no cards to play.")
            return None