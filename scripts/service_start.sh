#!/bin/bash
set -e

echo "Installing RPiCar Service"

sudo cp deploy/rpicar.service /etc/systemd/system/

sudo systemctl daemon-reload
sudo systemctl enable rpicar

echo "Done"