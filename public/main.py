'''
0~10(x4): 44
√*(x4): 8

total: 52

拿到√: 多領一張數字
拿到*: 丟掉 + 或 - 或 *

第一輪下注：有三張數字時
'''


import json
import logging
from itertools import chain
from itertools import permutations
from itertools import product
from itertools import takewhile
from itertools import zip_longest
from math import sqrt
from pprint import pformat


logger = logging.getLogger(__name__)

TARGET_BIG, TARGET_SMALL = 20, 1


class DefaultSign:
    div = '/'  # 不能丟
    add = '+'
    sub = '-'


class SpecialSign:
    mul = '*'
    rt = 'r'


SIGNS = {DefaultSign.div, DefaultSign.add, DefaultSign.sub, SpecialSign.mul, SpecialSign.rt}
NUMS = {str(i) for i in range(11)}


def str_sqrt(n: str):
    return str(sqrt(int(n)))


def _format_float(f: float):
    return int(f) if f.is_integer() else round(f, 3)  # just ok


def calculate_one(signs: tuple[str, ...], nums: tuple[str, ...]):
    calculation = ' '.join(takewhile(bool, chain.from_iterable(zip_longest(nums, signs))))
    result = _format_float(float(eval(calculation)))
    return result, calculation


def calculate_all(signs: list[str], nums: list[str]):
    # [validation]
    if set(signs) > SIGNS or set(nums) > NUMS:
        raise ValueError
    if len(nums) != 4:
        raise ValueError
    if SpecialSign.rt in signs:
        if len(signs) != 4:
            raise ValueError
    elif len(signs) != 3:
        raise ValueError
    # [preparation]
    perm_signs = permutations(x for x in signs if x != SpecialSign.rt)
    perm_nums = (
        chain.from_iterable(
            permutations(str_sqrt(n) if j == i else n for j, n in enumerate(nums))
            for i in range(len(nums))
        )
        if SpecialSign.rt in signs
        else permutations(nums)
    )
    # [calculation]
    bigs: dict[float, list[tuple[float, str]]] = {}
    smalls: dict[float, list[tuple[float, str]]] = {}
    for s, n in product(perm_signs, perm_nums):
        try:
            result, calculation = calculate_one(s, n)
        except ZeroDivisionError:
            continue
        _key_big = _format_float(float(abs(TARGET_BIG - result)))
        bigs[_key_big] = bigs.get(_key_big, [])
        bigs[_key_big].append((result, calculation))
        _key_small = _format_float(float(abs(TARGET_SMALL - result)))
        smalls[_key_small] = bigs.get(_key_big, [])
        smalls[_key_small].append((result, calculation))
    return bigs, smalls


def pick_one_calculation(d: dict[float, list[tuple[float, str]]]):
    return sorted((k, *v[0]) for k, v in d.items())


def wasm(*args, **kwargs):
    return json.dumps(calculate_all(*args, **kwargs))


def main():
    bigs, smalls = calculate_all(list('*/-r'), ['10', '6', ('4'), '9'])
    big_list, smalls_list = pick_one_calculation(bigs), pick_one_calculation(smalls)
    print(pformat(big_list[:5]))
    print(pformat(smalls_list[:5]))
    return bigs


if __name__ == '__main__':
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)
    main()
