#!/bin/bash
set -euo pipefail

RPI_HOST="${RPI_HOST:-raspberrypi}"
RPI_USER="${RPI_USER:-admin}"
RPI_PATH="${RPI_PATH:-/home/admin/RPiCar}"

echo "==> Synchronizing Project..."
scp -r * ${RPI_USER}@${RPI_USER}:${RPI_PATH}

echo
echo "==> Syncronizing Complete."
echo