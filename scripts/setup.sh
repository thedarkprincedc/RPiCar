#!/bin/bash
set -euo pipefail

PROJECT_DIR="/home/admin/RPiCar"
#VENV="$PROJECT_DIR/.venv"
VENV="$PROJECT_DIR/venv"
SERVICE="rpicar"
SERVICE_FILE="$PROJECT_DIR/scripts/rpicar.service"
SYSTEMD_FILE="/etc/systemd/system/$SERVICE.service"

echo "==> Setting up RPiCar"

# --------------------------------------------------
# 1. Check prerequisites
# --------------------------------------------------

if ! command -v python3 >/dev/null 2>&1; then
    echo "ERROR: python3 is not installed"
    exit 1
fi

if ! command -v systemctl >/dev/null 2>&1; then
    echo "ERROR: systemd is not available"
    exit 1
fi

if [ ! -d "$PROJECT_DIR" ]; then
    echo "ERROR: Project directory does not exist:"
    echo "       $PROJECT_DIR"
    exit 1
fi

cd "$PROJECT_DIR"

# --------------------------------------------------
# 2. Create virtual environment if necessary
# --------------------------------------------------

if [ ! -d "$VENV" ]; then
    echo "==> Creating virtual environment"
    python3 -m venv "$VENV"
else
    echo "==> Virtual environment already exists"
fi

# --------------------------------------------------
# 3. Install/update Python package
# --------------------------------------------------

echo "==> Installing RPiCar"

"$VENV/bin/python" -m pip install --upgrade pip
"$VENV/bin/python" -m pip install .

# --------------------------------------------------
# 4. Install systemd service
# --------------------------------------------------

if [ ! -f "$SERVICE_FILE" ]; then
    echo "ERROR: Service file not found:"
    echo "       $SERVICE_FILE"
    exit 1
fi

echo "==> Installing systemd service"

sudo cp "$SERVICE_FILE" "$SYSTEMD_FILE"

# --------------------------------------------------
# 5. Reload systemd
# --------------------------------------------------

echo "==> Reloading systemd"

sudo systemctl daemon-reload

# --------------------------------------------------
# 6. Enable service at boot
# --------------------------------------------------

echo "==> Enabling $SERVICE"

sudo systemctl enable "$SERVICE"

# --------------------------------------------------
# 7. Start/restart service
# --------------------------------------------------

if sudo systemctl is-active --quiet "$SERVICE"; then
    echo "==> Restarting $SERVICE"
    sudo systemctl restart "$SERVICE"
else
    echo "==> Starting $SERVICE"
    sudo systemctl start "$SERVICE"
fi

# --------------------------------------------------
# 8. Show status
# --------------------------------------------------

echo
echo "==> RPiCar setup complete"
echo

sudo systemctl --no-pager --full status "$SERVICE"