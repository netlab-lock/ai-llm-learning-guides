# Local File Serving over LAN

Serve a directory of files (HTML, PDF, etc.) over the local network so other devices (phone, tablet, another PC) can browse them like a website.

## Key Principle

**Run the server on the same OS where the files live.** If files are on Windows (D:\...), run the server on Windows. If files are only in WSL filesystem (~), run on WSL.

**PITFALL: Do NOT run the server in WSL to serve files on /mnt/d/ (Windows drives).** WSL2 uses NAT by default — LAN devices cannot reach WSL's IP directly. Even with mirrored networking (same IP), inbound connections from LAN are unreliable. Running on Windows avoids NAT, port forwarding, and firewall complexity entirely.

## Steps

### 1. Start the HTTP server (on Windows)

```powershell
# From WSL, launch on Windows side:
powershell.exe -Command "Start-Process python -ArgumentList '-m http.server 8080 --bind 0.0.0.0' -WorkingDirectory 'D:\学习' -WindowStyle Hidden"
```

- Replace `D:\学习` with the actual directory path
- Port 8080 is conventional; use any high port
- `--bind 0.0.0.0` listens on all interfaces (required for LAN access)
- `-WindowStyle Hidden` runs without a visible console window

### 2. Open Windows Firewall

```powershell
# Needs admin — use Start-Process -Verb RunAs:
powershell.exe -Command "Start-Process cmd -ArgumentList '/c netsh advfirewall firewall add rule name=\"HTTP-LAN\" dir=in action=allow protocol=TCP localport=8080' -Verb RunAs -Wait"
```

Verify:
```powershell
powershell.exe -Command "Get-NetFirewallRule -DisplayName 'HTTP-LAN' | Select-Object DisplayName, Enabled"
```

### 3. Get the LAN IP

```powershell
powershell.exe -Command "(Get-NetIPAddress -AddressFamily IPv4 -InterfaceAlias 'WLAN').IPAddress"
```

### 4. Verify

```bash
curl -s -o /dev/null -w "%{http_code}" http://localhost:8080/
# Should return 200
```

Access from other devices: `http://<LAN_IP>:8080`

## Landing Page

Create an `index.html` in the served directory with navigation cards linking to sub-topics. Dark theme recommended for technical content.

## Restart Script (Windows .bat)

Create `启动局域网服务.bat` in the served directory:

```bat
@echo off
chcp 65001 >nul
title 学习文档局域网服务
echo ========================================
echo   学习文档局域网 HTTP 服务
echo ========================================
echo.
:: Kill old python http.server
taskkill /F /IM python.exe /FI "WINDOWTITLE eq http.server*" >nul 2>&1
:: Auto-detect LAN IP
for /f "tokens=2 delims=:" %%a in ('ipconfig ^| findstr /i "IPv4" ^| findstr /v "127.0.0.1"') do (set LAN_IP=%%a)
set LAN_IP=%LAN_IP: =%
echo   本机访问:  http://localhost:8080
echo   局域网访问: http://%LAN_IP%:8080
echo.
echo   按 Ctrl+C 停止服务
echo ========================================
echo.
cd /d D:\学习
python -m http.server 8080 --bind 0.0.0.0
pause
```

## Stopping the Server

Multiple methods:
```powershell
# Method 1: taskkill (simplest)
taskkill /F /IM python.exe

# Method 2: PowerShell, by PID
powershell.exe -Command "Get-Process python | Select-Object Id, StartTime"
powershell.exe -Command "Stop-Process -Id <PID> -Force"

# Method 3: Find and kill by port
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :8080 ^| findstr LISTENING') do taskkill /PID %%a /F
```

## External Access from Outside LAN

When the user wants to access files from outside their home network, present these options:

### Option A: Tailscale (recommended for most users)
- Mesh VPN: install on both devices, log in with same account, done
- No public IP, no port forwarding, no domain needed
- Free for up to 100 personal devices
- Key explanation: "Tailscale = virtual LAN (devices think they're on same WiFi). 向日葵/ToDesk = remote desktop (see and control screen). Different things."
- Best when: user just wants to reach their own files from phone/laptop while out

### Option B: Cloud server (VPS)
- 24/7 online, doesn't depend on home PC being on
- Best when: user wants always-on access or to share with others
- **What to buy**: 轻量应用服务器 (NOT standard ECS/CVM). Cheapest tier: 1核2G, Ubuntu 22.04, 3Mbps, 40GB.
  - 腾讯云 ~10元/月 (student), 阿里云 ~99元/年 (new user), 华为云 similar
  - **Do NOT buy**: 对象存储(COS/OSS), 云数据库, 容器服务, Serverless, GPU服务器, CDN
- **Deploy**: apt install nginx → scp files to /var/www/ → configure nginx → open port 80 in security group

### Option C: Cloudflare Tunnel
- Free, gives a public domain, no public IP needed
- Requires owning a domain name (~50元/年)
- Best when: user has a domain and wants a clean URL

### Option D: FRP (Fast Reverse Proxy)
- Requires a VPS with public IP as relay
- Most flexible but most complex
- Best when: user already has a cloud server

## Pitfalls

1. **WSL NAT trap**: Files on /mnt/c/ or /mnt/d/ are Windows files. Serve from Windows, not WSL. WSL2 NAT blocks inbound LAN connections.
2. **Firewall needs admin**: `New-NetFirewallRule` from WSL fails with PermissionDenied. Use `Start-Process cmd -Verb RunAs` to elevate.
3. **Port conflict**: Check if port is already in use: `netstat -ano | findstr :8080`
4. **Python version**: Windows ships with Python 3.7+ in most setups. Check with `powershell.exe -Command "python --version"`.
5. **Hidden window**: `-WindowStyle Hidden` means no visible console. To stop the server: `taskkill /F /IM python.exe` or find the PID via netstat.
6. **Cloud provider product overload**: Users browsing cloud provider websites get overwhelmed by dozens of products. Directly tell them: "你需要的 = 一台远程电脑 (虚拟机)", point to 轻量应用服务器, and explicitly list what NOT to buy.
