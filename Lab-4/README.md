# Defender Repair Lab

This project is a single-file Defender-lite clone using **Pygame**. It introduces students to camera wrapping, world-space vs. screen-space coordinates, and multi-stage enemy AI using a small, readable object-oriented codebase.

---

## What's Provided

A working Defender-lite game with:

- A player ship that thrusts left/right and adjusts altitude, wrapping around a world several screens wide
- Humanoids on the ground that landers try to abduct, carry upward, and turn into a faster "mutant" enemy if they reach the top
- A radar strip along the top meant to show where everything is across the whole world
- Waves, lives, scoring, and bonus points for rescuing a humanoid mid-fall

It has **one deliberate bug** and **three optional features** left as empty functions. You are expected to **analyze**, **interact with an AI assistant**, and **complete/fix** the game to make it fully functional and more interesting.

### **Use an LLM (e.g. ChatGPT or Claude) as your debugging and pair-programming partner for this lab.**

---

## Getting Started

### Setup

1. Make sure you have Python 3.10+ installed.
2. Install dependencies:

```bash
pip install pygame
```

3. Run the game:

```bash
python game.py
```

**Controls:** Left/Right to thrust, Up/Down to change altitude, Space to fire, `R` to reset.

---

## Tasks to Complete

Each task must be completed using an iterative process involving LLM suggestions and your critical code review.

### Task 1: Fix the radar bug

> The radar strip is supposed to show every humanoid, lander, and the player at their true position across the entire wrapping world, so threats anywhere in the world are visible at a glance. In the current build, the radar only ever shows things clustered near the player's own position, because it plots each blip's position *relative to the player* (screen space) instead of its absolute position in the world. Fix `draw_radar` so each blip's horizontal position on the radar reflects its actual place in the world, from one edge to the other, regardless of where the player currently is.

### Task 2: Implement `sky_color(wave)`

> Called once per frame in `draw`, as `screen.fill(sky_color(self.wave) or (5, 5, 20))`. It receives the current wave number and should return an `(r, g, b)` color, or `None` to keep the default near-black sky. Idea: brighten or shift hue as waves progress.

### Task 3: Implement `on_humanoid_rescued(humanoid)`

> Called from `update()` the moment the player catches a falling humanoid (one a lander dropped or released mid-air), right after the 500-point bonus is added and the humanoid is placed safely back on the ground. It receives the rescued `Humanoid`. Its return value is ignored. Idea: a "+500" popup, or a short invulnerability boost as a reward.

### Task 4: Implement `bonus_life_threshold()`

> Called every frame in `update()`. It takes no arguments and should return an integer score value, or `None` to disable bonus lives entirely. Whenever the score crosses a multiple of that value for the first time, one life is awarded automatically — the bookkeeping (`self.bonus_awarded`) is already implemented, so you only need to choose the threshold. Idea: return `10000`.

---

## Expected Behavior

- The player and every enemy wrap smoothly across both edges of the world
- The radar shows the whole world at once; only the main viewport centers on the player, not the radar
- A lander that finishes carrying a humanoid off the top of the screen becomes a faster, more aggressive mutant
- Catching a humanoid mid-fall returns it safely to the ground and awards points; letting it fall too far kills it
- The game ends when lives reach zero

---

## Folder Structure

```
defender/
├── game.py
└── README.md
```

---

## Submission Checklist

Submission is only the following three things:

- [] A 10-second video of gameplay **before** your changes, showing the bug/broken behavior
- [] A 10-second video of gameplay **after** your changes, showing the bug fixed and the new features working
- [] The Chat/LLM used page link, with the complete chat history
