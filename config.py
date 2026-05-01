import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "config.json")

_DEFAULTS = {
    "mirrorto_title": "MirrorTo",
    "templates_dir": "templates",
    "game_left_offset": 80,
    "game_top_offset": 80,
    "game_right_offset": 22,
    "game_bottom_offset": 82,
    "confidence": 0.75,
    "loop_delay": 0.5,
    "click_delay": 0.3,
    "wheel_wait": 3.0,
    "card_positions": None,
    "dice_position": None,
}


def load():
    if not os.path.exists(CONFIG_PATH):
        return dict(_DEFAULTS)
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {**_DEFAULTS, **data}


def save(cfg):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=4)
