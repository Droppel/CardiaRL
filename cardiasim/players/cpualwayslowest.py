import typing
import random
from .player import Player
from ..cards import Card
if typing.TYPE_CHECKING:
    from ..game import KnownGameState

class CPUAlwaysLowest(Player):
    def __init__(self, name, id):
        super().__init__(name, id)

    def evaluate_state(self, game_state) -> float:
        # Simple evaluation: random value for now
        return random.random()

    def choose(self, name, choice_list, known_state: 'KnownGameState'):
        if name != "PlayCard" and name != "PlayFirst" and name != "PlaySecond":
            return random.choice(choice_list)
        # Use known_state to make a more informed decision
        lowest_influence_card = min(choice_list, key=lambda card: card.influence)
        return lowest_influence_card