# Network Ping Monitor Configuration

# Device Configuration
# Format: IP_ADDRESS = "Description"
DEVICES = {
    "192.168.200.102": "200 Switch",
    "192.168.1.8": "Main Server",
    "192.168.200.4": "Building 121", 
    "192.168.200.5": "Building 200"
}

# Monitoring Settings
PING_INTERVAL = 1  # seconds between ping attempts (fast monitoring like continuous ping)
PING_TIMEOUT = 4   # ping timeout in seconds (matches Windows default -w 4000ms)

# Logging Settings
LOG_DIRECTORY = "logs"  # Directory to store log files (optional)
LOG_PERIODIC_STATUS = True  # Log periodic status checks for online devices
PERIODIC_LOG_INTERVAL = 3600  # seconds (1 hour)

# Email Alert Settings
EMAIL_ALERTS_ENABLED = True
EMAIL_ALERT_THRESHOLD = 3  # Number of consecutive failed pings before sending email alert

# SMTP Configuration - Update these with your email provider settings
SMTP_SERVER = "smtp.office365.com"  # Gmail SMTP server (change for other providers)
SMTP_PORT = 587  # TLS port (use 465 for SSL)
SMTP_USE_TLS = True  # Use TLS encryption

# Email Credentials - IMPORTANT: Use app-specific passwords for Gmail
EMAIL_FROM = "emailrelay@stlinc.com"  # Your email address
EMAIL_PASSWORD = "TuloNop1932!!*Mz"  # Your email password or app-specific password
EMAIL_TO = ["garretts@stlinc.com", "DevOps@stlinc.com"]  # List of recipients

# Email Content Settings
EMAIL_SUBJECT_PREFIX = "[NETWORK ALERT]"
SEND_RECOVERY_EMAILS = True  # Send email when device comes back online