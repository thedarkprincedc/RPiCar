#!/bin/bash
set -e

source .env
ssh admin@$HOST_IP_OR_NAME "cd ~/RPiCar && python3 -m venv venv && source venv/bin/activate && pip install -r requirements.txt && python3 src/main-2.py"