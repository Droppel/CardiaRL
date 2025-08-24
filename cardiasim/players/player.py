
import typing
import random

from ..cards import *

class Player():
    deck:  typing.List[Card]
    hand: typing.List[Card]
    discard: typing.List[Card] 
    name: str
    id: int

    def __init__(self, name, id):
        self.name = name
        self.id = id
        self.hand = []
        self.deck = []
        self.discard = []
        self.setup_deck()
        self.draw_card(5)

    def setup_deck(self):
        # Dynamically import all Card subclasses from py
        self.deck = [HiredBlade(), Voidmage(), Surgeon(), Mediator(), Saboteur(),
                     FortuneTeller(), PalaceGuard(), Judge(), Ambusher(), Puppeteer(),
                     Clockmaker(), Treasurer(), SwampGuardian(), Magistra(), Inventor(),
                     Djinn()]
        random.shuffle(self.deck)

    def draw_card(self, count = 1):
        for _ in range(count):
            if len(self.deck) > 0:
                card = self.deck.pop(0)
                self.hand.append(card)

    def print_hand(self):
        print(f"{self.name}'s hand:")
        for card in self.hand:
            print(f"- {card.name}")

    def choose(self, name, choice_list):
        pass