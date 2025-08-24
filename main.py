import typing
from cardiasim.players.randomcpu import RandomCPU
from cardiasim.players.human import Human
from cardiasim.players.cpualwayshighest import CPUAlwaysHighest
from cardiasim.game import Game

if __name__ == "__main__":
    episodes = 100
    player1_wins = 0
    player2_wins = 0
    draws = 0
    for episode in range(episodes):
        players = [RandomCPU("Cpu1", 0), CPUAlwaysHighest("Cpu2", 1)]
        game = Game(players, render=False)
        done = -1
        while done == -1:
            done = game.turn()  # Start the game

        if done == 0:
            draws += 1
        elif done == 1:
            player1_wins += 1
        elif done == 2:
            player2_wins += 1

    print(f"--- Final Results ---")
    print(f"Results after {episode + 1} episodes:")
    print(f"Player 1 wins: {player1_wins}")
    print(f"Player 2 wins: {player2_wins}")
    print(f"Draws: {draws}")