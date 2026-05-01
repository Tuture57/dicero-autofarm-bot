---
status: partial
phase: 1-capture-fiable-script-de-capture
source: [01-VERIFICATION.md]
started: 2026-04-30
updated: 2026-04-30
---

## Current Test

[awaiting human testing]

## Tests

### 1. Qualité des pixels ImageGrab vs BitBlt
expected: La capture via ImageGrab.grab(bbox=GetWindowRect) produit une image nette correspondant à l'affichage Android dans MirrorTo, sans image noire ni artefacts
result: [pending]

### 2. Menu interactif capture_templates.py — flux complet
expected: Le menu s'affiche avec les 9 templates et leur statut existe/manquant, la sélection par numéro capture uniquement le template choisi, la confirmation d'écrasement fonctionne
result: [pending]

## Summary

total: 2
passed: 0
issues: 0
pending: 2
skipped: 0
blocked: 0

## Gaps
