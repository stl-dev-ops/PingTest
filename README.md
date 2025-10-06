# Network Ping Monitor with Email Alerts

A Python-based network monitoring tool that continuously pings specified devices, logs outages to CSV files, and sends email alerts when devices are unreachable for more than a specified threshold.

## Features

- **Continuous monitoring**: 24/7 monitoring of multiple network devices
- **Email alerts**: Automatic email notifications when devices are down for 3+ consecutive pings
- **CSV logging**: Detailed logging of all events to timestamped CSV files
- **Real-time status**: Live console output showing device status changes
- **Cross-platform**: Works on Windows, Linux, and macOS
- **Threaded pings**: Concurrent ping operations for faster monitoring
- **Recovery notifications**: Optional email alerts when devices come back online
- **Configurable thresholds**: Adjustable ping intervals, timeouts, and alert thresholds

## Device Configuration

The tool is pre-configured to monitor the following devices:

| IP Address | Description |
|------------|-------------|
| 192.168.200.102 | 200 Switch |
| 192.168.1.8 | Main Server |
| 192.168.200.4 | Building 121 |
| 192.168.200.5 | Building 200 |

## Quick Start

### 1. Configure Email Alerts (Recommended)

Run the email setup helper to configure your email settings:

```bash
python setup_email.py
```

This will guide you through setting up:
- Email provider (Gmail, Outlook, Yahoo, or custom SMTP)
- Your email credentials 
- Alert recipients
- Alert preferences

### 2. Start Monitoring

**Option 1 - Use the batch file:**
```
start_monitor.bat
```

**Option 2 - Run directly with Python:**
```powershell
cd c:\dev\PingTest
python ping_monitor.py
```

## Email Alert System

### Alert Threshold
- **Trigger**: 3 consecutive failed ping attempts
- **Outage alerts**: Sent when threshold is reached
- **Recovery alerts**: Sent when device comes back online (optional)

### Supported Email Providers
- **Gmail**: Requires app-specific password
- **Outlook/Hotmail**: Uses outlook.com SMTP
- **Yahoo**: Uses Yahoo SMTP
- **Custom**: Configure any SMTP server

### Gmail App Password Setup
1. Enable 2-factor authentication on your Google account
2. Go to Google Account settings → Security → 2-Step Verification
3. Click "App passwords" and generate a password for "Mail"
4. Use this app password instead of your regular password

## Configuration Options

Edit `config.py` to modify:

### Device Settings
```python
DEVICES = {
    "192.168.1.1": "Router",
    "192.168.1.10": "Server",
    # Add more devices as needed
}
```

### Monitoring Settings
```python
PING_INTERVAL = 30          # Seconds between ping cycles
PING_TIMEOUT = 5            # Ping timeout duration
EMAIL_ALERT_THRESHOLD = 3   # Failed pings before email alert
```

### Email Settings
```python
EMAIL_ALERTS_ENABLED = True
SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587
EMAIL_FROM = "your-email@gmail.com"
EMAIL_TO = ["admin@company.com", "it@company.com"]
SEND_RECOVERY_EMAILS = True
```

## CSV Log Format

Enhanced CSV format includes email alert tracking:

| Column | Description |
|--------|-------------|
| Timestamp | Date and time of the event |
| IP Address | Device IP address |
| Device Name | Friendly name/description |
| Event Type | OUTAGE_START, OUTAGE_END, OUTAGE_ALERT, OUTAGE_CONTINUE, STATUS_CHECK |
| Status | ONLINE or OFFLINE |
| Duration (minutes) | Duration of outage (for OUTAGE_END events) |
| Failed Ping Count | Number of consecutive failed pings |
| Email Sent | Whether an email alert was sent for this event |
| Notes | Additional information |

## Example Output

### Console Output with Email Alerts
```
🌐 Network Ping Monitor with Email Alerts
==================================================
Configuration loaded from config.py
Devices to monitor: 4
📧 Email alerts configured for 2 recipients

🔍 Starting continuous ping monitor for 4 devices...
⏱️  Ping interval: 30 seconds
⏰ Timeout: 5 seconds
📧 Email alerts: Enabled
🚨 Alert threshold: 3 failed pings
📬 Recipients: admin@company.com, it@company.com

✅ 192.168.200.102 (200 Switch) - ONLINE
✅ 192.168.1.8 (Main Server) - ONLINE
❌ 192.168.200.4 (Building 121) - OFFLINE
✅ 192.168.200.5 (Building 200) - ONLINE

🚀 Continuous monitoring started at 2025-10-06 14:30:52
================================================================================

📊 Monitoring cycle #1 - 14:31:22
❌ 192.168.1.8 (Main Server) went OFFLINE (attempt 1/3)
⏱️  Cycle completed in 1.23 seconds

📊 Monitoring cycle #2 - 14:31:52  
❌ 192.168.1.8 (Main Server) still OFFLINE (attempt 2/3)

📊 Monitoring cycle #3 - 14:32:22
❌ 192.168.1.8 (Main Server) still OFFLINE (attempt 3/3)
📧 Email alert sent for Main Server (192.168.1.8) - OUTAGE_ALERT

📊 Monitoring cycle #5 - 14:33:22
✅ 192.168.1.8 (Main Server) is back ONLINE after 2.15 minutes
📧 Email alert sent for Main Server (192.168.1.8) - RECOVERY_ALERT
```

### Email Alert Sample
```
Subject: [NETWORK ALERT] Device Outage - Main Server (192.168.1.8)

NETWORK DEVICE OUTAGE ALERT

Device: Main Server
IP Address: 192.168.1.8
Alert Time: 2025-10-06 14:32:22
Failed Ping Count: 3
Threshold: 3 failed pings

The device has failed to respond to 3 consecutive ping attempts.
Please check the device status and network connectivity.

This alert was generated automatically by the Network Ping Monitor.
```

### CSV Log Sample
```csv
Timestamp,IP Address,Device Name,Event Type,Status,Duration (minutes),Failed Ping Count,Email Sent,Notes
2025-10-06 14:30:52,192.168.1.8,Main Server,MONITOR_START,ONLINE,0.00,0,False,Initial status check
2025-10-06 14:31:22,192.168.1.8,Main Server,OUTAGE_START,OFFLINE,0.00,1,False,Device became unreachable
2025-10-06 14:32:22,192.168.1.8,Main Server,OUTAGE_ALERT,OFFLINE,0.00,3,True,Email alert threshold reached (3 failed pings)
2025-10-06 14:33:22,192.168.1.8,Main Server,OUTAGE_END,ONLINE,2.15,0,True,Device recovered after 2.15 minutes
```

## Requirements

- Python 3.6 or higher
- Windows, Linux, or macOS
- Network access to target devices
- **For email alerts**: Valid email account with SMTP access

## Files Included

- `ping_monitor.py` - Main monitoring application
- `config.py` - Configuration file (editable)
- `setup_email.py` - Interactive email configuration helper
- `start_monitor.bat` - Windows batch file for easy startup
- `README.md` - This documentation

## Installation & Setup

1. **Download/clone the files** to your desired directory
2. **Configure email** (recommended): `python setup_email.py`
3. **Start monitoring**: `python ping_monitor.py` or use `start_monitor.bat`

## Stopping the Monitor

Press `Ctrl+C` to stop monitoring. The tool will:
- Log final device status for all devices
- Display summary information
- Save all data to the CSV log file

## Troubleshooting

### Email Issues
- **Gmail**: Use app-specific passwords, not your regular password
- **Firewall**: Ensure SMTP ports (587/465) are not blocked
- **Authentication**: Verify email credentials in `config.py`

### Network Issues  
- **Permissions**: Some systems require admin rights for ping
- **Firewall**: Ensure ping (ICMP) traffic is allowed
- **Timeouts**: Increase `PING_TIMEOUT` for slow networks

## Security Notes

- Email passwords are stored in plain text in `config.py`
- Use app-specific passwords when possible
- Protect the `config.py` file from unauthorized access
- Consider using environment variables for sensitive data

## Advanced Configuration

### Running as a Service
For 24/7 monitoring, consider running as a system service:

**Windows (using NSSM):**
```powershell
nssm install PingMonitor "python" "C:\dev\PingTest\ping_monitor.py"
nssm start PingMonitor
```

**Linux (systemd):**
Create a service file in `/etc/systemd/system/ping-monitor.service`

### Multiple Configurations
You can run multiple instances with different config files:
```python
# In your custom script
from config_network1 import *
from ping_monitor import PingMonitor
```