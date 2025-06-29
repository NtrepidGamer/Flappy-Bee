#!/bin/bash

echo "Starting setup..."

# Check for Python
if command -v python3 &>/dev/null; then
    echo "Python is already installed."
else
    echo "Python is not installed. Installing Python..."

    # For Debian/Ubuntu
    sudo apt update
    sudo apt install -y python3 python3-pip

    if ! command -v python3 &>/dev/null; then
        echo "Python installation failed. Exiting."
        exit 1
    fi
fi

# Ensure pip is installed
if ! command -v pip3 &>/dev/null; then
    echo "pip not found. Installing pip..."
    sudo apt install -y python3-pip
fi

# Install required Python packages
echo "Installing Python packages..."

pip3 install --user pygame
echo "pygame installed successfully."
pip3 install --user pyautogui
echo "pyautogui installed successfully."
pip3 install --user pygetwindow
echo "pygetwindow installed successfully."

echo "All done!"
echo

# Run the game
echo "Launching the game..."

cd ./game_files

python3 ./game_files/transparrent.py
