import math

from hypothesis import given, strategies as st
from recycling_rewards import parse_collection, weight_average, net_points


# ---------- 1. Fuzz: arbitrary text / None must never raise ----------
@given(st.text() | st.none())
def test_parse_collection_no_crash(s):
    parse_collection(s)


@given(st.text() | st.none())
def test_weight_average_no_crash(s):
    weight_average(s)


@given(st.text() | st.none())
def test_net_points_no_crash(s):
    net_points(s)


# ---------- 2. Fuzz: well-formed input must give sensible results ----------
@given(
    st.text(alphabet=st.characters(whitelist_categories=("L",)), min_size=1),
    st.floats(min_value=0, max_value=1e6),
)
def test_parse_collection_valid_input(material, kg):
    result = parse_collection(f"{material}:{kg}")
    assert result is not None
    name, weight = result
    assert name == material.strip().title()
    assert weight == kg


@given(st.text(max_size=20) | st.none())
def test_parse_collection_result_is_finite_and_non_negative(s):
    result = parse_collection(s)
    if result is not None:
        assert math.isfinite(result[1]) and result[1] >= 0


@given(st.lists(st.integers(min_value=0, max_value=10**6), min_size=1))
def test_weight_average_valid_input_within_bounds(weights):
    avg = weight_average(",".join(str(w) for w in weights))
    assert min(weights) <= avg <= max(weights)


@given(st.floats(allow_nan=True, allow_infinity=True),
       st.floats(allow_nan=True, allow_infinity=True))
def test_net_points_never_nan_or_negative(points, penalty):
    result = net_points(f"{points}|{penalty}")
    if result is not None:
        assert math.isfinite(result) and result >= 0


@given(st.floats(min_value=0, max_value=1e6),
       st.floats(min_value=0, max_value=1e6))
def test_net_points_valid_input(points, penalty):
    assert net_points(f"{points}|{penalty}") == max(points * 2 - penalty, 0)
