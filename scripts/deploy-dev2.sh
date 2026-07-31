#!/bin/bash
set -e

PI=admin@magaman
DEST=/home/admin/RPiCar

echo "Syncing project..."

scp -r * $PI:$DEST

echo "Done."