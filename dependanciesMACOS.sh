#!/bin/bash

echo "Starting setup..."
sleep 1

# Check for Python 3
if ! command -v python3 &>/dev/null; then
    echo "Python 3 is not installed. Installing with Homebrew..."

    if ! command -v brew &>/dev/null; then
        echo "Homebrew is not installed. Installing Homebrew first..."
        /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

        # Update PATH for Homebrew (Apple Silicon compatibility)
        if [ -d /opt/homebrew/bin ]; then
            export PATH="/opt/homebrew/bin:$PATH"
        fi
    fi

    brew update
    brew install python

    if ! command -v python3 &>/dev/null; then
        echo "Python installation failed. Exiting."
        exit 1
    fi
else
    echo "Python 3 is already installed."
fi

# Ensure pip3 is available
if ! command -v pip3 &>/dev/null; then
    echo "pip3 not found. Attempting to install pip..."
    python3 -m ensurepip --upgrade
fi

# Install required Python packages
echo "Installing required Python packages..."
pip3 install --user pynput
echo "pynput installed successfully."
pip3 install --user pygame
echo "pygame installed successfully."
pip3 install --user pyautogui
echo "pyautogui installed successfully."
pip3 install --user pygetwindow pyobjc
echo "pygetwindow and pyobjc installed successfully."

echo "Setup complete. Launching the game..."

cd ./game_files

# Run the game
python3 ./game_files/transparrent.py
