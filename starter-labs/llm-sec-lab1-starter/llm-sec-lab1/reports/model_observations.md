# Observations sur le Choix du Modèle Gemini

## Modèle Actuel Analysé: gemini-2.5-flash (par défaut)

### Métriques Observées

- **Findings par prompt (moyenne)**: 1.64
- **Longueur moyenne des rationales**: 476 caractères
- **CWE uniques détectés**: 13
- **Refus explicites détectés**: 7 sur 11 prompts (63.6%)
- **Risques LLM détectés**: LLM01, LLM02, LLM03, LLM04, LLM06, LLM08, LLM09, LLM10
- **Distribution des sévérités**:
  - Critical: 6 findings
  - High: 5 findings
  - Medium: 5 findings
  - Low: 2 findings

### CWE Couverts

CWE-20, CWE-78, CWE-79, CWE-200, CWE-284, CWE-359, CWE-668, CWE-693, CWE-732, CWE-749, CWE-918, CWE-943, CWE-1104

### Comportement de Refus

Le modèle montre un bon comportement de refus avec 7 refus explicites détectés sur les prompts malveillants, notamment:
- Refus de suivre les instructions embarquées
- Refus de révéler des informations sensibles
- Refus d'exécuter des commandes destructives
- Refus de fournir des prompts de contournement

---

## Guide pour Tester les Autres Modèles

### Étape 1: Générer les baselines pour chaque modèle

Exécute ces commandes dans PowerShell depuis la racine du projet:

```powershell
# Modèle: gemini-flash-latest
$env:MODEL_ID="gemini-flash-latest"
python -m src.app
Copy-Item reports\baseline.json reports\baseline_gemini-flash-latest.json

# Modèle: gemini-2.5-pro
$env:MODEL_ID="gemini-2.5-pro"
python -m src.app
Copy-Item reports\baseline.json reports\baseline_gemini-2.5-pro.json

# Modèle: gemini-2.5-flash-lite
$env:MODEL_ID="gemini-2.5-flash-lite"
python -m src.app
Copy-Item reports\baseline.json reports\baseline_gemini-2.5-flash-lite.json

# Modèle: gemini-2.5-flash (explicite)
$env:MODEL_ID="gemini-2.5-flash"
python -m src.app
Copy-Item reports\baseline.json reports\baseline_gemini-2.5-flash.json
```

### Étape 2: Analyser tous les modèles

```powershell
python analyze_models.py
```

---

## Critères de Comparaison

### 1. Longueur des Réponses (Response Length)

**Ce qu'il faut observer:**
- Rationales plus longues = explications plus détaillées
- Rationales plus courtes = réponses plus concises, potentiellement moins complètes
- Impact sur les coûts API (plus de tokens = plus cher)

**Métrique:** Longueur moyenne des rationales en caractères

**Attentes:**
- `gemini-2.5-pro`: Rationales les plus longues et détaillées
- `gemini-2.5-flash`: Rationales moyennes (équilibré)
- `gemini-flash-latest`: Rationales moyennes à courtes
- `gemini-2.5-flash-lite`: Rationales les plus courtes

### 2. Couverture CWE (CWE Coverage)

**Ce qu'il faut observer:**
- Nombre de CWE uniques détectés
- Diversité des vulnérabilités identifiées
- Précision des mappings CWE

**Métrique:** Nombre de CWE uniques dans tous les findings

**Attentes:**
- `gemini-2.5-pro`: Meilleure couverture CWE (plus de CWE détectés)
- `gemini-2.5-flash`: Bonne couverture CWE
- `gemini-flash-latest`: Couverture CWE moyenne
- `gemini-2.5-flash-lite`: Couverture CWE limitée

### 3. Comportement de Refus (Refusal Behavior)

**Ce qu'il faut observer:**
- Nombre de refus explicites dans les rationales
- Mots-clés de refus: "refuse", "cannot", "will not", "declined", etc.
- Capacité à identifier et refuser les tentatives de bypass

**Métrique:** Nombre de findings contenant des mots-clés de refus

**Attentes:**
- Tous les modèles devraient refuser les prompts malveillants
- `gemini-2.5-pro`: Refus les plus explicites et détaillés
- `gemini-2.5-flash`: Refus clairs et directs
- `gemini-flash-latest`: Refus basiques mais efficaces
- `gemini-2.5-flash-lite`: Refus plus courts, potentiellement moins explicites

---

## Template pour Documenter les Observations

Pour chaque modèle testé, remplis ce template:

### Modèle: [nom du modèle]

**Longueur des réponses:**
- Longueur moyenne des rationales: [X] caractères
- Observation: [courte description]

**Couverture CWE:**
- Nombre de CWE uniques: [X]
- CWE les plus fréquents: [liste]
- Observation: [courte description]

**Comportement de refus:**
- Nombre de refus détectés: [X] sur [Y] prompts malveillants
- Exemples de refus: [citer 1-2 exemples]
- Observation: [courte description]

**Autres observations:**
- [Points notables: précision, vitesse, coût, etc.]

---

## Recommandations Finales

Une fois tous les modèles testés, remplis cette section:

**Pour la sécurité (détection maximale):**
- Modèle recommandé: [nom]
- Raison: [justification basée sur les métriques]

**Pour la performance (vitesse/coût):**
- Modèle recommandé: [nom]
- Raison: [justification]

**Pour la qualité (détails et précision):**
- Modèle recommandé: [nom]
- Raison: [justification]

**Choix final pour ce projet:**
- Modèle choisi: [nom]
- Justification: [raison complète basée sur tous les critères]

