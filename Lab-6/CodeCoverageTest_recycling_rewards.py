"""Lab 6 - Code (line) coverage tests for recycling_rewards.py.

Goal: execute every line of the module at least once.
Run:
    coverage run -m pytest CodeCoverageTest_recycling_rewards.py
    coverage report -m --include=recycling_rewards.py
"""
import pytest
from recycling_rewards import reward_points, collection_accepted, slot_status


# ---------- reward_points ----------
def test_below_minimum_weight():
    assert reward_points("paper", 3, False) == 0


def test_unknown_material_raises():
    with pytest.raises(ValueError, match="unknown material"):
        reward_points("glass", 10, False)


def test_negative_weight_raises():
    with pytest.raises(ValueError, match="invalid weight"):
        reward_points("paper", -1, False)


def test_paper_with_bonus_normal_rate():
    # minimum 5 - 1 (bonus) = 4, extra = 6, rate 6 -> 36
    assert reward_points("paper", 10, True) == 36


def test_metal_large_extra_gets_highest_rate():
    # minimum 2, extra = 28 (> 20), rate 12 + 4 + 2 = 18 -> 504
    assert reward_points("metal", 30, False) == 504


# ---------- collection_accepted ----------
def test_collection_accepted():
    assert collection_accepted(20, 2, False) is True


def test_hazardous_light_accepted():
    assert collection_accepted(3, 1, True) is True


def test_too_heavy_rejected():
    assert collection_accepted(60, 1, False) is False


# ---------- slot_status ----------
def test_morning_holiday_slot_open():
    # cutoff = 20 + 15 = 35
    assert slot_status(40, True, True) == "open"


def test_afternoon_slot_late():
    # cutoff = 10, late window is 10 - 15 = -5 .. 10
    assert slot_status(5, False, False) == "late"


def test_morning_slot_missed():
    # cutoff = 20, missed below 5
    assert slot_status(2, True, False) == "missed"
