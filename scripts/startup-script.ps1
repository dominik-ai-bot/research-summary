# Auto-Start Windows-WSL2 Port Proxy
# Add this to Windows Task Scheduler or put in shell:startup

# Kill existing port proxies (in case WSL2 IP changed)
netsh interface portproxy reset

# Get current WSL2 IP
$wslIP = wsl hostname -I

if (-not $wslIP) {
    Write-Host "❌ WSL2 not running. Please start WSL2 first."
    exit 1
}

Write-Host "WSL2 IP: $wslIP"

# Re-create port proxy with current WSL2 IP
netsh interface portproxy add v4tov4 listenport=8888 listenaddress=0.0.0.0 connectport=8888 connectaddress=$wslIP

Write-Host "✅ Port proxy active: 0.0.0.0:8888 → $wslIP:8888"
Write-Host ""
Write-Host "Server accessible at: http://S01068c763f5b0fc1.vw.shawcable.net:8888/"
