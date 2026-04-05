# OpenClaw Auto-Start - Single Script Solution
# Run as Administrator on Windows

Write-Host "=========================================="
Write-Host "  OpenClaw Auto-Start Script"
Write-Host "=========================================="
Write-Host ""

# Step 1: Check Admin
$isAdmin = ([Security.Principal.WindowsPrincipal][Security.Principal.WindowsIdentity]::GetCurrent()).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "[ERROR] This script must be run as Administrator"
    Write-Host "Right-click - Run as Administrator"
    Read-Host "Press Enter to exit..."
    exit 1
}

Write-Host "[OK] Running with Administrator privileges"
Write-Host ""

# Step 2: Start WSL2
Write-Host "[1/4] Starting WSL2/Ubuntu..."
wsl -d Ubuntu -u root /bin/echo "WSL2 started at $(date +%T)" 2>$null
Start-Sleep -Seconds 3

Write-Host "[OK] WSL2 started"
Write-Host ""

# Step 3: Wait for WSL2 to initialize
Write-Host "[2/4] Waiting for WSL2 to initialize (10 seconds)..."
for ($i = 10; $i -gt 0; $i--) {
    Write-Host "  $i seconds remaining..."
    Start-Sleep -Seconds 1
}

Write-Host "[OK] WSL2 should be initialized"
Write-Host ""

# Step 4: Get WSL2 IP
Write-Host "[3/4] Getting WSL2 IP address..."
$wslIP = wsl hostname -I

if (-not $wslIP) {
    Write-Host "[ERROR] Could not get WSL2 IP"
    Write-Host "WSL2 may not be running properly"
    Read-Host "Press Enter to exit..."
    exit 1
}

Write-Host "[OK] WSL2 IP: $wslIP"
Write-Host ""

# Step 5: Reset existing port proxy
Write-Host "[4/4] Configuring port proxy..."
netsh interface portproxy reset 2>$null

# Step 6: Create new port proxy
$cmd = "netsh interface portproxy add v4tov4 listenport=8888 listenaddress=0.0.0.0 connectport=8888 connectaddress=$wslIP"
$null = Invoke-Expression $cmd 2>&1

if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Failed to create port proxy"
    Write-Host "Error code: $LASTEXITCODE"
    Read-Host "Press Enter to exit..."
    exit 1
}

Write-Host "[OK] Port proxy created"
Write-Host ""

# Step 7: Verify port proxy
Write-Host "[INFO] Verifying port proxy configuration..."
$proxyStatus = netsh interface portproxy show v4tov4 | Select-String "8888"

if ($proxyStatus) {
    Write-Host "[OK] Port proxy is active:"
    Write-Host ""
    Write-Host $proxyStatus
} else {
    Write-Host "[WARNING] Port proxy verification failed"
}

Write-Host ""
Write-Host "=========================================="
Write-Host "  Configuration Complete!"
Write-Host "=========================================="
Write-Host ""
Write-Host "WSL2 is running (OpenClaw is active)"
Write-Host "Port Proxy: Windows 8888 -> WSL2 $wslIP:8888"
Write-Host ""
Write-Host "Access URL:"
Write-Host "  http://S01068c763f5b0fc1.vw.shawcable.net:8888/research-summary.html"
Write-Host ""
Write-Host "Press Enter to close this window (or close X)..."
Read-Host
