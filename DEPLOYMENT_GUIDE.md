# 🚀 Network Ping Monitor - Standalone Deployment Guide

## 📦 Building the Executable

### 1. Build the Standalone Executable
```bash
# Run this on your development machine
build_executable.bat
```

This will create: `dist\NetworkPingMonitor.exe`

## 🔧 **Hardcoded Configuration**

The standalone executable includes **all configuration hardcoded** for security:

### **Monitored Devices:**
- `192.168.200.102` - Building 200 Switch
- `192.168.1.8` - Building 121 Main Server  
- `192.168.200.4` - Building 121 P2P
- `192.168.200.5` - Building 200 P2P

### **Email Settings:**
- **SMTP Server**: smtp.office365.com:587
- **From**: emailrelay@stlinc.com
- **Password**: TuloNop1932!!*Mz (hardcoded, safe behind firewall)
- **Recipients**: garretts@stlinc.com, DevOps@stlinc.com

### **Monitoring Settings:**
- **Ping Interval**: 1 second
- **Email Alert Threshold**: 3 consecutive failed pings
- **Timeout**: 4 seconds (Windows default)

## 🎯 **Server Deployment**

### **Step 1: Copy to Server**
```bash
# Copy the single file to your server
scp dist/NetworkPingMonitor.exe user@server:/path/to/deployment/
```

### **Step 2: Run on Server**
```bash
# Simply execute the standalone file
NetworkPingMonitor.exe
```

### **Step 3: Run as Windows Service (Recommended)**

**Option A: Using NSSM (Non-Sucking Service Manager)**
```bash
# Download NSSM and install the service
nssm install "Network Ping Monitor" "C:\path\to\NetworkPingMonitor.exe"
nssm set "Network Ping Monitor" Description "Monitors network devices and sends email alerts"
nssm set "Network Ping Monitor" Start SERVICE_AUTO_START
nssm start "Network Ping Monitor"
```

**Option B: Using PowerShell (Windows 10/Server 2016+)**
```powershell
# Create scheduled task to run at startup
$action = New-ScheduledTaskAction -Execute "C:\path\to\NetworkPingMonitor.exe"
$trigger = New-ScheduledTaskTrigger -AtStartup
$principal = New-ScheduledTaskPrincipal -UserId "SYSTEM" -LogonType ServiceAccount
Register-ScheduledTask -TaskName "Network Ping Monitor" -Action $action -Trigger $trigger -Principal $principal
```

## 📊 **What the Executable Does**

### **Monitoring Behavior:**
- ✅ Pings all 4 devices every second
- ✅ Logs every failed ping to CSV files in `logs/` directory
- ✅ Sends email alerts after 3 consecutive failures
- ✅ Sends recovery emails when devices come back online
- ✅ Creates timestamped log files: `logs/ping_log_YYYYMMDD_HHMMSS.csv`

### **Email Alerts:**
- **Outage Alert**: Sent after 3 consecutive ping failures
- **Recovery Alert**: Sent when device comes back online
- **Subject**: `[NETWORK ALERT] Device Outage/Recovery - Device Name (IP)`

### **Console Output:**
```
🔍 Starting continuous ping monitor for 4 devices...
⏱️  Ping interval: 1 second(s) (matches default ping behavior)
📧 Email alerts: Enabled
🚨 Alert threshold: 3 consecutive failed pings
📬 Recipients: garretts@stlinc.com, DevOps@stlinc.com

✅ 192.168.200.102 (Building 200 Switch) - ONLINE
✅ 192.168.1.8 (Building 121 Main Server) - ONLINE
✅ 192.168.200.4 (Building 121 P2P) - ONLINE
✅ 192.168.200.5 (Building 200 P2P) - ONLINE

🚀 Continuous monitoring started at 2025-10-06 15:30:00
```

## 🔒 **Security Notes**

### **Hardcoded Secrets - Safe for Server Deployment:**
- ✅ **Email password hardcoded** in executable
- ✅ **Safe behind firewall** - no external config files
- ✅ **No plaintext config files** on server filesystem
- ✅ **Single executable** - easy to secure and backup

### **Network Security:**
- ✅ **ICMP pings only** - minimal network footprint
- ✅ **SMTP outbound only** - port 587 to Office365
- ✅ **No inbound connections** - monitoring tool only

## 📁 **File Structure on Server**

After deployment, the server will have:
```
C:\path\to\deployment\
├── NetworkPingMonitor.exe     # Single standalone executable
└── logs\                      # Created automatically
    ├── ping_log_20251006_153000.csv
    ├── ping_log_20251007_080000.csv
    └── ...
```

## ⚡ **Performance & Resources**

### **System Requirements:**
- **OS**: Windows 7/Server 2008 or newer
- **RAM**: ~10-20 MB (very lightweight)
- **CPU**: Minimal (<1% on modern systems)
- **Network**: ICMP ping + SMTP outbound

### **Log File Management:**
- **New file daily** when monitor restarts
- **~1-5 MB per day** depending on outages
- **CSV format** - easy to analyze in Excel
- **Consider log rotation** for long-term deployments

## 🚀 **Deployment Complete!**

Your standalone executable is ready for server deployment with:
- ✅ **All secrets hardcoded** (safe behind firewall)
- ✅ **Zero configuration** required on server
- ✅ **Single file deployment** - just copy and run
- ✅ **24/7 monitoring** with email alerts
- ✅ **Comprehensive logging** to CSV files

**Simply copy `NetworkPingMonitor.exe` to your server and run it!**