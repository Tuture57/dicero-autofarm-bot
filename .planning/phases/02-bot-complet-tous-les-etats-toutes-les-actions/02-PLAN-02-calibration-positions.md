---
phase: 2
plan: 02
type: execute
wave: 1
depends_on: []
files_modified:
  - config.py
  - capture_templates.py
autonomous: true
requirements:
  - ACT-03
  - ACT-05
  - STATE-03
  - STATE-04
  - STATE-05
  - STATE-07
---

## Objective

Permettre la calibration interactive des positions de cartes (`card_positions`) et du premier dé (`dice_position`) via `capture_templates.py`. Ces positions sont lues par `handle_select_skill()` et `handle_select_dice()` dans `bot.py` (Plan 01). Trois changements sont nécessaires :
1. Ajouter `card_positions` et `dice_position` à `config.py` _DEFAULTS (valeur `None`)
2. Ajouter la fonction `calibrate_positions()` dans `capture_templates.py` avec `cv2.setMouseCallback`
3. Ajouter l'option calibration au menu interactif dans `capture_templates.py`

## Tasks

<task id="T02-1" type="execute">
<name>Ajouter card_positions et dice_position aux _DEFAULTS de config.py</name>
<read_first>
- config.py — voir _DEFAULTS lignes 6-17 (état actuel)
</read_first>
<action>
Ajouter deux entrées à la fin du dictionnaire `_DEFAULTS` dans `config.py`, avant la fermeture `}`. Valeur `None` dans les deux cas (seront remplies par la calibration dans `config.json`).

Modifier le dictionnaire _DEFAULTS pour qu'il contienne :
```python
    "wheel_wait": 3.0,
    "card_positions": None,
    "dice_position": None,
```
</action>
<acceptance_criteria>
- config.py contient `"card_positions": None,`
- config.py contient `"dice_position": None,`
- config.py contient ces deux clés dans le dictionnaire `_DEFAULTS`
</acceptance_criteria>
</task>

<task id="T02-2" type="execute">
<name>Ajouter la fonction calibrate_positions() dans capture_templates.py</name>
<read_first>
- capture_templates.py — voir la fonction calibrate_offset() lignes 53-72 et la structure générale du fichier jusqu'à la ligne 100
</read_first>
<action>
Insérer la fonction `calibrate_positions()` après la fonction `calibrate_offset()` (après la ligne 72, avant la fonction `show_and_select()`).

La fonction affiche une capture de la zone de jeu dans une fenêtre OpenCV, utilise `cv2.setMouseCallback` avec `cv2.EVENT_LBUTTONDOWN` pour enregistrer les clics. Premier clic = première carte, deuxième = deuxième carte, troisième = troisième carte, quatrième = dé. Appuyer sur 'q' ou Echap pour terminer et sauvegarder.

Les coordonnées enregistrées sont relatives à la zone de jeu (déjà croppée par `screenshot_window`).

Nouvelle fonction exacte à insérer :
```python
def calibrate_positions(hwnd):
    screen = screenshot_window(hwnd)
    if screen is None or screen.size == 0:
        print("Erreur: capture vide. Verifie que MirrorTo est ouvert.")
        return

    clicks = []
    labels = ["Carte 1", "Carte 2", "Carte 3", "De 1 (gauche)"]
    display = screen.copy()

    def on_mouse(event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            idx = len(clicks)
            if idx < len(labels):
                clicks.append([x, y])
                label = labels[idx]
                cv2.circle(display, (x, y), 8, (0, 255, 0), -1)
                cv2.putText(display, label, (x + 10, y), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                print(f"  {label} enregistre : ({x}, {y})")
                cv2.imshow("Calibration positions", display)

    cv2.namedWindow("Calibration positions")
    cv2.setMouseCallback("Calibration positions", on_mouse)

    print("\n=== CALIBRATION POSITIONS ===")
    print("Clique sur chaque carte de skill (1, 2, 3) puis sur le premier de (gauche).")
    print("Appuie sur Q ou Echap quand tu as fini.\n")

    cv2.imshow("Calibration positions", display)
    while True:
        key = cv2.waitKey(50) & 0xFF
        if key in (ord('q'), 27):
            break
        if len(clicks) >= len(labels):
            break
    cv2.destroyAllWindows()

    if len(clicks) < 4:
        print(f"Calibration incomplete ({len(clicks)}/4 points). Annule.")
        return

    card_positions = clicks[:3]
    dice_position = clicks[3]

    cfg["card_positions"] = card_positions
    cfg["dice_position"] = dice_position
    config.save(cfg)
    print(f"\ncard_positions = {card_positions}")
    print(f"dice_position  = {dice_position}")
    print("Positions sauvegardees dans config.json.")
```
</action>
<acceptance_criteria>
- capture_templates.py contient `def calibrate_positions(hwnd):`
- capture_templates.py contient `cv2.setMouseCallback("Calibration positions", on_mouse)`
- capture_templates.py contient `cv2.EVENT_LBUTTONDOWN`
- capture_templates.py contient `card_positions = clicks[:3]`
- capture_templates.py contient `dice_position = clicks[3]`
- capture_templates.py contient `cfg["card_positions"] = card_positions`
- capture_templates.py contient `cfg["dice_position"] = dice_position`
- capture_templates.py contient `config.save(cfg)` dans calibrate_positions
</acceptance_criteria>
</task>

<task id="T02-3" type="execute">
<name>Ajouter l'option calibration positions dans le menu interactif de capture_templates.py</name>
<read_first>
- capture_templates.py — relire le fichier entier juste avant d'éditer (le hook runtime l'exige)
</read_first>
<action>
Modifier le menu `while True:` dans `main()` pour ajouter une option numérotée "Calibrer les positions cartes + de". Cette option doit apparaître dans l'affichage du menu et être gérée dans la logique de dispatch, AVANT la gestion des templates numérotés.

La modification implique deux sous-changements appliqués en un seul appel multi-edit (dans l'ordre : affichage d'abord, dispatch ensuite) :
1. Ajouter l'affichage de l'option dans le bloc d'affichage du menu (après la liste des CAPTURES, avant "0. Quitter")
2. Ajouter la gestion de ce choix dans le bloc de dispatch (avant le check `isdigit`)

**IMPORTANT — ordre des edits :** Appliquer les deux remplacements dans un seul appel (multi_edit ou deux SEARCH/REPLACE consécutifs dans CodeContent) en commençant par le bloc d'affichage, puis le bloc de dispatch. Ne pas les appliquer séparément car le contexte change entre les deux.

Le numéro de l'option calibration positions = `len(CAPTURES) + 1` (soit 10 si CAPTURES en a 9).

Nouvelle section d'affichage du menu (remplacer le bloc print actuel dans le while) :
```python
        print('\n=== MENU CAPTURE TEMPLATES ===')
        for i, (name, _) in enumerate(CAPTURES):
            path = os.path.join(TEMPLATES_DIR, f'{name}.png')
            status = 'existe' if os.path.exists(path) else 'manquant'
            print(f'  {i + 1}. [{status:8}] {name}')
        calib_opt = len(CAPTURES) + 1
        print(f'  {calib_opt}. Calibrer les positions cartes + de')
        print('  0. Quitter')
        print('')
```

Nouvelle logique de dispatch (remplacer le bloc `if not choice.isdigit()...` et ajouter AVANT) :
```python
        calib_opt = len(CAPTURES) + 1
        if choice == str(calib_opt):
            hwnd = find_mirrorto_window()
            if not hwnd:
                print('Erreur: fenetre MirrorTo perdue. Relance MirrorTo.')
                continue
            calibrate_positions(hwnd)
            continue

        if not choice.isdigit() or not (1 <= int(choice) <= len(CAPTURES)):
            print(f'Choix invalide. Entre un nombre entre 1 et {calib_opt}.')
            continue
```
</action>
<acceptance_criteria>
- capture_templates.py contient `calib_opt = len(CAPTURES) + 1`
- capture_templates.py contient `'Calibrer les positions cartes + de'`
- capture_templates.py contient `if choice == str(calib_opt):`
- capture_templates.py contient `calibrate_positions(hwnd)` dans le bloc dispatch du menu
- Le message d'erreur de choix invalide mentionne `calib_opt` comme borne haute : `f'Choix invalide. Entre un nombre entre 1 et {calib_opt}.'`
</acceptance_criteria>
</task>

## Verification

Après exécution de tous les tasks, vérifier avec :

```bash
grep -n "card_positions\|dice_position" config.py
# Doit trouver les deux clés avec valeur None dans _DEFAULTS

grep -n "def calibrate_positions\|setMouseCallback\|EVENT_LBUTTONDOWN" capture_templates.py
# Doit trouver les trois occurrences

grep -n "calib_opt\|Calibrer les positions" capture_templates.py
# Doit trouver les deux occurrences dans main()

python -c "import capture_templates" 2>&1
# Doit s'importer sans erreur de syntaxe

python -c "import config; d = config.load(); print(d.get('card_positions'), d.get('dice_position'))"
# Doit afficher : None None
```

## must_haves

- `config.py` _DEFAULTS contient `"card_positions": None` et `"dice_position": None` — sinon `cfg.get("card_positions")` dans `bot.py` lèverait une KeyError sur une config.json vierge
- `calibrate_positions()` enregistre exactement 3 points pour `card_positions` et 1 point pour `dice_position` via clics souris
- Les positions sont sauvegardées via `config.save(cfg)` dans `config.json` au format `[[x,y],[x,y],[x,y]]` pour card_positions et `[x,y]` pour dice_position
- L'option calibration est accessible depuis le menu interactif de `capture_templates.py` sans modifier le flux des captures de templates existantes
