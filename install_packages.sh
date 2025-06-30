#!/bin/bash

echo "Changing directory to project folder..."
cd /home/torabistore/store_project/

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing packages from requirements.txt..."
pip install -r requirements.txt

echo "Package installation complete."