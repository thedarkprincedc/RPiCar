#!/bin/bash
set -e

source .env

ssh $RPI_USER@$RPI_HOST \
    "cd ~/RPiCar && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python3 src/main.py"