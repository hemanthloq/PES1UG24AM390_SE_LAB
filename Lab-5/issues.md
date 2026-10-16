# Lab 5 — Static Code Analysis: Identified Issues

**Student:** R Hemanth Reddy — PES1UG24AM390
**Assigned repo:** [SETAPESU26/L5_28_blood_donation](https://github.com/SETAPESU26/L5_28_blood_donation)
**File analysed:** `blood_donation.py`

## Baseline (before any fixes)

| Tool | Result |
|------|--------|
| Pylint | **4.81/10** — 28 messages |
| Bandit | **4 findings** — 1 High, 1 Medium, 2 Low |
| Flake8 | **4 findings** — E501, E303, E261, E225 |

Full reports: [`before/pylint_report.txt`](before/pylint_report.txt),
[`before/bandit_report.txt`](before/bandit_report.txt),
[`before/flake8_report.txt`](before/flake8_report.txt)

## Issue table

Ordered by severity: security findings first, then correctness, then style.
Line numbers refer to the original file as handed out.

| Issue | Type | Line(s) | Description | Fix Approach |
|-------|------|---------|-------------|--------------|
| Shell command built from user input (`B605`) | Security — **High** | 65 | `os.system("send-sms " + " ".join(phoneList))` passes the joined phone list straight to a shell. A phone entry containing `; rm -rf ~` would be executed as a separate command — a textbook OS command injection (CWE-78). | Replaced with `subprocess.run` on an **argument list** with `shell=False`, so no shell parses the string. The executable is resolved to an absolute path with `shutil.which`, and every number is filtered through `.isdigit()` before it reaches argv. |
| Insecure temporary file (`B306`) | Security — **Medium** | 60 | `tempfile.mktemp()` only *returns a name*; it does not create the file. Between the name being returned and the program opening it, an attacker can create a symlink at that path and redirect the donor sheet — a TOCTOU race (CWE-377). | Switched to `tempfile.mkstemp()`, which creates the file atomically with restrictive permissions and hands back an open descriptor. The descriptor is closed and the path returned, so the function's contract is unchanged. |
| Hardcoded password (`B105`) | Security — Low | 5 | `OFFICER_PASSWORD = "bloodbank-demo"` puts a credential in source control, where it is visible to anyone with repo access and survives in git history forever (CWE-259). | Read from the environment instead: `os.environ.get("BLOODBANK_OFFICER_PASSWORD", "")`. The secret now lives in deployment config, not in the repository. |
| `assert` used for validation (`B101`) | Security / Correctness — Low | 18 | `assert bloodGroup in stock` is the only guard against an unknown blood group, but Python strips all `assert` statements when run with `-O`. In an optimised deployment the check silently vanishes and bad data enters the register (CWE-703). | Replaced with an explicit `if ... raise ValueError(...)`, which runs under every optimisation level. |
| Mutable default argument (`W0102`) | Bug | 17 | `notes=[]` is evaluated **once**, at function definition. Every call that omits `notes` shares the same list, so rejection messages accumulate across unrelated calls and leak between callers. | Default changed to `None`; the function creates a fresh list when none is supplied. |
| Overly broad exception (`W0718`) | Bug | 45 | `except Exception` in `unitsFor` swallows *everything* — a typo'd variable, a `TypeError`, a `MemoryError` — and silently returns `0`. A genuine bug would be indistinguishable from "no compatible units available", which in a blood bank is a dangerous thing to get wrong. | Narrowed to `except KeyError`, the one error the function actually anticipates (an unknown patient group). Any other exception now propagates and is visible. |
| Duplicated comparison (`R1714`) | Quality | 50 | `bloodGroup == "O-" or bloodGroup == "AB+"` repeats the operand and scales badly as groups are added. | Rewritten as a single membership test: `blood_group in ("O-", "AB+")`. |
| Non-PEP 8 naming (`C0103`) | Style | 17, 27, 33, 42, 49, 53, 58, 63 and their arguments | Every function and parameter used camelCase (`registerDonor`, `donorName`, `bloodGroup`…), which contradicts PEP 8 and the rest of the Python ecosystem. | Renamed throughout to snake_case (`register_donor`, `donor_name`, `blood_group`…), including all call sites in `main()`. |
| Missing docstrings (`C0114`, `C0116`) | Maintainability | 1 and every function | No module docstring and no function docstrings, so nothing states the 90-day rule, the age range, or what the return values mean. | Added a module docstring and a docstring for all nine functions, stating behaviour and return values. |
| Magic numbers | Maintainability | 19, 30 | `18`, `65` and `90` appeared as bare literals, so the eligibility policy was buried in the logic. | Extracted to the named constants `MIN_AGE`, `MAX_AGE` and `DONATION_GAP_DAYS`. |
| Line too long (`E501`) | Style | 7 | The `stock` dictionary ran to 82 characters, over PEP 8's 79-character limit. | Wrapped across three lines. |
| Too many blank lines (`E303`) | Style | 58 | Three blank lines between top-level functions where PEP 8 asks for two. | Reduced to two. |
| Inline comment spacing (`E261`) | Style | 80 | `lowStock()) # below 2 units` had one space before the comment; PEP 8 requires at least two. | Added the second space. |
| Missing whitespace around operator (`E225`) | Style | 81 | `eligible=[...]` with no spaces around `=`. | Written as `eligible = [...]`. |

## Note on the two `# nosec` markers

After the `B605` fix, Bandit reported three new **Low, informational** findings
that it raises for *any* use of `subprocess`: `B404` (the import itself),
`B603` (a subprocess call that is not demonstrably safe) and `B607` (a partial
executable path).

- **`B607` was fixed properly** — `shutil.which` resolves `send-sms` to an
  absolute path, so there is no PATH-hijacking window.
- **`B404` and `B603` are suppressed** with `# nosec` and a written
  justification in the source. They cannot be "fixed" without abandoning
  `subprocess` altogether, and the justification is substantive: the call uses
  `shell=False`, argv is constructed in code rather than parsed from a string,
  and every argument is validated as digits-only, so no argument can be read as
  a flag or a shell metacharacter.

This is the standard industry handling for unavoidable informational findings —
suppress narrowly, by specific test ID, with the reasoning recorded next to the
code. It is flagged here explicitly rather than hidden.

## Result (after fixes)

| Tool | Before | After |
|------|--------|-------|
| Pylint | 4.81/10 | **10.00/10** |
| Bandit | 1 High, 1 Medium, 2 Low | **No issues identified** |
| Flake8 | 4 findings | **0 findings** |

Full reports: [`after/pylint_report.txt`](after/pylint_report.txt),
[`after/bandit_report.txt`](after/bandit_report.txt),
[`after/flake8_report.txt`](after/flake8_report.txt)

The program's behaviour is unchanged. `python blood_donation.py` prints exactly
the same six lines before and after:

```
Stock: {'A+': 0, 'A-': 0, 'B+': 0, 'B-': 0, 'O+': 2, 'O-': 1, 'AB+': 0, 'AB-': 0}
Units for an A+ patient: 3
Units for a Z+ patient: 0
Is O- universal? True
Low stock groups: ['A+', 'A-', 'B+', 'B-', 'O-', 'AB+', 'AB-']
Donors eligible today: []
```

## One thing the tools did not catch

`COMPATIBLE` has entries for only five of the eight blood groups — `A-`, `B-`
and `AB-` are missing. So `units_for("A-")` returns `0` for a patient who may
well have compatible stock on the shelf, and before the fix the broad
`except Exception` made that failure completely silent.

No static analyser flagged this, because it is not a code defect — the syntax is
correct, the style is fine and nothing is insecure. It is a *domain* error: the
code faithfully implements the wrong medical rule. That boundary is worth
noting. Static analysis guards the form of the code; only tests written against
the domain, and review by someone who knows blood-group compatibility, catch
this class of bug. The behaviour has been left as-is, since fixing it would
change the program's output and go beyond the lab's brief.
