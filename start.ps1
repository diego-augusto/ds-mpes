# Script para iniciar o projeto Streamlit rapidamente

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "  🚀 Iniciando Projeto Streamlit" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Verificar se venv existe
if (-Not (Test-Path ".\venv")) {
    Write-Host "❌ Virtual environment não encontrado!" -ForegroundColor Red
    Write-Host "Execute este comando primeiro:" -ForegroundColor Yellow
    Write-Host "python -m venv venv" -ForegroundColor Green
    exit
}

# Ativar venv
Write-Host "📦 Ativando virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\Activate.ps1

# Verificar se requirements.txt foi instalado
Write-Host "✅ Virtual environment ativado" -ForegroundColor Green
Write-Host ""

# Iniciar Streamlit
Write-Host "🎨 Iniciando aplicação Streamlit..." -ForegroundColor Yellow
Write-Host "📱 Acessar em: http://localhost:8501" -ForegroundColor Cyan
Write-Host ""

streamlit run app.py
