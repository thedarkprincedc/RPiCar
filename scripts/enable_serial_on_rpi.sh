#!/bin/bash
set -e

CONFIG="/boot/firmware/config.txt"

echo "Configuring Raspberry Pi UART..."

if grep -q '^enable_uart=' "$CONFIG"; then
    sudo sed -i 's/^enable_uart=.*/enable_uart=1/' "$CONFIG"
else
    echo 'enable_uart=1' | sudo tee -a "$CONFIG" >/dev/null
fi

echo "UART configuration:"
grep '^enable_uart=' "$CONFIG"

echo
echo "Rebooting..."
sudo reboot