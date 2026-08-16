#!/bin/bash
set -e

PI=admin@magaman
PROJECT_DIR=/home/admin/RPiCar

echo "==> Synchronizing Project..."
scp -r * $PI:$PROJECT_DIR

echo
echo "==> Syncronizing Complete."
echo