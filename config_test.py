# Test Configuration for Ping Monitor
# This config includes a fake IP to test email alerts

# Device Configuration - includes one fake IP for testing
DEVICES = {
    "192.168.1.8": "Main Server",           # Real device (should work)
    "192.168.200.102": "200 Switch",        # Real device (should work) 
    "192.168.999.999": "Test Fake Device"   # Fake IP (will fail and trigger email)
}

# Monitoring Settings - faster for testing
PING_INTERVAL = 2  # 2 seconds between pings for faster testing
PING_TIMEOUT = 4   # 4 second timeout

# Logging Settings
LOG_DIRECTORY = "logs"
LOG_PERIODIC_STATUS = True
PERIODIC_LOG_INTERVAL = 3600

# Email Alert Settings
EMAIL_ALERTS_ENABLED = True
EMAIL_ALERT_THRESHOLD = 3  # Send email after 3 failed pings

# SMTP Configuration
SMTP_SERVER = "smtp.office365.com"
SMTP_PORT = 587
SMTP_USE_TLS = True

# Email Credentials
EMAIL_FROM = "emailrelay@stlinc.com"
EMAIL_PASSWORD = "TuloNop1932!!*Mz"
EMAIL_TO = ["garretts@stlinc.com", "DevOps@stlinc.com"]

# Email Content Settings
EMAIL_SUBJECT_PREFIX = "[NETWORK ALERT - TEST]"
SEND_RECOVERY_EMAILS = True