# Lab 2 Analysis Brief

**Authors:** MAZERAT Hugo, SINGHAVARA Enzo, ZHANG Anthony

**Model Evaluated:** Google Gemini 2.5 Flash (& Lite)

**Date:** 22/12/2025

## 1. Evaluation Summary

Nous avons mené une évaluation sur un dataset de **30 snippets** de code (code vulnérable et sécurisé) couvrant Java, Python et JavaScript.

* **Total Tests:** 30
* **Tests exécutés avec succès:** 29 (Un seul test du Batch 10 *"Path Traversal Safe"* est resté en erreur technique API *429* malgré les tentatives).
* **Precision:** **1.00** (Sur les 29 tests validés)
* **Recall:** **1.00** (Sur les 29 tests validés)
* **F1 Score:** **1.00**

Le modèle a démontré une capacité de raisonnement exceptionnelle, réussissant à distinguer les faux positifs subtils là où des SAST auraient échoué. Cependant, l'infrastructure d'évaluation a nécessité un durcissement important pour garantir la fiabilité du format de sortie.

## 2. False Positives

Initialement, le modèle a montré une tendance "paranoïaque" sur certains patterns sécurisés, notamment dans le **Batch 12**.

* **Snippet:** `04_os_cmd_safe.py`
* **Code:** Utilisation de `subprocess.run(['ls', '--', path])`.
* **Analyse :** Le code est sécurisé car il utilise une liste d'arguments (évitant l'injection shell) et le délimiteur `--`.
* **Comportement du Modèle :**
    * Le modèle *Gemini Flash Lite* (utilisé lors des fallbacks API) a tendance à marquer ce code comme vulnérable (CWE-78), confondant "présence d'input utilisateur" et "injection".
    * Le modèle *Gemini Flash Standard* (utilisé par la suite) a correctement analysé la structure de la commande et l'a classé comme **Safe**.
* **Conclusion :** La précision dépend fortement de la complexité du modèle utilisé. Les modèles "Lite" manquent de nuance pour l'analyse de flux de données sécurisés, ce qui génère plus de faux positifs.

## 3. False Negatives

Sur l'ensemble des 29 tests validés, **aucun faux négatif** n'a été détecté.
Le modèle a identifié toutes les catégories CWE testées :
* **Injection SQL** (Java/Python) : Distinction correcte entre concaténation et requêtes paramétrées.
* **XSS** (JavaScript/Python) : Identification des sorties non échappées.
* **Désérialisation non sécurisée** (Python `pickle`, Java `ObjectInputStream`).
* **Path Traversal** (Node.js).

## 4. Prompt & Pipeline Improvements

L'amélioration majeure ne s'est pas limitée au texte du prompt, mais à l'architecture globale de la requête et du post-traitement (Pipeline Engineering).

### Preuve d'Amélioration (Prompt Improvement Evidence)

#### BEFORE (Configuration Naïve - Batches 11, 12, 13, 14, 15)
* **Prompt:** "You are a security auditor. Output JSON."
* **Model:** `gemini-2.5-flash-lite` (Fallback automatique).
* **Problème :** Le modèle ignorait la contrainte de format et incluait du Markdown, rendant le parsing impossible.
* **Sortie Brute :**
    ```markdown
    ```json
    { "is_vuln": "yes", ... }
    ```
* **Résultat :** 5 échecs techniques ("JSON Parse Error"), F1 Score non calculable.

#### AFTER (Configuration Durcie & Post-Processing)
* **Prompt :** Inchangé, mais contraintes techniques renforcées dans les fichiers de configuration par batch (`_temp_config_batch_XX.yaml`).
* **Model :** Forçage de `google:gemini-2.5-flash` (Standard) via suppression du suffixe `-lite` et utilisation de `--no-cache`.
* **Post-Processing :** Injection d'une ligne `transform` JavaScript pour nettoyer la sortie avant validation :
    ```javascript
    transform: "output.replace(/```json/g, '').replace(/```/g, '').trim()"
    ```
* **Résultat :**
    * **JSON Parse Errors :** Réduits de 5 à 0.
    * **Précision :** Améliorée de 0.83 (estimé) à **1.00**.
    * **Fiabilité :** 100% de réponses valides syntaxiquement pour ces batchs.

## 5. Limitations

Même avec de bons prompts, le LLM présente des limitations structurelles pour l'automatisation :

1.  **Rate Limiting (API Free Tier) :**
    L'évaluation de 30 fichiers a déclenché de nombreuses erreurs **429 (Too Many Requests)**, nécessitant des délais importants (>20s) entre les requêtes. Cela rend l'utilisation de l'API gratuite impossible pour des pipelines CI/CD rapides.

2.  **Risque de "Silent Fallback" :**
    Le script d'évaluation initial basculait silencieusement sur un modèle "Lite" moins performant en cas de latence. Cela introduit un risque de sécurité majeur (faux négatifs ou faux positifs accrus) si le modèle utilisé n'est pas strictement verrouillé.

3.  **Non-Déterminisme :**
    Malgré une température basse, le modèle oscille parfois entre l'ajout ou non de Markdown, obligeant à utiliser des stratégies de nettoyage défensives (`transform`) pour couvrir tous les cas.

4.  **Gestion des Caractères Spéciaux (Regex - Batch 10) :**
    Le modèle peine à générer du JSON valide lorsqu'il cite des expressions régulières (exemple: `^[\w]+`). Le caractère backslash `\` est souvent mal échappé. Malgré nos correctifs logiciels (`split/join`), la complexité de validation de ce cas spécifique a conduit à une saturation de l'API (Erreur 429) sur le test sécurisé.