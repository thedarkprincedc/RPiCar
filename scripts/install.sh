#!/bin/bash
set -e

APP_DIR="$HOME/RPiCar"

echo "Updating packages..."
sudo apt update
sudo apt install -y \
    python3 \
    python3-venv \
    python3-pip \
    git

echo "Creating virtual environment..."
cd "$APP_DIR"

python3 -m venv .venv

source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt

echo "Installing systemd service..."
sudo cp systemd/rpicar.service /etc/systemd/system/

sudo systemctl daemon-reload
sudo systemctl enable rpicar

echo "Starting service..."
sudo systemctl restart rpicar

echo "Installation complete."