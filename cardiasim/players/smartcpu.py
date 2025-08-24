import typing
import random
from .player import Player
from ..cards import Card
if typing.TYPE_CHECKING:
    from ..game import KnownGameState

class RandomCPU(Player):
    def __init__(self, name, id):
        super().__init__(name, id)

    def evaluate_state(self, game_state) -> float:
        # Simple evaluation: random value for now
        return random.random()

    def choose(self, choice_list, known_state: 'KnownGameState'):
        # Use known_state to make a more informed decision
        return random.choice(choice_list)