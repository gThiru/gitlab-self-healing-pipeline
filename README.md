
# 🛠️ GitLab Self-Healing Pipeline

A resilient, self-healing CI/CD pipeline system for GitLab that:
- Detects pipeline stage failures
- Tracks pipeline progress per pipeline ID
- Automatically resumes execution from the last successful stage
- Limits retries to prevent infinite loops

## 📦 Features

- ✅ Modular `.gitlab-ci.yml` with `RESUME_STAGE` logic
- ✅ Watchdog script to monitor `.ci-progress.json` for stuck stages
- ✅ Per-pipeline checkpoint file tracking via `CI_PIPELINE_ID`
- ✅ Retry limit enforcement
- ✅ Bash helper function for stage progress updates
- ✅ Shared volume (e.g. NFS, EFS) for runner coordination
- ✅ Linux and Kubernetes CronJob automation support

## 📁 File Structure

```
.
├── .gitlab-ci.yml
├── gitlab_pipeline_watchdog_resume_multi.py
├── update_stage_status.sh
├── requirements.txt
├── .env.example
├── LICENSE
├── README.md
├── USAGE_GUIDE.md
└── docs/
    ├── architecture.png
    ├── cronjob-template.md
    ├── cronjob-linux-template.md
    └── examples/
        └── sample-ci-progress.json
```

## 🚀 Quick Start

1. Mount a shared directory across all GitLab runners:
   - e.g., `/mnt/ci-state/pipelines/{CI_PIPELINE_ID}`

2. Add `update_stage_status.sh` to your pipeline and call it in each job:
   ```bash
   update_stage_status test in_progress
   update_stage_status test done
   ```

3. Run the watchdog script using:
   - A Linux CronJob (see `docs/cronjob-linux-template.md`)
   - A Kubernetes CronJob (see `docs/cronjob-template.md`)

4. Watchdog monitors per-pipeline JSON and auto-resumes from last known stage, with retry limit protection and pipeline age validation.

---

© 2025 — Thirunavukkarasu Ganesan | DevOps Manager / Architect
