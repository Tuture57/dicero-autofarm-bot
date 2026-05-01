---
title: Créer main.py avec menu stylisé rich
date: 2026-05-01
priority: high
---

Créer un `main.py` point d'entrée unique avec un menu interactif stylisé via la lib `rich`.

## Comportement

- ASCII art / titre du projet en haut
- Deux options navigables :
  1. **Calibrer** — lance `capture_templates.py`
  2. **Lancer le bot** — lance `bot.py`
- Messages clairs à chaque étape (démarrage, arrêt, erreur)
- Quitter proprement avec Ctrl+C

## Notes

- Ajouter `rich` aux dépendances (`requirements.txt`)
- Navigation au clavier (flèches ou numéro)
