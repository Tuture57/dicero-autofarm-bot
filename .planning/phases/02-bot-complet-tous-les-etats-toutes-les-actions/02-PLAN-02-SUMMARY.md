---
phase: 2
plan: 02
status: complete
completed: 2026-04-30
---

## One-liner

Calibration séparée des positions de cartes et de dés dans capture_templates.py, avec ajout des templates chest_btn et edit_btn.

## What Was Built

- `capture_templates.py` refactorisé : `calibrate_positions()` séparée en `calibrate_cards()` et `calibrate_dice()` — deux options distinctes dans le menu
- Helper `_calibrate_clicks(hwnd, title, labels)` partagé entre les deux
- Templates ajoutés dans la liste CAPTURES : `chest_btn`, `edit_btn`
- Menu mis à jour : option 11 = calibrer cartes, option 12 = calibrer dé
- `config.save(cfg)` persistance vérifiée pour `card_positions` et `dice_position`

## Key Decisions

- **Calibration séparée** : cartes et dé apparaissent sur des écrans différents — impossible de calibrer les deux en une seule session
- **chest_btn et edit_btn** ajoutés suite aux besoins découverts en test : coffre avant select_skill, bouton Edit après sélection du dé

## Requirements Covered

TMPL-01, TMPL-02, TMPL-03, TMPL-04, TMPL-05
