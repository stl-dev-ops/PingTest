#!/usr/bin/env python3
"""Fix existing CSV logs by adding headers if missing.
Backs up original files to .bak before modifying.
"""
import os
import csv
import shutil

LOG_DIR = os.path.join(os.path.dirname(__file__), '..', 'logs')
HEADER = [
    'Timestamp',
    'IP Address',
    'Device Name',
    'Event Type',
    'Status',
    'Duration (minutes)',
    'Failed Ping Count',
    'Email Sent',
    'Notes'
]


def file_has_header(path):
    try:
        with open(path, 'r', encoding='utf-8') as f:
            first = f.readline()
            # crude heuristic: check if first line contains Timestamp and IP Address
            return 'Timestamp' in first and 'IP Address' in first
    except Exception:
        return False


def fix_file(path):
    bak = path + '.bak'
    print(f"Fixing {path} -> backup {bak}")
    shutil.copy2(path, bak)

    # Read original contents
    with open(bak, 'r', encoding='utf-8') as f:
        contents = f.read()

    # Write header + original contents
    with open(path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(HEADER)
        f.write(contents)


if __name__ == '__main__':
    if not os.path.isdir(LOG_DIR):
        print(f"Log directory does not exist: {LOG_DIR}")
        raise SystemExit(1)

    files = [f for f in os.listdir(LOG_DIR) if f.lower().endswith('.csv')]
    if not files:
        print("No CSV files found in logs directory")
        raise SystemExit(0)

    for f in files:
        path = os.path.join(LOG_DIR, f)
        if not file_has_header(path):
            fix_file(path)
        else:
            print(f"OK: {path} already has a header")

    print("Done.")
