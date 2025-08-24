import typing
import random
if typing.TYPE_CHECKING:
    from .game import Game, Player, Encounter

class Card():
    def __init__(self):
        self.name = "default"
        self.influence = -1
        self.faction = -1 # -1 Nothing, 0 Green, 1 Yellow, 2 Red, 3 Blue
        pass

    def effect(self, game: 'Game', player_id: 'int'):
        game.print(f"Activate {self.name} effect")

    def __str__(self):
        return self.name

class HiredBlade(Card):
    def __init__(self):
        super().__init__()
        self.name = "Hired Blade"
        self.influence = 1
        self.faction = 0
    
    def effect(self, game: 'Game', player_id: 'int'):
        super().effect(game, player_id)
        current_encounter = game.encounters[game.current_encounter]
        # Discard the played cards
        game.players[0].discard.append(current_encounter.cards[0])
        game.players[1].discard.append(current_encounter.cards[1])
        # Remove the encounter from the game
        game.encounters.remove(current_encounter)
        game.current_encounter -= 1

class VoidmageChoice():
    def __init__(self, encounter, modOrPerm, player):
        self.encounter = encounter
        self.modOrPerm = modOrPerm # True for mod, False for permanent
        self.player = player
    
    def __str__(self):
        return f"Enc {self.encounter}: {'Mod' if self.modOrPerm else 'Perm'} P{self.player}"

class Voidmage(Card):
    def __init__(self):
        super().__init__()
        self.name = "Voidmage"
        self.influence = 2
        self.faction = 1
    
    def effect(self, game: 'Game', player_id: 'int'):
        super().effect(game, player_id)
        options = []
        count = 0
        for enc in game.encounters:
            if enc.permanent[0]:
                options.append(VoidmageChoice(count, False, 0))
            if enc.permanent[1]:
                options.append(VoidmageChoice(count, False, 1))
            if enc.modifiers[0] != 0:
                options.append(VoidmageChoice(count, True, 0))
            if enc.modifiers[1] != 0:
                options.append(VoidmageChoice(count, True, 1))
            count += 1

        if not options:
            return
        choice: VoidmageChoice = game.players[player_id].choose("Voidmage", options, game.get_gamestate())
        encounter = game.encounters[choice.encounter]
        if choice.modOrPerm:
            encounter.modifiers[choice.player] = 0
        else:
            encounter.permanent[choice.player] = False
        game.print(f"Removed {'modifier' if choice.modOrPerm else 'permanent'} from encounter {choice.encounter} for player {choice.player}")

class Surgeon(Card):
    def __init__(self):
        self.name = "Surgeon"
        self.influence = 3
        self.faction = 2
    
    def effect(self, game: 'Game', player_id: 'int'):
        super().effect(game, player_id)
        next_encounter = game.get_encounter(game.current_encounter + 1)
        next_encounter.modifiers[player_id] -= 5

class Mediator(Card):
    def __init__(self):
        self.name = "Mediator"
        self.influence = 4
        self.faction = 3
    
    def effect(self, game: 'Game', player_id: 'int'):
        super().effect(game, player_id)
        game.encounters[game.current_encounter].permanent[player_id] = True

class Saboteur(Card):
    def __init__(self):
        self.name = "Saboteur"
        self.influence = 5
        self.faction = 0
    
    def effect(self, game: 'Game', player_id: 'int'):
        super().effect(game, player_id)
        other_player_id = player_id ^ 1
        for _ in range(min(2, len(game.players[other_player_id].deck))):
            card = game.players[other_player_id].deck.pop() 
            game.players[other_player_id].discard.append(card)
            game.print(f"{game.players[other_player_id].name} discards {card.name} from the top of their deck")

class FortuneTeller(Card):
    def __init__(self):
        self.name = "Fortune Teller"
        self.influence = 6
        self.faction = 1
    
    def effect(self, game: 'Game', player_id: 'int'):
        super().effect(game, player_id)
        other_player_id = player_id ^ 1
        game.playopen[other_player_id] = True

class PalaceGuard(Card):
    def __init__(self):
        self.name = "Palace Guard"
        self.influence = 7
        self.faction = 2
    
    def effect(self, game: 'Game', player_id: 'int'):
        super().effect(game, player_id)
        other_player_id = player_id ^ 1
        other_player = game.players[other_player_id]
        player = game.players[player_id]
        
        options = [0, 1, 2, 3]
        choice = player.choose("PalaceGuardFaction", options, game.get_gamestate())
        
        options = [card for card in other_player.hand if card.faction == choice]

        hasdiscarded = False
        # If player has cards matching the faction give option to discard one
        if options:
            options.append(None) # Option to not discard
            discard_choice = other_player.choose("PalaceGuardDiscard", options, game.get_gamestate())
            if discard_choice:
                other_player.hand.remove(discard_choice)
                other_player.discard.append(discard_choice)
                game.print(f"{other_player.name} discards {discard_choice.name}")
                hasdiscarded = True
        
        if not hasdiscarded:
            game.print(f"{other_player.name} does not discard a card.")
            game.encounters[game.current_encounter].modifiers[player_id] += 7

class Judge(Card):
    def __init__(self):
        self.name = "Judge"
        self.influence = 8
        self.faction = 3
    
    def effect(self, game: 'Game', player_id: 'int'):
        super().effect(game, player_id)
        encounter = game.encounters[game.current_encounter]
        encounter.permanent[player_id] = True

class Ambusher(Card):
    def __init__(self):
        self.name = "Ambusher"
        self.influence = 9
        self.faction = 0
    
    def effect(self, game: 'Game', player_id: 'int'):
        super().effect(game, player_id)
        options = [0, 1, 2, 3]
        player = game.players[player_id]
        choice = player.choose("Ambusher", options, game.get_gamestate())
        game.print(f"{player.name} chooses faction {choice} for opponent to discard")

        other_player_id = player_id ^ 1
        other_player = game.players[other_player_id]

        for card in other_player.hand:
            if card.faction == choice:
                other_player.hand.remove(card)
                other_player.discard.append(card)
                game.print(f"{other_player.name} discards {card.name}")

class Puppeteer(Card):
    def __init__(self):
        self.name = "Puppeteer"
        self.influence = 10
        self.faction = 1
    
    def effect(self, game: 'Game', player_id: 'int'):
        super().effect(game, player_id)
        encounter = game.encounters[game.current_encounter]
        player = game.players[player_id]
        other_player_id = player_id ^ 1
        other_player = game.players[other_player_id]
        if not other_player.hand:
            game.winner = player_id
            return
        other_player.discard.append(encounter.cards[other_player_id])
        encounter.cards[other_player_id] = None
        newcard = random.choice(other_player.hand)
        encounter.cards[other_player_id] = newcard
        other_player.hand.remove(newcard)

class Clockmaker(Card):
    def __init__(self):
        self.name = "Clockmaker"
        self.influence = 11
        self.faction = 2
    
    def effect(self, game: 'Game', player_id: 'int'):
        super().effect(game, player_id)
        prev_encounter = game.encounters[game.current_encounter - 1] if game.current_encounter > 0 else None
        if prev_encounter:
            prev_encounter.modifiers[player_id] += 3

        next_encounter = game.get_encounter(game.current_encounter + 1)
        next_encounter.modifiers[player_id] += 3

class Treasurer(Card):
    def __init__(self):
        self.name = "Treasurer"
        self.influence = 12
        self.faction = 3
    
    def effect(self, game: 'Game', player_id: 'int'):
        super().effect(game, player_id)
        encounter = game.encounters[game.current_encounter]
        encounter.permanent[player_id] = True

class SwampGuardian(Card):
    def __init__(self):
        self.name = "Swamp Guardian"
        self.influence = 13
        self.faction = 0
    
    def effect(self, game: 'Game', player_id: 'int'):
        super().effect(game, player_id)
        player = game.players[player_id]
        other_player_id = player_id ^ 1
        other_player = game.players[other_player_id]
        # Get available encounters
        options = range(0, game.current_encounter-1)
        if not options:
            return
        choice = player.choose("SwampGuardian", options, game.get_gamestate())
        encounter: Encounter = game.encounters[choice]
        # Give player card back, discard other player's card
        player.hand.append(encounter.cards[player_id])
        other_player.discard.append(encounter.cards[other_player_id])
        # Remove the encounter from the game
        game.encounters.remove(encounter)
        game.current_encounter -= 1

class Magistra(Card):
    def __init__(self):
        self.name = "Magistra"
        self.influence = 14
        self.faction = 1
    
    def effect(self, game: 'Game', player_id: 'int'):
        super().effect(game, player_id)
        mininfl = game.encounters[game.current_encounter].cards[player_id].influence
        options: typing.List[Card] = []
        option_names: typing.List[str] = []
        for enc in game.encounters:
            if enc.cards[player_id].influence > mininfl:
                options.append(enc.cards[player_id])
                option_names.append(enc.cards[player_id].name)
        if not options:
            return
        player = game.players[player_id]
        choice = player.choose("Magistra", option_names, game.get_gamestate())
        if choice:
            card = options[option_names.index(choice)]
            card.effect(game, player_id)

class InventorChoice():
    def __init__(self, enc, player_id):
        self.encounter: Encounter = enc
        self.player_id: int = player_id
    
    def __str__(self):
        return f"Enc {self.encounter} P{self.player_id}"

class Inventor(Card):
    def __init__(self):
        self.name = "Inventor"
        self.influence = 15
        self.faction = 2
    
    def effect(self, game: 'Game', player_id: 'int'):
        super().effect(game, player_id)
        player = game.players[player_id]
        other_player_id = player_id ^ 1

        options: typing.List[InventorChoice] = []
        for enc in game.encounters:
            options.append(InventorChoice(enc, player_id))
            options.append(InventorChoice(enc, other_player_id))

        inc_choice: InventorChoice = player.choose("InventorIncrease", options, game.get_gamestate())
        inc_choice.encounter.modifiers[inc_choice.player_id] += 3

        dec_choice: InventorChoice = player.choose("InventorDecrease", options, game.get_gamestate())
        dec_choice.encounter.modifiers[dec_choice.player_id] -= 3

class Djinn(Card):
    def __init__(self):
        self.name = "Djinn"
        self.influence = 16
        self.faction = 3

    def effect(self, game: 'Game', player_id: 'int'):
        super().effect(game, player_id)
        game.winner = player_id