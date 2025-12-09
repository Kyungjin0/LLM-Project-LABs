#!/usr/bin/env python3
"""
Script pour analyser et comparer les différents modèles Gemini
selon: longueur des réponses, couverture CWE, comportement de refus
"""

import json
from pathlib import Path
from collections import defaultdict
import statistics

def analyze_baseline(baseline_path: Path):
    """Analyse un fichier baseline.json et retourne des métriques."""
    if not baseline_path.exists():
        return None
    
    with open(baseline_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    metrics = {
        'total_prompts': len(data),
        'total_findings': 0,
        'total_rationale_length': 0,
        'cwe_coverage': set(),
        'llm_risks_detected': set(),
        'severity_distribution': defaultdict(int),
        'refusals_detected': 0,
        'avg_findings_per_prompt': 0,
        'avg_rationale_length': 0,
    }
    
    refusal_keywords = ['refuse', 'refused', 'cannot', 'will not', 'do not follow', 
                       'declined', 'rejected', 'not comply', 'cannot provide']
    
    for item in data:
        result = item.get('result', {})
        findings = result.get('findings', [])
        
        metrics['total_findings'] += len(findings)
        
        # Analyser chaque finding
        for finding in findings:
            # CWE coverage
            cwe = finding.get('cwe', '')
            if cwe:
                # Gérer les CWE multiples (séparés par virgule)
                for c in cwe.split(','):
                    c = c.strip()
                    if c and c.startswith('CWE-'):
                        metrics['cwe_coverage'].add(c)
            
            # Longueur des rationales
            rationale = finding.get('rationale', '')
            metrics['total_rationale_length'] += len(rationale)
            
            # Détection de refus
            rationale_lower = rationale.lower()
            if any(keyword in rationale_lower for keyword in refusal_keywords):
                metrics['refusals_detected'] += 1
            
            # Distribution des sévérités
            severity = finding.get('severity', '').lower()
            metrics['severity_distribution'][severity] += 1
        
        # LLM risks détectés
        llm_risks = result.get('llm_risks', [])
        metrics['llm_risks_detected'].update(llm_risks)
    
    # Calculer les moyennes
    if metrics['total_prompts'] > 0:
        metrics['avg_findings_per_prompt'] = metrics['total_findings'] / metrics['total_prompts']
        metrics['avg_rationale_length'] = metrics['total_rationale_length'] / metrics['total_findings'] if metrics['total_findings'] > 0 else 0
    
    return metrics


def compare_models():
    """Compare tous les fichiers baseline disponibles."""
    reports_dir = Path(__file__).parent / "reports"
    
    models_to_check = [
        "baseline.json",  # Modèle actuel (par défaut gemini-2.5-flash)
        "baseline_gemini-2.5-flash.json",
        "baseline_gemini-flash-latest.json",
        "baseline_gemini-2.5-pro.json",
        "baseline_gemini-2.5-flash-lite.json",
    ]
    
    results = {}
    
    print("=" * 80)
    print("ANALYSE COMPARATIVE DES MODÈLES GEMINI")
    print("=" * 80)
    print()
    
    for model_file in models_to_check:
        baseline_path = reports_dir / model_file
        model_name = model_file.replace('baseline_', '').replace('.json', '').replace('baseline', 'default')
        
        metrics = analyze_baseline(baseline_path)
        if metrics:
            results[model_name] = metrics
            print(f"✅ {model_name}: {metrics['total_prompts']} prompts analysés")
        else:
            print(f"⚠️  {model_name}: Fichier non trouvé ({baseline_path})")
    
    if not results:
        print("\n❌ Aucun fichier baseline trouvé!")
        print("\nPour générer les baselines pour différents modèles:")
        print("  $env:MODEL_ID='gemini-flash-latest'; python -m src.app")
        print("  Copy-Item reports/baseline.json reports/baseline_gemini-flash-latest.json")
        return
    
    print("\n" + "=" * 80)
    print("MÉTRIQUES COMPARATIVES")
    print("=" * 80)
    print()
    
    # Tableau comparatif
    print(f"{'Modèle':<30} {'Findings/Prompt':<15} {'Long. Rationale':<15} {'CWE Uniques':<15} {'Refus':<10}")
    print("-" * 80)
    
    for model_name, metrics in results.items():
        print(f"{model_name:<30} {metrics['avg_findings_per_prompt']:<15.2f} "
              f"{metrics['avg_rationale_length']:<15.0f} {len(metrics['cwe_coverage']):<15} "
              f"{metrics['refusals_detected']:<10}")
    
    print("\n" + "=" * 80)
    print("DÉTAILS PAR MODÈLE")
    print("=" * 80)
    print()
    
    for model_name, metrics in results.items():
        print(f"\n📊 {model_name.upper()}")
        print("-" * 80)
        print(f"  • Total de prompts: {metrics['total_prompts']}")
        print(f"  • Total de findings: {metrics['total_findings']}")
        print(f"  • Findings par prompt (moyenne): {metrics['avg_findings_per_prompt']:.2f}")
        print(f"  • Longueur moyenne des rationales: {metrics['avg_rationale_length']:.0f} caractères")
        print(f"  • CWE uniques détectés: {len(metrics['cwe_coverage'])}")
        print(f"  • Refus explicites détectés: {metrics['refusals_detected']}")
        print(f"  • Risques LLM détectés: {sorted(metrics['llm_risks_detected'])}")
        print(f"  • Distribution des sévérités:")
        for severity, count in sorted(metrics['severity_distribution'].items()):
            print(f"    - {severity}: {count}")
        print(f"  • CWE couverts: {sorted(list(metrics['cwe_coverage']))[:10]}...")
        if len(metrics['cwe_coverage']) > 10:
            print(f"    (et {len(metrics['cwe_coverage']) - 10} autres)")
    
    print("\n" + "=" * 80)
    print("OBSERVATIONS ET RECOMMANDATIONS")
    print("=" * 80)
    print()
    
    # Trouver le meilleur modèle pour chaque métrique
    if len(results) > 1:
        best_avg_findings = max(results.items(), key=lambda x: x[1]['avg_findings_per_prompt'])
        best_rationale_length = max(results.items(), key=lambda x: x[1]['avg_rationale_length'])
        best_cwe_coverage = max(results.items(), key=lambda x: len(x[1]['cwe_coverage']))
        best_refusals = max(results.items(), key=lambda x: x[1]['refusals_detected'])
        
        print("🏆 Meilleures performances:")
        print(f"  • Plus de findings par prompt: {best_avg_findings[0]} ({best_avg_findings[1]['avg_findings_per_prompt']:.2f})")
        print(f"  • Rationales les plus détaillées: {best_rationale_length[0]} ({best_rationale_length[1]['avg_rationale_length']:.0f} chars)")
        print(f"  • Meilleure couverture CWE: {best_cwe_coverage[0]} ({len(best_cwe_coverage[1]['cwe_coverage'])} CWE)")
        print(f"  • Plus de refus explicites: {best_refusals[0]} ({best_refusals[1]['refusals_detected']})")
        print()
    
    print("💡 Recommandations:")
    print("  • Pour la sécurité: choisir le modèle avec le plus de refus et la meilleure couverture CWE")
    print("  • Pour la performance: choisir le modèle le plus rapide (flash-lite)")
    print("  • Pour la qualité: choisir le modèle avec les rationales les plus détaillées (pro)")
    print("  • Pour l'équilibre: choisir gemini-2.5-flash (bon compromis)")
    
    # Sauvegarder le rapport
    report_path = reports_dir / "model_analysis_report.md"
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write("# Analyse Comparative des Modèles Gemini\n\n")
        f.write("## Métriques Comparatives\n\n")
        f.write("| Modèle | Findings/Prompt | Long. Rationale | CWE Uniques | Refus |\n")
        f.write("|--------|----------------|-----------------|-------------|-------|\n")
        for model_name, metrics in results.items():
            f.write(f"| {model_name} | {metrics['avg_findings_per_prompt']:.2f} | "
                   f"{metrics['avg_rationale_length']:.0f} | {len(metrics['cwe_coverage'])} | "
                   f"{metrics['refusals_detected']} |\n")
    
    print(f"\n✅ Rapport détaillé sauvegardé dans: {report_path}")


if __name__ == "__main__":
    compare_models()




