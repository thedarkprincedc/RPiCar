#!/bin/bash
set -e

echo "Stopping RPiCar..."
sudo systemctl stop rpicar || true

echo "Disabling RPiCar..."
sudo systemctl disable rpicar || true

echo "Removing systemd service..."
sudo rm -f /etc/systemd/system/rpicar.service

sudo systemctl daemon-reload
sudo systemctl reset-failed

echo "RPiCar service removed."