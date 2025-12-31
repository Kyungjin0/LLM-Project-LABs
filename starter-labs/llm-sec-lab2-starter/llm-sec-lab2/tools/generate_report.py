import json
import html
import os

# Configuration
INPUT_FILE = 'reports/merged_results.json'
OUTPUT_FILE = 'reports/lab2_report.html'

def generate_html():
    if not os.path.exists(INPUT_FILE):
        print(f"❌ Error: {INPUT_FILE} not found.")
        return

    with open(INPUT_FILE, 'r', encoding='utf-8') as f:
        data = json.load(f)

    results = data.get('results', {}).get('results', [])
    
    # HTML Header & Style (Style Promptfoo Classique)
    html_content = """<!doctype html>
<html>
<head>
    <meta charset="utf-8" />
    <title>Lab 2 Report</title>
    <style>
        body { font-family: -apple-system, BlinkMacSystemFont, Segoe UI, Roboto, Helvetica, Arial, sans-serif; padding: 20px; }
        h1 { color: #333; }
        table { border: 1px solid #ccc; border-collapse: collapse; width: 100%; text-align: left; table-layout: fixed;}
        th, td { border: 1px solid #ccc; padding: 10px; word-wrap: break-word; vertical-align: top; }
        th { background-color: #f4f4f4; }
        .pass { color: green; font-weight: bold; }
        .fail { color: #d32f2f; font-weight: bold; }
        .error { color: #e65100; font-weight: bold; }
        pre { white-space: pre-wrap; background: #f8f8f8; padding: 5px; border-radius: 3px; }
    </style>
</head>
<body>
    <h1>🛡️ Lab 2 Evaluation Report</h1>
    <p><strong>Total Tests:</strong> """ + str(len(results)) + """</p>
    <table>
        <thead>
        <tr>
            <th style="width: 5%">ID</th>
            <th style="width: 30%">Code Snippet</th>
            <th style="width: 10%">Expected</th>
            <th style="width: 45%">Model Response</th>
            <th style="width: 10%">Status</th>
        </tr>
        </thead>
    <tbody>
"""

    for i, res in enumerate(results):
        # Extraction des données
        vars = res.get('vars', {})
        code = vars.get('code', 'N/A')
        expected = vars.get('label', 'N/A')
        
        response = res.get('response', {})
        output = response.get('output', '')
        
        # 1. Récupération sécurisée des objets imbriqués
        # Si gradingResult est None (null dans le JSON), on force un dictionnaire vide {}
        grading_result = res.get('gradingResult')
        if grading_result is None:
            grading_result = {}

        # 2. Détermination du succès (Pass/Fail)
        # On regarde d'abord à la racine, puis dans gradingResult
        pass_status = res.get('pass')
        
        if pass_status is None:
            pass_status = grading_result.get('pass')
            
        # 3. Filet de sécurité : vérifier le score si 'pass' est introuvable
        if pass_status is None:
            score = res.get('score')
            if score is None:
                score = grading_result.get('score', 0)
            pass_status = (score == 1)
            
        # -------------------------------------------------------------

        # Définition visuelle (CSS)
        status_class = "pass" if pass_status else "fail"
        status_text = "PASS" if pass_status else "FAIL"
        
        # Détection spécifique des Erreurs API (429, Timeout, etc.)
        # On regarde dans la sortie brute pour voir s'il y a un message d'erreur
        output_str = str(output)
        if "API call error" in output_str or "Rate limited" in output_str or "429 Too Many Requests" in output_str:
            status_class = "error"
            status_text = "ERROR (429)"

        # Construction de la ligne
        html_content += f"""
        <tr>
            <td>{i+1}</td>
            <td><pre>{html.escape(code)}</pre></td>
            <td>{expected}</td>
            <td><pre>{html.escape(str(output))}</pre></td>
            <td class="{status_class}">{status_text}</td>
        </tr>
"""

    html_content += """
        </tbody>
    </table>
</body>
</html>
"""

    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✅ Report generated successfully: {OUTPUT_FILE}")

if __name__ == "__main__":
    generate_html()