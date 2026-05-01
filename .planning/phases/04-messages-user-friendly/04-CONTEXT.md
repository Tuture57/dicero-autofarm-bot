# Phase 4: Messages user-friendly dans bot.py et capture_templates.py - Context

**Gathered:** 2026-05-01
**Status:** Ready for planning

<domain>
## Phase Boundary

Réécrire tous les messages affichés à l'utilisateur dans `bot.py` et `capture_templates.py` pour les rendre clairs, non-techniques et visuellement cohérents avec `main.py`. La capture d'écran, la détection d'état et les clics ne changent pas. Phase purement cosmétique/UX.

</domain>

<decisions>
## Implementation Decisions

### Style bot.py
- **D-01:** Remplacer `logging.basicConfig` par `logging.basicConfig` avec `RichHandler` de `rich.logging`. Garder `logging` comme infrastructure, utiliser RichHandler pour le rendu.
- **D-02:** Timestamps activés (`show_time=True` dans RichHandler — comportement par défaut).
- **D-03:** La couleur par niveau de log (INFO=vert, WARNING=jaune, ERROR=rouge) est gérée nativement par RichHandler — différenciation visuelle erreurs bloquantes vs warnings récupérables automatique.

### Verbosité bot
- **D-04:** Mode épuré — seuls les événements notables sont loggés en INFO : démarrage, arrêt, changements d'état, erreurs. Les clics individuels répétitifs (`Clicking Attack`, `Selecting skill card at...`) passent en `log.debug()` (masqués par défaut).
- **D-05:** Pour les états répétés (ex: `attack_btn` en boucle) : loguer uniquement au changement d'état (Claude décide l'implémentation — variable `last_state` pour tracker le dernier état loggé).

### Messages erreur
- **D-06:** Ton instructif pour les erreurs critiques — message explicite + action à faire. Exemples :
  - Fenêtre MirrorTo introuvable → "Fenêtre MirrorTo introuvable. Lance MirrorTo, puis réessaie."
  - Config non calibrée → "Positions non calibrées — lance 'Calibrer les templates' depuis le menu."
  - Template manquant → "Template manquant : {nom}. Recalibre les templates depuis le menu."
- **D-07:** Distinction visuelle : warnings récupérables = `log.warning()` (jaune RichHandler), erreurs bloquantes = `log.error()` (rouge RichHandler).

### Style capture_templates.py
- **D-08:** Remplacer le menu `print()` par `questionary.select()` — navigation flèches, cohérent avec main.py.
- **D-09:** Messages de statut via `rich Console.print()` avec couleurs (vert = succès, rouge = erreur).
- **D-10:** Instructions de calibration (ex: "Navigue vers l'écran Select Skill...") encadrées dans des `rich Panel` avant chaque étape.

### Claude's Discretion
- Texte exact de chaque message (formulation française, ton conversationnel)
- Implémentation de la variable `last_state` pour le log au changement d'état
- Choix de couleurs et bordures des Panels rich dans capture_templates.py
- Import et initialisation de `console = Console()` dans capture_templates.py

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Fichiers à modifier
- `bot.py` — messages logging (lignes ~46, 57, 214, 223, 238, 241, 249, 251, 259, 268, 277, 286, 296, 308, 314, 324, 345, 347, 348, 359, 367, 371, 379, 384, 410)
- `capture_templates.py` — menu interactif et messages print() (lignes ~76-252)

### Requirements
- `.planning/REQUIREMENTS.md` — UX-05, UX-06, UX-07

### Contexte Phase 3
- `.planning/phases/03-menu-principal-main-py-rich/03-CONTEXT.md` — D-07 : cohérence visuelle rich entre les fichiers

No external specs — requirements fully captured in decisions above.

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `rich` et `questionary` déjà dans `requirements.txt` (ajoutés Phase 3) — aucune dépendance à ajouter
- `main.py` : pattern `Console()`, `Panel()`, `questionary.select()` — à reproduire dans capture_templates.py
- `bot.py` ligne 17 : `logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')` — à remplacer par RichHandler

### Established Patterns
- `bot.py` : architecture logging existante — `log = logging.getLogger(__name__)`, tous les appels via `log.info/warning/error()`
- `capture_templates.py` : menu avec `input()` et `print()` — à remplacer par questionary + rich
- La fonction `main()` dans capture_templates.py est le point d'entrée du menu (lignes ~207-252)

### Integration Points
- `bot.py` est importé par `main.py` — les messages apparaissent dans le terminal pendant que le bot tourne depuis le menu rich
- `capture_templates.py` est importé par `main.py` — idem
- RichHandler dans bot.py cohabite bien avec le Console de main.py (même terminal)

</code_context>

<specifics>
## Specific Ideas

- Cohérence visuelle avec main.py : même bibliothèques (rich + questionary), même style de messages
- Les erreurs instructives doivent mentionner l'action à faire (ex: "depuis le menu", "relance MirrorTo")

</specifics>

<deferred>
## Deferred Ideas

- Logging vers fichier (rotation, persistence) — pas demandé en v1.1
- Barre de progression ou spinner pendant les runs — out of scope

</deferred>

---

*Phase: 04-messages-user-friendly*
*Context gathered: 2026-05-01*
