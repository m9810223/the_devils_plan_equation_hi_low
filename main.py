'''
0~10(x4): 44
√*(x4): 8

total: 52

拿到√: 多領一張數字
拿到*: 丟掉 + 或 - 或 *

第一輪下注：有三張數字時
'''
import logging
from itertools import chain
from itertools import permutations
from itertools import product
from itertools import takewhile
from itertools import zip_longest
from math import sqrt


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


def calculate_one(signs: tuple[str, ...], nums: tuple[str, ...]):
    calculation = ' '.join(takewhile(bool, chain.from_iterable(zip_longest(nums, signs))))
    result = float(eval(calculation))
    if result.is_integer():
        result = int(result)
    else:
        result = round(result, 3)  # just ok
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
    bigs: list[tuple[float, float, str]] = []
    smalls: list[tuple[float, float, str]] = []
    for s, n in product(perm_signs, perm_nums):
        try:
            result, calculation = calculate_one(s, n)
        except ZeroDivisionError:
            continue
        bigs.append((abs(TARGET_BIG - result), result, calculation))
        smalls.append((abs(TARGET_SMALL - result), result, calculation))
    bigs.sort()
    smalls.sort()
    return bigs, smalls


if __name__ == '__main__':
    logging.basicConfig(format='%(message)s', level=logging.DEBUG)
    print(calculate_all(['+', '-', '/'], ['1', '2', '3', '4']))
