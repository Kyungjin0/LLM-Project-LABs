# Résumé des Observations - Section 12 (Version Courte)

## Observations from Reference Runs

### Gemini 2.5 Flash (Default)
- **Rationales les plus riches**: Longueur moyenne de 476 caractères avec explications complètes et contextuelles
- **CWE tagging consistant**: 13 CWE uniques détectés avec mapping fiable (CWE-943, CWE-200, CWE-693, etc.)
- **Couverture complète**: Tous les risques OWASP LLM Top 10 pertinents détectés (LLM01-LLM10)
- **Refus explicites**: 7 refus détectés sur 11 prompts (63.6%) pour les tentatives malveillantes
- **Justification**: Idéal pour les démonstrations et l'évaluation grâce aux explications détaillées

### Gemini 2.5 Flash-Lite
- **Findings similaires à Flash**: Même qualité de détection avec décisions cohérentes
- **Explanations plus courtes**: Rationales significativement réduites pour réduire latence et coûts
- **Avantages**: Latence réduite, coûts API inférieurs, fidélité du schéma préservée
- **Justification**: Parfait pour les budgets serrés et les environnements de production nécessitant une faible latence

### Gemini 2.5 Pro
- **Approche conservatrice**: Certains prompts à faible risque peuvent retourner des findings vides
- **Détection fiable des risques critiques**: Les prompts sensibles (exfiltration de mots de passe) déclenchent toujours des alertes de sévérité élevée
- **Mapping fiable**: LLM01/LLM06 correctement identifiés pour les attaques évidentes
- **Considération**: Nécessite des garde-fous supplémentaires ou une revue humaine pour compenser le sous-rapportage potentiel
- **Justification**: Idéal quand la précision prime sur l'exhaustivité, avec revue humaine appropriée

### Améliorations Techniques
- **Retry logic**: Élimine les crashes `503 UNAVAILABLE` avec 3 tentatives et backoff exponentiel
- **Gestion des fences markdown**: Nettoyage automatique des réponses avec ``` pour garantir un JSON valide
- **Warnings `thought_signature`**: Informatifs mais non-bloquants, JSON reste valide après nettoyage

### Choix Final: Gemini 2.5 Flash
**Justification**: Meilleur équilibre entre exhaustivité et précision, rationales riches pour l'évaluation, CWE tagging consistant, et robustesse technique avec retry logic.

**Référence**: Voir `reports/model-comparison.md` pour un tableau de comparaison détaillé.

