Title: [Bug/Deployment] Brief summary of the problem

## Summary
A concise description of the problem or request. Describe what you expected to happen and what actually happened.

## Steps to Reproduce
1. Environment (Server/VM name or snapshot):
2. Checkout commit or file version (if known):
3. Run the monitor (how you started it: scheduled task / background / service / exe):
4. Exact command or actions to reproduce the issue:

## Observed Behavior
Describe the behavior you saw. Include exact console output, CSV log lines and timestamps if available.

## Expected Behavior
What did you expect to happen instead?

## Logs / Attachments
- Path to CSV log(s): `logs/ping_log_YYYYMMDD_HHMMSS.csv`
- Attach the smallest possible slice of the CSV that shows the problem (3-10 rows)
- Attach service/scheduled task setup screenshots or exported XML if relevant

## Environment
- OS: Windows Server (version):
- Python: (if running from source) e.g. Python 3.13
- Executable: `dist\NetworkPingMonitor.exe` (yes/no)
- How started: Scheduled Task / NSSM Service / background .bat / manual command

## Configuration
Include relevant snippet from `config.py` or `ping_monitor_standalone.py` (redact secrets if needed). Specifically list:
- Monitored devices (IPs + friendly names)
- Ping interval & timeout
- Email server & `EMAIL_TO` recipients (redact password)
- EMAIL_ALERT_THRESHOLD value

## Severity / Priority
- Impact: (Low/Medium/High/Critical)
- Frequency: (Always / Intermittent / Rare)

## Reproducible on another host?
- Have you tried running the same executable on a different machine? (yes/no)

## Suggested next steps / Acceptance Criteria
1. Stop duplicate processes and ensure single instance runs at boot.
2. If running as a Windows Service, verify NSSM is used or convert monitor to a native service.
3. Confirm no duplicate email alerts and correct CSV entries for outages longer than 3 consecutive pings.

---
Please include any other details that will help reproduce and diagnose the issue.
