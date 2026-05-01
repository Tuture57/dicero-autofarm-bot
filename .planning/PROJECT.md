# Autofarm — Dungeon Bot

## What This Is

Bot Python qui automatise un jeu de donjon Android via MirrorTo (mirroring Android sur PC Windows 11).
Il capture l'écran, détecte l'état du jeu par template matching, et simule les clics souris pour jouer en boucle sans intervention humaine.
Le bot doit couvrir le cycle complet d'une partie : lancer le donjon, gérer tous les événements mid-run, et récupérer les récompenses en fin de run.

## Core Value

Le bot joue une partie complète sans jamais se bloquer — du menu jusqu'aux récompenses — en gérant tous les états du jeu.

## Requirements

### Validated

- ✓ Détection de la fenêtre MirrorTo par titre Win32 — existing
- ✓ Template matching via cv2.matchTemplate (TM_CCOEFF_NORMED) — existing
- ✓ Clic simulé via pyautogui avec offset fenêtre — existing
- ✓ Boucle principale avec gestion KeyboardInterrupt et erreurs — existing
- ✓ CAP-01 : Capture via PIL ImageGrab.grab + SetProcessDpiAwareness(2) — v1.0
- ✓ CAP-02 : Même méthode capture dans bot.py et capture_templates.py — v1.0
- ✓ CAP-03 : Taille < 100×100 gérée sans crash OpenCV — v1.0
- ✓ STATE-01 à STATE-09 : Détection des 9 états du jeu — v1.0
- ✓ ACT-01 à ACT-07 : Toutes les actions implémentées — v1.0
- ✓ TMPL-01 à TMPL-05 : Script de capture interactif complet — v1.0

## Current Milestone: v1.1 Publication GitHub

**Goal:** Rendre le bot propre, user-friendly et publiable sur GitHub pour des joueurs semi-tech.

**Target features:**
- Menu principal stylisé (`rich`) dans `main.py` — Calibrer / Lancer le bot
- Messages user-friendly dans `bot.py` et `capture_templates.py`
- README complet avec guide d'installation
- Nettoyage du repo + historique Git vierge signé Tuture

### Active

### Out of Scope

- Gestion de plusieurs fenêtres MirrorTo simultanées — complexité inutile pour l'usage solo
- Interface graphique pour le bot — CLI suffit
- Statistiques / logging avancé des runs — pas demandé
- Support d'autres jeux — bot dédié à ce donjon

## Context

- Windows 11, DPI scaling 125%, résolution 1080p
- MirrorTo positionné à `rect=(1323, -61, 1803, 927)` — partiellement hors écran (top négatif)
- Bug actuel : `GetWindowRect` retourne `53x23` de manière transitoire → OpenCV crash car template > image
- La capture BitBlt actuelle ne set pas DpiAwareness de manière cohérente entre bot.py et capture_templates.py → pixels différents → templates ne matchent pas
- Les emplacements des cartes (Select Skill, Angel Select) et des dés (Select Dice) sont **fixes à l'écran** → clics en positions calculées, pas de template matching sur les éléments cliquables
- Les templates servent uniquement à **identifier l'état** (quel écran est affiché), pas à localiser les éléments à cliquer (sauf attack_btn, try_luck_btn, confirm_btn, rewards_btn qui sont des boutons uniques)

## Constraints

- **Tech stack** : Python, pyautogui, opencv-python, Pillow, pywin32, numpy — pas de nouvelles dépendances
- **Compatibilité** : Windows 11 uniquement, DPI 125%
- **Fenêtre** : MirrorTo doit rester ouverte et à taille fixe pendant l'exécution
- **Pas de root/admin** : le bot tourne sans privilèges élevés

## Key Decisions

| Decision | Rationale | Outcome |
|----------|-----------|---------|
| PIL ImageGrab.grab pour la capture | GetWindowRect + BitBlt produit des tailles aberrantes (53x23) avec DPI 125% quand la fenêtre est partiellement hors écran ; ImageGrab gère le DPI nativement | ✓ Validé — capture stable v1.0 |
| Positions fixes pour cartes et dés | Les emplacements ne bougent pas ; template matching sur des éléments de couleurs/designs variables est fragile | ✓ Validé — fonctionne v1.0 |
| Templates = détection d'état uniquement | Sépare clairement "quel écran ?" (template) de "où cliquer ?" (position fixe ou bouton unique) | ✓ Validé — architecture claire v1.0 |
| capture_templates.py : menu interactif à la demande | L'ancien script forçait de relancer toute la boucle pour un seul template | ✓ Validé — calibration séparée cartes/dés v1.0 |
| SetProcessDpiAwareness(2) une seule fois au démarrage | Appelé à chaque screenshot dans l'ancien code — inutile et incorrect | ✓ Validé v1.0 |
| SetCursorPos + SendInput sans MOUSEEVENTF_VIRTUALDESK | MirrorTo filtre le flag VIRTUALDESK — testé 8 méthodes, seules celles sans ce flag passent | ✓ Validé — clics fonctionnels v1.0 |
| Admin requis au démarrage | MirrorTo tourne en mode élevé (UIPI) — PostMessage/SendMessage bloqués sans élévation | ✓ Validé — auto-runas au démarrage v1.0 |
| edit_btn détecté avant select_skill | L'écran Edit partage des pixels avec select_skill — ordre de priorité critique | ✓ Validé v1.0 |

## Context

- Windows 11, DPI scaling 125%, résolution 1080p
- Bot livré en v1.0 : ~400 LOC Python, 11 templates capturés
- Tech stack : Python, opencv-python, Pillow, pywin32, numpy, ctypes
- MirrorTo doit tourner en admin pour que les clics passent (UIPI)
- Templates capturés : menu_new_game, attack_btn, select_skill_v1, select_skill_v2, angel_select, try_luck_btn, select_dice_text, confirm_btn, rewards_btn, chest_btn, edit_btn

---
*Last updated: 2026-05-01 — Phase 5 complete (README written, DOC-01 to DOC-05 validated)*
