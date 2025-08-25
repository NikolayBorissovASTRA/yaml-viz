#!/bin/bash

echo "Starting Dynamic YAML Form Generator (pip version)..."

# Check Python version
if ! python3 -c "import sys; exit(0 if sys.version_info >= (3, 10) else 1)" 2>/dev/null; then
    echo "Python 3.10+ required"
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Start Streamlit app
echo "Starting Streamlit application..."
echo "Access the app at: http://localhost:8501"
echo "Press Ctrl+C to stop"

python -m streamlit run src/app.py