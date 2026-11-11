"""Lab 6 - Branch coverage tests for recycling_rewards.py.

Goal: make every decision evaluate to both True and False, including the
boundary values (>, >=, <, <=) of each condition.
Run:
    coverage run --branch -m pytest BranchCoverageTest_recycling_rewards.py
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


def test_zero_weight_is_valid_but_earns_nothing():
    # weight_kg < 0 is False at the boundary 0
    assert reward_points("plastic", 0, False) == 0


def test_exactly_minimum_weight_earns_nothing():
    # extra == 0 -> "extra <= 0" True
    assert reward_points("paper", 5, False) == 0


def test_one_over_minimum_earns_points():
    # extra == 1 -> "extra <= 0" False
    assert reward_points("paper", 6, False) == 6


def test_bonus_lowers_minimum_for_paper():
    # minimum 5 - 1 = 4, extra = 6, rate 6 -> 36
    assert reward_points("paper", 10, True) == 36


def test_bonus_lowers_minimum_for_plastic():
    # minimum 3 - 1 = 2, extra = 3, rate 6 -> 18
    assert reward_points("plastic", 5, True) == 18


def test_bonus_ignored_for_metal():
    # has_bonus True but material == "metal": minimum stays 2, extra = 3, rate 12
    assert reward_points("metal", 5, True) == 36


def test_no_bonus_keeps_minimum():
    # has_bonus False: minimum 3, extra = 2, rate 6 -> 12
    assert reward_points("plastic", 5, False) == 12


def test_metal_normal_rate():
    # minimum 2, extra = 4, rate 12 -> 48
    assert reward_points("metal", 6, False) == 48


def test_extra_exactly_20_has_no_high_rate():
    # extra == 20 -> "extra > 20" False; paper minimum 5, rate 6 -> 120
    assert reward_points("paper", 25, False) == 120


def test_extra_exactly_20_metal_has_no_high_rate():
    # metal minimum 2, extra == 20, rate 12 -> 240
    assert reward_points("metal", 22, False) == 240


def test_paper_extra_over_20_gets_high_rate():
    # extra == 21 -> rate 6 + 4 = 10 (not metal) -> 210
    assert reward_points("paper", 26, False) == 210


def test_plastic_extra_over_20_gets_high_rate():
    # minimum 3, extra = 27, rate 6 + 4 = 10 -> 270
    assert reward_points("plastic", 30, False) == 270


def test_metal_extra_over_20_gets_highest_rate():
    # minimum 2, extra = 28, rate 12 + 4 + 2 = 18 -> 504
    assert reward_points("metal", 30, False) == 504


# ---------- collection_accepted ----------
def test_collection_accepted():
    assert collection_accepted(20, 2, False) is True


def test_hazardous_light_accepted():
    assert collection_accepted(3, 1, True) is True


def test_hazardous_at_limit_accepted():
    assert collection_accepted(5, 1, True) is True


def test_hazardous_over_limit_rejected():
    assert collection_accepted(6, 1, True) is False


def test_hazardous_ignores_bag_and_normal_weight_limits():
    # hazardous branch returns early, bags are irrelevant
    assert collection_accepted(4, 10, True) is True


def test_too_heavy_rejected():
    assert collection_accepted(60, 1, False) is False


def test_exactly_50_kg_not_too_heavy():
    assert collection_accepted(50, 3, False) is True


def test_just_over_50_kg_rejected():
    assert collection_accepted(51, 1, False) is False


def test_too_many_bags_rejected():
    assert collection_accepted(20, 4, False) is False


def test_exactly_three_bags_accepted():
    assert collection_accepted(20, 3, False) is True


# ---------- slot_status ----------
def test_morning_holiday_slot_open():
    # cutoff = 20 + 15 = 35
    assert slot_status(40, True, True) == "open"


def test_morning_no_holiday_open_at_cutoff():
    # cutoff = 20, minutes_left >= cutoff is True at the boundary
    assert slot_status(20, True, False) == "open"


def test_afternoon_no_holiday_open_at_cutoff():
    # cutoff = 10
    assert slot_status(10, False, False) == "open"


def test_afternoon_holiday_open_at_cutoff():
    # cutoff = 10 + 15 = 25
    assert slot_status(25, False, True) == "open"


def test_afternoon_slot_late():
    # cutoff = 10, late window is -5 .. 9
    assert slot_status(5, False, False) == "late"


def test_morning_slot_late_just_below_cutoff():
    # cutoff = 20, 19 < 20 but >= 5
    assert slot_status(19, True, False) == "late"


def test_morning_slot_late_at_lower_boundary():
    # cutoff = 20, cutoff - 15 = 5 -> "late" at exactly 5
    assert slot_status(5, True, False) == "late"


def test_morning_slot_missed():
    # cutoff = 20, missed below 5
    assert slot_status(2, True, False) == "missed"


def test_morning_slot_missed_just_below_boundary():
    assert slot_status(4, True, False) == "missed"


def test_afternoon_holiday_slot_missed():
    # cutoff = 25, late window 10..24, missed below 10
    assert slot_status(9, False, True) == "missed"
