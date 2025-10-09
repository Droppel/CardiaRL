import typing
import random
from .player import Player
from ..cards import Card
if typing.TYPE_CHECKING:
    from ..game import KnownGameState

class HandCrafted(Player):
    def __init__(self, name, id):
        super().__init__(name, id)

    def base_play_card(self, choice_list, known_state: 'KnownGameState'):
        # Evaluate cards in hand
        evals = []
        for card in choice_list:
            eval = 0
            if card.name == "Mediator":
                if known_state.drawwinner == self.id +1:
                    eval += 2
                elif known_state.drawwinner != 0:
                    eval -= 2
            evals.append(eval)

        max_eval = max(evals)
        eval_ties = [card for card, eval in zip(choice_list, evals) if eval == max_eval]

        return max(eval_ties, key=lambda card: card.influence)

    def choose(self, name, choice_list, known_state: 'KnownGameState'):
        if name == "Ambusher":
            faction_counts = [0,0,0,0]
            for enc in known_state.encounters:
                if enc.cards[self.id ^ 1] is not None:
                    faction_counts[enc.cards[self.id ^ 1].faction] += 1
            for card in known_state.discards[self.id ^ 1]:
                faction_counts[card.faction] += 1
            least_common_faction = faction_counts.index(min(faction_counts))
            return least_common_faction
        elif name == "SwampGuardian":
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
        elif name == "PlayCard" or name == "PlayFirst" or name == "PlaySecond":
            return self.base_play_card(choice_list, known_state)
        elif name == "PlayFirst":
            return self.base_play_card(choice_list, known_state)
        elif name == "PlaySecond":
            return self.base_play_card(choice_list, known_state)
        else:
            return random.choice(choice_list)
        # Use known_state to make a more informed decision