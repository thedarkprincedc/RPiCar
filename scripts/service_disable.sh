#!/bin/bash
set -e

echo "Disable RPiCar Service"
sudo systemctl disable rpicar

echo "Done"