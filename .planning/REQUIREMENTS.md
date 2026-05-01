# Requirements — Autofarm Dungeon Bot

## Milestone v1.1 — Publication GitHub

### UX — Menu et point d'entrée

- [ ] **UX-01**: L'utilisateur peut lancer `python main.py` et voir un menu stylisé rich avec titre ASCII
- [ ] **UX-02**: L'utilisateur peut choisir "Calibrer" depuis le menu pour lancer la calibration
- [ ] **UX-03**: L'utilisateur peut choisir "Lancer le bot" depuis le menu pour démarrer le bot
- [ ] **UX-04**: L'utilisateur peut quitter proprement avec Ctrl+C depuis n'importe quel état

### UX — Messages et feedback

- [ ] **UX-05**: Les messages d'état du bot sont clairs et non-techniques (ex: "Fenêtre MirrorTo introuvable")
- [ ] **UX-06**: Les messages de calibration guident l'utilisateur étape par étape
- [ ] **UX-07**: Le style visuel (rich) est cohérent entre main.py, bot.py et capture_templates.py

### DOC — Documentation

- [x] **DOC-01**: Le README contient les prérequis (Python, MirrorTo, pip) — Validated in Phase 5: README
- [x] **DOC-02**: Le README contient les étapes d'installation numérotées, copier-coller ready — Validated in Phase 5: README
- [x] **DOC-03**: Le README explique comment utiliser le menu (`python main.py`) — Validated in Phase 5: README
- [x] **DOC-04**: Le README explique comment recalibrer si la fenêtre MirrorTo bouge — Validated in Phase 5: README
- [x] **DOC-05**: Le README mentionne Tuture comme auteur unique — Validated in Phase 5: README

### PUB — Publication

- [ ] **PUB-01**: Le repo ne contient aucun fichier de test/debug/temporaire
- [ ] **PUB-02**: Le `.gitignore` couvre `__pycache__`, `.venv`, captures temporaires, etc.
- [ ] **PUB-03**: L'historique Git est vierge — un seul commit "Initial release" signé Tuture
- [ ] **PUB-04**: Le nom de l'auteur Git est "Tuture" sur le commit final

---

## Traceability

| REQ-ID | Phase |
|--------|-------|
| UX-01 | Phase 3 |
| UX-02 | Phase 3 |
| UX-03 | Phase 3 |
| UX-04 | Phase 3 |
| UX-05 | Phase 4 |
| UX-06 | Phase 4 |
| UX-07 | Phase 4 |
| DOC-01 | Phase 5 |
| DOC-02 | Phase 5 |
| DOC-03 | Phase 5 |
| DOC-04 | Phase 5 |
| DOC-05 | Phase 5 |
| PUB-01 | Phase 6 |
| PUB-02 | Phase 6 |
| PUB-03 | Phase 6 |
| PUB-04 | Phase 6 |

---

## Out of Scope (v1.1)

- Interface graphique (GUI) — CLI + menu rich suffit
- Packaging en .exe — pip install suffit pour l'audience cible
- Traduction en anglais — le bot cible une audience FR pour l'instant
- Tests automatisés — pas demandé

---

## Previously Validated (v1.0)

- ✓ CAP-01 à CAP-03 : Capture PIL ImageGrab stable
- ✓ STATE-01 à STATE-09 : Détection des 9 états
- ✓ ACT-01 à ACT-07 : Toutes les actions
- ✓ TMPL-01 à TMPL-05 : Script de capture interactif
