
# Bash helper function for updating stage progress
update_stage_status() {
  local STAGE_NAME=$1
  local STATUS=$2
  local PIPELINE_DIR="/mnt/ci-state/pipelines/${CI_PIPELINE_ID}"
  mkdir -p "$PIPELINE_DIR"
  local PROGRESS_FILE="$PIPELINE_DIR/.ci-progress.json"

  if [ ! -f "$PROGRESS_FILE" ]; then
    echo '{"pipeline_id": '"${CI_PIPELINE_ID}"', "ref": "'"${CI_COMMIT_REF_NAME}"'", "stages": {}, "retry_count": 0}' > "$PROGRESS_FILE"
  fi

  jq '.stages["'"$STAGE_NAME"'"] = {"status": "'"$STATUS"'", "updated": "'"$(date -u +"%Y-%m-%dT%H:%M:%S")"'"}' "$PROGRESS_FILE" > "$PROGRESS_FILE.tmp" && mv "$PROGRESS_FILE.tmp" "$PROGRESS_FILE"
}
