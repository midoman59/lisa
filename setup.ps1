# Setup Script pour Agent Lisa Demo
# Windows PowerShell

Write-Host "`n╔════════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  🏦 AGENT LISA DEMO - Setup Script                                 ║" -ForegroundColor Cyan
Write-Host "║  LS V3.8.0 Loan Servicing System                                   ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

# 1. Vérifier Python
Write-Host "✓ Vérification Python..." -ForegroundColor Green
$pythonVersion = python --version
Write-Host "  → $pythonVersion`n"

# 2. Créer virtual environment
Write-Host "✓ Création du virtual environment..." -ForegroundColor Green
if (Test-Path "venv") {
    Write-Host "  → Venv existant trouvé, skip"
} else {
    python -m venv venv
    Write-Host "  → Créé ✓"
}
Write-Host ""

# 3. Activer venv
Write-Host "✓ Activation du venv..." -ForegroundColor Green
& ".\venv\Scripts\Activate.ps1"
Write-Host "  → Activé ✓`n"

# 4. Installer dépendances
Write-Host "✓ Installation des dépendances..." -ForegroundColor Green
pip install -q -r requirements.txt
Write-Host "  → Complété ✓`n"

# 5. Créer .env
Write-Host "✓ Configuration .env..." -ForegroundColor Green
if (Test-Path ".env") {
    Write-Host "  → .env existant trouvé, skip"
} else {
    Copy-Item ".env.example" ".env"
    Write-Host "  → Créé à partir de .env.example"
    Write-Host "  ⚠️  IMPORTANT: Éditer .env avec vos credentials Azure!"
}
Write-Host ""

# 6. Vérifier structure
Write-Host "✓ Vérification de la structure..." -ForegroundColor Green
$requiredDirs = @("src/agent", "src/data", "src/config", "docs", "scripts")
foreach ($dir in $requiredDirs) {
    if (Test-Path $dir) {
        Write-Host "  ✓ $dir"
    } else {
        Write-Host "  ✗ $dir (MANQUANT)" -ForegroundColor Red
    }
}
Write-Host ""

# 7. Test rapide
Write-Host "✓ Test de données..." -ForegroundColor Green
try {
    python -c "import json; data = json.load(open('src/data/dossiers.json')); print('  → ' + str(len(data)) + ' dossiers chargés')"
} catch {
    Write-Host "  ✗ Erreur de chargement des données" -ForegroundColor Red
}
Write-Host ""

Write-Host "╔════════════════════════════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  ✅ SETUP TERMINÉ!                                                 ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════════════════════════════╝`n" -ForegroundColor Cyan

Write-Host "📋 Prochaines étapes:" -ForegroundColor Yellow
Write-Host "  1. Éditer .env avec vos credentials Azure"
Write-Host "  2. Lancer l'agent: python main.py"
Write-Host "  3. Ou voir démo: python scripts/test_demo_ls_v3.py`n"
