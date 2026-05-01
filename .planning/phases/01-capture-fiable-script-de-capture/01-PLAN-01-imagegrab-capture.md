---
phase: 1
plan: 01
title: Réécrire la capture d'écran avec ImageGrab
type: execute
wave: 1
depends_on: []
files_modified:
  - bot.py
  - capture_templates.py
autonomous: true
requirements:
  - CAP-01
  - CAP-02
  - CAP-03
---

<objective>
Remplacer la méthode de capture BitBlt/PrintWindow par `PIL.ImageGrab.grab(bbox=...)` dans `bot.py` ET `capture_templates.py`. Appeler `SetProcessDpiAwareness(2)` une seule fois au démarrage de chaque script. Les coordonnées de clic dans `bot.py` deviennent left+GAME_LEFT_OFFSET+x, top+GAME_TOP_OFFSET+y (inchangé). La même méthode est utilisée dans les deux scripts — pixels identiques garantis.
</objective>

<tasks>

<task id="1.1">
<type>execute</type>
<title>Réécrire screenshot_window dans bot.py avec ImageGrab</title>
<read_first>
- bot.py (lire la fonction screenshot_window et l'import section en entier avant de toucher quoi que ce soit)
</read_first>
<action>
1. Ajouter `SetProcessDpiAwareness(2)` une seule fois dans `main()` avant la boucle principale (ligne ~ligne 221, avant `os.makedirs`). Ne pas l'appeler dans `screenshot_window`.

2. Remplacer la fonction `screenshot_window` (lignes ~48-77) par :

```python
def screenshot_window(hwnd):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    img = ImageGrab.grab(bbox=(left, top, right, bottom))
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    h_img, w_img = img.shape[:2]
    bottom_crop = h_img - GAME_BOTTOM_OFFSET if GAME_BOTTOM_OFFSET > 0 else h_img
    right_crop = w_img - GAME_RIGHT_OFFSET if GAME_RIGHT_OFFSET > 0 else w_img
    img = img[GAME_TOP_OFFSET:bottom_crop, GAME_LEFT_OFFSET:right_crop]
    w_game = right_crop - GAME_LEFT_OFFSET
    h_game = bottom_crop - GAME_TOP_OFFSET
    if w_game < 100 or h_game < 100:
        return None, (left, top)
    return img, (left, top)
```

3. Supprimer les imports devenus inutiles dans bot.py : `win32ui`, `win32con` (win32gui reste pour GetWindowRect et EnumWindows). Garder `ctypes` uniquement pour SetProcessDpiAwareness.

4. Dans `main()`, ajouter `ctypes.windll.shcore.SetProcessDpiAwareness(2)` comme toute première ligne du corps de `main()`.

5. Dans la boucle principale de `main()`, gérer le retour `None` de `screenshot_window` :
```python
screen, _ = screenshot_window(hwnd)
if screen is None:
    log.warning("Fenetre trop petite ou minimisee, attente...")
    time.sleep(1)
    continue
```
</action>
<acceptance_criteria>
- bot.py contient `def screenshot_window(hwnd):` avec `ImageGrab.grab(bbox=` dans son corps
- bot.py NE contient PAS `BitBlt` ni `PrintWindow`
- bot.py contient `SetProcessDpiAwareness(2)` exactement une fois, dans `main()`
- bot.py NE contient PAS `win32ui` ni `win32con` dans les imports
- bot.py contient `if screen is None:` dans la boucle principale
- bot.py ne contient pas `win32ui.CreateDCFromHandle` ni `win32ui.CreateBitmap`
</acceptance_criteria>
</task>

<task id="1.2">
<type>execute</type>
<title>Réécrire screenshot_window dans capture_templates.py avec ImageGrab</title>
<read_first>
- capture_templates.py (lire les fonctions screenshot_window, grab_full_window, et les imports avant d'éditer)
</read_first>
<action>
1. Remplacer les imports en tête de fichier : supprimer `win32con`, `win32ui`. Ajouter `from PIL import ImageGrab`. Garder `win32gui`, `ctypes`, `cv2`, `numpy as np`, `os`, `time`.

2. Ajouter `SetProcessDpiAwareness(2)` comme première ligne du corps de `main()`, avant le `find_mirrorto_window()`.

3. Remplacer la fonction `screenshot_window` (lignes ~34-57) par :
```python
def screenshot_window(hwnd):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    img = ImageGrab.grab(bbox=(left, top, right, bottom))
    img = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    h_img, w_img = img.shape[:2]
    bottom_crop = h_img - GAME_BOTTOM_OFFSET if GAME_BOTTOM_OFFSET > 0 else h_img
    right_crop = w_img - GAME_RIGHT_OFFSET if GAME_RIGHT_OFFSET > 0 else w_img
    img = img[GAME_TOP_OFFSET:bottom_crop, GAME_LEFT_OFFSET:right_crop]
    return img
```

4. Supprimer la fonction `grab_full_window` (qui utilisait BitBlt) et remplacer par :
```python
def grab_full_window(hwnd):
    left, top, right, bottom = win32gui.GetWindowRect(hwnd)
    img = ImageGrab.grab(bbox=(left, top, right, bottom))
    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
```

5. Supprimer l'appel `ctypes.windll.shcore.SetProcessDpiAwareness(2)` qui était dans `grab_full_window` (il sera dans `main()` désormais).
</action>
<acceptance_criteria>
- capture_templates.py contient `from PIL import ImageGrab`
- capture_templates.py contient `ImageGrab.grab(bbox=` dans `screenshot_window`
- capture_templates.py contient `ImageGrab.grab(bbox=` dans `grab_full_window`
- capture_templates.py NE contient PAS `BitBlt` ni `win32ui` ni `win32con`
- capture_templates.py contient `SetProcessDpiAwareness(2)` exactement une fois, dans `main()`
- capture_templates.py NE contient PAS `win32ui.CreateDCFromHandle` ni `win32ui.CreateBitmap`
</acceptance_criteria>
</task>

</tasks>

<verification>
1. `grep -n "BitBlt\|PrintWindow\|win32ui\|win32con" bot.py capture_templates.py` → aucun résultat
2. `grep -n "ImageGrab.grab" bot.py capture_templates.py` → au moins 1 résultat par fichier
3. `grep -c "SetProcessDpiAwareness" bot.py` → 1
4. `grep -c "SetProcessDpiAwareness" capture_templates.py` → 1
5. `python -c "import bot"` → aucune ImportError
6. `python -c "import capture_templates"` → aucune ImportError
</verification>

<success_criteria>
- Les deux scripts utilisent uniquement `ImageGrab.grab(bbox=...)` pour la capture — pixels identiques garantis
- `SetProcessDpiAwareness(2)` est appelé une seule fois par script, dans `main()`
- Aucun crash si la fenêtre est temporairement < 100×100 (bot.py gère `screen is None`)
- Aucune référence à BitBlt, win32ui, win32con dans les deux fichiers
</success_criteria>

<must_haves>
- bot.py utilise ImageGrab (CAP-01)
- capture_templates.py utilise ImageGrab (CAP-02) — même méthode, pixels identiques
- bot.py gère la fenêtre trop petite sans crash (CAP-03)
</must_haves>
