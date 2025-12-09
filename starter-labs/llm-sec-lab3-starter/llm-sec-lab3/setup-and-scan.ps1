# Script PowerShell pour configurer et exécuter les scans de sécurité Lab 3

Write-Host "=== Configuration de l'environnement Lab 3 ===" -ForegroundColor Cyan

# Activer l'environnement virtuel
if (Test-Path .venv) {
    Write-Host "Activation de l'environnement virtuel..." -ForegroundColor Yellow
    & .\.venv\Scripts\Activate.ps1
} else {
    Write-Host "Création de l'environnement virtuel..." -ForegroundColor Yellow
    python -m venv .venv
    & .\.venv\Scripts\Activate.ps1
}

# Installer les dépendances
Write-Host "Installation des dépendances..." -ForegroundColor Yellow
pip install -r requirements.txt

Write-Host "`n=== Exécution des scans de base ===" -ForegroundColor Cyan

# Exécuter Checkov
Write-Host "`n[1/2] Exécution de Checkov..." -ForegroundColor Green
python scripts/run_checkov.py

# Exécuter Semgrep
Write-Host "`n[2/2] Exécution de Semgrep..." -ForegroundColor Green
python scripts/run_semgrep.py

Write-Host "`n=== Scans terminés ===" -ForegroundColor Cyan
Write-Host "Vérifiez les fichiers dans le dossier reports/" -ForegroundColor Yellow
Write-Host "- reports/checkov.json" -ForegroundColor Gray
Write-Host "- reports/semgrep.json" -ForegroundColor Gray

