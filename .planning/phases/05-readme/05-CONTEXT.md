# Phase 5: README — Context

**Gathered:** 2026-05-01
**Status:** Ready for planning

<domain>
## Phase Boundary

Rédiger le fichier `README.md` complet pour publication GitHub. Le README existant est obsolète (décrit l'ancien workflow `python capture_templates.py` + `python bot.py` séparément, ne mentionne pas `main.py`). Cette phase remplace entièrement ce fichier. Aucun code Python n'est modifié.

</domain>

<decisions>
## Implementation Decisions

### Langue
- **D-01:** README entièrement en anglais pour maximiser la portée GitHub.

### Ton
- **D-02:** Formules neutres (ni tutoiement ni vouvoiement) — pas de "you" imperatif dans le style direct.

### Structure (sections dans l'ordre)
- **D-03:** Description courte du projet en haut.
- **D-04:** Prérequis : Python 3.10+, Windows 11 obligatoire, MirrorTo requis, droits admin (auto-élévation), dépendances pip.
- **D-05:** Installation / Lancement : `pip install -r requirements.txt` + `python main.py`.
- **D-06:** Recalibration : phrase courte — à quoi sert l'option "Calibrer" dans le menu, sans détail technique.
- **D-07:** Auteur : Tuture, visible en bas du README.

### Visuels
- **D-08:** Un badge Python 3.10+ (shields.io) en haut du README.
- **D-09:** Une capture d'écran du menu rich à inclure — placeholder `docs/screenshot.png` à créer dans le repo. La capture réelle sera faite manuellement par l'auteur avant publication.

### Contenu exclu
- **D-10:** Pas de section comportement (tableau état→action) — le README explique comment lancer, pas le fonctionnement interne.
- **D-11:** Pas de section dépannage — minimaliste.

### Claude's Discretion
- Formulation anglaise exacte de chaque section
- Choix du badge shields.io (couleur, texte)
- Emplacement exact de la capture d'écran dans la mise en page

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Requirements
- `.planning/REQUIREMENTS.md` — DOC-01, DOC-02, DOC-03, DOC-04, DOC-05

### Contexte phases précédentes
- `.planning/phases/03-menu-principal-main-py-rich/03-CONTEXT.md` — D-01/D-06 : point d'entrée `python main.py`, menu questionary
- `.planning/phases/04-messages-user-friendly/04-CONTEXT.md` — D-08/D-10 : style rich dans capture_templates.py

### Fichiers source à lire pour le contenu
- `main.py` — point d'entrée et options du menu (Calibrer / Lancer le bot)
- `requirements.txt` — liste des dépendances pip à refléter dans le README

No external specs — requirements fully captured in decisions above.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `README.md` existant : structure à remplacer entièrement (workflow obsolète)
- `requirements.txt` : 7 libs — pyautogui, opencv-python, Pillow, numpy, pywin32, rich, questionary
- `main.py` : options du menu = "Calibrer les templates" / "Lancer le bot" / "Quitter"

### Established Patterns
- App entièrement en français côté UX (messages, menus) — le README sera la seule pièce en anglais
- Auto-élévation admin transparente dans `main.py` (ShellExecuteW runas) — à mentionner comme comportement normal, pas comme problème

### Integration Points
- Le README remplace `README.md` à la racine du repo
- La capture d'écran sera dans `docs/screenshot.png` (dossier à créer)

</code_context>

<specifics>
## Specific Ideas

- Badge Python 3.10+ avec shields.io en haut
- Capture d'écran du menu rich ASCII — placeholder à placer dans le markdown, image à fournir manuellement avant publication GitHub

</specifics>

<deferred>
## Deferred Ideas

- Section comportement (tableau état→action) — pas demandé pour ce README minimaliste
- Traduction FR du README — out of scope v1.1 (REQUIREMENTS.md)
- Packaging .exe — out of scope v1.1

</deferred>

---

*Phase: 05-readme*
*Context gathered: 2026-05-01*
