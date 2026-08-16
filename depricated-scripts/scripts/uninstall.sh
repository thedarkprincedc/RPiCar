#!/bin/bash
set -e

sudo systemctl stop rpicar
sudo systemctl disable rpicar

sudo rm -f /etc/systemd/system/rpicar.service

sudo systemctl daemon-reload

echo "Service removed."