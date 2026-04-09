#!/usr/bin/env bash
set -Eeuo pipefail

RUN_TESTS=1
STAGE_ONLY=0
BUILD_DIR="build"
DIST_DIR="dist"
APP_NAME="dalifin_company.py"
OUTPUT_NAME="dalifin_company"
BUILD_INFO_PATH="./dist/build_info.json"
TEST_BIN_DIR="/data/dali/test/bin"
PROD_BIN_DIR="/data/dali/prod/bin"

log() { printf '[INFO]  %s\n' "$*"; }
err() { printf '[ERROR] %s\n' "$*" >&2; }

usage() {
  cat <<EOF
Usage: $0 [--skip-tests] [--stage-only]

Builds the dalifin_company PyInstaller binary and installs it into:
  $TEST_BIN_DIR
  $PROD_BIN_DIR

Options:
  --skip-tests  Skip pytest before building
  --stage-only  Refresh only $TEST_BIN_DIR
EOF
}

while [[ $# -gt 0 ]]; do
  case "$1" in
    --skip-tests)
      RUN_TESTS=0
      shift
      ;;
    --stage-only)
      STAGE_ONLY=1
      shift
      ;;
    --help|-h)
      usage
      exit 0
      ;;
    *)
      err "Unknown argument: $1"
      usage >&2
      exit 2
      ;;
  esac
done

install_with_backup() {
  local source_file="$1"
  local target_file="$2"
  local mode="$3"
  local timestamp
  local backup_file
  local tmp_file

  timestamp="$(date +%Y%m%d_%H%M%S)"
  backup_file="${target_file}.bak.${timestamp}"
  tmp_file="$(dirname "$target_file")/.tmp.$(basename "$target_file").${timestamp}"

  mkdir -p "$(dirname "$target_file")"
  install -m "$mode" "$source_file" "$tmp_file"

  if [[ -f "$target_file" ]]; then
    log "Backing up $(basename "$target_file") -> $(basename "$backup_file")"
    mv -f "$target_file" "$backup_file"
  fi

  mv -f "$tmp_file" "$target_file"
}

SCRIPT_DIR="$(dirname "$(readlink -f "$0")")"
cd "$SCRIPT_DIR" || { err "Failed to change directory to $SCRIPT_DIR"; exit 1; }

if [[ -x "./.venv/bin/python" ]]; then
  PYTHON="./.venv/bin/python"
elif [[ -x "./venv/bin/python" ]]; then
  PYTHON="./venv/bin/python"
else
  err "Virtualenv Python not found at ./.venv/bin/python or ./venv/bin/python"
  exit 1
fi

log "Using Python: $PYTHON"

log "Refreshing dependencies"
"$PYTHON" -m pip install -r requirements.txt
"$PYTHON" -m pip install pyinstaller

if [[ "$RUN_TESTS" -eq 1 ]]; then
  log "Running pytest"
  "$PYTHON" -m pytest
fi

log "Cleaning previous build artifacts"
rm -rf "$BUILD_DIR" "$DIST_DIR"
rm -f ./*.spec

log "Building $OUTPUT_NAME with PyInstaller"
"$PYTHON" -m PyInstaller --onefile "$APP_NAME" --clean \
  --name "$OUTPUT_NAME" \
  --add-data "app/templates:app/templates" \
  --add-data "app/static:app/static" \
  --collect-all jinja2 \
  --collect-all fastapi \
  --collect-all starlette \
  --collect-all uvicorn

log "Writing build metadata"
cat > "$BUILD_INFO_PATH" <<EOF
{
  "service": "dalifin_company",
  "git_commit": "$(git rev-parse HEAD 2>/dev/null || echo unknown)",
  "git_branch": "$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo unknown)",
  "build_time_utc": "$(date -u +"%Y-%m-%dT%H:%M:%SZ")",
  "artifact_name": "$OUTPUT_NAME",
  "artifact_path": "$PROD_BIN_DIR/$OUTPUT_NAME"
}
EOF

log "Installing staged artifacts into $TEST_BIN_DIR"
mkdir -p "$TEST_BIN_DIR"
install -m 0755 "./dist/$OUTPUT_NAME" "$TEST_BIN_DIR/$OUTPUT_NAME"
install -m 0644 "./dist/build_info.json" "$TEST_BIN_DIR/build_info.json"

if [[ "$STAGE_ONLY" -eq 1 ]]; then
  log "Stage-only mode enabled. Skipping production install."
  exit 0
fi

log "Installing artifacts atomically into $PROD_BIN_DIR"
install_with_backup "./dist/$OUTPUT_NAME" "$PROD_BIN_DIR/$OUTPUT_NAME" 0755
install_with_backup "./dist/build_info.json" "$PROD_BIN_DIR/build_info.json" 0644

log "Deployment complete"
