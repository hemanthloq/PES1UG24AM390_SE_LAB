"""Recycling rewards helpers.

Every parsing function validates its input and returns None when the input
is invalid (not a string, wrong format, non-numeric, NaN/infinite, negative
weight) instead of raising an exception.
"""
import math


def _to_finite_float(text):
    """Convert text to a finite float, or return None."""
    try:
        value = float(text)
    except ValueError:
        return None
    return value if math.isfinite(value) else None


def parse_collection(text):
    """Parse 'material:weight' into (Material, weight_kg), or None."""
    if not isinstance(text, str) or text.count(':') != 1:
        return None
    material, kg = text.split(':')
    material = material.strip()
    weight = _to_finite_float(kg)
    if not material or weight is None or weight < 0:
        return None
    return material.title(), weight


def weight_average(weights_csv):
    """Integer average of comma-separated non-negative whole kg, or None."""
    if not isinstance(weights_csv, str):
        return None
    try:
        values = [int(r) for r in weights_csv.split(',')]
    except ValueError:
        return None
    if not values or any(v < 0 for v in values):
        return None
    return sum(values) // len(values)


def net_points(text):
    """Parse 'points|penalty' and return max(points * 2 - penalty, 0), or None."""
    if not isinstance(text, str) or text.count('|') != 1:
        return None
    points_text, penalty_text = text.split('|')
    points = _to_finite_float(points_text)
    penalty = _to_finite_float(penalty_text)
    if points is None or penalty is None:
        return None
    total = points * 2 - penalty
    if not math.isfinite(total):
        return None
    return max(total, 0)


def main():
    print("==== Running parse_collection ====")
    user_input = input("Enter material:weight in kg (e.g. paper:12): ")
    result = parse_collection(user_input)
    print("Material and Weight:", result if result is not None else "Invalid input")

    print("\n==== Running weight_average ====")
    user_input = input("Enter weights in kg as CSV (e.g. 5,12,20): ")
    result = weight_average(user_input)
    print("Average Weight:", result if result is not None else "Invalid input")

    print("\n==== Running net_points ====")
    user_input = input("Enter points|penalty (e.g. 80|10): ")
    result = net_points(user_input)
    print("Net Points:", result if result is not None else "Invalid input")


if __name__ == "__main__":
    main()
