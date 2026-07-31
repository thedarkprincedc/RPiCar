#!/bin/bash
set -e

echo "Installing Python Dependencies"

sudo apt update

sudo apt install -y \
    python3-dev \
    build-essential \
    gcc

echo "Done"