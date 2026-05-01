# Phase 2: Bot complet — Discussion Log

> **Audit trail only.** Decisions are captured in CONTEXT.md.

**Date:** 2026-04-30
**Phase:** 02-bot-complet-tous-les-etats-toutes-les-actions
**Areas discussed:** Positions fixes des cartes et dés

---

## Positions fixes des cartes et dés

| Option | Description | Selected |
|--------|-------------|----------|
| Coordonnées exactes fournies | L'utilisateur donne les pixels maintenant | |
| Fractions de la zone de jeu | Calculé en 1/6, 1/2, 5/6 en X | |
| Calibration interactive via capture_templates.py | Clic sur les éléments pour enregistrer la position | ✓ |

**User's choice:** Calibration interactive via capture_templates.py

---

| Option | Description | Selected |
|--------|-------------|----------|
| 5 dés calibrés | Tous les dés de la rangée du haut | |
| Juste le premier dé | Une seule position à calibrer | ✓ |

**User's choice:** Juste le premier dé (ACT-05)

---

| Option | Description | Selected |
|--------|-------------|----------|
| config.json | Tout centralisé au même endroit | ✓ |
| positions.json | Fichier séparé | |

**User's choice:** config.json

---

## Claude's Discretion

- Ordre de priorité des états dans detect_state
- Gestion du délai après rewards
- Robustesse sur état unknown persistant (v1 = comportement actuel suffisant)

## Deferred Ideas

- ROB-01/02 (robustesse avancée) → v2 requirements
- Calibration des 5 dés → non nécessaire
