#!/bin/bash
set -e

PI=admin@192.168.1.50
DEST=~/RPiCar

echo "Syncing project..."

rsync -az --delete \
    --exclude ".git" \
    --exclude ".venv" \
    --exclude "venv" \
    --exclude "__pycache__" \
    --exclude "*.pyc" \
    ./ "$PI:$DEST"

echo "Done."