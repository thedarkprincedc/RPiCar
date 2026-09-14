#!/bin/bash
set -e

echo "Restarting RPiCar..."
sudo systemctl restart rpicar

echo "Done."