#!/bin/bash
set -e

PI=admin@192.168.1.50
DEST=~/RPiCar

echo "Stopping service..."
ssh $PI "sudo systemctl stop rpicar"

echo "Syncing files..."
rsync -avz \
    --delete \
    --exclude=".git" \
    --exclude=".venv" \
    ./ $PI:$DEST

echo "Installing Python packages..."
ssh $PI "
cd $DEST &&
source .venv/bin/activate &&
pip install -r requirements.txt
"

echo "Starting service..."
ssh $PI "sudo systemctl start rpicar"

echo "Deployment complete."