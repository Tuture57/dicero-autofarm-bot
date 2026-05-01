# Phase 5: README — Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-05-01
**Phase:** 05-readme
**Areas discussed:** Prérequis, Structure, Recalibration, Ton et langue

---

## Prérequis

| Option | Description | Selected |
|--------|-------------|----------|
| Python 3.10+ | Compatible majorité Windows récents | ✓ |
| Python 3.8+ | Plus permissif, installs plus anciennes | |
| Tu décides | Claude choisit | |

**User's choice:** Python 3.10+

---

| Option | Description | Selected |
|--------|-------------|----------|
| Windows 11 obligatoire | DPI 125%, ne fonctionne pas sur Mac/Linux | ✓ |
| MirrorTo requis | Doit être ouvert avec le jeu mirroré | ✓ |
| Droits admin (auto-élévation) | main.py se relance en admin automatiquement | ✓ |
| Dépendances pip | pip install -r requirements.txt | ✓ |

**User's choice:** Les 4 prérequis — tous à mentionner

---

## Structure

| Option | Description | Selected |
|--------|-------------|----------|
| Minimaliste — l'essentiel en 1-2 min de lecture | Titre + prérequis + install + utilisation + recalibration + auteur | ✓ |
| Complet — comme un vrai projet open source | + tableau comportement, dépannage, badges optionnels | |
| Tu décides | Claude choisit l'équilibre | |

**User's choice:** Minimaliste

---

| Option | Description | Selected |
|--------|-------------|----------|
| Section comportement (tableau état→action) | Oui — tableau état→action | |
| Non — pas de section comportement | README explique comment lancer, pas le fonctionnement interne | ✓ |

**User's choice:** Pas de section comportement

---

| Option | Description | Selected |
|--------|-------------|----------|
| Installation / Lancement | pip install + python main.py | ✓ |
| Recalibration | Quand et comment recalibrer | ✓ |
| Description | Description courte du projet en haut | ✓ |
| Auteur | Tuture, visible en bas (DOC-05) | ✓ |

**User's choice:** Toutes les sections

---

## Recalibration

| Option | Description | Selected |
|--------|-------------|----------|
| Phrase courte | Juste à quoi sert Calibrer, sans détail technique | ✓ |
| Paragraphe | Avec les 2 cas (cartes et dés), fenêtre fixe | |
| Guide pas-à-pas numéroté | Étapes détaillées | |

**User's choice:** Phrase courte

---

## Ton et langue

| Option | Description | Selected |
|--------|-------------|----------|
| Tutoiement (tu) | Cohérent avec l'app | |
| Vouvoiement (vous) | Plus formel | |
| Neutre | Formules impersonnelles sans tu/vous | ✓ |

**User's choice:** Neutre

---

| Option | Description | Selected |
|--------|-------------|----------|
| Français uniquement | Cohérent avec l'app et audience FR | |
| Anglais pour le titre, FR pour le reste | Mix | |
| Anglais uniquement | Maximiser portée GitHub | ✓ |

**User's choice:** Anglais uniquement

---

| Option | Description | Selected |
|--------|-------------|----------|
| Rien — texte uniquement | Plus simple, rien à maintenir | |
| Badge Python version uniquement | Aspect pro | |
| Badge + capture d'écran | Badge + screenshot du menu rich | ✓ |

**User's choice:** Badge + capture d'écran

---

## Claude's Discretion

- Formulation anglaise exacte de chaque section
- Choix du badge shields.io (couleur, texte)
- Emplacement exact de la capture d'écran dans la mise en page

## Deferred Ideas

- Section comportement (tableau état→action)
- Traduction FR du README
- Packaging .exe
