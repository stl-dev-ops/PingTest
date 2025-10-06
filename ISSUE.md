Title: Ping monitor produced duplicate instances and duplicate alerts

## Summary
When deploying the packaged `NetworkPingMonitor.exe` on Server-X, two instances of the monitor were running simultaneously (one started by a background .bat and another by a Scheduled Task). This resulted in duplicate email alerts and duplicate CSV log entries.

## Steps to Reproduce
1. Place `dist\NetworkPingMonitor.exe` on the server.
2. Start it once via `start_background.bat` and also create a Scheduled Task that runs the exe at startup.
3. Reboot or start both; observe two `NetworkPingMonitor.exe` processes in Task Manager.

## Observed Behavior
- Two processes run concurrently.
- Duplicate email alerts were sent for the same outage events.
- CSV logs contain duplicate entries.

## Expected Behavior
Only a single instance should run. Duplicate processes should not be allowed.

## Logs
- Example CSV logs: `logs/ping_log_20251006_151404.csv` (attach a small excerpt showing duplicate rows)

## Environment
- OS: Windows Server (version)
- Executable: `dist\NetworkPingMonitor.exe`
- Start method(s) used: background .bat and Scheduled Task

## Suggested Fix
1. Stop all running `NetworkPingMonitor.exe` processes: `taskkill /F /IM NetworkPingMonitor.exe`.
2. Choose a single start method. Recommended: Scheduled Task with "Do not start a new instance" concurrency setting.
3. If you need a true Windows Service, install NSSM and use it to wrap the exe.
4. Update deployment docs to recommend single start method and add a PID lockfile or singleton-check in the monitor to prevent duplicates.

## Acceptance Criteria
- Only one instance starts on reboot/start.
- No duplicate email alerts for the same event.
- CSV log entries are unique per event.
