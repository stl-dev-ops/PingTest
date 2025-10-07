#!/usr/bin/env python3
"""
Network Ping Monitor - Standalone Deployment Version
Single-file executable with hardcoded configuration for server deployment
Monitors network devices and sends email alerts for outages
"""

import subprocess
import time
import csv
import datetime
import threading
import os
import sys
import smtplib
import traceback
from email.message import EmailMessage
from typing import Dict, List, Tuple
import platform

# ============================================================================
# HARDCODED CONFIGURATION - Safe for server deployment behind firewall
# ============================================================================

# Device Configuration
DEVICES = {
    "192.168.200.102": "Building 200 Switch",
    "192.168.1.8": "Building 121 Main Server",
    "192.168.200.4": "Building 121 P2P", 
    "192.168.200.5": "Building 200 P2P"
}

# Monitoring Settings
PING_INTERVAL = 1  # seconds between ping attempts
PING_TIMEOUT = 4   # ping timeout in seconds (matches Windows default)

# Logging Settings
LOG_DIRECTORY = "logs"
LOG_PERIODIC_STATUS = True
PERIODIC_LOG_INTERVAL = 3600  # seconds (1 hour)

# Email Alert Settings
EMAIL_ALERTS_ENABLED = True
EMAIL_ALERT_THRESHOLD = 3  # Number of consecutive failed pings before sending email alert

# SMTP Configuration
SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587
SMTP_USE_TLS = True

# Email Credentials - Hardcoded for server deployment
EMAIL_FROM = "emailrelay@stlinc.com"
EMAIL_PASSWORD = "TuloNop1932!!*Mz"
EMAIL_TO = ["garretts@stlinc.com", "DevOps@stlinc.com"]

# Email Content Settings
EMAIL_SUBJECT_PREFIX = "[NETWORK ALERT]"
SEND_RECOVERY_EMAILS = True

# ============================================================================
# NETWORK PING MONITOR CLASS
# ============================================================================

# Single-instance guard (cross-platform)
import tempfile

class SingleInstance:
    def __init__(self, name: str = "NetworkPingMonitor"):
        self.name = name
        self.is_windows = platform.system().lower() == 'windows'
        self.handle = None
        self.fp = None
        if self.is_windows:
            try:
                import ctypes
                from ctypes import wintypes
                CreateMutex = ctypes.windll.kernel32.CreateMutexW
                CreateMutex.argtypes = [wintypes.LPVOID, wintypes.BOOL, wintypes.LPCWSTR]
                CreateMutex.restype = wintypes.HANDLE
                self.handle = CreateMutex(None, False, f"Global\\{self.name}")
                last = ctypes.windll.kernel32.GetLastError()
                ERROR_ALREADY_EXISTS = 183
                if last == ERROR_ALREADY_EXISTS:
                    raise RuntimeError("Another instance is already running")
            except Exception:
                raise
        else:
            import fcntl
            lockfile = os.path.join(tempfile.gettempdir(), f"{self.name}.lock")
            self.fp = open(lockfile, 'w')
            try:
                fcntl.flock(self.fp.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                raise RuntimeError("Another instance is already running")

    def release(self):
        if self.is_windows:
            try:
                import ctypes
                if self.handle:
                    ctypes.windll.kernel32.ReleaseMutex(self.handle)
                    ctypes.windll.kernel32.CloseHandle(self.handle)
                    self.handle = None
            except Exception:
                pass
        else:
            try:
                import fcntl
                if self.fp:
                    fcntl.flock(self.fp.fileno(), fcntl.LOCK_UN)
                    self.fp.close()
                    self.fp = None
            except Exception:
                pass

    def __del__(self):
        self.release()


# Instantiate singleton guard early
try:
    _single_instance = SingleInstance('NetworkPingMonitor')
except RuntimeError:
    print('Another instance of NetworkPingMonitor is already running; exiting.')
    sys.exit(0)

class PingMonitor:
    def __init__(self, devices: Dict[str, str], ping_interval: int = 1, timeout: int = 4):
        """
        Initialize the ping monitor
        
        Args:
            devices: Dictionary of {ip_address: description}
            ping_interval: Seconds between ping attempts
            timeout: Ping timeout in seconds
        """
        self.devices = devices
        self.ping_interval = ping_interval
        self.timeout = timeout
        self.running = False
        self.device_status = {ip: True for ip in devices.keys()}  # True = online, False = offline
        self.last_status_change = {ip: datetime.datetime.now() for ip in devices.keys()}
        self.failed_ping_count = {ip: 0 for ip in devices.keys()}  # Track consecutive failed pings
        self.email_sent_for_outage = {ip: False for ip in devices.keys()}  # Track if email was sent for current outage
        
        # CSV file setup - compute filename and ensure log directory exists before creating file
        timestamp_suffix = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"ping_log_{timestamp_suffix}.csv"

        # Determine a stable base directory: if running as a frozen exe use the exe location
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))

        # Create logs directory under base_dir if specified and adjust filename
        if LOG_DIRECTORY:
            log_dir = os.path.join(base_dir, LOG_DIRECTORY)
            os.makedirs(log_dir, exist_ok=True)
            self.csv_filename = os.path.join(log_dir, filename)
        else:
            self.csv_filename = os.path.join(base_dir, filename)

        # Create CSV file with headers if needed
        self.setup_csv_file()
        
        # Determine ping command based on OS
        self.is_windows = platform.system().lower() == "windows"
    
    def setup_csv_file(self):
        """Create CSV file with headers"""
        # Only create the file and write headers if it does not already exist or is empty
        try:
            need_header = True
            if os.path.exists(self.csv_filename) and os.path.getsize(self.csv_filename) > 0:
                need_header = False

            with open(self.csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                if need_header:
                    writer.writerow([
                        'Timestamp',
                        'IP Address', 
                        'Device Name',
                        'Event Type',
                        'Status',
                        'Duration (minutes)',
                        'Failed Ping Count',
                        'Email Sent',
                        'Notes'
                    ])
                    print(f"📄 CSV log file created with header: {self.csv_filename}")
        except Exception as e:
            print(f"❌ Failed to create CSV log file {self.csv_filename}: {e}")
    
    def send_email_alert(self, ip_address: str, event_type: str, failed_count: int = 0, duration_minutes: float = 0):
        """
        Send email alert for device outage or recovery
        
        Args:
            ip_address: IP address of the device
            event_type: OUTAGE_ALERT or RECOVERY_ALERT
            failed_count: Number of consecutive failed pings
            duration_minutes: Duration of outage for recovery alerts
        """
        if not EMAIL_ALERTS_ENABLED:
            return False
            
        try:
            device_name = self.devices.get(ip_address, "Unknown Device")
            timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            # Create message
            msg = EmailMessage()
            msg['From'] = EMAIL_FROM
            msg['To'] = ', '.join(EMAIL_TO)
            
            if event_type == "OUTAGE_ALERT":
                msg['Subject'] = f"{EMAIL_SUBJECT_PREFIX} Device Outage - {device_name} ({ip_address})"
                
                body = f"""NETWORK DEVICE OUTAGE ALERT

Device: {device_name}
IP Address: {ip_address}
Alert Time: {timestamp}
Failed Ping Count: {failed_count}
Threshold: {EMAIL_ALERT_THRESHOLD} failed pings

The device has failed to respond to {failed_count} consecutive ping attempts.
Please check the device status and network connectivity.

This alert was generated automatically by the Network Ping Monitor.
"""
            
            elif event_type == "RECOVERY_ALERT":
                msg['Subject'] = f"{EMAIL_SUBJECT_PREFIX} Device Recovery - {device_name} ({ip_address})"
                
                body = f"""NETWORK DEVICE RECOVERY ALERT

Device: {device_name}
IP Address: {ip_address}
Recovery Time: {timestamp}
Outage Duration: {duration_minutes:.2f} minutes

The device is now responding to ping requests and appears to be back online.

This recovery notification was generated automatically by the Network Ping Monitor.
"""
            
            msg.set_content(body)
            
            # Send email
            with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                if SMTP_USE_TLS:
                    server.starttls()
                server.login(EMAIL_FROM, EMAIL_PASSWORD)
                server.send_message(msg)
            
            print(f"📧 Email alert sent for {device_name} ({ip_address}) - {event_type}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to send email alert for {ip_address}: {e}")
            return False
    
    def ping_device(self, ip_address: str) -> bool:
        """
        Ping a single device and return True if successful
        Uses default system ping behavior to match 'ping <ip>' command
        
        Args:
            ip_address: IP address to ping
            
        Returns:
            bool: True if ping successful, False otherwise
        """
        try:
            if self.is_windows:
                # Windows ping command - use default timeout (4000ms) to match standard ping behavior
                # -n 1 = send 1 packet, -w 4000 = wait 4000ms (4 seconds) for reply
                command = ['ping', '-n', '1', '-w', '4000', ip_address]
            else:
                # Linux/Unix ping command
                command = ['ping', '-c', '1', '-W', str(self.timeout), ip_address]
            
            result = subprocess.run(
                command,
                capture_output=True,
                text=True,
                timeout=self.timeout + 2
            )
            
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            return False
        except Exception as e:
            print(f"Error pinging {ip_address}: {e}")
            return False
    
    def log_event(self, ip_address: str, event_type: str, status: str, duration_minutes: float = 0, 
                  failed_count: int = 0, email_sent: bool = False, notes: str = ""):
        """
        Log an event to the CSV file
        
        Args:
            ip_address: IP address of the device
            event_type: Type of event (OUTAGE_START, OUTAGE_END, OUTAGE_ALERT, STATUS_CHECK, etc.)
            status: Current status (ONLINE, OFFLINE)
            duration_minutes: Duration of the event in minutes
            failed_count: Number of consecutive failed pings
            email_sent: Whether an email alert was sent
            notes: Additional notes
        """
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        device_name = self.devices.get(ip_address, "Unknown")
        
        # Ensure header is present (defensive) before appending
        try:
            self.ensure_csv_header()

            with open(self.csv_filename, 'a', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow([
                    timestamp,
                    ip_address,
                    device_name,
                    event_type,
                    status,
                    f"{duration_minutes:.2f}",
                    failed_count,
                    email_sent,
                    notes
                ])
        except Exception as e:
            print(f"❌ Failed to write log event to {self.csv_filename}: {e}")

    def ensure_csv_header(self):
        """Check the CSV's first line and prepend header if missing."""
        try:
            if not os.path.exists(self.csv_filename) or os.path.getsize(self.csv_filename) == 0:
                # file missing or empty: setup_csv_file will create header
                self.setup_csv_file()
                return

            # Read first line to confirm header
            with open(self.csv_filename, 'r', encoding='utf-8') as f:
                first = f.readline()
                if 'Timestamp' in first and 'IP Address' in first:
                    return  # header present

            # Header missing: prepend header safely
            tmp = self.csv_filename + '.tmp'
            with open(self.csv_filename, 'r', encoding='utf-8') as orig, open(tmp, 'w', encoding='utf-8', newline='') as newf:
                writer = csv.writer(newf)
                writer.writerow([
                    'Timestamp', 'IP Address', 'Device Name', 'Event Type', 'Status',
                    'Duration (minutes)', 'Failed Ping Count', 'Email Sent', 'Notes'
                ])
                for line in orig:
                    newf.write(line)

            os.replace(tmp, self.csv_filename)
            print(f"Fixed missing header in: {self.csv_filename}")
        except Exception as e:
            print(f"❌ Failed to ensure CSV header for {self.csv_filename}: {e}")
    
    def check_device_status(self, ip_address: str):
        """
        Check a single device and handle status changes with continuous logging
        
        Args:
            ip_address: IP address to check
        """
        current_time = datetime.datetime.now()
        is_online = self.ping_device(ip_address)
        previous_status = self.device_status[ip_address]
        
        if is_online:
            # Device is responding
            if not previous_status:
                # Device came back online after being offline
                last_change_time = self.last_status_change[ip_address]
                duration_minutes = (current_time - last_change_time).total_seconds() / 60
                
                # Send recovery email if email was sent for the outage
                email_sent = False
                if SEND_RECOVERY_EMAILS and self.email_sent_for_outage[ip_address]:
                    email_sent = self.send_email_alert(ip_address, "RECOVERY_ALERT", 0, duration_minutes)
                
                self.log_event(ip_address, "OUTAGE_END", "ONLINE", duration_minutes, 
                             0, email_sent, f"Device recovered after {duration_minutes:.2f} minutes")
                
                print(f"✅ {current_time.strftime('%H:%M:%S')} - {ip_address} ({self.devices[ip_address]}) is back ONLINE after {duration_minutes:.2f} minutes")
                
                # Reset counters
                self.email_sent_for_outage[ip_address] = False
            
            # Reset failed ping counter
            self.failed_ping_count[ip_address] = 0
            self.device_status[ip_address] = True
            
            # Update last change time only if status actually changed
            if not previous_status:
                self.last_status_change[ip_address] = current_time
            
            # Periodic status logging (every hour for online devices)
            elif LOG_PERIODIC_STATUS and (current_time - self.last_status_change[ip_address]).total_seconds() >= PERIODIC_LOG_INTERVAL:
                self.log_event(ip_address, "STATUS_CHECK", "ONLINE", 0, 0, False, "Periodic status check")
                self.last_status_change[ip_address] = current_time
        
        else:
            # Device is not responding
            self.failed_ping_count[ip_address] += 1
            failed_count = self.failed_ping_count[ip_address]
            
            if previous_status:
                # Device just went offline - log the initial failure
                self.log_event(ip_address, "OUTAGE_START", "OFFLINE", 0, failed_count, False, 
                             "Device became unreachable")
                print(f"❌ {current_time.strftime('%H:%M:%S')} - {ip_address} ({self.devices[ip_address]}) went OFFLINE (ping #{failed_count})")
                self.device_status[ip_address] = False
                self.last_status_change[ip_address] = current_time
            
            else:
                # Device still offline - log every failed ping
                self.log_event(ip_address, "PING_FAILED", "OFFLINE", 0, failed_count, False, 
                             f"Consecutive failed ping #{failed_count}")
                print(f"❌ {current_time.strftime('%H:%M:%S')} - {ip_address} ({self.devices[ip_address]}) ping failed #{failed_count}")
            
            # Send email alert if threshold reached and not already sent
            if failed_count == EMAIL_ALERT_THRESHOLD and not self.email_sent_for_outage[ip_address]:
                email_sent = self.send_email_alert(ip_address, "OUTAGE_ALERT", failed_count)
                if email_sent:
                    self.email_sent_for_outage[ip_address] = True
                
                self.log_event(ip_address, "OUTAGE_ALERT", "OFFLINE", 0, failed_count, email_sent, 
                             f"Email alert sent after {failed_count} failed pings")
                print(f"📧 {current_time.strftime('%H:%M:%S')} - Email alert sent for {self.devices[ip_address]} after {failed_count} failed pings")
    
    def monitor_all_devices(self):
        """Monitor all devices in a single cycle"""
        threads = []
        
        for ip_address in self.devices.keys():
            thread = threading.Thread(target=self.check_device_status, args=(ip_address,))
            threads.append(thread)
            thread.start()
        
        # Wait for all threads to complete
        for thread in threads:
            thread.join()
    
    def start_monitoring(self):
        """Start the continuous monitoring loop"""
        self.running = True
        print(f"🔍 Starting continuous ping monitor for {len(self.devices)} devices...")
        print(f"⏱️  Ping interval: {self.ping_interval} second(s) (matches default ping behavior)")
        print(f"⏰ Timeout: {self.timeout} seconds (matches default ping behavior)")
        print(f"📧 Email alerts: {'Enabled' if EMAIL_ALERTS_ENABLED else 'Disabled'}")
        if EMAIL_ALERTS_ENABLED:
            print(f"🚨 Alert threshold: {EMAIL_ALERT_THRESHOLD} consecutive failed pings")
            print(f"📬 Recipients: {', '.join(EMAIL_TO)}")
        print(f"📄 Log file: {self.csv_filename}")
        print("📝 Logging: Every failed ping will be logged immediately")
        print("Press Ctrl+C to stop monitoring\n")
        
        # Log initial status
        for ip_address in self.devices.keys():
            is_online = self.ping_device(ip_address)
            status = "ONLINE" if is_online else "OFFLINE"
            self.device_status[ip_address] = is_online
            self.failed_ping_count[ip_address] = 0 if is_online else 1
            
            self.log_event(ip_address, "MONITOR_START", status, 0, 
                         self.failed_ping_count[ip_address], False, "Initial status check")
            
            status_symbol = "✅" if is_online else "❌"
            print(f"{status_symbol} {ip_address} ({self.devices[ip_address]}) - {status}")
        
        print(f"\n🚀 Continuous monitoring started at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("💡 Only status changes and failures will be displayed to reduce console spam")
        print("=" * 80)
        
        try:
            cycle_count = 0
            last_summary_time = datetime.datetime.now()
            
            while self.running:
                cycle_count += 1
                cycle_start = datetime.datetime.now()
                
                # Show summary every 60 seconds instead of every cycle
                if (cycle_start - last_summary_time).total_seconds() >= 60:
                    online_count = sum(1 for status in self.device_status.values() if status)
                    total_count = len(self.devices)
                    print(f"\n📊 Status Summary - {cycle_start.strftime('%H:%M:%S')} - {online_count}/{total_count} devices online")
                    last_summary_time = cycle_start
                
                self.monitor_all_devices()
                
                # Sleep for the remaining interval
                cycle_duration = (datetime.datetime.now() - cycle_start).total_seconds()
                sleep_time = max(0, self.ping_interval - cycle_duration)
                if sleep_time > 0:
                    time.sleep(sleep_time)
                
        except KeyboardInterrupt:
            print("\n\n🛑 Stopping monitor...")
            self.stop_monitoring()
    
    def stop_monitoring(self):
        """Stop the monitoring"""
        self.running = False
        
        print("📊 Final device status check...")
        # Log final status
        for ip_address in self.devices.keys():
            is_online = self.ping_device(ip_address)
            status = "ONLINE" if is_online else "OFFLINE"
            failed_count = self.failed_ping_count[ip_address]
            
            self.log_event(ip_address, "MONITOR_STOP", status, 0, failed_count, False, "Monitoring stopped")
            
            status_symbol = "✅" if is_online else "❌"
            print(f"{status_symbol} {ip_address} ({self.devices[ip_address]}) - {status}")
        
        print(f"\n✅ Monitoring stopped at {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📄 Log saved to: {self.csv_filename}")

# ============================================================================
# MAIN FUNCTION
# ============================================================================

def main():
    print("🌐 Network Ping Monitor - Standalone Deployment Version")
    print("=" * 60)
    print("Hardcoded configuration for server deployment")
    print(f"Monitoring {len(DEVICES)} devices with email alerts enabled")
    print()
    
    # Validate email configuration
    if EMAIL_ALERTS_ENABLED:
        if not EMAIL_FROM or not EMAIL_PASSWORD or not EMAIL_TO:
            print("⚠️  WARNING: Email alerts are enabled but email configuration is incomplete!")
            return
        else:
            print(f"📧 Email alerts configured for {len(EMAIL_TO)} recipients")
    
    print()
    
    # Create and start monitor
    monitor = PingMonitor(DEVICES, PING_INTERVAL, PING_TIMEOUT)
    monitor.start_monitoring()

# ============================================================================
# ENTRY POINT
# ============================================================================

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Fatal error: {e}")
        print(f"Traceback: {traceback.format_exc()}")
        input("Press Enter to exit...")
        sys.exit(1)