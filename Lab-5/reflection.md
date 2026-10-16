# Lab 5 — Reflection

**Student:** R Hemanth Reddy — PES1UG24AM390
**File analysed:** `blood_donation.py`

> The lab handout asks for answers to the reflection questions but does not
> print them. The four standard questions for this lab are restated below.

## 1. What is the purpose and scope of static code analysis, and what did it find here that reading the code might not?

Static analysis examines source code without running it. That is its defining
strength and its defining limit in the same sentence: it sees every path through
the program, including the ones no test ever exercises, but it only ever
reasons about the *form* of the code, never about whether the code is doing the
right thing.

Both halves showed up clearly in this file.

The strength: `notifyDonors` and `donorSheetPath` are never called by the demo.
Running the program a hundred times would never execute them, so no amount of
testing would reveal the command injection in one and the temp-file race in the
other. Bandit found both in under a second, because it never needed to run
them.

The same applies to the mutable default argument on line 17. `notes=[]` is
evaluated once at definition time, and the bug only manifests across repeated
calls that omit the argument — exactly the pattern a short demo does not
produce. Reading the line, it looks completely ordinary. I would not have
flagged it on a visual pass.

The limit showed up too. `COMPATIBLE` is missing three of the eight blood
groups, so `units_for("A-")` reports zero available units for a patient who may
have stock waiting. Not one of the three tools said a word about it. The syntax
is valid, the style is clean, nothing is insecure — the code correctly
implements an incorrect rule. Static analysis cannot know what blood-group
compatibility *should* be.

So the honest scope is: static analysis is very good at "this code is built
wrong" and completely blind to "this code is solving the wrong problem."

## 2. Which tool was most useful, and how do the three differ?

The three are not competitors; they answer different questions, and the
difference is sharpest when you look at what each one *missed*.

- **Bandit** was the most valuable here, by a clear margin. It found the only
  issue that could cause real harm: `os.system("send-sms " + ...)` hands a
  donor-supplied string to a shell. A phone number entered as
  `123; rm -rf ~` executes as a second command. Bandit was also the only tool
  that cared about `assert` being stripped under `-O`, which is a genuine
  correctness trap and not an obvious one.
- **Pylint** was the most valuable for *maintainability*. It drove the score
  from 4.81 to 10.00, but the number matters much less than two specific
  findings: the mutable default argument and the bare `except Exception`.
  Both are real bugs, not style complaints, and both were invisible to Flake8
  and Bandit.
- **Flake8** was the cheapest and the shallowest. Four findings, all cosmetic,
  all fixable in under a minute. That is not a criticism — its job is to remove
  the arguments nobody should be having, so that review time goes to logic
  instead of whitespace.

The severity ordering is also worth stating plainly. Bandit rated the
hardcoded password **Low** and the `mktemp` race **Medium**, while rating the
shell injection **High**. That ranking is correct, and it is the kind of
judgement the tool is encoding on your behalf: not every finding deserves equal
attention, and a report with 28 messages is useless if it does not tell you
which three matter.

## 3. How does static analysis contribute to code quality and maintainability?

Three things, in rough order of how much they actually matter:

**It catches a specific class of bug early and cheaply.** The injection flaw in
`notifyDonors` costs one `subprocess.run` call to fix today. The same flaw found
after a blood bank deploys it is an incident, with donor phone records on the
other side of it. The cost of a defect rises steeply with how late it is found,
and static analysis sits at the earliest point where a tool can look at all.

**It makes code review about the things humans are good at.** When the tool has
already settled naming, spacing and line length, a reviewer spends their
attention on whether the 90-day donation gap is the right policy — which is the
only part of the review a machine cannot do. Consistency is not an aesthetic
preference here; it is what makes the diff readable.

**It encodes institutional knowledge.** I did not know that `tempfile.mktemp`
was deprecated for a symlink race, or that `assert` disappears under `-O`.
Bandit knows, because someone was burned by each of those and wrote a check.
Every run is a transfer of expertise I did not have to acquire the hard way.

The caveat is the one from question 1, and it is worth keeping in view: a clean
report is evidence of the absence of *known categories of defect*, not evidence
of correctness. This file scores 10.00/10 from Pylint and still returns the
wrong unit count for an A- patient. A perfect score is a floor, not a finish
line.

## 4. Would you use these tools in your own workflow, and how?

Yes, but with the configuration done deliberately rather than accepting the
defaults, because badly-tuned static analysis gets ignored and ignored tools
are worse than no tools.

Concretely:

- **Flake8 on save, in the editor.** Formatting issues should never survive
  long enough to reach a commit, let alone a reviewer.
- **Pylint and Bandit in CI, on every pull request.** Bandit's High and Medium
  findings would block the merge. Pylint would gate on a score threshold rather
  than on zero messages, because the long tail of Pylint conventions is not
  worth blocking a deploy over.
- **Suppress narrowly and in writing.** The two `# nosec` markers in this file
  name a specific test ID and carry a justification comment next to the code. A
  blanket `# nosec` on a whole file, or a long `disable=` list in a config,
  quietly turns the tool off — and that failure mode is invisible precisely
  because everything goes green.
- **Tune the baseline once, at the start.** Running Pylint on an existing
  codebase for the first time produces hundreds of messages and the natural
  response is to ignore all of them. Fixing the baseline up front is what makes
  every subsequent run meaningful, because a new message then actually means
  something new broke.

The working principle I would take from this lab: let the tools own everything
mechanical, so that human review is spent entirely on whether the program is
solving the right problem. On this file the tools fixed thirteen issues
correctly and had nothing to say about the one that would actually have hurt a
patient. Both of those facts are the point.
