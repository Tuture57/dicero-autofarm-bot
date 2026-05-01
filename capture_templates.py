"""
Utility to capture template images from the MirrorTo window.
Run this script, wait for the right screen state in the game,
then press the key to capture the region.
"""
import cv2
import numpy as np
import os
import win32gui
import win32ui
import ctypes
import config
import questionary
from rich.console import Console
from rich.panel import Panel

console = Console()

ctypes.windll.shcore.SetProcessDpiAwareness(2)

cfg = config.load()

TEMPLATES_DIR      = cfg["templates_dir"]
MIRRORTO_TITLE     = cfg["mirrorto_title"]
GAME_LEFT_OFFSET   = cfg["game_left_offset"]
GAME_TOP_OFFSET    = cfg["game_top_offset"]
GAME_RIGHT_OFFSET  = cfg["game_right_offset"]
GAME_BOTTOM_OFFSET = cfg["game_bottom_offset"]

os.makedirs(TEMPLATES_DIR, exist_ok=True)


def find_mirrorto_window():
    result = []
    def enum_cb(hwnd, _):
        if win32gui.IsWindowVisible(hwnd):
            if MIRRORTO_TITLE.lower() in win32gui.GetWindowText(hwnd).lower():
                result.append(hwnd)
    win32gui.EnumWindows(enum_cb, None)
    return result[0] if result else None


def _printwindow_capture(hwnd):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    w = right - left
    h = bottom - top
    hwnd_dc = win32gui.GetWindowDC(hwnd)
    mfc_dc  = win32ui.CreateDCFromHandle(hwnd_dc)
    save_dc = mfc_dc.CreateCompatibleDC()
    bmp     = win32ui.CreateBitmap()
    bmp.CreateCompatibleBitmap(mfc_dc, w, h)
    save_dc.SelectObject(bmp)
    ctypes.windll.user32.PrintWindow(hwnd, save_dc.GetSafeHdc(), 2)
    bmp_info = bmp.GetInfo()
    bmp_bits = bmp.GetBitmapBits(True)
    img = np.frombuffer(bmp_bits, dtype=np.uint8).reshape(bmp_info['bmHeight'], bmp_info['bmWidth'], 4)
    img = cv2.cvtColor(img, cv2.COLOR_BGRA2BGR)
    save_dc.DeleteDC()
    mfc_dc.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwnd_dc)
    win32gui.DeleteObject(bmp.GetHandle())
    return img


def screenshot_window(hwnd):
    img = _printwindow_capture(hwnd)
    h_img, w_img = img.shape[:2]
    bottom_crop = h_img - GAME_BOTTOM_OFFSET if GAME_BOTTOM_OFFSET > 0 else h_img
    right_crop  = w_img - GAME_RIGHT_OFFSET  if GAME_RIGHT_OFFSET  > 0 else w_img
    return img[GAME_TOP_OFFSET:bottom_crop, GAME_LEFT_OFFSET:right_crop]


def grab_full_window(hwnd):
    return _printwindow_capture(hwnd)


def calibrate_offset(hwnd):
    img = grab_full_window(hwnd)
    h_img, w_img = img.shape[:2]

    console.print(Panel(
        "Dessine un rectangle autour de la zone du jeu uniquement (sans les barres MirrorTo).\n"
        "[dim]Espace/Entrée pour confirmer, C pour annuler.[/dim]",
        title="[bold]Calibration des offsets[/bold]",
        border_style="cyan",
    ))

    roi = cv2.selectROI("Calibration - entoure la zone du jeu", img, fromCenter=False, showCrosshair=True)
    cv2.destroyAllWindows()

    if roi[2] > 0 and roi[3] > 0:
        x, y, w, h = roi
        offsets = (x, y, w_img - (x + w), h_img - (y + h))
        console.print(f"\n  game_left_offset   = [cyan]{offsets[0]}[/cyan]")
        console.print(f"  game_top_offset    = [cyan]{offsets[1]}[/cyan]")
        console.print(f"  game_right_offset  = [cyan]{offsets[2]}[/cyan]")
        console.print(f"  game_bottom_offset = [cyan]{offsets[3]}[/cyan]")
        return offsets
    return None


def _calibrate_clicks(hwnd, title, labels):
    screen = screenshot_window(hwnd)
    if screen is None or screen.size == 0:
        console.print("[red]Erreur : capture vide. Vérifie que MirrorTo est ouvert.[/red]")
        return None

    clicks = []
    display = screen.copy()

    def on_mouse(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            idx = len(clicks)
            if idx < len(labels):
                clicks.append([x, y])
                cv2.circle(display, (x, y), 8, (0, 255, 0), -1)
                cv2.putText(display, labels[idx], (x + 10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                console.print(f"  [green]{labels[idx]}[/green] enregistré : ({x}, {y})")
                cv2.imshow(title, display)

    cv2.namedWindow(title)
    cv2.setMouseCallback(title, on_mouse)
    cv2.imshow(title, display)
    while True:
        key = cv2.waitKey(50) & 0xFF
        if key in (ord('q'), 27):
            break
        if len(clicks) >= len(labels):
            break
    cv2.destroyAllWindows()
    return clicks if len(clicks) == len(labels) else None


def calibrate_cards(hwnd):
    console.print(Panel(
        "Navigue vers l'écran [bold]Select Skill[/bold], puis clique sur chaque carte (1, 2, 3).\n"
        "[dim]Appuie sur Q ou Echap quand tu as fini.[/dim]",
        title="[bold]Calibration cartes de skill[/bold]",
        border_style="cyan",
    ))
    clicks = _calibrate_clicks(hwnd, "Calibration cartes", ["Carte 1", "Carte 2", "Carte 3"])
    if clicks is None:
        console.print("[yellow]Calibration incomplète. Annulé.[/yellow]")
        return
    cfg["card_positions"] = clicks
    config.save(cfg)
    console.print(f"\n[dim]card_positions = {clicks}[/dim]")
    console.print("[green]Positions des cartes sauvegardées.[/green]")


def calibrate_dice(hwnd):
    console.print(Panel(
        "Navigue vers l'écran [bold]Select Dice[/bold], puis clique sur le premier dé (gauche) de la rangée du haut.\n"
        "[dim]Appuie sur Q ou Echap quand tu as fini.[/dim]",
        title="[bold]Calibration position du dé[/bold]",
        border_style="cyan",
    ))
    clicks = _calibrate_clicks(hwnd, "Calibration de", ["De 1 (gauche)"])
    if clicks is None:
        console.print("[yellow]Calibration incomplète. Annulé.[/yellow]")
        return
    cfg["dice_position"] = clicks[0]
    config.save(cfg)
    console.print(f"\n[dim]dice_position = {clicks[0]}[/dim]")
    console.print("[green]Position du dé sauvegardée.[/green]")


def show_and_select(screen, name):
    clone = screen.copy()
    roi = cv2.selectROI(f"Select region for: {name}", clone, fromCenter=False, showCrosshair=True)
    cv2.destroyAllWindows()
    if roi[2] > 0 and roi[3] > 0:
        x, y, w, h = roi
        region = screen[y:y+h, x:x+w]
        path = os.path.join(TEMPLATES_DIR, f"{name}.png")
        cv2.imwrite(path, region)
        console.print(f"[green]Template sauvegardé :[/green] {path} ({w}×{h})")
        return True
    return False


CAPTURES = [
    ("menu_new_game",     "Navigue vers l'ecran Menu principal (bouton New Game visible)"),
    ("attack_btn",        "Navigue vers le donjon principal (bouton Attack visible)"),
    ("select_skill_v1",   "Navigue vers Select Skill variante 1 (texte seul, sans dessin)"),
    ("select_skill_v2",   "Navigue vers Select Skill variante 2 (texte avec dessin)"),
    ("angel_select",      "Navigue vers Angel Select (ange a la place du texte)"),
    ("try_luck_btn",      "Navigue vers la roue (bouton Try Your Luck visible)"),
    ("select_dice_text",  "Navigue vers Select Dice (texte Select Dice visible)"),
    ("confirm_btn",       "Navigue vers la popup de confirmation (bouton Confirm visible)"),
    ("rewards_btn",       "Navigue vers l'ecran Recompenses (bouton de collecte visible)"),
    ("chest_btn",         "Navigue vers l'ecran du coffre (bouton pour ouvrir le coffre visible)"),
    ("edit_btn",          "Navigue vers l'ecran apres selection du de (bouton Edit visible)"),
]


def main():
    global GAME_LEFT_OFFSET, GAME_TOP_OFFSET, GAME_RIGHT_OFFSET, GAME_BOTTOM_OFFSET

    hwnd = find_mirrorto_window()
    if not hwnd:
        console.print("[red]Fenêtre MirrorTo introuvable. Lance MirrorTo, puis réessaie.[/red]")
        return
    console.print(f"[dim]Fenêtre MirrorTo trouvée (hwnd={hwnd})[/dim]")

    result = calibrate_offset(hwnd)
    if result is not None:
        l, t, r, b = result
        GAME_LEFT_OFFSET, GAME_TOP_OFFSET, GAME_RIGHT_OFFSET, GAME_BOTTOM_OFFSET = l, t, r, b
        cfg["game_left_offset"]   = l
        cfg["game_top_offset"]    = t
        cfg["game_right_offset"]  = r
        cfg["game_bottom_offset"] = b
        config.save(cfg)
        console.print("[green]Offsets sauvegardés dans config.json.[/green]\n")

    while True:
        choices = []
        for name, _ in CAPTURES:
            path = os.path.join(TEMPLATES_DIR, f'{name}.png')
            choices.append(questionary.Choice(
                title=f"{name}  [{'existe' if os.path.exists(path) else 'manquant':8}]",
                value=name,
            ))
        choices.append(questionary.Choice(title="Calibrer les positions des cartes de skill", value="calib_cards"))
        choices.append(questionary.Choice(title="Calibrer la position du dé", value="calib_dice"))
        choices.append(questionary.Separator())
        choices.append(questionary.Choice(title="Quitter", value="quit"))

        choice = questionary.select(
            "Que veux-tu capturer ou calibrer ?",
            choices=choices,
            pointer="»",
        ).ask()

        if choice is None or choice == "quit":
            console.print("[dim]Terminé.[/dim]")
            break

        if choice == "calib_cards":
            hwnd = find_mirrorto_window()
            if not hwnd:
                console.print("[red]Fenêtre MirrorTo perdue. Relance MirrorTo.[/red]")
                continue
            calibrate_cards(hwnd)
            continue

        if choice == "calib_dice":
            hwnd = find_mirrorto_window()
            if not hwnd:
                console.print("[red]Fenêtre MirrorTo perdue. Relance MirrorTo.[/red]")
                continue
            calibrate_dice(hwnd)
            continue

        idx = next(i for i, (n, _) in enumerate(CAPTURES) if n == choice)
        name, instruction = CAPTURES[idx]
        path = os.path.join(TEMPLATES_DIR, f'{name}.png')

        if os.path.exists(path):
            overwrite = questionary.confirm(
                f"'{name}.png' existe déjà. Écraser ?",
                default=False,
            ).ask()
            if not overwrite:
                console.print("[yellow]Annulé.[/yellow]")
                continue

        console.print(Panel(
            f"{instruction}\n[dim]Appuie sur Entrée quand le bon écran est visible dans MirrorTo...[/dim]",
            title=f"[bold]{name}[/bold]",
            border_style="blue",
        ))
        input()

        hwnd = find_mirrorto_window()
        if not hwnd:
            console.print("[red]Fenêtre MirrorTo perdue. Relance MirrorTo.[/red]")
            continue

        screen = screenshot_window(hwnd)
        if screen is None or screen.size == 0:
            console.print("[red]Erreur : capture vide. Vérifie que MirrorTo est ouvert et non minimisé.[/red]")
            continue

        saved = show_and_select(screen, name)
        if saved:
            console.print(f"[green]Template '{name}' sauvegardé avec succès.[/green]")
        else:
            console.print("[yellow]Capture annulée (aucun rectangle sélectionné).[/yellow]")


if __name__ == "__main__":
    main()
