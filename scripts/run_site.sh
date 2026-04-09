#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
APP_MODULE="app.main:app"
PID_FILE="${DALIFIN_PID_FILE:-$ROOT_DIR/.run/dalifin_company.pid}"
LOG_FILE="${DALIFIN_LOG_FILE:-/tmp/dalifin_company.out}"
ERR_FILE="${DALIFIN_ERR_FILE:-/tmp/dalifin_company.err}"
HOST="${DALIFIN_HOST:-127.0.0.1}"
PORT="${DALIFIN_PORT:-5104}"
ENV_FILE=""

usage() {
  cat <<EOF
Usage:
  ./scripts/run_site.sh <start|stop|restart|status> [--env-file path] [--host 127.0.0.1] [--port 5104]
EOF
}

load_env_file() {
  if [[ -n "$ENV_FILE" ]]; then
    set -a
    # shellcheck disable=SC1090
    source "$ENV_FILE"
    set +a
  fi
}

ensure_runtime_dirs() {
  mkdir -p "$(dirname "$PID_FILE")"
  mkdir -p "$(dirname "$LOG_FILE")"
  mkdir -p "$(dirname "$ERR_FILE")"
}

is_running() {
  if [[ -f "$PID_FILE" ]]; then
    local pid
    pid="$(cat "$PID_FILE")"
    if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
      return 0
    fi
  fi
  return 1
}

start_site() {
  load_env_file
  ensure_runtime_dirs
  if is_running; then
    echo "dalifin_company already running with pid $(cat "$PID_FILE")"
    return 0
  fi
  cd "$ROOT_DIR"
  nohup python -m uvicorn "$APP_MODULE" --host "$HOST" --port "$PORT" >"$LOG_FILE" 2>"$ERR_FILE" < /dev/null &
  echo "$!" > "$PID_FILE"
  echo "started dalifin_company on $HOST:$PORT pid $(cat "$PID_FILE")"
}

stop_site() {
  if ! [[ -f "$PID_FILE" ]]; then
    echo "dalifin_company not running"
    return 0
  fi
  local pid
  pid="$(cat "$PID_FILE")"
  if [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null; then
    kill "$pid"
    sleep 2
    if kill -0 "$pid" 2>/dev/null; then
      kill -9 "$pid" || true
    fi
  fi
  rm -f "$PID_FILE"
  echo "stopped dalifin_company"
}

status_site() {
  if is_running; then
    echo "dalifin_company running with pid $(cat "$PID_FILE")"
  else
    echo "dalifin_company not running"
    return 1
  fi
}

COMMAND="${1:-}"
shift || true

while [[ $# -gt 0 ]]; do
  case "$1" in
    --env-file)
      ENV_FILE="$2"
      shift 2
      ;;
    --host)
      HOST="$2"
      shift 2
      ;;
    --port)
      PORT="$2"
      shift 2
      ;;
    *)
      echo "unknown argument: $1" >&2
      usage
      exit 2
      ;;
  esac
done

case "$COMMAND" in
  start)
    start_site
    ;;
  stop)
    stop_site
    ;;
  restart)
    stop_site
    start_site
    ;;
  status)
    status_site
    ;;
  *)
    usage
    exit 2
    ;;
esac
