---
plan: "04-02"
status: complete
---

## Summary

Refactored `capture_templates.py` UI without touching capture/calibration logic:

- Added `import questionary`, `from rich.console import Console`, `from rich.panel import Panel`, `console = Console()`
- Replaced 3 calibration instruction blocks with `rich Panel` (cyan border, titled)
- Replaced all `print()` status messages with `console.print()` with colors (green=success, yellow=warning, red=error, cyan=values, dim=technical)
- Replaced entire `print()`/`input()` main menu with `questionary.select()` arrow-key navigation
- Replaced overwrite confirmation `input()` with `questionary.confirm()`
- Removed `calib_cards_opt`/`calib_dice_opt` numeric variables (no longer needed)
- Each capture step now shows a `rich Panel` with blue border instead of bare `print()`

## Key files

- `capture_templates.py` — all changes

## Self-Check: PASSED

All acceptance criteria verified:
- import questionary: 1 ✓
- from rich.console/panel: 1 each ✓
- console = Console(): 1 ✓
- questionary.select: 1 ✓
- questionary.confirm: 1 ✓
- Panel(: 4 (3 calibration + 1 per-template) ✓
- border_style="cyan": 3 ✓
- calib_cards_opt/calib_dice_opt: 0 ✓
- input('Numero…'): 0 ✓
- print('Erreur: fenetre…'): 0 ✓
- def main / if __name__: 1 each ✓
