import typing
from cardiasim.players.randomcpu import RandomCPU
from cardiasim.players.human import Human
from cardiasim.game import Game

if __name__ == "__main__":
    players = [RandomCPU("Cpu", 0), Human("Human", 1)]
    game = Game(players)
    game.turn()  # Start the game
