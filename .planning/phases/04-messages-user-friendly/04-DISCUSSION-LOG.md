# Phase 4: Messages user-friendly — Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-01
**Phase:** 04-messages-user-friendly
**Areas discussed:** Style bot.py, Verbosité bot, Messages erreur, Style capture_templates

---

## Style bot.py

| Option | Description | Selected |
|--------|-------------|----------|
| Rich pur — plus de logging | Remplacer logging par rich Console.print() | |
| logging + RichHandler | Garder logging, ajouter RichHandler pour le rendu | ✓ |
| Textes seulement | Juste réécrire les textes, pas de rich dans bot.py | |

**User's choice:** logging + RichHandler
**Notes:** Compatible debug, timestamps activés par défaut.

---

## Timestamps RichHandler

| Option | Description | Selected |
|--------|-------------|----------|
| Avec timestamps | show_time=True (défaut RichHandler) | ✓ |
| Sans timestamps | show_time=False, plus épuré | |
| Claude décide | — | |

**User's choice:** Avec timestamps

---

## Verbosité bot

| Option | Description | Selected |
|--------|-------------|----------|
| Épuré — événements notables uniquement | Clics en DEBUG, états/erreurs en INFO | ✓ |
| Verbeux — tout visible | Pareil qu'aujourd'hui mais formaté rich | |
| Ligne unique — rich Live spinner | rich.Live, plus compact | |

**User's choice:** Épuré — événements notables uniquement

---

## États répétés

| Option | Description | Selected |
|--------|-------------|----------|
| Changement d'état seulement | Log uniquement quand l'état change | |
| Throttle — une fois toutes les 5s | Log périodiquement | |
| Claude décide | Granularité laissée à Claude | ✓ |

**User's choice:** Claude décide
**Notes:** Implémentation prévue : variable `last_state` pour ne logger que les changements.

---

## Messages erreur

| Option | Description | Selected |
|--------|-------------|----------|
| Instructif — quoi faire ensuite | Message + action à faire | ✓ |
| Minimaliste — message seul | Message court sans instruction | |
| Claude décide | — | |

**User's choice:** Instructif — quoi faire ensuite

---

## Distinction visuelle erreurs

| Option | Description | Selected |
|--------|-------------|----------|
| Oui — différencier visuellement | Bloquant vs récupérable visuellement distincts | ✓ |
| Non — logging gère le niveau | Pas de distinction visuelle supplémentaire | |

**User's choice:** Oui — différencier visuellement
**Notes:** RichHandler gère nativement les couleurs par niveau (rouge=error, jaune=warning).

---

## Style capture_templates

| Option | Description | Selected |
|--------|-------------|----------|
| Rich + questionary — comme main.py | Menu flèches questionary + rich Console | ✓ |
| Print reformulé + rich messages | Garder menu print(), ajouter rich pour statut | |
| Textes seulement | Aucun changement de lib | |

**User's choice:** Rich + questionary — comme main.py

---

## Instructions calibration

| Option | Description | Selected |
|--------|-------------|----------|
| Panel rich pour les instructions | Instructions dans des rich Panel | ✓ |
| Instructions en texte simple | Garder print() pour les instructions | |
| Claude décide | — | |

**User's choice:** Panel rich pour les instructions

---

## Claude's Discretion

- Texte exact de chaque message reformulé
- Implémentation de `last_state` pour log au changement d'état
- Couleurs et bordures des Panels dans capture_templates.py
- Initialisation de `console = Console()` dans capture_templates.py

## Deferred Ideas

- Logging vers fichier (rotation, persistence) — pas v1.1
- Spinner/barre de progression pendant les runs — out of scope
