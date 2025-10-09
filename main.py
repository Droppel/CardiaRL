import typing
from cardiasim.players.randomcpu import RandomCPU
from cardiasim.players.human import Human
from cardiasim.players.cpualwayshighest import CPUAlwaysHighest
from cardiasim.players.cpualwayslowest import CPUAlwaysLowest
from cardiasim.players.handcrafted import HandCrafted
from cardiasim.players.handcraftedprev import HandCraftedPrev
from cardiasim.game import Game
import cProfile

def run_game(player_class_1, player_class_2, render=False):
    players = [
        player_class_1(player_class_1.__name__, 0),
        player_class_2(player_class_2.__name__, 1)
    ]
    game = Game(players, render=False)
    done = -1
    while done == -1:
        done, known_state = game.turn()  # Start the game

    return done

def run_2p_evaluation(episodes: int, player1_class: typing.Type, player2_class: typing.Type):
    player1_wins, player2_wins, draws = 0, 0, 0
    for episode in range(episodes):
        result = run_game(player1_class, player2_class, render=False)
        if result == 0:
            draws += 1
        elif result == 1:
            player1_wins += 1
        else:
            player2_wins += 1

    return player1_wins, player2_wins, draws

def main():
    episodes = 500
    player_classes = [CPUAlwaysHighest, HandCrafted, HandCraftedPrev]

    results = {}

    for i, player1 in enumerate(player_classes):
        for j in range(i):
            player2 = player_classes[j]
            print(f"Evaluating {player1.__name__} vs {player2.__name__} for {episodes} episodes.")
            player1_wins, player2_wins, draws = run_2p_evaluation(episodes, player1, player2)
            results[(player1.__name__, player2.__name__)] = (player1_wins, player2_wins, draws)

    print(f"--- Final Results ---")
    header = "           "
    for player in player_classes:
        header += f"{player.__name__:>20}"
    print(header)
    for player1 in player_classes:
        row = f"{player1.__name__:<25} "
        for player2 in player_classes:
            p1_wins, p2_wins, draws = results.get((player1.__name__, player2.__name__), (-1, -1, -1))
            if p1_wins == -1:
                row += f"{'-':<14} "
            else:
                row += f"{p1_wins}-{p2_wins}-{draws:<14}"
        print(row)

if __name__ == "__main__":
    main()
    # cProfile.run("main()", "profiling_results.prof")