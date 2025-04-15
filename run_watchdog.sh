#!/bin/bash
### It's a wrapper script for watchdog env var setup and running the watchdog script
### make sure this script is executable permission added
### Check the cron scheduler example in README file

#cd <Python watchdog script>
export $(grep -v '^#' .env | xargs)
python gitlab_pipeline_watchdog_resume_multi.py