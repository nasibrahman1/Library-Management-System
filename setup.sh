#!/bin/bash

# Check operating system (optional - comment out if not needed)
#os_type=$(uname -s)

# Check if virtualenv is installed
if ! command -v virtualenv >/dev/null 2>&1; then
  echo "Error: virtualenv is not installed. Please install it first."
  exit 1
fi

# Create virtual environment
python3 -m venv flaskenv

# Activate the virtual environment
source flaskenv/bin/activate

# Check if requirements.txt exists
if [ ! -f requirements.txt ]; then
  echo "Error: requirements.txt not found. Please create it with your project dependencies."
  exit 1
fi

# Install libraries from requirements.txt
pip install -r requirements.txt

echo "Virtual environment 'flaskenv' created and activated with dependencies installed."

# (Optional) Print instructions on how to activate the environment in the future
echo "To activate the environment in the future, run:"
echo "source flaskenv/bin/activate"
