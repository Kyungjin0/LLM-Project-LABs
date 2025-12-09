# Script PowerShell pour générer tous les baselines des modèles Gemini
# Usage: .\generate_all_baselines.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Génération des Baselines pour Tous les Modèles" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

$models = @(
    "gemini-flash-latest",
    "gemini-2.5-pro",
    "gemini-2.5-flash-lite",
    "gemini-2.5-flash"
)

$successCount = 0
$failCount = 0

foreach ($model in $models) {
    Write-Host "🔄 Génération du baseline pour: $model" -ForegroundColor Yellow
    
    try {
        # Définir le modèle
        $env:MODEL_ID = $model
        
        # Exécuter l'app
        python -m src.app
        
        if ($LASTEXITCODE -eq 0) {
            # Sauvegarder le baseline
            $outputFile = "reports\baseline_$model.json"
            Copy-Item reports\baseline.json $outputFile -ErrorAction Stop
            Write-Host "  ✅ Baseline sauvegardé: $outputFile" -ForegroundColor Green
            $successCount++
        } else {
            Write-Host "  ❌ Erreur lors de l'exécution de python -m src.app" -ForegroundColor Red
            $failCount++
        }
    } catch {
        Write-Host "  ❌ Erreur: $_" -ForegroundColor Red
        $failCount++
    }
    
    Write-Host ""
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Résumé" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "✅ Succès: $successCount" -ForegroundColor Green
Write-Host "❌ Échecs: $failCount" -ForegroundColor $(if ($failCount -gt 0) { "Red" } else { "Green" })

if ($successCount -gt 0) {
    Write-Host "`n📊 Analyse des modèles..." -ForegroundColor Cyan
    python analyze_models.py
    
    Write-Host "`n✅ Terminé!" -ForegroundColor Green
    Write-Host "Consulte reports/model_analysis_report.md pour les résultats détaillés." -ForegroundColor Cyan
}




