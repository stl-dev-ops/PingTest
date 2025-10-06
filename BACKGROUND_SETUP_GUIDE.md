# 🚀 Running Network Ping Monitor as Background Task

## 🎯 **Three Options Available:**

### **Option 1: Windows Service (Recommended for Production) ⭐**

**Best for**: Production servers, automatic startup, robust operation

**Steps:**
1. **Download NSSM**: https://nssm.cc/download
2. **Extract `nssm.exe`** to your PingTest folder
3. **Run as Administrator**: `install_service.bat`

**Commands:**
```bash
# Install as service
install_service.bat

# Manage service
nssm start NetworkPingMonitor      # Start
nssm stop NetworkPingMonitor       # Stop
nssm restart NetworkPingMonitor    # Restart
sc query NetworkPingMonitor        # Check status

# Uninstall service
uninstall_service.bat
```

**Benefits:**
- ✅ **Automatic startup** with Windows
- ✅ **Runs as SYSTEM** (no user login required)
- ✅ **Automatic restart** if crashes
- ✅ **Log rotation** built-in
- ✅ **Professional service management**

---

### **Option 2: Scheduled Task (Built-in Windows) 🔧**

**Best for**: When you can't install NSSM, built-in Windows solution

**Steps:**
1. **Right-click PowerShell** → "Run as Administrator"
2. **Navigate** to PingTest folder: `cd C:\dev\PingTest`
3. **Run**: `.\install_scheduled_task.ps1`

**Commands:**
```powershell
# Install as scheduled task
.\install_scheduled_task.ps1

# Manage task
Start-ScheduledTask -TaskName "NetworkPingMonitor"    # Start
Stop-ScheduledTask -TaskName "NetworkPingMonitor"     # Stop
Get-ScheduledTask -TaskName "NetworkPingMonitor"      # Status

# Uninstall task
.\uninstall_scheduled_task.ps1
```

**Benefits:**
- ✅ **No external tools** required
- ✅ **Automatic startup** with Windows
- ✅ **Runs as SYSTEM**
- ✅ **Built-in Windows management**

---

### **Option 3: Simple Background Process (Quick Start) ⚡**

**Best for**: Testing, development, temporary monitoring

**Steps:**
1. **Double-click**: `start_background.bat`

**Commands:**
```bash
# Start in background
start_background.bat

# Check if running
tasklist | findstr NetworkPingMonitor

# Stop background process
stop_background.bat
```

**Benefits:**
- ✅ **Instant start** - no setup required
- ✅ **Simple management**
- ✅ **Good for testing**

**Limitations:**
- ❌ **Manual startup** after reboot
- ❌ **Stops when user logs out**
- ❌ **No automatic restart**

---

## 📊 **Comparison Matrix:**

| Feature | Windows Service | Scheduled Task | Background Process |
|---------|----------------|----------------|-------------------|
| **Auto-start** | ✅ | ✅ | ❌ |
| **Survives logout** | ✅ | ✅ | ❌ |
| **Auto-restart** | ✅ | ❌ | ❌ |
| **Easy setup** | ⚠️ (needs NSSM) | ✅ | ✅ |
| **Log management** | ✅ | ❌ | ❌ |
| **Production ready** | ✅ | ✅ | ❌ |

---

## 🎯 **Recommended Setup for Production:**

### **Step 1: Download NSSM**
```bash
# Download from: https://nssm.cc/download
# Extract nssm.exe to C:\dev\PingTest\
```

### **Step 2: Install as Service**
```bash
# Right-click Command Prompt → "Run as Administrator"
cd C:\dev\PingTest
install_service.bat
```

### **Step 3: Verify Installation**
```bash
# Check service status
sc query NetworkPingMonitor

# Check logs
type logs\service_output.log
```

---

## 📁 **File Structure After Service Installation:**

```
C:\dev\PingTest\
├── dist\
│   └── NetworkPingMonitor.exe          # Main executable
├── logs\
│   ├── ping_log_YYYYMMDD_HHMMSS.csv   # Ping monitoring logs
│   ├── service_output.log              # Service console output
│   └── service_errors.log              # Service error log
├── install_service.bat                 # Service installer
├── uninstall_service.bat              # Service uninstaller
├── start_background.bat               # Background process starter
├── stop_background.bat                # Background process stopper
├── install_scheduled_task.ps1         # Scheduled task installer
├── uninstall_scheduled_task.ps1       # Scheduled task uninstaller
└── nssm.exe                           # Service manager (download separately)
```

---

## 🔍 **Monitoring the Background Service:**

### **Check Service Status:**
```bash
# Windows Service
sc query NetworkPingMonitor
nssm status NetworkPingMonitor

# Scheduled Task
Get-ScheduledTask -TaskName "NetworkPingMonitor"

# Background Process
tasklist | findstr NetworkPingMonitor
```

### **View Logs:**
```bash
# Monitoring logs (CSV)
dir logs\ping_log_*.csv

# Service logs (if using NSSM)
type logs\service_output.log
type logs\service_errors.log
```

### **Performance Monitoring:**
```bash
# Check CPU/Memory usage
tasklist /FI "IMAGENAME eq NetworkPingMonitor.exe" /FO TABLE

# Real-time monitoring
wmic process where name="NetworkPingMonitor.exe" get ProcessId,PageFileUsage,WorkingSetSize
```

---

## 🚀 **Quick Start (Recommended):**

**For Production Server:**
1. Copy `NetworkPingMonitor.exe` to server
2. Download NSSM to same folder
3. Run `install_service.bat` as Administrator
4. Service automatically starts and runs 24/7!

**For Testing:**
1. Double-click `start_background.bat`
2. Monitor runs in background immediately

Your ping monitor will now run continuously in the background, monitoring all devices and sending email alerts! 🎉