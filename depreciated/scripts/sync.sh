#!bin/bash
set -e

echo "Sync to $RPI_HOST..."
scp -r * $RPI_USER@$RPI_HOST:$RPI_DIR

echo "Setup DualSense"
ssh $RPI_USER@$RPI_HOST <<'EOF'
cd $RPI_DIR
sudo ./scripts/setup_dualsense.sh
EOF

echo "Done."