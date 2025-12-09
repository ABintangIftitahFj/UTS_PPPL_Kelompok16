@echo off
REM Script untuk membersihkan semua proses browser yang tertinggal dari testing

echo.
echo ================================================
echo    Cleanup Browser Processes from Testing
echo ================================================
echo.

echo Stopping Chrome processes...
taskkill /F /IM chrome.exe /T 2>nul
taskkill /F /IM chromedriver.exe /T 2>nul

echo Stopping Firefox processes...
taskkill /F /IM firefox.exe /T 2>nul
taskkill /F /IM geckodriver.exe /T 2>nul

echo Stopping Edge processes...
taskkill /F /IM msedge.exe /T 2>nul
taskkill /F /IM msedgedriver.exe /T 2>nul

echo.
echo Browser cleanup completed!
echo.
pause