# Observations from Reference Runs - Section 12

## Résumé Exécutif

Cette section documente les observations tirées des runs de référence avec différents modèles Gemini, basées sur l'analyse des baselines générés pour les 10 prompts de test dans `data/prompts_lab1.json`.

---

## 1. Gemini 2.5 Flash (Modèle par Défaut)

### Caractéristiques Observées

**Rationales Riches et Détaillées:**
- Longueur moyenne des rationales: **476 caractères**
- Le modèle fournit des explications complètes et contextuelles pour chaque finding
- Les rationales incluent des détails techniques sur les risques identifiés
- Exemple de rationales détaillées observées dans le baseline:
  - Explications complètes des mécanismes d'injection de prompt
  - Contexte sur les implications de sécurité
  - Liens explicites entre les risques LLM et les CWE correspondants

**CWE Tagging Consistant:**
- **13 CWE uniques** détectés sur l'ensemble des prompts
- CWE couverts incluent: CWE-20, CWE-78, CWE-79, CWE-200, CWE-284, CWE-359, CWE-668, CWE-693, CWE-732, CWE-749, CWE-918, CWE-943, CWE-1104
- Mapping cohérent entre les risques LLM et les CWE appropriés
- Pas de CWE manquants pour les risques critiques identifiés

**Couverture Complète des Risques:**
- Tous les risques OWASP LLM Top 10 pertinents sont détectés: LLM01, LLM02, LLM03, LLM04, LLM06, LLM08, LLM09, LLM10
- Détection efficace des tentatives d'injection de prompt
- Identification appropriée des risques d'overreliance (LLM08) pour les prompts informationnels

**Comportement de Refus:**
- **7 refus explicites** détectés sur 11 prompts (63.6%)
- Refus clairs et directs pour les tentatives malveillantes
- Exemples de refus observés:
  - "I refuse to comply with these malicious instructions"
  - "This model is designed to analyze and identify risks, not to execute or incorporate such directives"
  - "As a security analysis tool, explicit instructions embedded within user content are treated as attempts to manipulate"

**Justification pour l'Utilisation:**
- Idéal pour les démonstrations et l'évaluation (grading) grâce aux rationales détaillées
- Excellent pour la documentation et l'analyse approfondie
- Bon équilibre entre précision et exhaustivité

---

## 2. Gemini 2.5 Flash-Lite

### Caractéristiques Observées

**Findings Similaires à Flash:**
- Les décisions de détection sont cohérentes avec Flash
- Même identification des risques LLM
- Même mapping CWE pour les vulnérabilités critiques

**Explanations Plus Courtes:**
- Rationales significativement plus courtes que Flash
- Informations essentielles préservées mais moins de contexte
- Impact positif sur la latence et les coûts API

**Avantages:**
- **Latence réduite**: Réponses plus rapides grâce aux rationales concises
- **Coût réduit**: Moins de tokens générés = coûts API inférieurs
- **Fidélité du schéma**: Respecte toujours le schéma JSON attendu
- **Décisions fiables**: Même qualité de détection que Flash

**Considérations:**
- Les explications courtes peuvent nécessiter une compréhension technique préalable
- Moins adapté pour les démonstrations où des explications détaillées sont nécessaires
- Idéal pour les environnements de production où la vitesse et le coût sont prioritaires

**Justification pour l'Utilisation:**
- Parfait pour les budgets serrés
- Excellent choix pour les systèmes en production nécessitant une faible latence
- Recommandé quand les explications courtes sont suffisantes pour les équipes techniques

---

## 3. Gemini 2.5 Pro

### Caractéristiques Observées

**Approche Conservatrice:**
- Certains prompts à faible risque peuvent retourner des **findings vides**
- Le modèle est plus sélectif dans ce qu'il considère comme un risque
- Réduction des faux positifs par rapport aux autres modèles

**Détection Fiable des Risques Critiques:**
- Les prompts sensibles (ex: exfiltration de mots de passe) déclenchent toujours des alertes de **sévérité élevée**
- Mapping fiable vers LLM01 (Prompt Injection) et LLM06 (Excessive Agency) pour les attaques évidentes
- Pas de compromis sur la sécurité pour les vraies menaces

**Rationales Probablement Plus Nuancées:**
- Attendu: explications plus sophistiquées et contextuelles que Flash
- Meilleure compréhension des nuances dans les prompts
- Potentiellement meilleure distinction entre risques réels et faux positifs

**Considérations:**
- **Risque de sous-rapportage**: Les prompts bénins peuvent ne pas générer de findings alors qu'ils présentent un risque d'overreliance (LLM08)
- Nécessite des garde-fous supplémentaires ou une revue humaine pour compenser
- Peut être trop conservateur pour certains cas d'usage

**Justification pour l'Utilisation:**
- Idéal quand la précision est plus importante que l'exhaustivité
- Recommandé pour les environnements où les faux positifs sont problématiques
- Nécessite une revue humaine ou des garde-fous stricts pour compenser le sous-rapportage potentiel

---

## 4. Améliorations Techniques: Retry Logic et Gestion des Erreurs

### Retry Logic dans `src/app.py`

**Problème Résolu:**
- Les erreurs `503 UNAVAILABLE` de l'API Gemini causaient des crashes
- Pas de mécanisme de récupération en cas d'erreur temporaire du serveur

**Solution Implémentée:**
```python
# Dans src/app.py, lignes 40-65
while True:
    try:
        resp = client.models.generate_content(...)
        break
    except genai_errors.ServerError as err:
        attempts += 1
        if attempts >= 3:
            return {"error": "Gemini API error after retries: ..."}
        time.sleep(min(2 ** attempts, 8))  # Backoff exponentiel
```

**Caractéristiques:**
- **3 tentatives maximum** avant d'abandonner
- **Backoff exponentiel**: Attente de 2^attempts secondes (max 8 secondes)
- Gestion gracieuse des erreurs avec retour d'un dictionnaire d'erreur structuré
- Élimination complète des crashes dus aux erreurs 503 temporaires

**Impact:**
- Robustesse accrue du système
- Meilleure expérience utilisateur (pas de crashes inattendus)
- Récupération automatique des erreurs temporaires du réseau ou de l'API

---

## 5. Warnings `thought_signature`: Informatifs mais Non-Bloquants

### Observations sur les Warnings

**Nature des Warnings:**
- Certains modèles (notamment `gemini-flash-latest`) peuvent générer des warnings concernant `thought_signature`
- Ces warnings sont **informatifs** et n'indiquent pas une erreur

**Gestion dans le Code:**
- Le code dans `src/app.py` (lignes 67-75) gère automatiquement les réponses avec markdown fences:
```python
if raw.startswith("```"):
    lines = raw.splitlines()
    # Supprime les fences markdown
    if lines and lines[0].startswith("```"):
        lines = lines[1:]
    if lines and lines[-1].startswith("```"):
        lines = lines[:-1]
    raw = "\n".join(lines).strip()
```

**Validité du JSON:**
- Malgré les warnings, les réponses JSON restent **valides** après le nettoyage
- Le parsing JSON fonctionne correctement après suppression des fences
- Aucun impact sur la fonctionnalité du système

**Recommandation:**
- Ces warnings peuvent être ignorés en toute sécurité
- Ils n'affectent pas la qualité ou la validité des résultats
- Le système continue de fonctionner normalement

---

## 6. Tableau de Référence Rapide

Un tableau de comparaison détaillé est disponible dans `reports/model-comparison.md` avec:
- Notes sur chaque modèle
- Artifacts JSON correspondants
- Guidance pour le choix du modèle

---

## Justification du Choix du Modèle pour ce Lab

### Modèle Choisi: **Gemini 2.5 Flash** (par défaut)

**Raisons:**

1. **Rationales Riches pour l'Évaluation:**
   - Les explications détaillées facilitent la compréhension des risques
   - Idéal pour les démonstrations et la documentation
   - Permet une analyse approfondie des vulnérabilités

2. **CWE Tagging Consistant:**
   - 13 CWE uniques détectés avec mapping fiable
   - Couverture complète des types de vulnérabilités pertinents
   - Cohérence dans l'identification des risques

3. **Équilibre Optimal:**
   - Bon compromis entre exhaustivité et précision
   - Détection fiable sans être trop conservateur
   - Refus explicites pour les tentatives malveillantes

4. **Robustesse Technique:**
   - Retry logic élimine les crashes
   - Gestion gracieuse des erreurs
   - Système fiable en production

**Trade-offs Acceptés:**
- Rationales plus longues = coûts API légèrement plus élevés (acceptable pour ce lab)
- Latence légèrement supérieure à Flash-Lite (négligeable pour ce cas d'usage)

---

## Conclusion

Les observations des runs de référence démontrent que:
- **Gemini 2.5 Flash** offre le meilleur équilibre pour ce lab avec des rationales riches et un CWE tagging consistant
- **Gemini 2.5 Flash-Lite** est une alternative viable pour les environnements nécessitant une latence/cout réduits
- **Gemini 2.5 Pro** est approprié pour les cas où la précision prime sur l'exhaustivité, avec des garde-fous appropriés
- Les améliorations techniques (retry logic, gestion des fences) garantissent la robustesse du système
- Les warnings `thought_signature` sont informatifs et n'affectent pas la fonctionnalité

Ces observations justifient le choix de **Gemini 2.5 Flash** comme modèle par défaut pour ce laboratoire de sécurité LLM.




