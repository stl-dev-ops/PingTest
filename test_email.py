#!/usr/bin/env python3
"""
Email Test Script for Ping Monitor
Tests email functionality by simulating device failures
"""

import datetime
import smtplib
from email.message import EmailMessage
from config import *

def test_email_connection():
    """Test basic email connection and authentication"""
    print("🧪 Testing Email Connection...")
    print(f"📧 SMTP Server: {SMTP_SERVER}:{SMTP_PORT}")
    print(f"📬 From: {EMAIL_FROM}")
    print(f"📨 To: {', '.join(EMAIL_TO)}")
    print()
    
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            if SMTP_USE_TLS:
                print("🔒 Starting TLS encryption...")
                server.starttls()
            
            print("🔑 Authenticating...")
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            
            print("✅ Email connection successful!")
            return True
            
    except Exception as e:
        print(f"❌ Email connection failed: {e}")
        return False

def send_test_alert():
    """Send a test outage alert email"""
    print("\n📧 Sending test outage alert...")
    
    try:
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Create test message
        msg = EmailMessage()
        msg['From'] = EMAIL_FROM
        msg['To'] = ', '.join(EMAIL_TO)
        msg['Subject'] = f"{EMAIL_SUBJECT_PREFIX} TEST ALERT - Ping Monitor Test"
        
        body = f"""TEST NETWORK DEVICE OUTAGE ALERT

This is a test message from the Network Ping Monitor.

Device: Test Device
IP Address: 192.168.999.999 (fake IP for testing)
Alert Time: {timestamp}
Failed Ping Count: 3
Threshold: 3 failed pings

This is a test to verify that email alerts are working correctly.
If you receive this message, the email relay is functioning properly.

This test alert was generated automatically by the Network Ping Monitor test script.
"""
        
        msg.set_content(body)
        
        # Send email
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            if SMTP_USE_TLS:
                server.starttls()
            server.login(EMAIL_FROM, EMAIL_PASSWORD)
            server.send_message(msg)
        
        print("✅ Test alert email sent successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Failed to send test alert: {e}")
        return False

def main():
    print("🔧 Network Ping Monitor - Email Test")
    print("=" * 50)
    
    if not EMAIL_ALERTS_ENABLED:
        print("❌ Email alerts are disabled in config.py")
        print("Set EMAIL_ALERTS_ENABLED = True to test email functionality")
        return
    
    # Test 1: Connection
    if not test_email_connection():
        print("\n💡 Email connection troubleshooting:")
        print("   1. Check SMTP server and port settings")
        print("   2. Verify email credentials")
        print("   3. For Office365: ensure 'Modern Authentication' is enabled")
        print("   4. Check firewall settings for SMTP ports")
        return
    
    # Test 2: Send test alert
    if send_test_alert():
        print(f"\n✅ Email test completed successfully!")
        print(f"📬 Check your inbox at: {', '.join(EMAIL_TO)}")
        print("🕐 The test email should arrive within a few minutes")
    else:
        print("\n❌ Email test failed")
        
    print("\n🚀 If email test passed, you can now run: python ping_monitor.py")

if __name__ == "__main__":
    main()