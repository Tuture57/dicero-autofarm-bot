# Roadmap: Autofarm — Dungeon Bot

## Milestones

- ✅ **v1.0 MVP** — Phases 1-2 (shipped 2026-04-30)
- 🔄 **v1.1 Publication GitHub** — Phases 3-6 (in progress)

## Phases

<details>
<summary>✅ v1.0 MVP (Phases 1-2) — SHIPPED 2026-04-30</summary>

- [x] Phase 1: Capture fiable + Script de capture (2/2 plans) — completed 2026-04-30
- [x] Phase 2: Bot complet tous les états + toutes les actions (2/2 plans) — completed 2026-04-30

</details>

### v1.1 Publication GitHub (Phases 3-6)

- [x] Phase 3: Menu principal `main.py` avec rich (2/2 plans) — completed 2026-05-01
- [x] Phase 4: Messages user-friendly dans bot.py et capture_templates.py (2/2 plans) — completed 2026-05-01
- [x] Phase 5: README — guide d'installation et d'utilisation (1/1 plans) — completed 2026-05-01
- [ ] Phase 6: Nettoyage repo + historique Git vierge signé Tuture

**Phase 3: Menu principal `main.py` avec rich**
Goal: Créer le point d'entrée unique avec menu stylisé
Requirements: UX-01, UX-02, UX-03, UX-04
Success criteria:
1. `python main.py` affiche un menu avec titre ASCII et 2 options
2. Choix "Calibrer" lance capture_templates.py
3. Choix "Lancer le bot" lance bot.py
4. Ctrl+C quitte proprement sans stack trace

**Phase 4: Messages user-friendly**
Goal: Retravailler tous les messages affichés dans bot.py et capture_templates.py
Requirements: UX-05, UX-06, UX-07
Success criteria:
1. Aucun message de debug brut affiché à l'utilisateur
2. Erreur "fenêtre introuvable" affiche un message explicite
3. Style cohérent avec le menu rich de main.py

**Phase 5: README**
Goal: Rédiger le README complet pour GitHub
Requirements: DOC-01, DOC-02, DOC-03, DOC-04, DOC-05
Success criteria:
1. README contient prérequis, installation en étapes numérotées, guide utilisation
2. Section recalibration expliquée clairement
3. Auteur = Tuture, visible en bas du README

**Phase 6: Nettoyage et publication**
Goal: Nettoyer le repo et créer l'historique vierge
Requirements: PUB-01, PUB-02, PUB-03, PUB-04
Success criteria:
1. Aucun fichier test/debug dans le repo
2. `.gitignore` complet
3. Un seul commit "Initial release" avec auteur Tuture

## Progress

| Phase | Milestone | Plans Complete | Status | Completed |
|-------|-----------|---------------|--------|-----------|
| 1. Capture fiable | v1.0 | 2/2 | Complete | 2026-04-30 |
| 2. Bot complet | v1.0 | 2/2 | Complete | 2026-04-30 |
| 3. Menu main.py rich | v1.1 | 2/2 | Complete | 2026-05-01 |
| 4. Messages user-friendly | v1.1 | 2/2 | Complete | 2026-05-01 |
| 5. README | v1.1 | 1/1 | Complete | 2026-05-01 |
| 6. Nettoyage + publication | v1.1 | 0/? | Pending | — |

---
*See .planning/milestones/v1.0-ROADMAP.md for full archive*

