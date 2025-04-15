# ⏱️ GitLab CI Watchdog CronJob Template

This file describes a sample Kubernetes CronJob for running the `gitlab_pipeline_watchdog_resume_multi.py` script to monitor and resume pipelines.

---

## 🛠️ Requirements

- Python 3.9+ Docker image
- Access to shared persistent volume (e.g., EFS, NFS)
- GitLab project trigger token
- Secrets stored in Kubernetes

---

## 🧩 Sample Kubernetes CronJob YAML

```yaml
apiVersion: batch/v1
kind: CronJob
metadata:
  name: ci-watchdog-cron
spec:
  schedule: "*/10 * * * *"  # Every 10 minutes
  jobTemplate:
    spec:
      template:
        spec:
          containers:
          - name: watchdog
            image: python:3.9
            command: ["python", "/mnt/scripts/gitlab_pipeline_watchdog_resume_multi.py"]
            volumeMounts:
            - name: ci-state
              mountPath: /mnt/ci-state
            env:
              - name: GITLAB_TRIGGER_TOKEN
                valueFrom:
                  secretKeyRef:
                    name: ci-watchdog-secrets
                    key: trigger_token
              - name: GITLAB_PROJECT_ID
                value: "123456"
              - name: GITLAB_REF
                value: "main"
              - name: STUCK_THRESHOLD_MINUTES
                value: "10"
              - name: MAX_RETRY_COUNT
                value: "2"
              - name: MAX_PIPELINE_AGE_MINUTES
                value: "60"
          restartPolicy: OnFailure
          volumes:
          - name: ci-state
            persistentVolumeClaim:
              claimName: ci-state-pvc