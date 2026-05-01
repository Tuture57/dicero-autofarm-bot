---
phase: 1
plan: 02
title: Réécrire capture_templates.py avec menu interactif et liste complète
type: execute
wave: 1
depends_on: []
files_modified:
  - capture_templates.py
autonomous: true
requirements:
  - TMPL-01
  - TMPL-02
  - TMPL-03
  - TMPL-04
  - TMPL-05
---

<objective>
Réécrire `capture_templates.py` pour :
1. Afficher un menu interactif listant les 9 templates avec statut "existe" ou "manquant"
2. Permettre de capturer un template individuel via son numéro de menu (sans relancer toute la boucle)
3. Demander confirmation avant d'écraser un template existant
4. Utiliser ImageGrab (déjà réécrit en Plan 01) — même méthode que bot.py
5. Couvrir les 9 templates canoniques : `menu_new_game`, `attack_btn`, `select_skill_v1`, `select_skill_v2`, `angel_select`, `try_luck_btn`, `select_dice_text`, `confirm_btn`, `rewards_btn`
</objective>

<tasks>

<task id="2.1">
<type>execute</type>
<title>Mettre à jour la liste CAPTURES avec les 9 templates canoniques</title>
<read_first>
- capture_templates.py (lire la liste CAPTURES et la fonction main() en entier)
</read_first>
<action>
Remplacer la liste `CAPTURES` (actuellement 7 éléments, lignes ~122-130) par la liste des 9 templates canoniques :

```python
CAPTURES = [
    ("menu_new_game",     "Navigue vers l'écran Menu principal (bouton New Game visible)"),
    ("attack_btn",        "Navigue vers le donjon principal (bouton Attack visible)"),
    ("select_skill_v1",   "Navigue vers Select Skill variante 1 (texte seul, sans dessin)"),
    ("select_skill_v2",   "Navigue vers Select Skill variante 2 (texte avec dessin)"),
    ("angel_select",      "Navigue vers Angel Select (ange à la place du texte)"),
    ("try_luck_btn",      "Navigue vers la roue (bouton Try Your Luck visible)"),
    ("select_dice_text",  "Navigue vers Select Dice (texte Select Dice visible)"),
    ("confirm_btn",       "Navigue vers la popup de confirmation (bouton Confirm visible)"),
    ("rewards_btn",       "Navigue vers l'écran Récompenses (bouton de collecte visible)"),
]
```

Ne pas modifier les fonctions `find_mirrorto_window`, `screenshot_window`, `grab_full_window`, `calibrate_offset`, `show_and_select` — elles sont correctes après Plan 01.
</action>
<acceptance_criteria>
- capture_templates.py contient `"menu_new_game"` dans la liste CAPTURES
- capture_templates.py contient `"select_skill_v1"` et `"select_skill_v2"` dans la liste CAPTURES
- capture_templates.py contient `"angel_select"` dans la liste CAPTURES
- capture_templates.py contient `"rewards_btn"` dans la liste CAPTURES
- capture_templates.py contient `"confirm_btn"` dans la liste CAPTURES
- `grep -c '(".*",' capture_templates.py` dans la liste CAPTURES compte exactement 9 entrées de template
</acceptance_criteria>
</task>

<task id="2.2">
<type>execute</type>
<title>Réécrire main() avec menu interactif et capture individuelle</title>
<read_first>
- capture_templates.py (lire la fonction main() complète après la tâche 2.1)
</read_first>
<action>
Remplacer la fonction `main()` intégralement par la version avec menu interactif :

```python
def main():
    global GAME_LEFT_OFFSET, GAME_TOP_OFFSET, GAME_RIGHT_OFFSET, GAME_BOTTOM_OFFSET
    ctypes.windll.shcore.SetProcessDpiAwareness(2)

    hwnd = find_mirrorto_window()
    if not hwnd:
        print("Erreur: fenetre MirrorTo introuvable. Lance MirrorTo d'abord.")
        return
    print(f"Fenetre MirrorTo trouvee (hwnd={hwnd})")

    result = calibrate_offset(hwnd)
    if result is not None:
        l, t, r, b = result
        GAME_LEFT_OFFSET, GAME_TOP_OFFSET, GAME_RIGHT_OFFSET, GAME_BOTTOM_OFFSET = l, t, r, b
        print(f"\nOffsets appliques pour cette session.")
        print(f"Pour les rendre permanents, mets ces valeurs dans bot.py ET capture_templates.py :")
        print(f"  GAME_LEFT_OFFSET   = {l}")
        print(f"  GAME_TOP_OFFSET    = {t}")
        print(f"  GAME_RIGHT_OFFSET  = {r}")
        print(f"  GAME_BOTTOM_OFFSET = {b}\n")

    while True:
        print("\n=== MENU CAPTURE TEMPLATES ===")
        for i, (name, _) in enumerate(CAPTURES):
            path = os.path.join(TEMPLATES_DIR, f"{name}.png")
            status = "existe" if os.path.exists(path) else "manquant"
            print(f"  {i + 1}. [{status:8}] {name}")
        print(f"  0. Quitter")
        print("")

        choice = input("Numero du template a capturer (0 pour quitter) : ").strip()
        if choice == "0":
            print("Termine.")
            break

        if not choice.isdigit() or not (1 <= int(choice) <= len(CAPTURES)):
            print(f"Choix invalide. Entre un nombre entre 1 et {len(CAPTURES)}.")
            continue

        idx = int(choice) - 1
        name, instruction = CAPTURES[idx]
        path = os.path.join(TEMPLATES_DIR, f"{name}.png")

        if os.path.exists(path):
            confirm = input(f"'{name}.png' existe deja. Ecraser ? [y/N] : ").strip().lower()
            if confirm != "y":
                print("Annule.")
                continue

        print(f"\n[{name}] {instruction}")
        input("Appuie sur Entree quand le bon ecran est visible dans MirrorTo...")

        hwnd = find_mirrorto_window()
        if not hwnd:
            print("Erreur: fenetre MirrorTo perdue. Relance MirrorTo.")
            continue

        screen = screenshot_window(hwnd)
        if screen is None or screen.size == 0:
            print("Erreur: capture vide. Verifie que MirrorTo est ouvert et non minimise.")
            continue

        saved = show_and_select(screen, name)
        if saved:
            print(f"Template '{name}' sauvegarde avec succes.")
        else:
            print("Capture annulee (aucun rectangle selectionne).")
```

Note : `screenshot_window` dans capture_templates.py ne retourne pas de tuple — juste l'image (contrairement à bot.py qui retourne `(img, (left, top))`). Vérifier ce point lors de la lecture du fichier.
</action>
<acceptance_criteria>
- capture_templates.py contient `while True:` dans `main()` (boucle de menu)
- capture_templates.py contient `MENU CAPTURE TEMPLATES` dans `main()`
- capture_templates.py contient `"existe"` et `"manquant"` dans `main()` (affichage du statut)
- capture_templates.py contient `"Ecraser ? [y/N]"` dans `main()` (confirmation overwrite)
- capture_templates.py contient `"0. Quitter"` dans `main()`
- capture_templates.py contient `input("Numero du template` dans `main()`
- `python -c "import ast, sys; ast.parse(open('capture_templates.py').read()); print('OK')"` → `OK`
</acceptance_criteria>
</task>

</tasks>

<verification>
1. `python -c "import ast, sys; ast.parse(open('capture_templates.py').read()); print('syntaxe OK')"` → `syntaxe OK`
2. `grep -c "manquant\|existe" capture_templates.py` → au moins 1 (affichage du statut dans le menu)
3. `grep "menu_new_game\|select_skill_v1\|select_skill_v2\|angel_select\|rewards_btn\|confirm_btn" capture_templates.py` → 6 lignes minimum (les 6 nouveaux templates)
4. `grep "Ecraser" capture_templates.py` → au moins 1 résultat (confirmation overwrite)
5. `grep "while True" capture_templates.py` → 1 résultat (boucle menu)
</verification>

<success_criteria>
- Menu interactif : affiche les 9 templates avec statut existe/manquant (TMPL-01)
- Capture individuelle par numéro de menu sans relancer la boucle (TMPL-02)
- Confirmation avant écrasement pour chaque template existant (TMPL-03)
- Capture via ImageGrab — même méthode que bot.py, pixels identiques (TMPL-04)
- Les 9 templates canoniques sont listés dans CAPTURES (TMPL-05)
</success_criteria>

<must_haves>
- Menu affiche 9 templates avec statut existe/manquant (TMPL-01)
- Sélection individuelle d'un template possible (TMPL-02)
- Confirmation avant écrasement (TMPL-03)
- ImageGrab utilisé dans screenshot_window (TMPL-04, déjà fait par Plan 01)
- 9 templates dans CAPTURES : menu_new_game, attack_btn, select_skill_v1, select_skill_v2, angel_select, try_luck_btn, select_dice_text, confirm_btn, rewards_btn (TMPL-05)
</must_haves>
