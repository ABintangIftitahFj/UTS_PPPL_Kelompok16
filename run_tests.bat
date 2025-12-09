@echo off
REM Script untuk menjalankan MathsTeam Regression Tests
REM Usage: run_tests.bat [test_type]

echo.
echo ================================================
echo    MathsTeam Regression Testing Suite
echo ================================================
echo.

REM Set Python executable path
set PYTHON_EXE=C:/Program-Language/python/python.exe

REM Check if Python exists
if not exist "%PYTHON_EXE%" (
    echo ERROR: Python not found at %PYTHON_EXE%
    echo Please update PYTHON_EXE path in this script
    pause
    exit /b 1
)

REM Create reports directory if not exists
if not exist "reports" mkdir reports
if not exist "reports\screenshots" mkdir reports\screenshots

REM Set test type based on parameter
set TEST_TYPE=%1
if "%TEST_TYPE%"=="" set TEST_TYPE=all

echo Running tests: %TEST_TYPE%
echo.

REM Run tests based on type
if /i "%TEST_TYPE%"=="all" (
    echo Running all tests...
    "%PYTHON_EXE%" -m pytest -v --html=reports\report_all.html --self-contained-html
) else if /i "%TEST_TYPE%"=="smoke" (
    echo Running smoke tests...
    "%PYTHON_EXE%" -m pytest -v -m smoke --html=reports\report_smoke.html --self-contained-html
) else if /i "%TEST_TYPE%"=="login" (
    echo Running login tests...
    "%PYTHON_EXE%" -m pytest -v -m login --html=reports\report_login.html --self-contained-html
) else if /i "%TEST_TYPE%"=="dashboard" (
    echo Running dashboard tests...
    "%PYTHON_EXE%" -m pytest -v -m dashboard --html=reports\report_dashboard.html --self-contained-html
) else if /i "%TEST_TYPE%"=="regression" (
    echo Running regression tests...
    "%PYTHON_EXE%" -m pytest -v -m regression --html=reports\report_regression.html --self-contained-html
) else if /i "%TEST_TYPE%"=="critical" (
    echo Running critical tests...
    "%PYTHON_EXE%" -m pytest -v -m critical --html=reports\report_critical.html --self-contained-html
) else (
    echo Running custom test: %TEST_TYPE%
    "%PYTHON_EXE%" -m pytest -v %TEST_TYPE% --html=reports\report_custom.html --self-contained-html
)

echo.
echo ================================================
echo Test execution completed!
echo Check the reports folder for detailed results.
echo ================================================
echo.

REM Ask if user wants to open report
set /p OPEN_REPORT=Do you want to open the test report? (y/n): 
if /i "%OPEN_REPORT%"=="y" (
    if exist "reports\report_%TEST_TYPE%.html" (
        start reports\report_%TEST_TYPE%.html
    ) else if exist "reports\report_all.html" (
        start reports\report_all.html
    ) else (
        echo No report file found.
    )
)

pause