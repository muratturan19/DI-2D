# DI-2D Startup Script for Windows

Write-Host "🚀 Starting DI-2D - 2D Drawing Intelligence System" -ForegroundColor Cyan
Write-Host ""

# Check if .env exists in backend
if (-not (Test-Path "backend\.env")) {
    Write-Host "⚠️  .env file not found in backend\" -ForegroundColor Yellow
    Write-Host "Please create backend\.env with your API keys" -ForegroundColor Yellow
    Write-Host "Example:" -ForegroundColor Yellow
    Write-Host "OPENAI_API_KEY=your_key"
    Write-Host "ANTHROPIC_API_KEY=your_key"
    exit 1
}

# Start Backend
Write-Host "📦 Starting Backend (Port 8001)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd backend; python -m uvicorn main:app --reload --host 0.0.0.0 --port 8001"

# Wait for backend to start
Start-Sleep -Seconds 3

# Start Frontend
Write-Host "🎨 Starting Frontend (Port 3001)..." -ForegroundColor Green
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd frontend; npm run dev"

Write-Host ""
Write-Host "✅ DI-2D is running!" -ForegroundColor Green
Write-Host ""
Write-Host "📍 Frontend: http://localhost:3001" -ForegroundColor Cyan
Write-Host "📍 Backend API: http://localhost:8001" -ForegroundColor Cyan
Write-Host "📍 API Docs: http://localhost:8001/docs" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press any key to continue..." -ForegroundColor Yellow
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
