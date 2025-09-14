@echo off
REM Production Startup Script for Management System (Windows)
REM This script handles production deployment with proper error handling and logging

setlocal enabledelayedexpansion

REM Configuration
set APP_NAME=Management System
set LOG_FILE=logs\startup.log
set PID_FILE=app.pid

REM Create logs directory if it doesn't exist
if not exist "logs" mkdir logs
if not exist "uploads" mkdir uploads

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    exit /b 1
)

REM Check if requirements are installed
python -c "import flask" >nul 2>&1
if errorlevel 1 (
    echo ERROR: Flask not found. Please run: pip install -r requirements.txt
    exit /b 1
)

REM Check environment variables
if "%SECRET_KEY%"=="" (
    echo ERROR: SECRET_KEY environment variable is not set
    exit /b 1
)

if "%ADMIN_USERNAME%"=="" (
    echo ERROR: ADMIN_USERNAME environment variable is not set
    exit /b 1
)

if "%ADMIN_PASSWORD_HASH%"=="" (
    echo ERROR: ADMIN_PASSWORD_HASH environment variable is not set
    exit /b 1
)

if "%FIREBASE_PROJECT_ID%"=="" (
    echo ERROR: FIREBASE_PROJECT_ID environment variable is not set
    exit /b 1
)

REM Parse command line arguments
if "%1"=="start" goto start
if "%1"=="stop" goto stop
if "%1"=="restart" goto restart
if "%1"=="status" goto status
if "%1"=="health" goto health
if "%1"=="" goto start

echo Usage: %0 {start^|stop^|restart^|status^|health}
echo.
echo Commands:
echo   start   - Start the application (default)
echo   stop    - Stop the application
echo   restart - Restart the application
echo   status  - Show application status
echo   health  - Perform health check
exit /b 1

:start
echo [%date% %time%] Starting %APP_NAME%...
echo [%date% %time%] Starting %APP_NAME%... >> %LOG_FILE%

REM Check if already running
if exist "%PID_FILE%" (
    for /f %%i in (%PID_FILE%) do (
        tasklist /FI "PID eq %%i" 2>NUL | find /I "%%i" >NUL
        if not errorlevel 1 (
            echo WARNING: Application is already running with PID %%i
            set /p choice="Do you want to stop it and restart? (y/N): "
            if /i "!choice!"=="y" (
                echo Stopping existing application...
                taskkill /PID %%i /F >NUL 2>&1
                timeout /t 2 >NUL
                del "%PID_FILE%" >NUL 2>&1
            ) else (
                echo Exiting without changes
                exit /b 0
            )
        ) else (
            echo Removing stale PID file
            del "%PID_FILE%" >NUL 2>&1
        )
    )
)

REM Start the application
echo Starting application...
start /b python app.py > logs\app.log 2>&1

REM Get the PID
for /f "tokens=2" %%i in ('tasklist /FI "IMAGENAME eq python.exe" /FO CSV ^| find "python.exe"') do (
    echo %%i > %PID_FILE%
    goto :health_check
)

echo ERROR: Failed to start application
exit /b 1

:health_check
echo Performing health check...
timeout /t 5 >NUL

REM Simple health check
for /L %%i in (1,1,10) do (
    curl -f -s http://localhost:5000/health >NUL 2>&1
    if not errorlevel 1 (
        echo Health check passed
        echo %APP_NAME% started successfully!
        goto :show_status
    )
    echo Health check attempt %%i/10 failed, retrying in 2 seconds...
    timeout /t 2 >NUL
)

echo ERROR: Health check failed after 10 attempts
exit /b 1

:show_status
echo.
echo Application Status:
echo ==================
if exist "%PID_FILE%" (
    for /f %%i in (%PID_FILE%) do (
        tasklist /FI "PID eq %%i" 2>NUL | find /I "%%i" >NUL
        if not errorlevel 1 (
            echo Status: Running (PID: %%i)
            echo Logs: type logs\app.log
            echo Stop: taskkill /PID %%i /F
        ) else (
            echo Status: Not running (stale PID file)
        )
    )
) else (
    echo Status: Not running
)
exit /b 0

:stop
echo Stopping %APP_NAME%...
if exist "%PID_FILE%" (
    for /f %%i in (%PID_FILE%) do (
        taskkill /PID %%i /F >NUL 2>&1
        del "%PID_FILE%" >NUL 2>&1
        echo Application stopped
    )
) else (
    echo WARNING: No PID file found
)
exit /b 0

:restart
echo Restarting %APP_NAME%...
call :stop
timeout /t 2 >NUL
call :start
exit /b 0

:status
call :show_status
exit /b 0

:health
echo Performing health check...
curl -f -s http://localhost:5000/health >NUL 2>&1
if not errorlevel 1 (
    echo Health check passed
    exit /b 0
) else (
    echo Health check failed
    exit /b 1
)
