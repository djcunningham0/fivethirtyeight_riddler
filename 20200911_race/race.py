# https://fivethirtyeight.com/features/can-you-reach-the-summit-first/
#
# For every mountain in the Tour de FiveThirtyEight, the first few riders to
# reach the summit are awarded points. The rider with the most such points at
# the end of the Tour is named “King of the Mountains” and gets to wear a
# special polka dot jersey.
#
# At the moment, you are racing against three other riders up one of the
# mountains. The first rider over the top gets 5 points, the second rider gets
# 3, the third rider gets 2, and the fourth rider gets 1.
#
# All four of you are of equal ability — that is, under normal circumstances,
# you all have an equal chance of reaching the summit first. But there’s a
# catch — two of your competitors are on the same team. Teammates are able to
# work together, drafting and setting a tempo up the mountain. Whichever
# teammate happens to be slower on the climb will get a boost from their faster
# teammate, and the two of them will both reach the summit at the faster
# teammate’s time.
#
# As a lone rider, the odds may be stacked against you. In your quest for the
# polka dot jersey, how many points can you expect to win on this mountain, on
# average?

import numpy as np

np.random.seed(0)

N_SIMULATIONS = 1e6

score_map = {
    1: 5,
    2: 3,
    3: 2,
    4: 1
}


def run_simulation(n: int) -> float:
    """Simulate n races and report the average score"""
    scores = []
    for _ in range(int(n)):
        scores.append(simulate_one_race())

    return np.mean(scores)


def simulate_one_race() -> int:
    """Simulate a single race and report your score"""
    # each racer has equal chance of finishing 1st, 2nd, 3rd, 4th
    results = np.random.permutation([1, 2, 3, 4])

    # assume the teammates are the last two indices -- set to better result
    teammate_finish = results[-2:].min()
    results[-2] = teammate_finish
    results[-1] = teammate_finish

    # assume you are the first index and calculate points
    your_score = get_racer_score(results, racer_index=0)
    return your_score


def get_racer_score(results: np.array, racer_index: int) -> int:
    racer_result = get_racer_result(results=results, racer_index=racer_index)
    return score_map[racer_result]


def get_racer_result(results: np.array, racer_index: int) -> int:
    return np.argsort(results).tolist().index(racer_index) + 1


if __name__ == "__main__":
    avg_score = run_simulation(n=N_SIMULATIONS)
    print(avg_score)

    # result: 2.417516
