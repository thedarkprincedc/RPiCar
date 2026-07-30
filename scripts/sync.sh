#!bin/bash
set -e

echo "Sync to $RPI_HOST..."

#scp -r * $RPI_USER@$RPI_HOST:$PROJECT_DIR
#scp -r * $RPI_USER@10.1.20.235:$PROJECT_DIR

rsync -av --delete \
  --exclude '__pycache__/' \
  --exclude '*.pyc' \
  --exclude '.venv/' \
  --exclude 'venv/' \
  --exclude '.git/' \
  ./ $RPI_USER@$RPI_HOST:$PROJECT_DIR

ssh $RPI_USER@$RPI_HOST <<'EOF'
cd $PROJECT_DIR
sudo ./scripts/setup_dualsense.sh
EOF