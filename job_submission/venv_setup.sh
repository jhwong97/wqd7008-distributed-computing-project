#!/bin/bash

cd /home/ubuntu/

sudo apt install python3-pip
sudo apt install python3.10-venv

# Define the folder name and make new directory
FOLDER_NAME="venv"

# Check if the folder exists in the current directory
if [ -d "$FOLDER_NAME" ]; then
    echo "Folder '$FOLDER_NAME' exists. Activating the virtual environment..."
    source /home/ubuntu/venv/bin/activate
    echo "Virtual Environment is activated"
    pip install --upgrade pip setuptools wheel
    /usr/bin/python3 /home/ubuntu/scripts/venv_setup.py
    
else
    echo "Folder '$FOLDER_NAME' does not exist in the current directory."
    echo "Creating the virtual environment..."
    /usr/bin/python3 -m venv venv
    echo "Activating the virtual environment..."
    source /home/ubuntu/venv/bin/activate
    echo "Virtual Environment is activated"
    pip install --upgrade pip setuptools wheel
    /usr/bin/python3 /home/ubuntu/scripts/venv_setup.py

fi

pip install -r /home/ubuntu/requirements.txt
deactivate