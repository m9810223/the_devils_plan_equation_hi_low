import pytest

from public.main import calculate
from public.main import calculate_permutations
from public.main import format_float
from public.main import str_sqrt


@pytest.mark.parametrize(
    'signs, nums, expected',
    [
        # https://www.netflix.com/watch/81659323?trackId=200257859
        # 29:12
        ('*/-', ('10', '6', str_sqrt('4'), '9'), 21),
        ('/*-', (str_sqrt('9'), '6', '10', '4'), 1),
        ('/+-', ('10', '5', '0', '1'), 1),
        ('/+-', (str_sqrt('4'), '7', '9', '8'), 1.286),
        ('+-/', ('10', '8', '1', '2'), 17.5),
        ('/+-', ('5', '3', '2', '3'), 0.667),
        ('*/-', ('8', '3', '1', '4'), 20),
        ('+-/', ('10', '7', '2', '6'), 16.667),
    ],
)
def test_calculate(signs: str, nums: tuple[str, ...], expected: float):
    calculation, result = calculate(signs, nums)
    assert format_float(result, precision=3) == expected


@pytest.mark.parametrize(
    'signs, has_sqrt, nums, expected_big, expected_small',
    [
        # https://www.netflix.com/watch/81659323?trackId=200257859 -> 38:36
        ('*/-', True, ('10', '6', '4', '9'), 20.051, 1),
        ('/*-', True, ('9', '6', '10', '4'), 20.051, 1),
        ('/+-', False, ('10', '5', '0', '1'), 15, 1),
        ('/+-', True, ('4', '7', '9', '8'), 16.714, 1.222),
        ('+-/', False, ('10', '8', '1', '2'), 17.5, 1.75),
        ('/+-', False, ('5', '3', '2', '3'), 7.333, 0.667),
        ('*/-', False, ('8', '3', '1', '4'), 20, 1),
        ('+-/', False, ('10', '7', '2', '6'), 16.667, 1.2),
    ],
)
def test_calculate_permutations(
    signs: str, has_sqrt: bool, nums: tuple[str, ...], expected_big: float, expected_small: float
):
    bigs, smalls = calculate_permutations(list(signs), has_sqrt, list(nums))
    big, small = min(bigs.items()), min(smalls.items())
    result_big, result_small = big[1][0][1], small[1][0][1]
    assert expected_big == result_big
    assert expected_small == result_small
