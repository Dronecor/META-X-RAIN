Write-Host "Starting Agentic CRM Locally..." -ForegroundColor Cyan

# 1. Check/Install Dependencies
Write-Host "Checking dependencies..."
pip install -r backend/requirements.txt

# 2. Set Environment Variables
$env:PYTHONPATH = "$PWD"
Write-Host "PYTHONPATH set to $PWD"

# 3. Start Backend
Write-Host "Launching Backend API (Port 8000)..." -ForegroundColor Green
Start-Process -FilePath "python" -ArgumentList "-m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload" -WindowStyle Normal

# 4. Start Admin Dashboard
Write-Host "Launching Admin Dashboard (Port 8501)..." -ForegroundColor Green
Start-Sleep -Seconds 2
Start-Process -FilePath "python" -ArgumentList "-m streamlit run frontend_admin/app.py --server.port 8501" -WindowStyle Normal

# 5. Start Customer App
Write-Host "Launching Customer App (Port 8502)..." -ForegroundColor Green
Start-Sleep -Seconds 2
Start-Process -FilePath "python" -ArgumentList "-m streamlit run frontend_customer/app.py --server.port 8502" -WindowStyle Normal

Write-Host "System started! Check the new windows." -ForegroundColor Cyan
