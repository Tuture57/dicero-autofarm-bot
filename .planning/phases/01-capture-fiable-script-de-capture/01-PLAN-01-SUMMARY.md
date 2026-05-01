---
phase: 1
plan: 01
subsystem: capture
tags: [imagegrab, dpi, screenshot]
key-files:
  created: []
  modified:
    - bot.py
    - capture_templates.py
metrics:
  tasks_completed: 2
  tasks_total: 2
---

## Summary

Replaced BitBlt/PrintWindow capture with `PIL.ImageGrab.grab(bbox=GetWindowRect)` in both `bot.py` and `capture_templates.py`. `SetProcessDpiAwareness(2)` is now called once in `main()` of each script. `bot.py` handles a `None` return from `screenshot_window` when the window is too small.

## Commits

| Task | Description |
|------|-------------|
| 1.1 | feat(1-01): rewrite screenshot_window in bot.py with ImageGrab |
| 1.2 | feat(1-01): rewrite screenshot_window and grab_full_window in capture_templates.py with ImageGrab |

## Deviations

None.

## Self-Check: PASSED

- bot.py: no BitBlt/win32ui/win32con references ✓
- bot.py: ImageGrab.grab used ✓
- bot.py: SetProcessDpiAwareness(2) once in main() ✓
- bot.py: screen is None guard in main loop ✓
- capture_templates.py: no BitBlt/win32ui/win32con references ✓
- capture_templates.py: ImageGrab.grab in screenshot_window and grab_full_window ✓
- capture_templates.py: SetProcessDpiAwareness(2) once in main() ✓
- Both files parse without syntax errors ✓
