---
title: Nettoyer le repo et préparer la publication GitHub
date: 2026-05-01
priority: high
---

Supprimer tous les fichiers de test/debug du repo, mettre à jour `.gitignore`,
puis repartir sur un historique vierge (orphan branch) avec un seul commit "Initial release".

## Checklist

- [ ] Identifier tous les fichiers inutiles (test_*, debug_*, captures temporaires, etc.)
- [ ] Mettre à jour `.gitignore` (captures, `__pycache__`, `.venv`, etc.)
- [ ] Créer une branche orpheline propre
- [ ] Commit unique "Initial release — Tuture"
