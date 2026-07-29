#!bin/bash
set -e

source .env

echo "Deploying to $HOST_IP_OR_NAME..."

#scp -r * admin@magaman:/home/admin/RPiCar
#scp -r * admin@10.1.20.235:/home/admin/RPiCar

rsync -av --delete \
  --exclude '__pycache__/' \
  --exclude '*.pyc' \
  --exclude '.venv/' \
  --exclude 'venv/' \
  --exclude '.git/' \
  ./ admin@magaman:/home/admin/RPiCar/

ssh admin@magaman <<'EOF'
cd /home/admin/RPiCar
sudo ./scripts/setup_dualsense.sh
EOF