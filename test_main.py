import pytest

from public.main import calculate_all
from public.main import calculate_one
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
def test_calculate_one(signs: str, nums: tuple[str, ...], expected: float):
    assert calculate_one(tuple(signs), nums)[0] == expected


@pytest.mark.parametrize(
    'signs, nums, expected',
    [
        # https://www.netflix.com/watch/81659323?trackId=200257859 -> 38:36
        ('*/-r', ('10', '6', ('4'), '9'), 21),
        ('/*-r', (('9'), '6', '10', '4'), 1),
        ('/+-', ('10', '5', '0', '1'), 1),
        ('/+-r', (('4'), '7', '9', '8'), 1.286),
        ('+-/', ('10', '8', '1', '2'), 17.5),
        ('/+-', ('5', '3', '2', '3'), 0.667),
        ('*/-', ('8', '3', '1', '4'), 20),
        ('+-/', ('10', '7', '2', '6'), 16.667),
    ],
)
def test_main(signs: str, nums: tuple[str, ...], expected: float):
    bigs, smalls = calculate_all(list(signs), list(nums))
    big, small = sorted(bigs.items())[0], sorted(smalls.items())[0]
    assert expected == big[1] if big < small else small[1]
