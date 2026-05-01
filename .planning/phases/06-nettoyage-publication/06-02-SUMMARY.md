---
phase: 6
plan: "06-02"
subsystem: git-history
tags: [git, orphan, publication]
key-files:
  created: []
  modified: ["(historique git réécrit)"]
metrics:
  tasks_completed: 3/3
  commits: 1
---

## Summary

Créé branche orpheline `fresh-start`, stagé tous les fichiers nettoyés (avec `git rm --cached` pour exclure `config.json` et `__pycache__/` qui n'étaient pas encore ignorés sur la nouvelle branche), puis commit unique "Initial release — AutoFarm Dungeon Bot v1.0". Supprimé `master`, renommé `fresh-start` en `main`.

## Commits

| Task | Commit | Description |
|------|--------|-------------|
| T2+T3 | 8f070b5 | Initial release — AutoFarm Dungeon Bot v1.0 |

## Deviations

`git add -A` a stagé `config.json` et `__pycache__/` malgré le `.gitignore` (sur une branche orpheline, tous les fichiers sont "new" et ne sont pas encore ignorés automatiquement). Corrigé avec `git rm --cached config.json` et `git rm --cached -r __pycache__/` avant le commit final.

## Self-Check: PASSED

- [x] 1 seul commit sur branche `main`
- [x] Message: "Initial release — AutoFarm Dungeon Bot v1.0"
- [x] Auteur: Tuture57
- [x] config.json absent du commit (exlu manuellement)
- [x] __pycache__/ absent du commit
- [x] bot_backup.py, test_clicks.py absents
- [x] config.json.example présent
- [x] Branche `master` supprimée
