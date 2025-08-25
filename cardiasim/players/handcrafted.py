import typing
import random
from .player import Player
from ..cards import Card
if typing.TYPE_CHECKING:
    from ..game import KnownGameState

class HandCrafted(Player):
    def __init__(self, name, id):
        super().__init__(name, id)

    def choose(self, name, choice_list, known_state: 'KnownGameState'):
        if name == "SwampGuardian":
            # If possible choose a loosing encounter
            looser_number = 2 if self.id == 0 else 1
            for i, enc in enumerate(known_state.encounters[:-1]):
                if enc.get_sigil(known_state.drawwinner) == looser_number:
                    return choice_list[i]
            # If not possible choose a drawing encounter
            for i, enc in enumerate(known_state.encounters[:-1]):
                if enc.get_sigil(known_state.drawwinner) == 0:
                    return choice_list[i]
            # Otherwise choose randomly
            return random.choice(choice_list)
        elif name == "PlayCard":
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