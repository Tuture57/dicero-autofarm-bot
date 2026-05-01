# Phase 2 Research

**Date:** 2026-04-30
**Phase:** 02-bot-complet-tous-les-etats-toutes-les-actions
**Researcher:** Claude Sonnet 4.6

---

## Key Findings

### 1. State Detection Gaps — How to Structure detect_state

**Current bot.py** (lines 117-138) has these states in order:
`confirm_popup > wheel > select_dice > select_skill > dungeon > unknown`

**REQUIREMENTS.md** defines 9 states: STATE-01 (menu) through STATE-09 (rewards).
**CONTEXT.md D-03** says ACT-03 applies to Select Skill v1, v2, AND Angel Select — same click action.

**Decision (from CONTEXT.md Claude's Discretion):** Keep all 3 skill variants (v1/v2/angel) as a SINGLE detected state called `select_skill` — detected by checking any of the 3 templates (`select_skill_v1`, `select_skill_v2`, `angel_select`). One handler covers all 3.

**New detect_state order (CONTEXT.md):**
```
rewards > confirm_popup > wheel > select_dice > select_skill > dungeon > menu > unknown
```
Rewards is highest priority because it is the terminal state of a run — missing it would cause the bot to loop forever on a completed run.

**Concrete implementation for detect_state:**
- Check `rewards_btn` template → `"rewards"`
- Check `confirm_btn` template → `"confirm_popup"`
- Check `try_luck_btn` template → `"wheel"`
- Check `select_dice_text` template → `"select_dice"`
- Check `select_skill_v1` OR `select_skill_v2` OR `angel_select` template → `"select_skill"`
- Check `attack_btn` template → `"dungeon"`
- Check `menu_new_game` template → `"menu"`
- Return `"unknown"`

### 2. Config.json Extension — card_positions and dice_position

**Current config.py `_DEFAULTS`** (lines 6-17) does NOT include `card_positions` or `dice_position`.

**CONTEXT.md D-02:** `card_positions` = list of 3 `[x, y]` pairs (relative to game area).
**CONTEXT.md D-05:** `dice_position` = single `[x, y]` pair (relative to game area).

**Handling missing keys (not-yet-calibrated):** The `config.load()` function (config.py line 20-25) uses `{**_DEFAULTS, **data}` — so keys absent from both `_DEFAULTS` and `config.json` will simply be absent from the returned dict. 

**Pattern for bot.py handlers:**
```python
card_positions = cfg.get("card_positions")   # None if not calibrated
dice_position  = cfg.get("dice_position")    # None if not calibrated
```
If `None`, log an error and skip (do NOT use pixel-fraction fallbacks — CONTEXT.md D-10 says positions fixes only, no template matching on cards/dice).

**Add to _DEFAULTS in config.py:**
```python
"card_positions": None,
"dice_position": None,
```
This makes `cfg.get("card_positions")` return `None` by default, which is explicit and safe.

### 3. Calibration UX in capture_templates.py — Click to Record Point

**CONTEXT.md D-07:** Add calibration option to the menu in `capture_templates.py`.
**CONTEXT.md D-06:** Interactive click (NOT selectROI rectangle) — user clicks on the card/die.
**CONTEXT.md specifics:** Show game capture, user clicks on each card/die, record pixel position relative to game area.

**OpenCV implementation pattern:**
```python
def calibrate_positions(hwnd):
    screen = screenshot_window(hwnd)  # already cropped to game area
    points = []
    window_name = "Calibration — clique sur chaque carte/de"

    def on_mouse(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            points.append([x, y])
            # draw a marker so user sees where they clicked
            cv2.circle(display, (x, y), 5, (0, 255, 0), -1)
            cv2.imshow(window_name, display)

    display = screen.copy()
    cv2.namedWindow(window_name)
    cv2.setMouseCallback(window_name, on_mouse)
    cv2.imshow(window_name, display)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return points
```

**Two separate calibration flows:**
1. **Cards:** Show select_skill screen, user clicks 3 times (card 1, 2, 3), save as `card_positions`.
2. **First die:** Show select_dice screen, user clicks once on leftmost die, save as `dice_position`.

**Menu integration:** Add option `C` (or a numbered option like `10`) in the `while True` loop of `main()` — separate from the 9 template capture options. Must save to `config.json` via `config.save(cfg)`.

### 4. Template Set Alignment — Old vs New

**Current bot.py `templates_to_load`** (lines 221-229):
```
attack_btn, select_skill_text, select_dice_text, try_luck_btn, confirm_btn, skill_card, active_die
```

**New template set (REQUIREMENTS.md TMPL-05 / CONTEXT.md canonical):**
```
menu_new_game, attack_btn, select_skill_v1, select_skill_v2, angel_select,
try_luck_btn, select_dice_text, confirm_btn, rewards_btn
```

**Templates on disk (already captured in Phase 1):**
```
menu_new_game.png      ✓
attack_btn.png         ✓
select_skill_v1.png    ✓
select_skill_v2.png    ✓
angel_select.png       ✓
try_luck_btn.png       ✓
select_dice_text.png   ✓
confirm_btn.png        ✓
rewards_btn.png        ✓
```
All 9 required templates exist on disk. The old `skill_card.png` and `active_die.png` remain on disk but are no longer used by the new bot.

**Action:** Replace `templates_to_load` list in `main()` and update all `templates["select_skill_text"]` references to `templates["select_skill_v1"]` etc.

### 5. State Detection Priority — Why Rewards First

From CONTEXT.md Claude's Discretion: rewards is a **terminal state** for the run. If the Rewards screen is up and the bot doesn't detect it before checking `attack_btn`, it might match `attack_btn` if it's partially visible in the transition, causing a stuck loop. Checking rewards first guarantees clean detection.

The full priority rationale:
- `rewards` — terminal state, must not be missed
- `confirm_popup` — blocking popup, must be cleared before anything
- `wheel` — blocking animation screen
- `select_dice` — blocking selection screen
- `select_skill` — blocking selection screen
- `dungeon` — normal play state
- `menu` — start/end of run
- `unknown` — catch-all

### 6. handle_select_skill Redesign

**Current bot.py** (lines 165-177): tries `skill_card` template → falls back to pixel fractions.

**New design (CONTEXT.md D-10):**
```python
def handle_select_skill(hwnd, screen, templates, cfg):
    positions = cfg.get("card_positions")
    if not positions or len(positions) < 1:
        log.error("card_positions not calibrated — run capture_templates.py first")
        return False
    chosen = random.choice(positions)
    log.info(f"Selecting skill card at fixed position {chosen}")
    click_in_window(hwnd, chosen[0], chosen[1])
    return True
```
Note: `cfg` must be passed in or accessed as module-level `cfg` (already loaded at line 19 of bot.py). Since `cfg` is a module-level dict, it can be re-read or referenced directly.

**Same pattern for handle_select_dice:**
```python
def handle_select_dice(hwnd, screen, templates, cfg):
    position = cfg.get("dice_position")
    if not position:
        log.error("dice_position not calibrated — run capture_templates.py first")
        return False
    log.info(f"Selecting first die at fixed position {position}")
    click_in_window(hwnd, position[0], position[1])
    return True
```

### 7. handle_menu — New Handler

Simple template match + click:
```python
def handle_menu(hwnd, screen, templates):
    match = find_template(screen, templates["menu_new_game"])
    if match:
        log.info("Clicking New Game")
        click_in_window(hwnd, match[0], match[1])
        return True
    return False
```

### 8. handle_rewards — New Handler

Per CONTEXT.md Claude's Discretion: click rewards_btn, wait 2s, return to cycle. The detect_state loop will pick up `menu` state on the next iteration.
```python
def handle_rewards(hwnd, screen, templates):
    match = find_template(screen, templates["rewards_btn"])
    if match:
        log.info("Collecting rewards")
        click_in_window(hwnd, match[0], match[1])
        time.sleep(2.0)
        return True
    return False
```

### 9. Plan Structure — 2 Independent Plans, Wave 1 (Parallel)

**Plan A — bot.py rewrite:**
- Files: `bot.py`
- Changes: templates_to_load list, detect_state order, handle_select_skill, handle_select_dice, handle_menu (new), handle_rewards (new), main() dispatch block
- Requirements: STATE-01 to STATE-09, ACT-01 to ACT-07

**Plan B — capture_templates.py calibration extension:**
- Files: `capture_templates.py`, `config.py`, `config.json`
- Changes: add calibrate_positions() function, add menu option for calibration, update _DEFAULTS with card_positions/dice_position
- Requirements: D-01 through D-08

These two plans are **independent** (different files, no shared state during implementation) and can be executed in **Wave 1 in parallel**.

### 10. Reusable Assets Confirmed (Phase 1 verified)

From reading bot.py (current state, post-Phase 1):
- `screenshot_window(hwnd)` — returns `(img, (left, top))`, uses ImageGrab (line 48-60) ✓
- `click_in_window(hwnd, x, y)` — uses game-area-relative coords (lines 63-68) ✓
- `find_template` / `find_all_templates` — stable, reusable (lines 78-114) ✓
- `config.load()` / `config.save()` — used in both scripts ✓
- `SetProcessDpiAwareness(2)` — called once in main() (line 208) ✓

**No regressions to avoid:** Phase 1 delivered the exact capture method (ImageGrab) and menu structure. Phase 2 must NOT change screenshot_window, click_in_window, or the calibrate_offset function.

---

## Validation Architecture

### How to verify bot.py rewrite works

1. **Template loading:** `python -c "import bot"` — no ImportError, no missing template warnings for the 9 canonical templates (all exist on disk).

2. **State detection unit test (manual):** Run bot.py with each game screen visible, confirm log output shows correct state name.

3. **Calibration prerequisite check:** Before testing ACT-03/ACT-05, run capture_templates.py calibration option and verify `config.json` contains `card_positions` (3 entries) and `dice_position` (1 entry).

4. **Full cycle test (human UAT):**
   - Start bot at menu → verify `menu` state detected, New Game clicked
   - Dungeon → verify `dungeon` state, Attack clicked in loop
   - Select Skill → verify `select_skill` detected, one of 3 card positions clicked
   - Wheel → verify `wheel` detected, Try Your Luck clicked
   - Select Dice → verify `select_dice` detected, first die position clicked
   - Confirm Popup → verify `confirm_popup` detected, Confirm clicked
   - Rewards → verify `rewards` detected, button clicked, bot returns to menu

5. **Regression check:** Window-too-small handling — `screen is None` path in main() loop still present after rewrite.

### Key risk: card_positions not yet calibrated

If the user runs bot.py before running the calibration option in capture_templates.py:
- `cfg.get("card_positions")` returns `None`
- `handle_select_skill` logs error and returns `False`
- Bot logs "Unknown action" or similar — does NOT crash
- This is acceptable for v1 — ROB-01/02 are v2 concerns

---

## RESEARCH COMPLETE

**Files read:**
- `C:\Users\barto\Desktop\autofarm\bot.py` (lines 1-297)
- `C:\Users\barto\Desktop\autofarm\capture_templates.py` (lines 1-173)
- `C:\Users\barto\Desktop\autofarm\config.py` (lines 1-31)
- `C:\Users\barto\Desktop\autofarm\config.json` (lines 1-14)
- `C:\Users\barto\Desktop\autofarm\.planning\REQUIREMENTS.md` (lines 1-99)
- `C:\Users\barto\Desktop\autofarm\.planning\ROADMAP.md` (lines 1-50)
- `C:\Users\barto\Desktop\autofarm\.planning\STATE.md` (lines 1-28)
- `C:\Users\barto\Desktop\autofarm\.planning\phases\02-.../02-CONTEXT.md` (lines 1-103)
- `C:\Users\barto\Desktop\autofarm\.planning\phases\02-.../02-DISCUSSION-LOG.md` (lines 1-51)
- `C:\Users\barto\Desktop\autofarm\.planning\phases\01-.../01-PLAN-01-imagegrab-capture.md`
- `C:\Users\barto\Desktop\autofarm\.planning\phases\01-.../01-PLAN-02-menu-interactif-templates.md`
- Templates directory listing (12 files, all 9 canonical templates confirmed present)

**Key constraint discovered:** `card_positions` and `dice_position` are not in `_DEFAULTS` today — must add them as `None` to make `cfg.get()` behavior explicit and consistent.

**Architectural clarity:** 2 independent plans (bot.py rewrite + capture_templates.py calibration) → Wave 1 parallel execution. No cross-plan dependency during implementation.
