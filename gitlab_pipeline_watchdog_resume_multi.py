
import os
import json
import time
import requests
from datetime import datetime, timedelta

# Constants
CI_STATE_ROOT = "/mnt/ci-state/pipelines"
TRIGGER_TOKEN = os.getenv("GITLAB_TRIGGER_TOKEN")
GITLAB_PROJECT_ID = os.getenv("GITLAB_PROJECT_ID")
PIPELINE_REF = os.getenv("GITLAB_REF", "main")
PIPELINE_URL = f"https://gitlab.com/api/v4/projects/{GITLAB_PROJECT_ID}/trigger/pipeline"
STUCK_THRESHOLD_MINUTES = int(os.getenv("STUCK_THRESHOLD_MINUTES", 10))
MAX_RETRY_COUNT = int(os.getenv("MAX_RETRY_COUNT", 2))
MAX_PIPELINE_AGE_MINUTES = int(os.getenv("MAX_PIPELINE_AGE_MINUTES", 60))

def load_json(path):
    try:
        with open(path, "r") as f:
            return json.load(f)
    except Exception:
        return None

def write_json(path, data):
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Failed to write JSON to {path}: {e}")

def file_is_recent(path):
    try:
        mtime = os.path.getmtime(path)
        return datetime.utcnow() - datetime.utcfromtimestamp(mtime) < timedelta(minutes=MAX_PIPELINE_AGE_MINUTES)
    except Exception:
        return False

def process_pipeline(pipeline_dir):
    progress_file = os.path.join(pipeline_dir, ".ci-progress.json")
    if not file_is_recent(progress_file):
        print(f"Skipping old pipeline state file: {pipeline_dir}")
        return

    data = load_json(progress_file)
    if not data or "stages" not in data:
        return

    retry_count = data.get("retry_count", 0)
    if retry_count >= MAX_RETRY_COUNT:
        print(f"Retry limit reached for pipeline {pipeline_dir}")
        return

    for stage, info in data["stages"].items():
        if info["status"] == "in_progress":
            last_updated = datetime.strptime(info["updated"], "%Y-%m-%dT%H:%M:%S")
            if datetime.utcnow() - last_updated > timedelta(minutes=STUCK_THRESHOLD_MINUTES):
                print(f"Pipeline {data['pipeline_id']} is stuck at stage {stage}")
                trigger_resume_pipeline(stage)
                data["retry_count"] = retry_count + 1
                write_json(progress_file, data)
                break

def trigger_resume_pipeline(stage_name):
    payload = {
        "token": TRIGGER_TOKEN,
        "ref": PIPELINE_REF,
        "variables[RESUME_STAGE]": stage_name
    }
    response = requests.post(PIPELINE_URL, data=payload)
    print("Triggered recovery pipeline:", response.status_code)

def main():
    for dir_entry in os.scandir(CI_STATE_ROOT):
        if dir_entry.is_dir():
            process_pipeline(dir_entry.path)

if __name__ == "__main__":
    main()
