Deployment checklist for Network Ping Monitor

1. Verify configuration
   - [ ] `config.py` contains correct device IPs and friendly names
   - [ ] SMTP credentials set and tested with `test_email.py`
   - [ ] `EMAIL_ALERT_THRESHOLD` set to desired value

2. Build and package (optional)
   - [ ] Activate venv
   - [ ] Install pyinstaller: `pip install pyinstaller`
   - [ ] Build exe: `pyinstaller --onefile --name "NetworkPingMonitor" --console ping_monitor_standalone.py`

3. Install auto-start (choose one)
   - Scheduled Task (recommended for Windows)
     - [ ] Edit `install_scheduled_task.ps1` with paths and run as Admin
     - [ ] Verify Scheduled Task concurrency set to "Do not start a new instance"
   - NSSM (for Windows Service behavior)
     - [ ] Download NSSM and use `nssm install` to wrap the exe
     - [ ] Configure service to restart on failure

4. Start and verify
   - [ ] Stop any running instances: `taskkill /F /IM NetworkPingMonitor.exe`
   - [ ] Start scheduled task or service
   - [ ] Check Task Manager for a single `NetworkPingMonitor.exe`
   - [ ] Verify that logs are being written to `logs/`
   - [ ] Simulate an outage to confirm email alerts

5. Monitoring
   - [ ] Set up simple alerting for unexpected exits (Scheduled Task/Service restart)
   - [ ] Rotate logs periodically (e.g., monthly archive)

6. Security
   - [ ] Move SMTP credentials to secure store if possible
   - [ ] Ensure `config.py` permissions restrict read access

