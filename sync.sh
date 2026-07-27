#!bin/bash
set -e

source .env

echo "Deploying to $HOST_IP_OR_NAME..."

scp -r * \
    admin@$HOST_IP_OR_NAME:/home/admin/RPiCar

ssh admin@$HOST_IP_OR_NAME <<'EOF'
cd /home/admin/RPiCar
sudo ./scripts/setup_dualsense.sh
EOF