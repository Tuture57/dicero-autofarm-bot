---
phase: 1
plan: 02
subsystem: capture
tags: [templates, menu-interactif, captures]
key-files:
  created: []
  modified:
    - capture_templates.py
metrics:
  tasks_completed: 2
  tasks_total: 2
---

## Summary

Rewrote `capture_templates.py` with an interactive menu listing all 9 canonical templates with existe/manquant status, individual selection by number, and overwrite confirmation. Template list updated from 7 items to the 9 canonical templates: `menu_new_game`, `attack_btn`, `select_skill_v1`, `select_skill_v2`, `angel_select`, `try_luck_btn`, `select_dice_text`, `confirm_btn`, `rewards_btn`.

## Commits

| Task | Description |
|------|-------------|
| 2.1 | feat(1-02): update CAPTURES to 9 canonical templates |
| 2.2 | feat(1-02): rewrite main() with interactive menu and individual capture |

## Deviations

None.

## Self-Check: PASSED

- 9 templates in CAPTURES ✓
- menu_new_game, select_skill_v1, select_skill_v2, angel_select, rewards_btn present ✓
- while True menu loop ✓
- existe/manquant status display ✓
- Overwrite confirmation "Ecraser ? [y/N]" ✓
- "0. Quitter" exit option ✓
- Individual template selection by number ✓
- Syntax valid ✓
