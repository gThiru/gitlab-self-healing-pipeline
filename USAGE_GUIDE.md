
# 📘 GitLab Self-Healing CI/CD Pipeline — Advanced Usage Guide

This guide describes how to set up a resilient GitLab CI/CD system that:
- Tracks execution progress per pipeline
- Recovers from mid-stage failure
- Uses shared volumes and retry logic for reliability

## 🧱 Architecture Overview

Each pipeline writes a checkpoint file to:
```
/mnt/ci-state/pipelines/${CI_PIPELINE_ID}/.ci-progress.json
```

The watchdog script checks these files periodically to:
- Detect long-running or stuck stages
- Trigger a recovery pipeline with `RESUME_STAGE`
- Limit retries using `retry_count`
- Skip old `.ci-progress.json` files using `MAX_PIPELINE_AGE_MINUTES`

## 🔧 Components

### 1. `.gitlab-ci.yml`
Modular jobs using:
```yaml
rules:
  - if: '$RESUME_STAGE == "test" || $RESUME_STAGE == ""'
```
Each stage begins with:
```bash
source ./update_stage_status.sh
update_stage_status <stage> in_progress
...
update_stage_status <stage> done
```

### 2. `update_stage_status.sh`
Shell helper to write checkpoint JSON

### 3. `gitlab_pipeline_watchdog_resume_multi.py`
Python script that:
- Scans all pipeline directories
- Detects stuck jobs by `updated` timestamp
- Respects retry count and max pipeline age

### 4. `requirements.txt`
Install dependencies:
```bash
pip install -r requirements.txt
```

### 5. Linux & Kubernetes CronJob Support
- Run `run_watchdog.sh` via crontab (see `cronjob-linux-template.md`)
- Or deploy a Kubernetes CronJob (see `cronjob-template.md`)

---

## ✅ Best Practices

- Use per-pipeline folders for isolation
- Auto-clean up old progress files periodically
- Secure write access to the shared volume

---

You’re now fully equipped to automate and harden your CI/CD pipeline 🎯
