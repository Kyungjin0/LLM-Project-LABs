import os
import glob
import yaml
import re

# Configuration
OUTPUT_FILE = "_generated/tests_flat.yaml"
SEARCH_PATTERN = "snippets/**/*" 

def analyze_snippet(content):
    """
    Détermine si le snippet est vulnérable en cherchant des indices dans le code.
    Regarde les commentaires // CWE-XXX ou # CWE-XXX
    """
    label = "no"
    cwe = "CWE-Unknown"
    
    # Détection basée sur les commentaires laissés dans les fichiers snippets fournis
    cwe_match = re.search(r'CWE-(\d+)', content, re.IGNORECASE)
    
    if cwe_match:
        label = "yes"
        cwe = f"CWE-{cwe_match.group(1)}"
    elif "vulnerability" in content.lower() or "risks" in content.lower() or "weak hash" in content.lower():
        # Fallback pour certains cas comme YAML load risks
        label = "yes"
        cwe = "CWE-Misc"
        
    return label, cwe

def generate():
    tests = []
    valid_extensions = ('.java', '.js', '.py')
    
    # Récupération de tous les fichiers
    files = [f for f in glob.glob(SEARCH_PATTERN, recursive=True) if f.endswith(valid_extensions)]
    files = sorted(files)
    
    if not files:
        print(f"❌ Erreur : Aucun fichier trouvé dans 'snippets/'.")
        print("   Assure-toi d'avoir dézippé tes dossiers 'java', 'javascript', 'python' DANS le dossier 'snippets'.")
        return

    print(f"📦 Analyse de {len(files)} snippets...")

    for filepath in files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                
            label, cwe = analyze_snippet(content)
            filename = os.path.basename(filepath)
            
            # Construction de l'objet de test pour promptfoo
            test_case = {
                "vars": {
                    "code": content,
                    "label": label,
                    "cwe_hint": cwe if label == "yes" else None,
                    "snippet": filename
                }
            }
            tests.append(test_case)
            print(f"   - {filename}: {label} ({cwe})")
            
        except Exception as e:
            print(f"   ⚠️ Erreur lecture {filepath}: {e}")

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    
    # Écriture du YAML
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        yaml.dump(tests, f, sort_keys=False, default_flow_style=False)
    
    print(f"\n✅ Succès ! Fichier généré : {OUTPUT_FILE}")
    print(f"   Nombre total de tests : {len(tests)}")

if __name__ == "__main__":
    generate()