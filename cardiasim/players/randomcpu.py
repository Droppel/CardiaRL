import typing
import random
from .player import Player
from ..cards import Card

class RandomCPU(Player):
    def __init__(self, name, id):
        super().__init__(name, id)

    def choose(self, name, choice_list):
        return random.choice(choice_list)