import typing
from .player import Player
from ..cards import *

class Human(Player):
    def __init__(self, name, id):
        super().__init__(name, id)

    def choose(self, name, choice_list):
        print(f"Available choices for {name}:")
        for i, choice in enumerate(choice_list):
            print(f"{i + 1}: {choice}")

        choice_index = int(input("Choose an option: ")) - 1
        if 0 <= choice_index < len(choice_list):
            return choice_list[choice_index]
        return choice_list[0]