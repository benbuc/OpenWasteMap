#! /usr/bin/env sh
set -e

HOST=${HOST:-0.0.0.0}
PORT=${PORT:-80}

# Let the DB start
python /app/app/tile_manager_pre_start.py

# Start Uvicorn
exec uvicorn --proxy-headers --host $HOST --port $PORT "app.tile_manager:app"