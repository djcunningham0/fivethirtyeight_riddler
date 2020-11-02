# https://fivethirtyeight.com/features/beware-the-hot-pumpkin/

# Instead of playing hot potato, you and 60 of your closest friends decide to
# play a socially distanced game of hot pumpkin.
#
# Before the game starts, you all sit in a circle and agree on a positive
# integer N. Once the number has been chosen, you (the leader of the group)
# start the game by counting “1” and passing the pumpkin to the person sitting
# directly to your left. She then declares “2” and passes the pumpkin one space
# to her left. This continues with each player saying the next number in the
# sequence, wrapping around the circle as many times as necessary, until the
# group has collectively counted up to N. At that point, the player who counted
# “N” is eliminated, and the player directly to his or her left starts the next
# round, again proceeding to the same value of N. The game continues until just
# one player remains, who is declared the victor.
#
# In the game’s first round, the player 18 spaces to your left is the first to
# be eliminated. Ricky, the next player in the sequence, begins the next round.
# The second round sees the elimination of the player 31 spaces to Ricky’s left.
# Zach begins the third round, only to find himself eliminated in a cruel twist
# of fate. (Woe is Zach.)
#
# What was the smallest value of N the group could have used for this game?
#
# Extra credit: Suppose the players were numbered from 1 to 61, with you as
# Player No. 1, the player to your left as Player No. 2 and so on. Which player
# won the game?
#
# Extra extra credit: What’s the smallest N that would have made you the winner?

import numpy as np
from typing import List, Tuple


def simulate_game(n_players: int, n: int, verbose: bool = False) -> int:
    players = _initialize_players(n_players)
    current_index = 0

    for _ in range(n_players - 1):
        current_index, eliminated_player = process_one_round(players, current_index, n)
        if verbose:
            print(f"round of {n_players}: player {eliminated_player} eliminated (index {current_index})")
        players = np.delete(players, current_index)
        n_players -= 1

    return players.tolist()[0]


def process_one_round(players: List[int], current_index: int, n: int) -> Tuple[int, int]:
    n_players = len(players)
    new_index = (current_index + n - 1) % n_players
    eliminated_player = players[new_index]
    return new_index, eliminated_player


def solve_for_first_eliminations(n_players: int, first_eliminations: List[int], max_n: int = int(1e6)) -> int:
    _validate_first_eliminations(n_players, first_eliminations)
    players = _initialize_players(n_players)

    n = 1
    while n <= max_n:
        result = _test_n_for_first_eliminations(n, players, first_eliminations)
        if result:
            return n
        n += 1

    raise ValueError(f"reached max_n={max_n} before finding solution")


def solve_for_winner(n_players: int, winner: int, max_n: int = int(1e6)) -> int:
    if winner > n_players:
        raise ValueError("winner cannot be greater than n_players")

    n = 1
    while n <= max_n:
        if simulate_game(n_players=n_players, n=n) == winner:
            return n
        n += 1

    raise ValueError(f"reached max_n={max_n} before finding solution")


def _initialize_players(n_players: int) -> np.ndarray:
    return np.array(range(n_players)) + 1


def _test_n_for_first_eliminations(n: int, players: np.ndarray, first_eliminations: List[int]) -> bool:
    n_players = len(players)
    current_index = 0
    for i in range(len(first_eliminations)):
        current_index, eliminated_player = process_one_round(players=players, current_index=current_index, n=n)
        # if eliminated player is not what we're looking for, stop early
        if eliminated_player != first_eliminations[i]:
            return False
        # otherwise continue simulating game
        players = np.delete(players, current_index)
        n_players -= 1

    # if we reached this point, we found the solution
    return True


def _validate_first_eliminations(n_players: int, first_eliminations: List[int]):
    if any(x > n_players for x in first_eliminations):
        raise ValueError("one of values in first_eliminations is larger than n_players")
    if any(x < 1 for x in first_eliminations):
        raise ValueError("one of values in first_eliminations is less than 1")
    if len(set(first_eliminations)) < len(first_eliminations):
        raise ValueError("values in first_eliminations are not unique")


# main question
n = solve_for_first_eliminations(n_players=61, first_eliminations=[19, 51, 52])
print(f"main answer:\nN = {n}")

# extra credit
winner = simulate_game(n_players=61, n=n, verbose=False)
print(f"\nextra credit:\nwinner = {winner}")

# extra extra credit
n = solve_for_winner(n_players=61, winner=1)
print(f"\nextra extra credit:\nN = {n}")


"""
OUTPUT:

main answer:
N = 136232

extra credit:
winner = 58

extra extra credit:
N = 140
"""
