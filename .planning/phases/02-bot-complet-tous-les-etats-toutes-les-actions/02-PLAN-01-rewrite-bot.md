---
phase: 2
plan: 01
type: execute
wave: 1
depends_on: []
files_modified:
  - bot.py
autonomous: true
requirements:
  - STATE-01
  - STATE-02
  - STATE-03
  - STATE-04
  - STATE-05
  - STATE-06
  - STATE-07
  - STATE-08
  - STATE-09
  - ACT-01
  - ACT-02
  - ACT-03
  - ACT-04
  - ACT-05
  - ACT-06
  - ACT-07
---

## Objective

Réécrire `bot.py` pour détecter et gérer les 9 états du jeu. Cela implique :
- Mettre à jour `templates_to_load` avec les bons noms de fichiers (menu_new_game, select_skill_v1, select_skill_v2, angel_select, rewards_btn — plus skill_card et active_die)
- Réécrire `detect_state()` avec l'ordre de priorité correct et les nouvelles clés de templates
- Réécrire `handle_select_skill()` pour utiliser `card_positions` depuis config (sans template matching sur les cartes)
- Réécrire `handle_select_dice()` pour utiliser `dice_position` depuis config (sans template matching sur les dés)
- Ajouter `handle_menu()` et `handle_rewards()`
- Mettre à jour le bloc dispatch dans `main()` pour couvrir les cas menu et rewards

## Tasks

<task id="T01-1" type="execute">
<name>Mettre à jour templates_to_load dans main()</name>
<read_first>
- bot.py — voir la liste actuelle lignes 221-229 et le contexte de main()
</read_first>
<action>
Remplacer le bloc `templates_to_load` (lignes 221-229) par la nouvelle liste. Supprimer "skill_card" et "active_die". Ajouter "menu_new_game", "select_skill_v1", "select_skill_v2", "angel_select", "rewards_btn".

Nouvelle liste exacte :
```python
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
    ]
```
</action>
<acceptance_criteria>
- bot.py contient `"menu_new_game",` dans templates_to_load
- bot.py contient `"select_skill_v1",` dans templates_to_load
- bot.py contient `"select_skill_v2",` dans templates_to_load
- bot.py contient `"angel_select",` dans templates_to_load
- bot.py contient `"rewards_btn",` dans templates_to_load
- bot.py ne contient plus `"skill_card"` dans templates_to_load
- bot.py ne contient plus `"active_die"` dans templates_to_load
</acceptance_criteria>
</task>

<task id="T01-2" type="execute">
<name>Réécrire detect_state() avec le nouvel ordre de priorité et les nouvelles clés</name>
<read_first>
- bot.py — voir detect_state() lignes 117-138 (état actuel à remplacer)
</read_first>
<action>
Remplacer entièrement la fonction `detect_state()` (lignes 117-138). Ordre de priorité : rewards > confirm_popup > wheel > select_dice > select_skill (v1 OR v2 OR angel_select) > dungeon > menu > unknown.

La logique select_skill doit vérifier trois templates avec OR : `select_skill_v1`, `select_skill_v2`, `angel_select`.

Nouvelle fonction exacte :
```python
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

    skill_templates = ["select_skill_v1", "select_skill_v2", "angel_select"]
    for key in skill_templates:
        if templates.get(key) is not None:
            if find_template(screen, templates[key]):
                return "select_skill"

    if templates.get("attack_btn") is not None:
        if find_template(screen, templates["attack_btn"]):
            return "dungeon"

    if templates.get("menu_new_game") is not None:
        if find_template(screen, templates["menu_new_game"]):
            return "menu"

    return "unknown"
```
</action>
<acceptance_criteria>
- bot.py contient `def detect_state(screen, templates):`
- bot.py contient `return "rewards"` dans detect_state
- bot.py contient `return "menu"` dans detect_state
- bot.py contient `skill_templates = ["select_skill_v1", "select_skill_v2", "angel_select"]`
- bot.py contient `for key in skill_templates:` dans detect_state
- L'ordre dans detect_state est : rewards_btn, confirm_btn, try_luck_btn, select_dice_text, skill_templates loop, attack_btn, menu_new_game
- bot.py ne contient plus `"skill_card"` dans detect_state (ancienne clé présente ligne 166 du fichier original)
</acceptance_criteria>
</task>

<task id="T01-3" type="execute">
<name>Réécrire handle_select_skill() pour utiliser card_positions depuis config</name>
<read_first>
- bot.py — voir handle_select_skill() lignes 165-177 (état actuel à remplacer)
</read_first>
<action>
Remplacer entièrement la fonction `handle_select_skill()` (lignes 165-177). La nouvelle version lit `cfg["card_positions"]` (liste de [x,y] relatifs à la zone de jeu), choisit une entrée au hasard avec `random.choice`, et clique. Si `card_positions` est None ou vide, logguer une erreur et retourner False. Ne pas utiliser de template matching sur les cartes.

Nouvelle fonction exacte :
```python
def handle_select_skill(hwnd, screen, templates):
    positions = cfg.get("card_positions")
    if not positions:
        log.error("card_positions non calibre dans config.json — lance capture_templates.py pour calibrer")
        return False
    chosen = random.choice(positions)
    log.info(f"Selecting skill card at {chosen}")
    click_in_window(hwnd, chosen[0], chosen[1])
    return True
```
</action>
<acceptance_criteria>
- bot.py contient `def handle_select_skill(hwnd, screen, templates):`
- bot.py contient `positions = cfg.get("card_positions")`
- bot.py contient `chosen = random.choice(positions)`
- bot.py contient `"card_positions non calibre dans config.json"` dans handle_select_skill
- bot.py ne contient plus `find_all_templates` dans handle_select_skill
- bot.py ne contient plus `"skill_card"` dans handle_select_skill
</acceptance_criteria>
</task>

<task id="T01-4" type="execute">
<name>Réécrire handle_select_dice() pour utiliser dice_position depuis config</name>
<read_first>
- bot.py — voir handle_select_dice() lignes 180-195 (état actuel à remplacer)
</read_first>
<action>
Remplacer entièrement la fonction `handle_select_dice()` (lignes 180-195). La nouvelle version lit `cfg["dice_position"]` (coordonnées [x,y] relatives à la zone de jeu du premier dé, le plus à gauche), et clique. Si `dice_position` est None, logguer une erreur et retourner False. Ne pas utiliser de template matching sur les dés.

Nouvelle fonction exacte :
```python
def handle_select_dice(hwnd, screen, templates):
    pos = cfg.get("dice_position")
    if not pos:
        log.error("dice_position non calibre dans config.json — lance capture_templates.py pour calibrer")
        return False
    log.info(f"Selecting first die at {pos}")
    click_in_window(hwnd, pos[0], pos[1])
    return True
```
</action>
<acceptance_criteria>
- bot.py contient `def handle_select_dice(hwnd, screen, templates):`
- bot.py contient `pos = cfg.get("dice_position")`
- bot.py contient `"dice_position non calibre dans config.json"` dans handle_select_dice
- bot.py ne contient plus `find_all_templates` dans handle_select_dice
- bot.py ne contient plus `"active_die"` dans handle_select_dice
</acceptance_criteria>
</task>

<task id="T01-5" type="execute">
<name>Ajouter handle_menu()</name>
<read_first>
- bot.py — voir handle_confirm_popup() lignes 198-204 pour le style à suivre, et la structure générale du fichier
</read_first>
<action>
Insérer la fonction `handle_menu()` après `handle_confirm_popup()` (après la ligne 204). Elle cherche le template `menu_new_game` et clique dessus.

Nouvelle fonction exacte :
```python
def handle_menu(hwnd, screen, templates):
    match = find_template(screen, templates["menu_new_game"])
    if match:
        log.info("Clicking New Game on menu")
        click_in_window(hwnd, match[0], match[1])
        return True
    return False
```
</action>
<acceptance_criteria>
- bot.py contient `def handle_menu(hwnd, screen, templates):`
- bot.py contient `find_template(screen, templates["menu_new_game"])`
- bot.py contient `"Clicking New Game on menu"`
</acceptance_criteria>
</task>

<task id="T01-6" type="execute">
<name>Ajouter handle_rewards()</name>
<read_first>
- bot.py — voir handle_menu() nouvellement ajoutée (T01-5) et l'emplacement dans le fichier
</read_first>
<action>
Insérer la fonction `handle_rewards()` après `handle_menu()`. Elle cherche le template `rewards_btn`, clique dessus, puis attend 2.0 secondes pour laisser l'animation se terminer.

Nouvelle fonction exacte :
```python
def handle_rewards(hwnd, screen, templates):
    match = find_template(screen, templates["rewards_btn"])
    if match:
        log.info("Clicking rewards button")
        click_in_window(hwnd, match[0], match[1])
        time.sleep(2.0)
        return True
    return False
```
</action>
<acceptance_criteria>
- bot.py contient `def handle_rewards(hwnd, screen, templates):`
- bot.py contient `find_template(screen, templates["rewards_btn"])`
- bot.py contient `time.sleep(2.0)` dans handle_rewards
- bot.py contient `"Clicking rewards button"`
</acceptance_criteria>
</task>

<task id="T01-7" type="execute">
<name>Mettre à jour le bloc dispatch dans main() pour ajouter les cas menu et rewards</name>
<read_first>
- bot.py — voir le bloc dispatch lignes 274-284 (état actuel)
</read_first>
<action>
Remplacer le bloc dispatch (lignes 274-284) pour ajouter les deux nouveaux cas : `"menu"` appelant `handle_menu()` et `"rewards"` appelant `handle_rewards()`. Conserver tous les cas existants.

Nouveau bloc dispatch exact :
```python
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
```
</action>
<acceptance_criteria>
- bot.py contient `elif state == "menu":` dans le bloc dispatch de main()
- bot.py contient `handle_menu(hwnd, screen, templates)` dans le bloc dispatch
- bot.py contient `elif state == "rewards":` dans le bloc dispatch de main()
- bot.py contient `handle_rewards(hwnd, screen, templates)` dans le bloc dispatch
</acceptance_criteria>
</task>

## Verification

Après exécution de tous les tasks, vérifier avec :

```bash
grep -n "def handle_" bot.py
# Doit lister : handle_dungeon, handle_wheel, handle_select_skill, handle_select_dice, handle_confirm_popup, handle_menu, handle_rewards

grep -n "return \"" bot.py
# Dans detect_state doit lister : rewards, confirm_popup, wheel, select_dice, select_skill, dungeon, menu, unknown

grep -n "card_positions\|dice_position" bot.py
# Doit trouver cfg.get("card_positions") et cfg.get("dice_position")

grep -n "skill_card\|active_die" bot.py
# Ne doit rien trouver (templates supprimés)

python -c "import bot" 2>&1
# Doit s'importer sans erreur de syntaxe
```

## must_haves

- `detect_state()` retourne exactement les valeurs : `"rewards"`, `"confirm_popup"`, `"wheel"`, `"select_dice"`, `"select_skill"`, `"dungeon"`, `"menu"`, `"unknown"` — dans cet ordre de priorité
- `detect_state()` retourne `"select_skill"` pour les trois templates : select_skill_v1, select_skill_v2, angel_select (D-03)
- `handle_select_skill()` utilise uniquement `cfg["card_positions"]` pour cliquer, sans aucun template matching sur les cartes
- `handle_select_dice()` utilise uniquement `cfg["dice_position"]` pour cliquer, sans aucun template matching sur les dés
- Le bloc dispatch de `main()` couvre les 7 états actionnables : dungeon, wheel, select_skill, select_dice, confirm_popup, menu, rewards
- `templates_to_load` contient exactement les 9 clés : menu_new_game, attack_btn, select_skill_v1, select_skill_v2, angel_select, try_luck_btn, select_dice_text, confirm_btn, rewards_btn
