# Conventions

## Style
- Single-file modules (no packages, no classes)
- Functions named `handle_<state>`, `find_*`, `screenshot_*`, `get_*`
- Module-level constants in `UPPER_SNAKE_CASE`
- `log = logging.getLogger(__name__)` with `logging.INFO`
- French-language comments and print strings; English identifiers

## Error handling
- `KeyboardInterrupt` caught in main loop → clean exit
- Generic `Exception` caught → log error, sleep 1s, continue
- Missing templates → `log.warning` + geometric fallback click
- Window lost mid-run → log.warning, sleep 2s, retry

## No tests, no type hints, no docstrings.
## No CLI argument parsing (all config via module-level constants).
