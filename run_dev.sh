#!/bin/sh

VENV_DIR=".venv"

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

# Activate virtual environment
. $VENV_DIR/bin/activate

# Change to project directory and add it to PYTHONPATH
cd "$SCRIPT_DIR"
export PYTHONPATH="$SCRIPT_DIR:$PYTHONPATH"

# Run with dev settings
SETTINGS_MODULE=config.settings.dev gunicorn -c config/gunicorn.conf.py
