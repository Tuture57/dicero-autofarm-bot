# Concerns

## Critical — Screenshot capture inconsistency
**Problem**: `bot.py::screenshot_window` calls `SetProcessDpiAwareness(2)` on every loop iteration (inside the function). `capture_templates.py::screenshot_window` does NOT set it. `capture_templates.py::grab_full_window` does. Result: templates are captured with different pixel values than what the bot sees → `cv2.matchTemplate` fails silently (returns `unknown` state).

**Fix recommended**: use `PIL.ImageGrab.grab(bbox=win32gui.GetWindowRect(hwnd))` in both scripts, called once with `SetProcessDpiAwareness(2)` at startup only. See CLAUDE.md for full plan.

## High — Duplicate constants
`GAME_*_OFFSET` and `MIRRORTO_TITLE` are copy-pasted between `bot.py` and `capture_templates.py`. Changing offsets requires editing both files manually.

**Fix recommended**: extract to a shared `config.py`.

## Medium — Missing template: `confirm_btn`
`templates/confirm_btn.png` not present. The bot references it in `detect_state` and `handle_confirm_popup` but will silently skip it (template loads as `None`, `find_template` returns `None`). The replacement popup will never be handled.

## Medium — `SetProcessDpiAwareness` called in loop
Even if DPI awareness were consistent, calling it on every screenshot iteration is wasteful and technically incorrect (the call is idempotent after the first set, but it's a system-level side-effect that belongs at process startup).

## Low — Unpinned dependencies
`requirements.txt` has no version pins. `opencv-python`, `pyautogui`, and `pywin32` have had breaking API changes in the past.

## Low — `EXPECTED_SIZE = None` is dead code
Defined at module level in `bot.py`, never assigned or read after initialization.

## Low — Wheel handler double-click heuristic
`handle_wheel` clicks the button, waits 3 seconds, then clicks again if the button is still visible — this may double-trigger if the animation completes quickly and a different state appears.
