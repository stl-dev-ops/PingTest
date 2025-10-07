#!/usr/bin/env python3
"""Smoke test: instantiate PingMonitor with localhost, write a log entry, and print the CSV head."""
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from ping_monitor import PingMonitor
import datetime

# Use localhost to ensure ping will succeed
devices = {'127.0.0.1': 'Localhost'}

monitor = PingMonitor(devices, ping_interval=1, timeout=2)
# Log a test event
monitor.log_event('127.0.0.1', 'SMOKE_TEST', 'ONLINE', 0.0, 0, False, 'Smoke test event')

print('CSV file:', monitor.csv_filename)
print('\nFirst 20 lines of the CSV file:')
with open(monitor.csv_filename, 'r', encoding='utf-8') as f:
    for i, line in enumerate(f):
        if i >= 20:
            break
        print(line.strip())
