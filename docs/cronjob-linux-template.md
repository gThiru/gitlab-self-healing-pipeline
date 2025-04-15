
# 🕒 Linux CronJob Template for GitLab Self-Healing Pipeline

This template guides you through setting up a Linux-based cron job to run the self-healing pipeline watchdog script on a schedule.

---

## 📁 Directory Structure (Recommended)

```
/opt/gitlab-watchdog/
├── .env
├── venv/
├── gitlab_pipeline_watchdog_resume_multi.py
├── requirements.txt
└── run_watchdog.sh
```

---

## ⚙️ Step-by-Step Setup

### 1. 🐍 Create a Python Virtual Environment

```bash
cd /opt/gitlab-watchdog
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

---

### 2. 📝 Create the `.env` File

```bash
cat <<EOF > .env
GITLAB_TRIGGER_TOKEN=your_token_here
GITLAB_PROJECT_ID=your_project_id
GITLAB_REF=main
STUCK_THRESHOLD_MINUTES=10
MAX_RETRY_COUNT=2
MAX_PIPELINE_AGE_MINUTES=60
EOF
```

---

### 3. 🖊️ Create `run_watchdog.sh`

```bash
#!/bin/bash
cd /opt/gitlab-watchdog
source venv/bin/activate
export $(grep -v '^#' .env | xargs)
python gitlab_pipeline_watchdog_resume_multi.py
```

Make it executable:
```bash
chmod +x run_watchdog.sh
```

---

### 4. 🗓️ Add to Crontab

```bash
crontab -e
```

Add this line to run every 10 minutes:
```cron
*/10 * * * * /opt/gitlab-watchdog/run_watchdog.sh >> /opt/gitlab-watchdog/watchdog.log 2>&1
```

---

✅ This setup will ensure your GitLab CI pipelines are continuously monitored and automatically resumed when necessary.

