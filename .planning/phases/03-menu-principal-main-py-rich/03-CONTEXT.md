# Phase 3: Menu principal main.py avec rich - Context

**Gathered:** 2026-05-01
**Status:** Ready for planning

<domain>
## Phase Boundary

Créer `main.py` comme point d'entrée unique de l'application. Il affiche un menu TUI stylisé (rich + questionary) avec deux options : Calibrer et Lancer le bot. Il orchestre les appels aux modules `bot.py` et `capture_templates.py` via import direct. Après chaque action, le menu réapparaît automatiquement. La phase ne touche pas encore aux messages internes de bot.py/capture_templates.py (Phase 4).

</domain>

<decisions>
## Implementation Decisions

### Lancement des modules
- **D-01:** Import direct des fonctions `main()` de `bot.py` et `capture_templates.py` — pas de sous-processus
- **D-02:** L'auto-élévation admin (ShellExecuteW runas) est déplacée dans `main.py` uniquement et retirée de `bot.py` et `capture_templates.py`

### Retour au menu
- **D-03:** Après que le bot ou la calibration se terminent (normalement ou Ctrl+C), le menu rich réapparaît automatiquement — pas de fermeture du programme
- **D-04:** Ctrl+C dans le menu principal lui-même quitte l'application proprement (sans stack trace)

### Style visuel
- **D-05:** Titre ASCII art en haut du menu (nom du bot)
- **D-06:** Navigation par flèches haut/bas + Entrée pour valider — via `questionary` (pas de saisie de numéro)
- **D-07:** Style rich pour le titre et les messages d'état (couleurs, bordures) — `questionary` gère le menu interactif lui-même

### Dépendances ajoutées
- **D-08:** `rich` + `questionary` ajoutés à `requirements.txt`

### Claude's Discretion
- Palette de couleurs exacte du titre ASCII art
- Texte exact des options du menu (peut être "Calibrer les templates" / "Lancer le bot" ou similaire)
- Gestion des messages d'état entre les sessions (ex: "Bot arrêté" avant de réafficher le menu)

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Fichiers source à modifier
- `bot.py` — retirer le bloc auto-élévation admin (lignes ~17-19), garder `main()` appelable
- `capture_templates.py` — retirer le bloc auto-élévation admin, garder `main()` appelable

### Requirements
- `.planning/REQUIREMENTS.md` — UX-01, UX-02, UX-03, UX-04

No external specs — requirements fully captured in decisions above.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `bot.main()` : fonction principale du bot, appelable directement après retrait de l'auto-élévation
- `capture_templates.main()` : fonction principale de calibration, appelable directement
- `config.py` / `config.json` : système de config existant, aucune modification nécessaire

### Established Patterns
- Auto-élévation admin : pattern `ctypes.windll.shell32.IsUserAnAdmin()` + `ShellExecuteW` — à déplacer dans `main.py`
- `logging` utilisé dans `bot.py`, `print()` dans `capture_templates.py` — cohérence à adresser en Phase 4

### Integration Points
- `main.py` importe `bot` et `capture_templates` comme modules
- L'élévation admin doit se faire AVANT tout import win32 (qui peut nécessiter les droits)

</code_context>

<specifics>
## Specific Ideas

- Navigation flèches style TUI — questionary est la lib choisie
- Le menu doit réapparaître après chaque action sans relancer le programme

</specifics>

<deferred>
## Deferred Ideas

- Messages internes user-friendly dans bot.py et capture_templates.py — Phase 4
- Packaging .exe — out of scope v1.1

</deferred>

---

*Phase: 03-menu-principal-main-py-rich*
*Context gathered: 2026-05-01*
