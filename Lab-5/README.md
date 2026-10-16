# Lab 5: Static Code Analysis — Blood Donation Management System

**Student:** R Hemanth Reddy — PES1UG24AM390
**Assigned repo:** [SETAPESU26/L5_28_blood_donation](https://github.com/SETAPESU26/L5_28_blood_donation)
**File analysed:** `blood_donation.py`

Pylint, Bandit and Flake8 were run against the assigned script, the findings
documented, and at least four fixed — one commit per tool.

## Results

| Tool | Before | After |
|------|--------|-------|
| Pylint | 4.81/10 | **10.00/10** |
| Bandit | 1 High, 1 Medium, 2 Low | **No issues identified** |
| Flake8 | 4 findings | **0 findings** |

The program's behaviour is unchanged — `python blood_donation.py` prints the
same six lines before and after the fixes.

## Contents

| Path | What it is |
|------|------------|
| `blood_donation.py` | The cleaned script |
| `issues.md` | The completed issue table, with the fix approach for each finding |
| `reflection.md` | Answers to the four reflection questions |
| `before/` | Pylint, Bandit and Flake8 reports from the original file |
| `after/` | The same three reports after the fixes |

## Commits

The fixes are split one commit per tool, so each can be reviewed on its own:

1. `Lab 5: add assigned blood donation script and baseline reports` — the file as handed out, plus the "before" reports
2. `Lab 5: fix Bandit security findings` — B605 shell injection, B306 temp-file race, B105 hardcoded password, B101 assert
3. `Lab 5: fix Pylint issues, score 4.81/10 -> 10.00/10` — mutable default argument, broad except, snake_case, docstrings
4. `Lab 5: fix Flake8 formatting issues` — E501, E303, E261, E225
5. `Lab 5: add after reports, issue table and reflection` — the remaining deliverables

## Reproducing

```bash
python -m venv venv
venv\Scripts\activate          # Windows
python -m pip install pylint bandit flake8

python blood_donation.py
python -m pylint blood_donation.py
python -m bandit -r blood_donation.py
python -m flake8 blood_donation.py
```
