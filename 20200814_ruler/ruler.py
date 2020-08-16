# https://fivethirtyeight.com/features/are-you-hip-enough-to-be-square/

# Recently, there was an issue with the production of foot-long rulers. It seems that each ruler was accidentally
# sliced at three random points along the ruler, resulting in four pieces. Looking on the bright side, that means
# there are now four times as many rulers -- they just happen to have different lengths.
#
# On average, how long are the pieces that contain the 6-inch mark?

import numpy as np
import time
from typing import List


class Ruler(object):
    def __init__(self, start: float = 0, end: float = 12):
        self.start = start
        self.end = end
        self.length = end - start

    def create_pieces(self, n_slices: int) -> List["Ruler"]:
        slice_points = np.random.uniform(self.start, self.end, n_slices)
        nodes = np.insert(slice_points, 0, self.start)
        nodes = np.append(nodes, self.end)
        nodes = np.sort(nodes)
        return [Ruler(start=nodes[i], end=nodes[i+1]) for i in range(len(nodes) - 1)]

    def contains_point(self, x: float) -> bool:
        return self.start <= x < self.end


def find_piece_that_contains_point(pieces: List[Ruler], x: float) -> Ruler:
    return [p for p in pieces if p.contains_point(x)][0]


def run_simulation(n_trials: int, ruler_length: float, n_slices: int, point: int) -> float:
    lengths = []
    for _ in range(n_trials):
        length = run_one(ruler_length, n_slices, point)
        lengths.append(length)
    return float(np.mean(lengths))


def run_one(ruler_length: float, n_slices: int, point: int) -> float:
    ruler = Ruler(start=0, end=ruler_length)
    pieces = ruler.create_pieces(n_slices=n_slices)
    p = find_piece_that_contains_point(pieces, point)
    return p.length


if __name__ == "__main__":
    np.random.seed(538)
    start_time = time.time()
    avg_length = run_simulation(
        n_trials=1000000,
        ruler_length=12,
        n_slices=3,
        point=6
    )
    print(avg_length)
    print(f"{round(time.time() - start_time, 2)} seconds")

    # result = 5.626762987140483
