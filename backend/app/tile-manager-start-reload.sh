#! /usr/bin/env sh
set -e

HOST=${HOST:-0.0.0.0}
PORT=${PORT:-9999}
LOG_LEVEL=${LOG_LEVEL:-info}

# Let the DB start
python /app/app/tile_manager_pre_start.py

# Start Uvicorn with live reload
exec uvicorn --reload --host $HOST --port $PORT --log-level $LOG_LEVEL "app.tile_manager:app"