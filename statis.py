import statistics
import time
from functools import partial
from functools import wraps
from itertools import chain
from itertools import product
from multiprocessing.pool import Pool
from pprint import pformat
from random import choices

from public.main import NUMS
from public.main import SIGN_COMB
from public.main import calculate_permutations


SIGN_COMBS = {k: [list(x) for x in v] for k, v in SIGN_COMB.items()}

THRESHOLD = 10.5


def timing(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        print('time:', time.time() - start_time)
        return result

    return wrapper


def get_random_nums():
    return choices(list(NUMS), k=4)


def best(result: dict[float, list[tuple[str, float]]]):
    '''
    取最好的算式
    '''
    return min(result)


def difficulty(result: dict[float, list[tuple[str, float]]], threshold: float):
    '''
    取 差距 <= threshold 的算式取平均差距
    差距越小越容易贏，難度越低
    '''
    cands = [diff for diff in result if diff <= threshold]
    if cands:
        return sum(cands) / len(cands)
    return 0


def stat(
    threshold: float,
    has_sqrt: bool,
    signs: list[str],
    *,
    n: int,
):
    reduce_big, reduce_small = [], []
    for _ in range(n):
        result_big, result_small = calculate_permutations(signs, has_sqrt, get_random_nums())
        reduce_big.extend(result_big)
        reduce_small.extend(result_small)
    return (
        (threshold, has_sqrt, signs),
        statistics.quantiles(reduce_big, n=10),
        statistics.quantiles(reduce_small, n=10),
    )


@timing
def main():
    n = 10**2
    has_sqrts = [
        False,
        # True,
    ]
    thresholds = [
        2,
        5,
        10,
    ]
    sign_combs = list(chain.from_iterable(SIGN_COMBS.values()))
    func = partial(stat, n=n)
    with Pool() as pool:
        result = pool.starmap(
            func,
            product(
                thresholds,
                has_sqrts,
                sign_combs,
            ),
        )
    print(pformat(result))


if __name__ == '__main__':
    main()

'''
沒 r
    1:
        - 拿 `-`
    20:
        - `-*/`
'''
