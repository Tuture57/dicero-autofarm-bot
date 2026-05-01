# Phase 3 Research — Menu principal main.py avec rich

**Date:** 2026-05-01
**Phase:** 03-menu-principal-main-py-rich

---

## Q1 — questionary API for arrow-key menus

### Minimal working pattern

```python
import questionary

choice = questionary.select(
    "Que veux-tu faire ?",
    choices=[
        "Calibrer les templates",
        "Lancer le bot",
        "Quitter",
    ]
).ask()
```

- `.ask()` blocks until the user picks an option and presses Enter.
- Returns the selected string (or the `Choice.value` if `Choice` objects are used).
- Returns `None` if the user presses Ctrl+C (questionary catches it silently by default).
- Arrow keys are enabled by default (`use_arrow_keys=True`).
- `j`/`k` and Ctrl+N/Ctrl+P are also active by default — no extra config needed.

### Key parameters to know

| Parameter | Default | Purpose |
|-----------|---------|---------|
| `message` | — | Question text shown above the list |
| `choices` | — | List of strings, `Choice` objects, or `Separator` |
| `default` | `None` | Pre-positions the cursor on this item |
| `pointer` | `»` | Symbol before highlighted item |
| `instruction` | auto | Navigation hint shown in parentheses |
| `use_arrow_keys` | `True` | Arrow key navigation |

### Separator for visual grouping

```python
questionary.select("...", choices=[
    "Option A",
    questionary.Separator(),
    "Quitter",
])
```

### Choice with explicit value

```python
from questionary import Choice
questionary.select("...", choices=[
    Choice("Calibrer les templates", value="calibrate"),
    Choice("Lancer le bot", value="run"),
    Choice("Quitter", value="quit"),
]).ask()
```

---

## Q2 — rich styled headers/panels

### Minimal Panel

```python
from rich import print
from rich.panel import Panel

print(Panel("[bold cyan]AUTOFARM BOT[/bold cyan]", title="v1.1", expand=False))
```

- `expand=False` sizes the panel to fit its content (not full terminal width).
- `Panel.fit(content)` is an equivalent shorthand for `expand=False`.
- `title=` adds a label at the top border; `subtitle=` at the bottom.

### Console object (recommended for this project)

```python
from rich.console import Console
console = Console()
console.print(Panel("[bold green]AUTOFARM[/bold green]"))
console.print("[yellow]Bot arrêté.[/yellow]")
```

Using a single `Console()` instance throughout `main.py` ensures consistent output handling.

### Markup syntax

- `[bold]`, `[italic]`, `[red]`, `[green cyan]`, `[bold red on white]`
- Close with `[/bold]`, `[/]` (closes last opened tag), or implicit end-of-string
- Emoji: `[green]:white_check_mark:[/green]`

### ASCII art title

Rich itself has no built-in ASCII art generator. Options:
- **Hardcode the ASCII art** as a multi-line string inside the Panel (simplest, zero dependency)
- Use `pyfiglet` if a fancier font is wanted (adds a dependency)

Given D-08 only adds `rich` + `questionary`, hardcoding the ASCII art string is the correct approach.

---

## Q3 — Ctrl+C handling when calling bot.main() or capture_templates.main() inline

### Current behavior in bot.py

`bot.main()` already handles `KeyboardInterrupt` at line 412:

```python
# bot.py lines 360-418
while not _stop_event.is_set():
    try:
        ...
    except KeyboardInterrupt:
        _stop_event.set()
    except Exception as e:
        ...
_shutdown(console_hwnd)
```

So calling `bot.main()` from `main.py` and pressing Ctrl+C will set `_stop_event`, call `_shutdown()`, and return normally — the `KeyboardInterrupt` is consumed inside the bot loop and does NOT propagate to `main.py`.

### Pattern for main.py

```python
while True:
    choice = questionary.select("Menu", choices=[...]).ask()

    if choice is None or choice == "Quitter":   # None = Ctrl+C in menu
        break

    if choice == "Lancer le bot":
        try:
            bot.main()
        except KeyboardInterrupt:
            pass   # bot already handles it; this is a safety net
        console.print("[yellow]Bot arrêté. Retour au menu.[/yellow]")

    elif choice == "Calibrer les templates":
        try:
            capture_templates.main()
        except KeyboardInterrupt:
            pass
        console.print("[yellow]Calibration terminée. Retour au menu.[/yellow]")
```

- **D-03** (auto-return to menu) is satisfied by the `while True` loop.
- **D-04** (Ctrl+C in menu quits cleanly) is satisfied by checking `choice is None` and `break`-ing, then printing no stack trace.

### capture_templates.main() note

`capture_templates.main()` uses `input()` internally (line 222 of `capture_templates.py`). Ctrl+C inside `input()` raises `KeyboardInterrupt` which will propagate out of `capture_templates.main()` — so the `except KeyboardInterrupt: pass` wrapper in `main.py` is necessary.

---

## Q4 — Restructuring admin elevation into main.py only

### Current state

Both files have the elevation block at module top-level (executed on import):

- `bot.py` lines 21–23:
  ```python
  if not ctypes.windll.shell32.IsUserAnAdmin():
      ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(f'"{a}"' for a in sys.argv), None, 1)
      sys.exit(0)
  ```
- `capture_templates.py` lines 17–19: identical block.

### Problem with import-time execution

If `bot.py` or `capture_templates.py` is imported from `main.py`, these top-level blocks execute **at import time** before `main()` is called — which is exactly what D-02 says to fix.

### Required changes

1. **Remove** the 3-line elevation block from `bot.py` (lines 21–23).
2. **Remove** the 3-line elevation block from `capture_templates.py` (lines 17–19).
   - Also remove `import sys` from `capture_templates.py` if it becomes unused after removal (currently `sys` is only used in those 3 lines at line 9 and 18).
3. **Add** the elevation block to `main.py` as the **very first executable code**, before any other imports that touch win32 APIs:

```python
import ctypes
import sys

if not ctypes.windll.shell32.IsUserAnAdmin():
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable,
        " ".join(f'"{a}"' for a in sys.argv), None, 1
    )
    sys.exit(0)

# Only after elevation: import win32 and other modules
import bot
import capture_templates
from rich.console import Console
import questionary
```

### Why elevation must come first

`capture_templates.py` calls `ctypes.windll.shcore.SetProcessDpiAwareness(2)` at line 15 (top-level, before elevation check). In the new structure, since `capture_templates.py` will be imported (not run as `__main__`), that line will execute at import time — which is fine, it doesn't require admin rights. Only `win32gui`/`win32ui` calls may require elevation, and those happen inside functions, not at import time.

---

## Q5 — Known issues combining rich + questionary on Windows terminals

### The core compatibility concern

Both rich and questionary use `prompt_toolkit` under the hood (questionary is built on top of it). Rich writes directly to `sys.stdout` using ANSI sequences; questionary also writes to stdout via prompt_toolkit's output layer. On Windows, there is one known tension:

**Issue: `colorama` or legacy Windows console APIs interfering with color depth**

If a third-party library initializes `colorama` before rich does (e.g., some pip packages auto-initialize colorama), rich loses true-color support and falls back to 16 colors. questionary itself does not initialize colorama, so this is not a questionary-specific problem.

**Issue: Output interleaving**

If rich `console.print()` is called and questionary then immediately renders its prompt, there can be a brief visual flicker or misaligned cursor. This is cosmetic only and resolves itself. Standard mitigation: `console.print()` before `questionary.select()` — not interleaved.

### Windows Terminal (Windows 11) — verdict: no real issue

On Windows 11 with Windows Terminal (the default), both rich and questionary work correctly:
- Full ANSI/VT support
- True color
- Arrow key navigation works in questionary

### Legacy cmd.exe — minor limitation

In the old `cmd.exe`, arrow keys still work (questionary uses Windows console APIs as fallback), but rich colors may be limited to 16 colors. Not a concern for this project since the target platform is Windows 11.

### Practical mitigation for this project

1. Always use a single `Console()` instance; do not mix `rich.print()` and `console.print()`.
2. Do not call `console.print()` and `questionary.select().ask()` in the same expression or concurrent thread — sequential calls are fine.
3. `questionary.select().ask()` already returns before `console.print()` is called for status messages, so ordering is naturally safe.

### No `patch_stdout` needed

`questionary`'s `patch_stdout=True` parameter is for scenarios where background threads are printing to stdout while a questionary prompt is active. In this project, there are no background threads active during the menu — the menu is shown only after `bot.main()` has fully returned — so `patch_stdout` is not needed.

---

## Summary: Key planning inputs

| Topic | Key fact |
|-------|----------|
| questionary API | `questionary.select("msg", choices=[...]).ask()` — returns `None` on Ctrl+C |
| rich Panel | `Console().print(Panel("[bold]Title[/bold]", expand=False))` |
| Ctrl+C in bot.main() | Already handled inside bot; does NOT propagate — safety `except KeyboardInterrupt: pass` in main.py is sufficient |
| Ctrl+C in capture_templates.main() | Propagates via `input()` — must be caught in main.py |
| Ctrl+C in menu | `choice is None` → `break` → sys.exit or return |
| Elevation removal | Remove lines 21–23 from bot.py, lines 17–19 from capture_templates.py |
| Elevation placement | Must be FIRST in main.py, before `import bot` / `import capture_templates` |
| rich + questionary on Win11 | No known blocking issues; use sequential calls (print then ask) |
| ASCII art | Hardcode as string (no new dependency) |
| `sys` import in capture_templates | Used only for elevation block → removable after D-02 |

---

*Research gathered: 2026-05-01*
*Sources: questionary docs (readthedocs.io), rich docs (readthedocs.io), rich GitHub issues, codebase inspection*
