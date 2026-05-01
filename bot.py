import cv2
import numpy as np
import time
import os
import random
import threading
from PIL import Image, ImageGrab
import logging
from rich.logging import RichHandler
import win32gui
import win32api
import win32con
import win32ui
import ctypes
import ctypes.wintypes
import config

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
    datefmt="[%H:%M:%S]",
    handlers=[RichHandler(rich_tracebacks=True)],
)
log = logging.getLogger(__name__)

cfg = config.load()

TEMPLATES_DIR    = cfg["templates_dir"]
MIRRORTO_TITLE   = cfg["mirrorto_title"]
CONFIDENCE       = cfg["confidence"]
LOOP_DELAY       = cfg["loop_delay"]
CLICK_DELAY      = cfg["click_delay"]
WHEEL_WAIT       = cfg["wheel_wait"]
GAME_LEFT_OFFSET   = cfg["game_left_offset"]
GAME_TOP_OFFSET    = cfg["game_top_offset"]
GAME_RIGHT_OFFSET  = cfg["game_right_offset"]
GAME_BOTTOM_OFFSET = cfg["game_bottom_offset"]

_user32 = ctypes.windll.user32
ctypes.windll.shcore.SetProcessDpiAwareness(2)

_console_hwnd = ctypes.windll.kernel32.GetConsoleWindow()
_stop_event = threading.Event()


def _listen_escape():
    import msvcrt
    while not _stop_event.is_set():
        if msvcrt.kbhit():
            ch = msvcrt.getch()
            if ch == b'\x1b':
                log.info("Echap détecté, arrêt en cours...")
                _stop_event.set()
                return
        time.sleep(0.05)


def _shutdown(console_hwnd):
    _stop_event.set()
    if console_hwnd:
        _user32.ShowWindow(console_hwnd, 9)
        _user32.SetForegroundWindow(console_hwnd)
    log.info("Bot arrêté.")


def find_mirrorto_window():
    result = []
    def enum_cb(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            title = win32gui.GetWindowText(hwnd)
            if MIRRORTO_TITLE.lower() in title.lower():
                result.append(hwnd)
    win32gui.EnumWindows(enum_cb, None)
    return result[0] if result else None


def get_window_rect(hwnd):
    return win32gui.GetWindowRect(hwnd)


def screenshot_window(hwnd):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bottom - top
    if w < 10 or h < 10:
        return None, (left, top)

    hwnd_dc = win32gui.GetWindowDC(hwnd)
    mfc_dc  = win32ui.CreateDCFromHandle(hwnd_dc)
    save_dc = mfc_dc.CreateCompatibleDC()
    bmp     = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(mfc_dc, w, h)
    save_dc.SelectObject(bmp)

    # PW_RENDERFULLCONTENT = 2, rend la fenêtre même cachée/derrière
    ctypes.windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 2)

    bmp_info = bmp.GetInfo()
    bmp_bits = bmp.GetBitmapBits(True)
    img = np.frombuffer(bmp_bits, dtype=np.uint8).reshape(bmp_info['bmHeight'], bmp_info['bmWidth'], 4)
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)

    save_dc.DeleteDC()
    mfc_dc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwnd_dc)
    win32gui.DeleteObject(bmp.GetHandle())

    h_img, w_img = img.shape[:2]
    bottom_crop = h_img - GAME_BOTTOM_OFFSET if GAME_BOTTOM_OFFSET > 0 else h_img
    right_crop  = w_img - GAME_RIGHT_OFFSET  if GAME_RIGHT_OFFSET  > 0 else w_img
    img = img[GAME_TOP_OFFSET:bottom_crop, GAME_LEFT_OFFSET:right_crop]
    w_game = right_crop - GAME_LEFT_OFFSET
    h_game = bottom_crop - GAME_TOP_OFFSET
    if w_game < 100 or h_game < 100:
        return None, (left, top)
    return img, (left, top)


def click_in_window(hwnd, x, y):
    win_x = GAME_LEFT_OFFSET + int(x)
    win_y = GAME_TOP_OFFSET + int(y)
    lparam = win32api.MAKELONG(win_x, win_y)
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONDOWN, win32con.MK_LBUTTON, lparam)
    time.sleep(0.05)
    win32gui.PostMessage(hwnd, win32con.WM_LBUTTONUP, 0, lparam)
    time.sleep(CLICK_DELAY)


def load_template(name):
    path = os.path.join(TEMPLATES_DIR, name)
    if not os.path.exists(path):
        return None
    return cv2.imread(path, cv2.IMREAD_COLOR)


def find_template(screen, template, confidence=None):
    if template is None:
        return None
    if confidence is None:
        confidence = CONFIDENCE
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    _, max_val, _, max_loc = cv2.minMaxLoc(result)
    if max_val >= confidence:
        h, w = template.shape[:2]
        cx = max_loc[0] + w // 2
        cy = max_loc[1] + h // 2
        return (cx, cy, max_val)
    return None


def find_all_templates(screen, template, confidence=None):
    if template is None:
        return []
    if confidence is None:
        confidence = CONFIDENCE
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= confidence)
    h, w = template.shape[:2]
    matches = []
    for pt in zip(*locations[::-1]):
        cx = pt[0] + w // 2
        cy = pt[1] + h // 2
        matches.append((cx, cy))
    return _deduplicate(matches, min_dist=30)


def _deduplicate(points, min_dist=30):
    result = []
    for p in points:
        if not any(abs(p[0]-r[0]) < min_dist and abs(p[1]-r[1]) < min_dist for r in result):
            result.append(p)
    return result


def detect_state(screen, templates):
    if templates.get("rewards_btn") is not None:
        if find_template(screen, templates["rewards_btn"]):
            return "rewards"

    if templates.get("confirm_btn") is not None:
        if find_template(screen, templates["confirm_btn"]):
            return "confirm_popup"

    if templates.get("try_luck_btn") is not None:
        if find_template(screen, templates["try_luck_btn"]):
            return "wheel"

    if templates.get("select_dice_text") is not None:
        if find_template(screen, templates["select_dice_text"]):
            return "select_dice"

    if templates.get("edit_btn") is not None:
        if find_template(screen, templates["edit_btn"]):
            return "edit_btn"

    skill_templates = ["select_skill_v1", "select_skill_v2", "angel_select"]
    for key in skill_templates:
        if templates.get(key) is not None:
            if find_template(screen, templates[key]):
                return "select_skill"

    if templates.get("chest_btn") is not None:
        if find_template(screen, templates["chest_btn"]):
            return "chest"

    if templates.get("attack_btn") is not None:
        if find_template(screen, templates["attack_btn"]):
            return "dungeon"

    if templates.get("menu_new_game") is not None:
        if find_template(screen, templates["menu_new_game"]):
            return "menu"

    return "unknown"


def handle_dungeon(hwnd, screen, templates):
    match = find_template(screen, templates["attack_btn"])
    if match:
        log.debug("Clicking Attack")
        click_in_window(hwnd, match[0], match[1])
        return True
    return False


def handle_wheel(hwnd, screen, templates):
    match = find_template(screen, templates["try_luck_btn"])
    if match:
        log.debug("Clicking Try Your Luck")
        click_in_window(hwnd, match[0], match[1])
        time.sleep(WHEEL_WAIT)
        screen2, _ = screenshot_window(hwnd)
        if screen2 is not None:
            match2 = find_template(screen2, templates["try_luck_btn"])
            if match2:
                click_in_window(hwnd, match2[0], match2[1])
        return True
    return False


def handle_select_skill(hwnd, screen, templates):
    positions = cfg.get("card_positions")
    if not positions:
        log.error("Positions des cartes non calibrées. Lance 'Calibrer les templates' depuis le menu.")
        return False
    chosen = random.choice(positions)
    log.debug(f"Selecting skill card at {chosen}")
    click_in_window(hwnd, chosen[0], chosen[1])
    return True


def handle_select_dice(hwnd, screen, templates):
    pos = cfg.get("dice_position")
    if not pos:
        log.error("Position du dé non calibrée. Lance 'Calibrer les templates' depuis le menu.")
        return False
    log.debug(f"Selecting die at {pos}")
    click_in_window(hwnd, pos[0], pos[1])
    return True


def handle_chest(hwnd, screen, templates):
    match = find_template(screen, templates["chest_btn"])
    if match:
        log.debug("Clicking chest button")
        click_in_window(hwnd, match[0], match[1])
        return True
    return False


def handle_edit_btn(hwnd, screen, templates):
    match = find_template(screen, templates["edit_btn"])
    if match:
        log.debug("Clicking Edit button")
        click_in_window(hwnd, match[0], match[1])
        return True
    return False


def handle_menu(hwnd, screen, templates):
    match = find_template(screen, templates["menu_new_game"])
    if match:
        log.debug("Clicking New Game on menu")
        click_in_window(hwnd, match[0], match[1])
        return True
    return False


def handle_rewards(hwnd, screen, templates):
    match = find_template(screen, templates["rewards_btn"])
    if match:
        log.debug("Clicking rewards button")
        click_in_window(hwnd, match[0], match[1])
        time.sleep(2.0)
        return True
    return False


def handle_confirm_popup(hwnd, screen, templates):
    match = find_template(screen, templates["confirm_btn"])
    if match:
        log.debug("Clicking Confirm on popup")
        click_in_window(hwnd, match[0], match[1])
        return True
    return False


def main():
    ctypes.windll.shcore.SetProcessDpiAwareness(2)
    os.makedirs(TEMPLATES_DIR, exist_ok=True)

    hwnd = find_mirrorto_window()
    if not hwnd:
        log.error(f"Fenêtre MirrorTo introuvable. Lance MirrorTo, puis réessaie.")
        return

    rect = get_window_rect(hwnd)
    ref_w = rect[2] - rect[0]
    ref_h = rect[3] - rect[1]
    log.debug(f"Fenêtre MirrorTo trouvée : hwnd={hwnd}, taille={ref_w}x{ref_h}")

    console_hwnd = ctypes.windll.kernel32.GetConsoleWindow()
    if console_hwnd:
        ctypes.windll.user32.ShowWindow(console_hwnd, 6)
        time.sleep(0.2)

    ctypes.windll.user32.ShowWindow(hwnd, 9)
    ctypes.windll.user32.SetForegroundWindow(hwnd)
    time.sleep(0.3)
    log.info("Bot démarré, appuie sur Echap pour arrêter.")

    templates_to_load = [
        "menu_new_game",
        "attack_btn",
        "select_skill_v1",
        "select_skill_v2",
        "angel_select",
        "try_luck_btn",
        "select_dice_text",
        "confirm_btn",
        "rewards_btn",
        "chest_btn",
        "edit_btn",
    ]

    templates = {}
    for name in templates_to_load:
        t = load_template(f"{name}.png")
        templates[name] = t
        if t is None:
            log.warning(f"Template manquant : {name}.png, recalibre les templates depuis le menu.")

    log.info(f"Templates chargés : {sum(1 for v in templates.values() if v is not None)}/{len(templates_to_load)}")

    esc_thread = threading.Thread(target=_listen_escape, daemon=True)
    esc_thread.start()

    consecutive_unknown = 0
    last_state = None

    while not _stop_event.is_set():
        try:
            hwnd = find_mirrorto_window()
            if not hwnd:
                log.warning("Fenêtre MirrorTo perdue., nouvelle tentative...")
                time.sleep(2)
                continue

            cur_rect = get_window_rect(hwnd)
            cur_w = cur_rect[2] - cur_rect[0]
            cur_h = cur_rect[3] - cur_rect[1]
            if cur_w != ref_w or cur_h != ref_h:
                log.warning(f"Taille de fenêtre changée ({cur_w}x{cur_h} au lieu de {ref_w}x{ref_h}). Les templates peuvent ne plus fonctionner.")

            screen, _ = screenshot_window(hwnd)
            if screen is None:
                log.warning("Fenêtre trop petite ou minimisée., en attente...")
                time.sleep(1)
                continue
            state = detect_state(screen, templates)

            if state == "unknown":
                consecutive_unknown += 1
                if consecutive_unknown % 10 == 0:
                    log.warning(f"État inconnu depuis {consecutive_unknown} cycles., vérification en cours...")
                time.sleep(LOOP_DELAY)
                continue

            consecutive_unknown = 0
            if state != last_state:
                log.info(f"État : {state}")
                last_state = state

            if state == "dungeon":
                handle_dungeon(hwnd, screen, templates)
            elif state == "wheel":
                handle_wheel(hwnd, screen, templates)
            elif state == "select_skill":
                handle_select_skill(hwnd, screen, templates)
            elif state == "select_dice":
                handle_select_dice(hwnd, screen, templates)
            elif state == "confirm_popup":
                handle_confirm_popup(hwnd, screen, templates)
            elif state == "menu":
                handle_menu(hwnd, screen, templates)
            elif state == "rewards":
                handle_rewards(hwnd, screen, templates)
            elif state == "chest":
                handle_chest(hwnd, screen, templates)
            elif state == "edit_btn":
                handle_edit_btn(hwnd, screen, templates)

            time.sleep(LOOP_DELAY)

        except KeyboardInterrupt:
            _stop_event.set()
        except Exception as e:
            log.error(f"Erreur inattendue : {e}")
            time.sleep(1)

    _shutdown(console_hwnd)


if __name__ == "__main__":
    main()
