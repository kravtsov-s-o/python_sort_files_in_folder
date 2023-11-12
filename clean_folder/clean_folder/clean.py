import sys
import time
from partials.Sorting import Sorting


def init():
    path = sys.argv[1]
    print(f"Start in {path}")

    sorting = Sorting(path)
    sorting.sort()


if __name__ == '__main__':
    start = time.perf_counter()
    init()
    finish = time.perf_counter()
    print(f'Time spent: {finish - start}')
