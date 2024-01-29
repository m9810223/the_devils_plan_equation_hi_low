'''
# Rules

0~10(x4): 44
√*(x4): 8

total: 52

拿到√: 多領一張數字
拿到*: 丟掉 + 或 - 或 *

第一輪下注：有三張數字時

# Analyze

- 一定是 4 個數字
- 一定有 /, 而 *, +, - 三個符號選兩個
- sqrt 隨機

## Combinations and Permutations

- *+/
    - +(*/)
        - _*_/_+_
        - _/_*_+_
        - _+_*_/_
        - _+_/_*_
    - (*)+(/)
        - _*_+_/_
        - _/_+_*_
- *-/
    - (*/)-
        - _*_/_-_
        - _/_*_-_
    - -(*/)
        - _-_*_/_
        - _-_/_*_
    - (*)-(/)
        - _*_-_/_
    - (/)-(*)
        - _/_-_*_
- +-/
    - (/+)-
        - _/_+_-_
        - _/_-_+_
        - _+_/_-_
        - _-_+_/_
    - +-(/)
        - _+_-_/_
        - _-_/_+_
'''


import json
import logging
import typing as t
from itertools import chain
from itertools import permutations
from itertools import product
from itertools import takewhile
from itertools import zip_longest
from math import sqrt
from pprint import pformat


logger = logging.getLogger(__name__)

TARGET_BIG, TARGET_SMALL = 20, 1
NUMS = [str(i) for i in range(11)]


SIGNS = ['*', '+', '-', '/']
SQRT = 'r'
SIGN_COMB = {
    '*+/': ['*/+', '*+/'],
    '*-/': ['*/-', '-*/', '*-/', '/-*'],
    '+-/': ['/+-', '+-/'],
}


def str_sqrt(n: t.Union[int, str]):
    return str(sqrt(float(n)))


def format_float(f: float, *, precision: t.Optional[int] = None):
    if isinstance(f, int):
        return f
    if f.is_integer():
        return int(f)
    if precision is None:
        return f
    return round(f, precision)  # just ok


def calculate(signs: str, nums: tuple[str, ...]):
    calculation = ' '.join(takewhile(bool, chain.from_iterable(zip_longest(nums, signs))))
    result = eval(calculation)
    return calculation, result


def calculate_permutations(signs: list[str], has_sqrt: bool, nums: list[str]):
    # [validation]
    if (
        set(signs) > set(SIGNS)
        or set(nums) > set(NUMS)
        or len(nums) != 4
        or len(signs) != 3
        or '/' not in signs
    ):
        raise ValueError
    # [preparation]
    num_perm = sorted(
        chain.from_iterable(
            permutations(
                str(format_float(sqrt(int(num)), precision=3)) if i == j else num
                for i, num in enumerate(nums)
            )
            for j in range(len(nums))
        )
        if has_sqrt
        else permutations(nums)
    )
    logger.debug('perm_nums:\n' + pformat(num_perm))
    # [calculation]
    # {diff: set((calculation, result,), ...), ...}
    bigs: dict[float, set[tuple[str, float]]] = {}
    smalls: dict[float, set[tuple[str, float]]] = {}
    # TODO: remove same num perms
    for s, n in product(chain(SIGN_COMB[''.join(sorted(signs))]), num_perm):
        try:
            calculation, result = calculate(s, n)
            result = format_float(result, precision=3)
        except ZeroDivisionError:
            continue
        # big
        diff_big = format_float(abs(TARGET_BIG - result), precision=3)
        bigs[diff_big] = bigs.get(diff_big, set())
        bigs[diff_big].add((calculation, result))
        # small
        diff_small = format_float(abs(TARGET_SMALL - result), precision=3)
        smalls[diff_small] = smalls.get(diff_small, set())
        smalls[diff_small].add((calculation, result))
    result_big = {k: sorted(v) for k, v in bigs.items()}
    result_small = {k: sorted(v) for k, v in smalls.items()}
    return result_big, result_small


def pick_best_from_each(d: dict[float, list[tuple[str, float]]], *, n: int):
    return sorted((k, sorted(v)[:n]) for k, v in d.items())


def js_api(signs: str, has_sqrt: str, nums: str, m: str, n: str):
    bigs, smalls = calculate_permutations(list(signs), has_sqrt == 'true', nums.split())
    big_list, smalls_list = (
        pick_best_from_each(bigs, n=int(n))[: int(m)],
        pick_best_from_each(smalls, n=int(n))[: int(m)],
    )
    return print(json.dumps({'bigs': big_list, 'smalls': smalls_list}))


def main():
    bigs, smalls = calculate_permutations(list('/*-'), True, [('9'), '6', '10', '4'])
    big_list, smalls_list = pick_best_from_each(bigs, n=1)[:5], pick_best_from_each(smalls, n=1)[:5]
    logger.info('big_list:\n' + pformat(big_list))
    logger.info('smalls_list:\n' + pformat(smalls_list))


if __name__ == '__main__':
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    js_api('*/-', 'true', '10 6 4 9', '5', '1')
    main()
    logger.info(
        pformat(
            json.loads(
                json.dumps(calculate_permutations(list('/*-'), True, [('9'), '6', '10', '4']))
            )
        )
    )
