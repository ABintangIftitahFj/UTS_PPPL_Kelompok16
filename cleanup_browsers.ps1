# PowerShell script untuk cleanup browser processes
# Usage: .\cleanup_browsers.ps1

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "    Cleanup Browser Processes from Testing" -ForegroundColor Cyan  
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Stopping Chrome processes..." -ForegroundColor Yellow
Stop-Process -Name "chrome" -Force -ErrorAction SilentlyContinue
Stop-Process -Name "chromedriver" -Force -ErrorAction SilentlyContinue
Write-Host "✓ Chrome processes stopped" -ForegroundColor Green

Write-Host "Stopping Firefox processes..." -ForegroundColor Yellow
Stop-Process -Name "firefox" -Force -ErrorAction SilentlyContinue
Stop-Process -Name "geckodriver" -Force -ErrorAction SilentlyContinue
Write-Host "✓ Firefox processes stopped" -ForegroundColor Green

Write-Host "Stopping Edge processes..." -ForegroundColor Yellow
Stop-Process -Name "msedge" -Force -ErrorAction SilentlyContinue
Stop-Process -Name "msedgedriver" -Force -ErrorAction SilentlyContinue
Write-Host "✓ Edge processes stopped" -ForegroundColor Green

# Alternative method using taskkill
Write-Host ""
Write-Host "Running additional cleanup..." -ForegroundColor Yellow
Start-Process -FilePath "taskkill" -ArgumentList "/F", "/IM", "chrome.exe", "/T" -WindowStyle Hidden -Wait -ErrorAction SilentlyContinue
Start-Process -FilePath "taskkill" -ArgumentList "/F", "/IM", "chromedriver.exe", "/T" -WindowStyle Hidden -Wait -ErrorAction SilentlyContinue
Start-Process -FilePath "taskkill" -ArgumentList "/F", "/IM", "firefox.exe", "/T" -WindowStyle Hidden -Wait -ErrorAction SilentlyContinue  
Start-Process -FilePath "taskkill" -ArgumentList "/F", "/IM", "geckodriver.exe", "/T" -WindowStyle Hidden -Wait -ErrorAction SilentlyContinue
Start-Process -FilePath "taskkill" -ArgumentList "/F", "/IM", "msedge.exe", "/T" -WindowStyle Hidden -Wait -ErrorAction SilentlyContinue
Write-Host "Additional cleanup completed" -ForegroundColor Gray

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "Browser cleanup completed successfully!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

Read-Host "Press Enter to exit"