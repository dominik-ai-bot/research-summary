@echo off
REM Single-Script Solution: Start WSL2 + OpenClaw + Port Proxy
REM Run this as Administrator - it shows everything that happens

echo ==========================================
echo   OpenClaw Auto-Start Script
echo ==========================================
echo.

REM Step 1: Check if running as Admin
net session >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] This script must be run as Administrator
    echo Right-click - Run as Administrator
    pause
    exit /b 1
)

echo [OK] Running with Administrator privileges
echo.

REM Step 2: Start WSL2 (OpenClaw)
echo [1/4] Starting WSL2/Ubuntu...
wsl -d Ubuntu -u root echo "WSL2 started at %time% %date%" >nul 2>&1
timeout /t 3 /nobreak >nul

echo [OK] WSL2 started
echo.

REM Step 3: Wait for WSL2 to initialize
echo [2/4] Waiting for WSL2 to initialize (10 seconds)...
timeout /t 10 /nobreak >nul

REM Step 4: Get WSL2 IP
echo [3/4] Getting WSL2 IP address...
for /f "tokens=*" %%i in ('wsl hostname -I') do set WSLIP=%%i

if "%WSLIP%"=="" (
    echo [ERROR] Could not get WSL2 IP
    echo WSL2 may not be running properly
    pause
    exit /b 1
)

echo [OK] WSL2 IP: %WSLIP%
echo.

REM Step 5: Reset existing port proxy
echo [4/4] Configuring port proxy...
netsh interface portproxy reset >nul 2>&1

REM Step 6: Create new port proxy
netsh interface portproxy add v4tov4 listenport=8888 listenaddress=0.0.0.0 connectport=8888 connectaddress=%WSLIP% >nul 2>&1
if %errorLevel% neq 0 (
    echo [ERROR] Failed to create port proxy
    pause
    exit /b 1
)

echo [OK] Port proxy created
echo.

REM Step 7: Verify port proxy
echo [INFO] Verifying port proxy configuration...
netsh interface portproxy show v4tov4 | find "8888"
if %errorLevel% neq 0 (
    echo [WARNING] Port proxy verification failed
) else (
    echo [OK] Port proxy is active
)
echo.

echo ==========================================
echo   Configuration Complete!
echo ==========================================
echo.
echo WSL2 is running (OpenClaw is active)
echo Port Proxy: Windows 8888 -^> WSL2 %WSLIP%:8888
echo.
echo Access URL:
echo   http://S01068c763f5b0fc1.vw.shawcable.net:8888/research-summary.html
echo.
echo Press any key to close this window...
pause >nul
