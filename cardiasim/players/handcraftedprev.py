import typing
import random
from .player import Player
from ..cards import Card
if typing.TYPE_CHECKING:
    from ..game import KnownGameState

class HandCraftedPrev(Player):
    def __init__(self, name, id):
        super().__init__(name, id)

    def choose(self, name, choice_list, known_state: 'KnownGameState'):
        if name == "PlayCard":
            highest_influence_card = max(choice_list, key=lambda card: card.influence)
            return highest_influence_card
        elif name == "PlayFirst":
            highest_influence_card = max(choice_list, key=lambda card: card.influence)
            return highest_influence_card
        elif name == "PlaySecond":
            highest_influence_card = max(choice_list, key=lambda card: card.influence)
            return highest_influence_card
        else:
            return random.choice(choice_list)
        # Use known_state to make a more informed decision