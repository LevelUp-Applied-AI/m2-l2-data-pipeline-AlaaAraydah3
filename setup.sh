#!/bin/bash
set -euo pipefail

echo "========================================"
echo "   Data Pipeline Environment Setup"
echo "========================================"

# --- [1/4] 
echo "[1/4] Creating virtual environment..."
python3 -m venv .venv

# --- [2/4]
echo "[2/4] Activating virtual environment..."
source .venv/Scripts/activate

# --- [3/4]
echo "[3/4] Upgrading pip..."
python.exe -m pip install --upgrade pip

# --- [4/4]
echo "[4/4] Installing requirements..."
pip install -r requirements.txt

echo "========================================"
echo "✅ Setup completed successfully!"
echo "========================================"
