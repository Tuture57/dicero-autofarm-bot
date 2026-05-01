# Architecture

## Pattern: Polling state machine

```
main()
  └─ find_mirrorto_window()          # Win32 HWND lookup by title
  └─ load templates (PNG → cv2)
  └─ loop forever:
        screenshot_window(hwnd)      # BitBlt → numpy array, cropped to game area
        detect_state(screen, tpl)    # priority-ordered template matching
        handle_<state>(hwnd, screen, tpl)   # click logic per state
        time.sleep(LOOP_DELAY)
```

## State detection priority (hardcoded order)
1. `confirm_popup` — must be handled before skill/dice screens
2. `wheel` — try-your-luck button present
3. `select_dice` — dice selection text present
4. `select_skill` — skill selection text present
5. `dungeon` — attack button present
6. `unknown` — no match (throttled logging, skip cycle)

## Coordinate system
- `screenshot_window` crops the raw BitBlt image by fixed offsets (`GAME_*_OFFSET`) → game-only pixels
- `find_template` returns `(cx, cy)` in cropped-image space
- `click_in_window` converts back: `screen_x = win_left + GAME_LEFT_OFFSET + cx`

## Capture utility (`capture_templates.py`)
- Interactive CLI: calibrates offsets via `cv2.selectROI`, then loops through 7 named templates
- Saves cropped PNG regions to `templates/`
- Separate from bot.py but shares the same offset constants and BitBlt screenshot logic

## Known architectural issue
`bot.py::screenshot_window` calls `SetProcessDpiAwareness(2)` on **every** screenshot (inside the loop) — it should be called once at startup. `capture_templates.py::screenshot_window` does NOT set DPI awareness, while `grab_full_window` does — causing pixel mismatch between captured templates and bot screenshots.
