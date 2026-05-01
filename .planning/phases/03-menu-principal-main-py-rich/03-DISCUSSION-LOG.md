# Phase 3: Menu principal main.py - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-01
**Phase:** 3 — Menu principal main.py avec rich
**Areas discussed:** Lancement des modules, Retour au menu, Style visuel du menu

---

## Lancement des modules

| Option | Description | Selected |
|--------|-------------|----------|
| Sous-processus (subprocess) | main.py lance bot.py ou capture_templates.py comme un nouveau processus Python — propre, isolé | |
| Import direct | main.py importe et appelle les fonctions main() directement — auto-élévation à déplacer dans main.py | ✓ |

**User's choice:** Import direct
**Notes:** L'auto-élévation admin (ShellExecuteW runas) sera déplacée dans main.py uniquement et retirée des deux autres scripts.

---

## Retour au menu

| Option | Description | Selected |
|--------|-------------|----------|
| Retour automatique au menu | Quand le bot s'arrête (Ctrl+C ou fin normale), le menu rich réapparaît automatiquement | ✓ |
| Quitter après chaque action | Quand le bot s'arrête, le programme se ferme | |

**User's choice:** Retour automatique au menu

---

## Style visuel du menu

| Option | Description | Selected |
|--------|-------------|----------|
| ASCII art + numéros | Titre ASCII art, couleurs riches, navigation par touches numérotées | |
| Navigation flèches (TUI) | Flèches haut/bas pour naviguer, Entrée pour valider | ✓ |

**User's choice:** Navigation flèches (TUI)

| Option | Description | Selected |
|--------|-------------|----------|
| Oui, ajouter la dépendance | Ajouter questionary ou InquirerPy — pip install simple, très léger | ✓ |
| Non, rester simple | Rester avec rich seul + touches numérotées | |

**User's choice:** Ajouter questionary (lib TUI légère pour navigation flèches)

---

## Claude's Discretion

- Palette de couleurs exacte du titre ASCII art
- Texte exact des options du menu
- Messages d'état entre sessions (ex: "Bot arrêté" avant de réafficher le menu)

## Deferred Ideas

- Messages internes user-friendly dans bot.py et capture_templates.py → Phase 4
- Packaging .exe → out of scope v1.1
