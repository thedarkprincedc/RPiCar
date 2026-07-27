#!/bin/bash

set -e

echo "Setting up DualSense permissions..."

RULE_FILE="/etc/udev/rules.d/99-dualsense.rules"

sudo bash -c "cat > $RULE_FILE" <<'EOF'
# Sony DualSense controller
KERNEL=="hidraw*", SUBSYSTEM=="hidraw", MODE="0666"
EOF

echo "Reloading udev rules..."

sudo udevadm control --reload-rules
sudo udevadm trigger

echo "DualSense udev rule installed."

# Fix currently connected controller if it exists
if ls /dev/hidraw* >/dev/null 2>&1; then
    echo "Updating existing hidraw devices..."
    sudo chmod 666 /dev/hidraw*
fi

echo "Done."