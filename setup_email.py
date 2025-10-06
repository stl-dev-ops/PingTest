#!/usr/bin/env python3
"""
Email Configuration Setup Helper
Helps configure email settings for the ping monitor
"""

import os
import sys

def setup_email_config():
    """Interactive email configuration setup"""
    print("🔧 Email Configuration Setup")
    print("=" * 40)
    print()
    
    print("This will help you configure email alerts for the ping monitor.")
    print("You can edit these settings later in config.py")
    print()
    
    # Get email provider choice
    print("📧 Email Provider:")
    print("1. Gmail")
    print("2. Outlook/Hotmail")
    print("3. Yahoo")
    print("4. Custom SMTP")
    
    choice = input("\nSelect your email provider (1-4): ").strip()
    
    smtp_configs = {
        "1": ("smtp.gmail.com", 587, True),
        "2": ("smtp-mail.outlook.com", 587, True), 
        "3": ("smtp.mail.yahoo.com", 587, True),
        "4": (None, None, None)
    }
    
    if choice in smtp_configs:
        smtp_server, smtp_port, use_tls = smtp_configs[choice]
        
        if choice == "4":
            smtp_server = input("Enter SMTP server: ").strip()
            smtp_port = int(input("Enter SMTP port (usually 587 or 465): ").strip())
            use_tls_input = input("Use TLS? (y/n): ").strip().lower()
            use_tls = use_tls_input in ['y', 'yes', 'true']
    else:
        print("Invalid choice. Using Gmail defaults.")
        smtp_server, smtp_port, use_tls = smtp_configs["1"]
    
    # Get email credentials
    print(f"\n📬 Email Account Setup for {smtp_server}")
    print("Note: For Gmail, you need to use an 'App Password', not your regular password.")
    print("See: https://support.google.com/accounts/answer/185833")
    print()
    
    email_from = input("Enter your email address: ").strip()
    email_password = input("Enter your email password (or app password): ").strip()
    
    # Get recipients
    print("\n📨 Alert Recipients")
    print("Enter email addresses that should receive alerts (one per line).")
    print("Press Enter on empty line when done:")
    
    recipients = []
    while True:
        recipient = input("Recipient email: ").strip()
        if not recipient:
            break
        recipients.append(recipient)
    
    if not recipients:
        recipients = [email_from]  # Default to sender
    
    # Generate config file content
    config_content = f'''# Network Ping Monitor Configuration

# Device Configuration
# Format: IP_ADDRESS = "Description"
DEVICES = {{
    "192.168.200.102": "200 Switch",
    "192.168.1.8": "Main Server",
    "192.168.200.4": "Building 121", 
    "192.168.200.5": "Building 200"
}}

# Monitoring Settings
PING_INTERVAL = 30  # seconds between ping attempts
PING_TIMEOUT = 5    # ping timeout in seconds

# Logging Settings
LOG_DIRECTORY = "logs"  # Directory to store log files (optional)
LOG_PERIODIC_STATUS = True  # Log periodic status checks for online devices
PERIODIC_LOG_INTERVAL = 3600  # seconds (1 hour)

# Email Alert Settings
EMAIL_ALERTS_ENABLED = True
EMAIL_ALERT_THRESHOLD = 3  # Number of consecutive failed pings before sending email alert

# SMTP Configuration
SMTP_SERVER = "{smtp_server}"
SMTP_PORT = {smtp_port}
SMTP_USE_TLS = {use_tls}

# Email Credentials
EMAIL_FROM = "{email_from}"
EMAIL_PASSWORD = "{email_password}"
EMAIL_TO = {recipients}

# Email Content Settings
EMAIL_SUBJECT_PREFIX = "[NETWORK ALERT]"
SEND_RECOVERY_EMAILS = True  # Send email when device comes back online
'''
    
    # Write to config file
    with open('config.py', 'w') as f:
        f.write(config_content)
    
    print("\n✅ Email configuration saved to config.py")
    print("\n📋 Configuration Summary:")
    print(f"   SMTP Server: {smtp_server}:{smtp_port}")
    print(f"   From Email: {email_from}")
    print(f"   Recipients: {', '.join(recipients)}")
    print(f"   Alert Threshold: 3 failed pings")
    print(f"   Recovery Emails: Enabled")
    print()
    print("🔒 Security Note:")
    print("   Your email password is stored in plain text in config.py")
    print("   Make sure to protect this file and use app-specific passwords when possible.")
    print()
    print("▶️  You can now run: python ping_monitor.py")

if __name__ == "__main__":
    setup_email_config()