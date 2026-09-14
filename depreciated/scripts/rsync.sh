#!bin/bash
set -e

echo "Sync to $RPI_HOST..."
rsync -av --delete \
  --exclude '__pycache__/' \
  --exclude '*.pyc' \
  --exclude '.venv/' \
  --exclude 'venv/' \
  --exclude '.git/' \
  ./ $RPI_USER@$RPI_HOST:$RPI_DIR

echo "Setup DualSense"
ssh $RPI_USER@$RPI_HOST <<'EOF'
cd $RPI_DIR
sudo ./scripts/setup_dualsense.sh
EOF

echo "Done"