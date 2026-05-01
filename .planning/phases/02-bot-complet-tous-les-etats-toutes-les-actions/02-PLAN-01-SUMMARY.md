---
phase: 2
plan: 01
status: complete
completed: 2026-04-30
---

## One-liner

Réécriture complète de bot.py : détection des 9 états du jeu, clics fiables via SetCursorPos+SendInput (sans VIRTUALDESK), auto-élévation admin, sortie propre par Échap.

## What Was Built

- `detect_state()` reécrit avec ordre de priorité : rewards > confirm_popup > wheel > select_dice > edit_btn > select_skill (v1/v2/angel) > chest > dungeon > menu
- `handle_select_skill()` utilise `card_positions` depuis config (positions fixes, pas de template matching)
- `handle_select_dice()` utilise `dice_position` depuis config (positions fixes)
- `handle_menu()`, `handle_rewards()`, `handle_chest()`, `handle_edit_btn()` ajoutés
- Bloc dispatch dans `main()` couvre tous les états
- `_raw_click()` via `SetCursorPos` + `SendInput` sans flag `MOUSEEVENTF_VIRTUALDESK` (MirrorTo filtrait ce flag)
- Auto-élévation admin au démarrage (`ShellExecuteW runas`)
- `_console_hwnd` restauré au premier plan après chaque clic
- Thread daemon `_listen_escape` + `_stop_event` pour quitter proprement avec Échap
- Coordonnées numpy castées en `int()` avant `SetCursorPos` (fix TypeError)

## Key Decisions

- **SetCursorPos + SendInput sans VIRTUALDESK** : testé 8 méthodes de clic — seules celles sans MOUSEEVENTF_VIRTUALDESK passent dans MirrorTo
- **Admin requis** : MirrorTo tourne en mode élevé (UIPI bloque PostMessage/SendMessage sans admin)
- **edit_btn avant select_skill** dans `detect_state` : l'écran Edit partage des pixels avec select_skill, priorité nécessaire

## Requirements Covered

CAP-01, CAP-02, CAP-03, STATE-01, STATE-02, STATE-03, STATE-04, STATE-05, STATE-06, STATE-07, STATE-08, STATE-09, ACT-01, ACT-02, ACT-03, ACT-04, ACT-05, ACT-06, ACT-07
