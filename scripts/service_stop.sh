#!/bin/bash
set -e

echo "Stopping RPiCar Service"

sudo systemctl stop rpicar

sudo systemctl disable rpicar

sudo systemctl restart rpicars

