---
plan: "03-02"
status: complete
---

# Summary — 03-02: Créer main.py avec menu rich + questionary

## What was built
Created `main.py` as the single entry point for the autofarm application. The file opens with an admin-elevation block (before any win32 imports), then presents a rich-styled ASCII art header and a questionary arrow-key menu with three choices: Calibrer les templates, Lancer le bot, Quitter. Each action wraps the target `main()` in a `KeyboardInterrupt` guard and returns to the menu automatically via `press_any_key_to_continue`.

Also added `rich` and `questionary` to `requirements.txt`.

## Key files modified
- `main.py` — created (82 lines)
- `requirements.txt` — added `rich` and `questionary`

## Commits
- `feat(03-02): create main.py with rich menu + questionary; add rich/questionary to requirements.txt`

## Self-Check: PASSED
- `import ctypes` and `import sys` are the first two imports ✓
- Elevation block precedes `import bot` and `import capture_templates` ✓
- `def show_header(`, `def run_menu(`, `while True:` all present ✓
- `bot.main()` and `capture_templates.main()` both wrapped in `try/except KeyboardInterrupt` ✓
- `if __name__ == "__main__": run_menu()` at end ✓
- `grep ShellExecuteW main.py` → 1 result (elevation block only) ✓
- `grep "rich\|questionary" requirements.txt` → 2 results ✓
