# Testing

## Current state: no automated tests.

## Manual validation flow
1. Run `capture_templates.py` → visually verify saved PNGs look correct
2. Run `bot.py` → watch log output to confirm state detection and clicks
3. Check `consecutive_unknown` counter — high values mean templates don't match

## Known gap
Templates captured by `capture_templates.py::screenshot_window` (no DPI awareness set) differ in pixel content from frames captured by `bot.py::screenshot_window` (DPI awareness set inside the function). This makes manual validation unreliable — templates that look correct may still fail matching at runtime.

## Suggested test approach (not implemented)
- Save a reference screenshot from the bot's own capture path
- Run `find_template` against it offline to verify confidence scores before deploying
