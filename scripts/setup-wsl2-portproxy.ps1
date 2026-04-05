# Windows-WSL2 Port Proxy Setup
# Run this ONCE as Administrator on Windows

# Set up port forwarding from Windows:8888 to WSL2:8888

# Get WSL2 IP (may change on restart)
$wslIP = wsl hostname -I
Write-Host "WSL2 IP detected: $wslIP"

# Add port proxy
netsh interface portproxy add v4tov4 listenport=8888 listenaddress=0.0.0.0 connectport=8888 connectaddress=$wslIP

# Configure Windows Firewall to allow port 8888
New-NetFirewallRule -DisplayName "OpenClaw Server" -Direction Inbound -LocalPort 8888 -Protocol TCP -Action Allow

Write-Host "✅ Port proxy configured: 0.0.0.0:8888 → $wslIP:8888"
Write-Host ""
Write-Host "To make this persist across restarts, run the startup script:"
Write-Host "  startup-script.ps1"
