# PowerShell script untuk menjalankan MathsTeam Regression Tests
# Usage: .\run_tests.ps1 [test_type]

param(
    [string]$TestType = "all",  
    [switch]$Headless,
    [string]$Browser = "chrome"
)

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
Write-Host "    MathsTeam Regression Testing Suite" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Set Python executable path
$PythonExe = "C:/Program-Language/python/python.exe"

# Check if Python exists
if (-not (Test-Path $PythonExe)) {
    Write-Host "ERROR: Python not found at $PythonExe" -ForegroundColor Red
    Write-Host "Please update PythonExe path in this script" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Create reports directory if not exists
if (-not (Test-Path "reports")) {
    New-Item -ItemType Directory -Path "reports" | Out-Null
}
if (-not (Test-Path "reports/screenshots")) {
    New-Item -ItemType Directory -Path "reports/screenshots" | Out-Null
}

Write-Host "Running tests: $TestType" -ForegroundColor Yellow
if ($Headless) {
    Write-Host "Mode: Headless" -ForegroundColor Yellow
}
Write-Host "Browser: $Browser" -ForegroundColor Yellow
Write-Host ""

# Build pytest command
$PytestCmd = @(
    "-m", "pytest",
    "-v"
)

# Add browser option if not default
if ($Browser -ne "chrome") {
    $PytestCmd += "--browser=$Browser"
}

# Add headless option
if ($Headless) {
    $PytestCmd += "--headless"
}

# Add test type and report options
switch ($TestType.ToLower()) {
    "all" {
        Write-Host "Running all tests..." -ForegroundColor Green
        $PytestCmd += @(
            "--html=reports/report_all.html",
            "--self-contained-html"
        )
    }
    "smoke" {
        Write-Host "Running smoke tests..." -ForegroundColor Green
        $PytestCmd += @(
            "-m", "smoke",
            "--html=reports/report_smoke.html",
            "--self-contained-html"
        )
    }
    "login" {
        Write-Host "Running login tests..." -ForegroundColor Green
        $PytestCmd += @(
            "-m", "login",
            "--html=reports/report_login.html",
            "--self-contained-html"
        )
    }
    "dashboard" {
        Write-Host "Running dashboard tests..." -ForegroundColor Green
        $PytestCmd += @(
            "-m", "dashboard",
            "--html=reports/report_dashboard.html",
            "--self-contained-html"
        )
    }
    "regression" {
        Write-Host "Running regression tests..." -ForegroundColor Green
        $PytestCmd += @(
            "-m", "regression",
            "--html=reports/report_regression.html",
            "--self-contained-html"
        )
    }
    "critical" {
        Write-Host "Running critical tests..." -ForegroundColor Green
        $PytestCmd += @(
            "-m", "critical",
            "--html=reports/report_critical.html",
            "--self-contained-html"
        )
    }
    default {
        Write-Host "Running custom test: $TestType" -ForegroundColor Green
        $PytestCmd += @(
            $TestType,
            "--html=reports/report_custom.html",
            "--self-contained-html"
        )
    }
}

# Execute pytest
Write-Host "Executing command: $PythonExe $($PytestCmd -join ' ')" -ForegroundColor Cyan
& $PythonExe $PytestCmd

$ExitCode = $LASTEXITCODE

Write-Host ""
Write-Host "================================================" -ForegroundColor Cyan
if ($ExitCode -eq 0) {
    Write-Host "Test execution completed successfully!" -ForegroundColor Green
} else {
    Write-Host "Test execution completed with errors (Exit Code: $ExitCode)" -ForegroundColor Red
}
Write-Host "Check the reports folder for detailed results." -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Ask if user wants to open report
$OpenReport = Read-Host "Do you want to open the test report? (y/n)"
if ($OpenReport -eq "y" -or $OpenReport -eq "Y") {
    $ReportFile = "reports/report_$TestType.html"
    if ($TestType -eq "all") {
        $ReportFile = "reports/report_all.html"
    }
    
    if (Test-Path $ReportFile) {
        Start-Process $ReportFile
    } elseif (Test-Path "reports/report_all.html") {
        Start-Process "reports/report_all.html"
    } else {
        Write-Host "No report file found." -ForegroundColor Red
    }
}

Read-Host "Press Enter to exit"