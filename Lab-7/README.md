# L6_L7_50 — Recycling Rewards

Lab 7: Fuzz Testing

## About

A small Python module that parses collections, averages collected weights and works out the net reward points after a penalty.

## Files

| File | Description |
|------|-------------|
| `recycling_rewards.py` | The code under test |
| `test_recycling_rewards.py` | Starter test file |

Refer to the lab handout for instructions.

## Fuzz testing results

Tool: [Hypothesis](https://hypothesis.readthedocs.io/). Run with
`python -m pytest test_recycling_rewards.py`.

| Run | Result | Report |
|-----|--------|--------|
| Original code | 5 failed, 3 passed | `before/fuzz_report.txt` |
| Fixed code | 8 passed | `after/fuzz_report.txt` |

### Bugs found and fixed

| Function | Input that broke it | Original behaviour | Fix |
|----------|---------------------|--------------------|-----|
| all three | `None` | `AttributeError: 'NoneType' has no attribute 'split'` | type check, return `None` |
| `parse_collection` | `""`, `"paper"`, `"a:b:c"` | `ValueError` (unpack) | require exactly one `:` |
| `parse_collection` | `"paper:abc"`, `"paper:"` | `ValueError` (float) | catch and return `None` |
| `parse_collection` | `"paper:nan"`, `"paper:inf"`, `"paper:-5"` | accepted silently | reject non-finite and negative weights |
| `parse_collection` | `":5"` | empty material accepted | reject empty material |
| `weight_average` | `""`, `"1,,2"`, `"1.5"` | `ValueError` (int) | catch and return `None` |
| `weight_average` | `"-5,3"` | negative weight accepted | reject negative weights |
| `net_points` | `"5"`, `"1\|2\|3"` | `ValueError` (unpack) | require exactly one `\|` |
| `net_points` | `"nan\|1"`, `"inf\|inf"`, `"1e308\|0"` | returned `nan`/`inf` | reject non-finite input and result |

Invalid input now returns `None` and `main()` prints "Invalid input".
