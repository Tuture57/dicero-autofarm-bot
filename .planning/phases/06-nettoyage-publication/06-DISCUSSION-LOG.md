# Phase 6: Nettoyage et publication — Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-01
**Phase:** 6 — Nettoyage et publication
**Areas discussed:** config.json, templates/ et .gitignore, Fichiers à supprimer, Historique Git vierge

---

## config.json

| Option | Description | Selected |
|--------|-------------|----------|
| Inclure tel quel | Valeurs calibrées incluses, bot fonctionne directement | |
| Fichier .example + gitignore | config.json.example versionné, config.json ignoré | ✓ |
| Inclure + note README | Inclure + documentation README | |

**User's choice:** Fichier .example + gitignore
**Notes:** config.json.example garde les vraies valeurs calibrées comme point de départ

---

## templates/ et .gitignore

| Option | Description | Selected |
|--------|-------------|----------|
| Inclure les templates | 14 PNG dans le repo, bot opérationnel immédiatement | ✓ |
| Ignorer les templates | Chaque utilisateur calibre les siens | |
| Placeholder uniquement | Dossier vide ou .gitkeep | |

**User's choice:** Inclure les templates

**.gitignore entries sélectionnées :** `__pycache__/`, `*.pyc`, `config.json`, `.venv/`, `venv/`
**Notes:** `docs/screenshot.png` reste versionné

---

## Fichiers à supprimer

| Option | Description | Selected |
|--------|-------------|----------|
| bot_backup.py | Sauvegarde obsolète | ✓ |
| test_clicks.py | Script de développement | ✓ |
| test_admin_background.py | Untracked, jamais commité | ✓ |

**User's choice:** Tous les trois

---

## Historique Git vierge

| Option | Description | Selected |
|--------|-------------|----------|
| "Initial release" | Message court standard | |
| "Initial release — AutoFarm Dungeon Bot v1.0" | Plus descriptif | ✓ |
| Claude décide | | |

**Auteur Git :** Config actuelle (Tuture57) — pas de changement
**Branche finale :** `main` (renommée depuis `master`)

---

## Claude's Discretion

- Ordre des étapes de nettoyage
- Format du .gitignore
- Valeur email Git

## Deferred Ideas

- Mention explicite de config.json.example dans le README
- Publication effective sur GitHub (push) — action manuelle utilisateur
