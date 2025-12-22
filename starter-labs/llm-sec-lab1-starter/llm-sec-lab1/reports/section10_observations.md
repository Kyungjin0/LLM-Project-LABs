# Réponses à la Section 10: Explore Other Gemini Models

## Instructions du README

La section 10 demande de:
1. Tester différents modèles Gemini (`gemini-flash-latest`, `gemini-2.5-pro`, `gemini-2.5-flash-lite`)
2. Noter les observations sur:
   - **Response length** (longueur des réponses)
   - **CWE coverage** (couverture CWE)
   - **Refusal behavior** (comportement de refus)
3. Utiliser ces observations pour la section "Observations"

---

## Comment Générer les Baselines pour Tous les Modèles

### Méthode 1: PowerShell (Recommandée)

Depuis la racine du projet (`C:\llm-cybesecurity-labs-project\starter-labs\llm-sec-lab1-starter\llm-sec-lab1`):

```powershell
# 1. gemini-flash-latest
$env:MODEL_ID="gemini-flash-latest"
python -m src.app
Copy-Item reports\baseline.json reports\baseline_gemini-flash-latest.json
Write-Host  Baseline généré pour gemini-flash-latest"

# 2. gemini-2.5-pro
$env:MODEL_ID="gemini-2.5-pro"
python -m src.app
Copy-Item reports\baseline.json reports\baseline_gemini-2.5-pro.json
Write-Host  Baseline généré pour gemini-2.5-pro"

# 3. gemini-2.5-flash-lite
$env:MODEL_ID="gemini-2.5-flash-lite"
python -m src.app
Copy-Item reports\baseline.json reports\baseline_gemini-2.5-flash-lite.json
Write-Host  Baseline généré pour gemini-2.5-flash-lite"

# 4. gemini-2.5-flash (explicite, pour comparaison)
$env:MODEL_ID="gemini-2.5-flash"
python -m src.app
Copy-Item reports\baseline.json reports\baseline_gemini-2.5-flash.json
Write-Host  Baseline généré pour gemini-2.5-flash"
```

### Méthode 2: Via le Notebook Jupyter

Dans `notebooks/lab1_live_run.ipynb`, ajoute une cellule pour chaque modèle:

```python
import os
os.environ["MODEL_ID"] = "gemini-flash-latest"  # Change pour chaque modèle
from src import app
app.main()
```

Puis copie manuellement `reports/baseline.json` vers le nom approprié.

---

## Comment Analyser et Comparer les Modèles

### Étape 1: Exécuter le script d'analyse

```powershell
python analyze_models.py
```

Ce script génère automatiquement:
- Un tableau comparatif des métriques
- Des détails pour chaque modèle
- Un rapport markdown dans `reports/model_analysis_report.md`

### Étape 2: Examiner les métriques clés

Pour chaque modèle, note:

1. **Response Length (Longueur des réponses)**
   - Regarde la colonne "Long. Rationale" dans le tableau
   - Compare avec les autres modèles
   - Plus long = plus détaillé mais plus cher

2. **CWE Coverage (Couverture CWE)**
   - Regarde la colonne "CWE Uniques"
   - Compare le nombre de CWE différents détectés
   - Plus de CWE = meilleure détection de divers types de vulnérabilités

3. **Refusal Behavior (Comportement de refus)**
   - Regarde la colonne "Refus"
   - Compare le nombre de refus explicites
   - Plus de refus = meilleure résistance aux attaques

---

## Observations Basées sur le Modèle Actuel (gemini-2.5-flash)

### Métriques Observées

- **Findings par prompt**: 1.64 (moyenne)
- **Longueur moyenne des rationales**: 476 caractères
- **CWE uniques détectés**: 13
- **Refus explicites**: 7 sur 11 prompts (63.6%)
- **Risques LLM couverts**: LLM01, LLM02, LLM03, LLM04, LLM06, LLM08, LLM09, LLM10

### Points Forts
 **Bonne couverture CWE**: 13 CWE différents détectés, couvrant un large éventail de vulnérabilités **Refus explicites**: 7 refus détectés sur les prompts malveillants **Rationales détaillées**: 476 caractères en moyenne, explications complètes **Détection complète**: Tous les risques OWASP LLM Top 10 pertinents sont détectés

### Points à Améliorer

⚠️ Certains prompts légitimes génèrent des findings (overreliance détectée, ce qui est correct mais peut être considéré comme "trop strict")
⚠️ Rationales parfois longues (impact sur les coûts API)

---

## Comparaison Attendue avec les Autres Modèles

### gemini-2.5-pro

**Attentes basées sur la documentation:**
- Rationales plus longues et détaillées que Flash
- Meilleure couverture CWE
- Refus plus explicites et nuancés
- **Risque**: Peut sous-rapporter sur les prompts bénins (retourne findings vides)

**Utilisation recommandée**: Quand la qualité et la précision sont prioritaires, avec revue humaine

### gemini-flash-latest

**Attentes basées sur la documentation:**
- Rationales similaires à Flash mais plus courtes
- Couverture CWE similaire
- Refus efficaces mais moins détaillés
- **Note**: Peut générer des warnings `thought_signature` mais JSON valide après nettoyage

**Utilisation recommandée**: Bon compromis vitesse/qualité

### gemini-2.5-flash-lite

**Attentes basées sur la documentation:**
- Rationales les plus courtes
- Décisions similaires à Flash mais explications réduites
- Bon pour budgets serrés
- **Risque**: Rationales courtes peuvent être moins claires

**Utilisation recommandée**: Quand le coût/latence sont critiques et que les explications courtes sont acceptables

---

## Template pour Documenter Tes Observations

Une fois que tu as généré tous les baselines, remplis ce template:

```markdown
## Observations sur les Modèles Gemini

### 1. Response Length (Longueur des Réponses)

| Modèle | Longueur Moyenne | Observation |
|--------|------------------|-------------|
| gemini-2.5-flash | 476 chars | [Tes observations] |
| gemini-2.5-pro | [X] chars | [Tes observations] |
| gemini-flash-latest | [X] chars | [Tes observations] |
| gemini-2.5-flash-lite | [X] chars | [Tes observations] |

**Conclusion**: [Quel modèle a les réponses les plus longues/courtes et pourquoi c'est important]

### 2. CWE Coverage (Couverture CWE)

| Modèle | CWE Uniques | CWE les Plus Fréquents | Observation |
|--------|-------------|------------------------|-------------|
| gemini-2.5-flash | 13 | CWE-943, CWE-200, CWE-693 | [Tes observations] |
| gemini-2.5-pro | [X] | [Liste] | [Tes observations] |
| gemini-flash-latest | [X] | [Liste] | [Tes observations] |
| gemini-2.5-flash-lite | [X] | [Liste] | [Tes observations] |

**Conclusion**: [Quel modèle détecte le plus de types de vulnérabilités]

### 3. Refusal Behavior (Comportement de Refus)

| Modèle | Refus Détectés | Exemples de Refus | Observation |
|--------|----------------|-------------------|-------------|
| gemini-2.5-flash | 7/11 | "I refuse to comply", "cannot provide" | [Tes observations] |
| gemini-2.5-pro | [X]/11 | [Exemples] | [Tes observations] |
| gemini-flash-latest | [X]/11 | [Exemples] | [Tes observations] |
| gemini-2.5-flash-lite | [X]/11 | [Exemples] | [Tes observations] |

**Conclusion**: [Quel modèle refuse le mieux les tentatives malveillantes]

### Recommandation Finale

**Modèle choisi pour ce projet**: [nom du modèle]

**Justification**:
- [Raison 1 basée sur les métriques]
- [Raison 2 basée sur les métriques]
- [Raison 3 basée sur les métriques]

**Trade-offs acceptés**:
- [Ce qu'on gagne]
- [Ce qu'on perd]
```

---

## Commandes Rapides pour Tout Faire d'un Coup

Crée un fichier `generate_all_baselines.ps1`:

```powershell
# Script PowerShell pour générer tous les baselines

$models = @(
    "gemini-flash-latest",
    "gemini-2.5-pro",
    "gemini-2.5-flash-lite",
    "gemini-2.5-flash"
)

foreach ($model in $models) {
    Write-Host "`n🔄 Génération du baseline pour $model..."
    $env:MODEL_ID = $model
    python -m src.app
    $outputFile = "reports\baseline_$model.json"
    Copy-Item reports\baseline.json $outputFile
    Write-Host  Baseline sauvegardé: $outputFile"
}

Write-Host "`n📊 Analyse des modèles..."
python analyze_models.py

Write-Host "` Terminé! Consulte reports/model_analysis_report.md pour les résultats."
```

Puis exécute:
```powershell
.\generate_all_baselines.ps1
```

---

## Prochaines Étapes

1. Génère les baselines pour tous les modèles (voir commandes ci-dessus)
2. Exécute `python analyze_models.py` pour obtenir les métriques
3. Compare les résultats dans les tableaux générés
4. Remplis le template d'observations ci-dessus
5. Intègre tes observations dans la section "Observations" de ton rapport final

