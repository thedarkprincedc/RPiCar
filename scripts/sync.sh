#!/bin/bash
set -euo pipefail

RPI_HOST="${RPI_HOST:-raspberrypi}"
RPI_USER="${RPI_USER:-admin}"
RPI_PATH="${RPI_PATH:-/home/admin/RPiCar}"

echo "==> Synchronizing Project..."
rsync -avz \
  --exclude '.git/' \
  --exclude 'venv/' \
  --exclude '__pycache__/' \
  --exclude 'logs/' \
  --exclude '.env' \
  --exclude '.pytest_cache/' \
  --exclude '.mypy_cache/' \
  --exclude '.idea/' \
  --exclude '.vscode/' \
  ./ "${RPI_USER}@${RPI_HOST}:${RPI_PATH}/"

echo
echo "==> Syncronizing Complete."
echo