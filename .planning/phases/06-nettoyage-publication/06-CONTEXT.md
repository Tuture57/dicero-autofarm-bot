# Phase 6: Nettoyage et publication — Context

**Gathered:** 2026-05-01
**Status:** Ready for planning

<domain>
## Phase Boundary

Nettoyer le repo pour publication GitHub : supprimer les fichiers de développement, créer `.gitignore`, gérer `config.json`, et réécrire l'historique Git en un seul commit "Initial release" sur la branche `main`.
Aucun code Python n'est modifié. Aucune nouvelle fonctionnalité.

</domain>

<decisions>
## Implementation Decisions

### config.json
- **D-01:** `config.json` ne sera PAS dans le repo. Créer `config.json.example` qui sera versionné à sa place.
- **D-02:** `config.json.example` contient les vraies valeurs calibrées actuelles comme point de départ (offsets, positions, confidence, delays). L'utilisateur copie le fichier et recalibre avec le menu.
- **D-03:** `config.json` ajouté au `.gitignore` — le bot le crée/utilise localement, les utilisateurs en créent un via la calibration.

### Fichiers à supprimer
- **D-04:** Supprimer du repo (et du disque) : `bot_backup.py`, `test_clicks.py`, `test_admin_background.py` (untracked).
- **D-05:** `__pycache__/` sera couvert par `.gitignore` — pas besoin de le supprimer manuellement si déjà ignoré.

### templates/
- **D-06:** Les 14 PNG dans `templates/` sont inclus dans le repo. Le bot fonctionne immédiatement après `git clone` + `pip install` + copie de `config.json.example`.

### .gitignore
- **D-07:** Entrées `.gitignore` :
  - `__pycache__/`
  - `*.pyc`
  - `*.pyo`
  - `config.json`
  - `.venv/`
  - `venv/`
- **D-08:** `docs/screenshot.png` reste versionné (placeholder inclus).

### Historique Git vierge
- **D-09:** Technique : `git checkout --orphan` sur une nouvelle branche, ajouter tous les fichiers, commit unique, remplacer `master`.
- **D-10:** Message du commit final : `"Initial release — AutoFarm Dungeon Bot v1.0"`
- **D-11:** Auteur : config Git globale actuelle (Tuture57) — pas de changement.
- **D-12:** Branche finale : renommer en `main` avant publication (convention GitHub actuelle).

### Claude's Discretion
- Ordre exact des étapes de nettoyage (suppression fichiers → .gitignore → config.json.example → orphan commit → rename branch)
- Format exact du `.gitignore` (commentaires, sections)
- Valeur de l'email Git si besoin

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Requirements
- `.planning/REQUIREMENTS.md` — PUB-01, PUB-02, PUB-03, PUB-04

### Fichiers source à inspecter
- `config.json` — valeurs actuelles à copier dans `config.json.example`
- `bot.py` — vérifier qu'il lit bien `config.json` (pas hardcodé)
- `main.py` — vérifier qu'il n'y a pas de référence à des fichiers supprimés

No external specs — requirements fully captured in decisions above.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `config.json` (actuel) : source pour `config.json.example` — copier les valeurs telles quelles
- `templates/` : 14 PNG à conserver tels quels

### Established Patterns
- `bot.py` et `capture_templates.py` lisent `config.json` via `config.py` — le fichier doit exister au runtime
- `main.py` : auto-élévation admin via `ShellExecuteW` — aucun impact sur le nettoyage

### Integration Points
- Le README mentionne déjà `python main.py` comme point d'entrée — cohérent avec le repo nettoyé
- `config.json.example` devra être mentionné dans le README (étape de setup) — ou dans un commentaire de la section Installation

### Fichiers à supprimer (confirmés)
- `bot_backup.py` — sauvegarde obsolète
- `test_clicks.py` — script de développement
- `test_admin_background.py` — untracked, jamais commité

</code_context>

<specifics>
## Specific Ideas

- `config.json.example` : même contenu que `config.json` actuel, avec les vraies valeurs comme base de départ
- Branche finale : `main` (renommer depuis `master` après l'orphan commit)
- Commit message exact : `Initial release — AutoFarm Dungeon Bot v1.0`

</specifics>

<deferred>
## Deferred Ideas

- Mention de `config.json.example` dans le README (section Installation) — pourrait être ajoutée dans une phase future si nécessaire, mais le README actuel explique déjà la calibration via le menu
- Publication effective sur GitHub (push) — hors scope de cette phase, action manuelle de l'utilisateur

</deferred>

---

*Phase: 06-nettoyage-publication*
*Context gathered: 2026-05-01*
