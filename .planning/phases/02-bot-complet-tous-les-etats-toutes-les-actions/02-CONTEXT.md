# Phase 2: Bot complet — tous les états + toutes les actions - Context

**Gathered:** 2026-04-30
**Status:** Ready for planning

<domain>
## Phase Boundary

Réécriture de `bot.py` pour détecter et gérer les 9 états du jeu (Menu, Dungeon, Select Skill v1/v2, Angel Select, Wheel, Select Dice, Confirm Popup, Rewards) et exécuter les 7 actions correspondantes. Couvre le cycle complet Menu→Dungeon→Events→Rewards→Menu sans interruption.

Ajout d'un mode de calibration des positions fixes dans `capture_templates.py`.

</domain>

<decisions>
## Implementation Decisions

### Positions fixes — Cartes (Select Skill / Angel Select)
- **D-01:** Les 3 emplacements de cartes sont calibrés interactivement via `capture_templates.py` (clic sur chaque carte pour enregistrer la position pixel relative à la zone de jeu).
- **D-02:** Les positions calibrées sont stockées dans `config.json` sous les clés `card_positions` (liste de 3 coordonnées `[x, y]` relatives à la zone de jeu).
- **D-03:** ACT-03 s'applique à Select Skill v1, Select Skill v2 ET Angel Select — même logique de clic sur l'un des 3 emplacements fixes.

### Positions fixes — Dés (Select Dice)
- **D-04:** Seul le premier dé (à gauche) est ciblé — une seule position à calibrer.
- **D-05:** La position est stockée dans `config.json` sous la clé `dice_position` (`[x, y]` relatif à la zone de jeu).
- **D-06:** La calibration du premier dé se fait aussi via `capture_templates.py` (même mode interactif que les cartes).

### Calibration dans capture_templates.py
- **D-07:** `capture_templates.py` ajoute une option de calibration des positions fixes (cartes + 1er dé) dans son menu interactif — option numérotée séparée des templates.
- **D-08:** Après calibration, les positions sont sauvegardées dans `config.json` automatiquement (même pattern que `calibrate_offset`).

### Acquis de la Phase 1 (verrouillés)
- **D-09:** Capture via `ImageGrab.grab(bbox=GetWindowRect)` — inchangé.
- **D-10:** Templates = détection d'état uniquement. Clics sur cartes/dés = positions fixes. Pas de template matching sur les cartes ni les dés.
- **D-11:** Toutes les variables de configuration passent par `config.json` / `config.py`.

### Claude's Discretion
- Ordre de priorité des états dans `detect_state` — garder l'ordre actuel (confirm_popup > wheel > select_dice > select_skill > dungeon) et ajouter menu en dernier fallback avant unknown, rewards en tête (priorité maximale car état terminal du run).
- Gestion rewards : attente fixe de 2s après le clic, puis retour au cycle normal (detect_state gère le retour au menu).
- Robustesse unknown : comportement actuel (log toutes les 10 itérations) suffisant pour v1 — ROB-01/02 sont des requirements v2.

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Project context
- `.planning/PROJECT.md` — Vision, contraintes tech stack, decisions clés
- `.planning/REQUIREMENTS.md` — STATE-01 à STATE-09, ACT-01 à ACT-07 (requirements Phase 2)

### Code existant
- `bot.py` — Script actuel à réécrire (voir fonctions detect_state, handle_*)
- `capture_templates.py` — Script à étendre avec calibration des positions fixes
- `config.py` — Module load/save à utiliser pour persister les positions
- `config.json` — Fichier de configuration à étendre avec card_positions et dice_position

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `screenshot_window(hwnd)` → retourne `(img, (left, top))` — inchangé
- `click_in_window(hwnd, x, y)` → clic à coordonnées relatives à la zone de jeu — à réutiliser pour les positions fixes
- `find_template` / `find_all_templates` — à réutiliser pour les nouveaux templates (menu_new_game, rewards_btn)
- `config.load()` / `config.save()` — à utiliser pour lire/écrire card_positions et dice_position
- `calibrate_offset()` dans capture_templates.py — pattern à réutiliser pour la calibration des positions fixes

### Established Patterns
- `detect_state` : série de `if find_template(screen, templates[...])` avec ordre de priorité — étendre avec les nouveaux états
- `handle_*` : une fonction par état, appelée depuis la boucle principale — même pattern pour handle_menu, handle_rewards
- Toutes les constantes chargées depuis `config.json` au démarrage

### Integration Points
- `main()` dans bot.py : ajouter `menu_new_game` et `rewards_btn` dans `templates_to_load`
- `detect_state` : ajouter `menu` et `rewards` dans les conditions
- `capture_templates.py` menu : ajouter une option "Calibrer positions fixes" (cartes + 1er dé)

</code_context>

<specifics>
## Specific Ideas

- La calibration des positions dans capture_templates.py affiche la capture de l'écran de jeu et demande de cliquer sur chaque carte (ou le 1er dé) pour enregistrer la position — même UX que `selectROI` mais avec un simple clic plutôt qu'un rectangle.

</specifics>

<deferred>
## Deferred Ideas

- ROB-01 : Détection de boucle infinie avec relance automatique — v2
- ROB-02 : Screenshot de debug automatique sur unknown persistant — v2
- Calibration des 5 dés individuellement — non nécessaire, seul le premier est ciblé

</deferred>

---

*Phase: 02-bot-complet-tous-les-etats-toutes-les-actions*
*Context gathered: 2026-04-30*
