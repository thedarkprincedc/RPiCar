#!/bin/bash
set -e

echo "Building Python Executable"

pyinstaller \
    --clean \
    --onefile \
    --name rpicar \
    src/main.py

mkdir -p bin

cp dist/rpicar bin/

echo "Done"