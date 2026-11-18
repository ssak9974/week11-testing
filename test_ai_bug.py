
import pytest

from bug3_logic import find_max, count_pass


# -------------------------
# find_max 테스트
# -------------------------

def test_find_max_normal():
    assert find_max([70, 85, 60, 95]) == 95


def test_find_max_increasing():
    assert find_max([10, 20, 30]) == 30


def test_find_max_decreasing():
    assert find_max([95, 85, 70, 60]) == 95


def test_find_max_one_value():
    assert find_max([50]) == 50


def test_find_max_empty():
    with pytest.raises(IndexError):
        find_max([])


# -------------------------
# count_pass 테스트
# -------------------------

def test_count_pass_normal():
    assert count_pass([70, 85, 95]) == 3


def test_count_pass_boundary():
    assert count_pass([60, 60, 59]) == 2


def test_count_pass_all_fail():
    assert count_pass([10, 20, 30]) == 0


def test_count_pass_all_pass():
    assert count_pass([70, 80, 90]) == 3


def test_count_pass_custom_cutoff():
    assert count_pass([70, 80, 90], cutoff=80) == 2


def test_count_pass_empty():
    assert count_pass([]) == 0


def test_count_pass_boundary_custom():
    assert count_pass([80, 79, 81], cutoff=80) == 2
