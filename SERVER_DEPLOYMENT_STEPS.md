# 📦 Server Deployment Checklist

## 🎯 **What to Copy to Server:**

Copy this **entire folder structure** to your server:

```
📁 PingTest\                              ← Copy this whole folder
├── 📁 dist\
│   └── 📄 NetworkPingMonitor.exe         ← Main executable (7.8 MB)
├── 📄 install_service_builtin.bat        ← Service installer
├── 📄 uninstall_service_builtin.bat      ← Service uninstaller
└── 📁 logs\                              ← Will be created automatically
    └── (log files created during operation)
```

## 🚀 **Server Installation Steps:**

### **Step 1: Copy Files**
```bash
# Copy entire PingTest folder to server
# Example: Copy to C:\NetworkMonitor\
```

### **Step 2: Install Service (Run as Administrator)**
```bash
# On the server:
1. Right-click Command Prompt → "Run as administrator"
2. cd C:\NetworkMonitor
3. install_service_builtin.bat
```

### **Step 3: Verify Installation**
```bash
# Check service was created:
1. Press Win+R
2. Type: services.msc
3. Press Enter
4. Look for "Network Ping Monitor"
```

## ✅ **What Happens After Installation:**

### **Service Details:**
- **Name**: NetworkPingMonitor
- **Display Name**: Network Ping Monitor
- **Description**: Monitors network devices and sends email alerts
- **Startup Type**: Automatic (starts with Windows)
- **Status**: Running

### **Service Management:**
Right-click on "Network Ping Monitor" in Services console:
- ▶️ **Start** - Start the monitoring
- ⏹️ **Stop** - Stop the monitoring
- 🔄 **Restart** - Restart if needed
- ⚙️ **Properties** - View/change settings

### **Monitoring Behavior:**
- ✅ **Starts automatically** when server boots
- ✅ **Runs continuously** 24/7
- ✅ **Pings devices every 1 second**
- ✅ **Sends email alerts** after 3 failures
- ✅ **Logs everything** to CSV files in logs\ folder

## 📊 **Files Created During Operation:**

After installation and running, you'll see:
```
📁 C:\NetworkMonitor\
├── 📁 dist\
│   └── 📄 NetworkPingMonitor.exe
├── 📄 install_service_builtin.bat
├── 📄 uninstall_service_builtin.bat
└── 📁 logs\                              ← Created automatically
    ├── 📄 ping_log_20251006_120000.csv   ← Today's monitoring log
    ├── 📄 ping_log_20251007_080000.csv   ← Tomorrow's log (if restarted)
    └── ...
```

## 🔧 **Service Management Commands:**

### **From Command Line:**
```bash
# Start service
sc start NetworkPingMonitor

# Stop service
sc stop NetworkPingMonitor

# Check status
sc query NetworkPingMonitor

# Uninstall service (if needed)
uninstall_service_builtin.bat
```

### **From Services Console (services.msc):**
- Right-click → Start/Stop/Restart
- Double-click → Properties (startup type, etc.)

## 📧 **What Gets Monitored:**

**Devices (hardcoded in executable):**
- 192.168.200.102 (Building 200 Switch)
- 192.168.1.8 (Building 121 Main Server)
- 192.168.200.4 (Building 121 P2P)
- 192.168.200.5 (Building 200 P2P)

**Email Alerts sent to:**
- garretts@stlinc.com
- DevOps@stlinc.com

## 🎉 **Summary:**

**Copy → Run Batch → Manage in Services = DONE!**

Your network monitoring will be running as a proper Windows service, visible and manageable through the standard Windows Services console! 🚀