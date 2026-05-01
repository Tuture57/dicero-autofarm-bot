# Structure

```
autofarm/
├── bot.py                  # Main bot — state machine + handlers
├── capture_templates.py    # Interactive template capture utility
├── requirements.txt        # pip dependencies (5 packages, unpinned)
├── README.md               # Usage guide (FR/EN mixed)
└── templates/              # Captured PNG reference images
    ├── attack_btn.png
    ├── select_skill_text.png
    ├── select_dice_text.png
    ├── try_luck_btn.png
    ├── skill_card.png
    ├── active_die.png
    └── (confirm_btn.png)   # missing — not yet captured
```

## Key constants (duplicated in both py files)
| Constant | Value | Meaning |
|---|---|---|
| `GAME_LEFT_OFFSET` | 80 | MirrorTo left chrome (icons bar) |
| `GAME_TOP_OFFSET` | 80 | MirrorTo top chrome (title bar) |
| `GAME_RIGHT_OFFSET` | 22 | MirrorTo right border |
| `GAME_BOTTOM_OFFSET` | 82 | MirrorTo bottom chrome (Android nav) |
| `CONFIDENCE` | 0.75 | cv2.TM_CCOEFF_NORMED threshold |
| `LOOP_DELAY` | 0.5s | Main loop sleep |
| `CLICK_DELAY` | 0.3s | Post-click sleep |
