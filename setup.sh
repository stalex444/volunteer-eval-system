#!/bin/bash

# Volunteer Evaluation System Setup Script

echo "========================================="
echo "Volunteer Evaluation System Setup"
echo "========================================="
echo ""

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python 3 found"

# Create virtual environment
echo ""
echo "Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo ""
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo ""
    echo "Creating .env file..."
    cp .env.example .env
    echo "✓ .env file created. Please edit it with your configuration."
else
    echo ""
    echo "✓ .env file already exists"
fi

# Create database directory
echo ""
echo "Creating database directory..."
mkdir -p database

# Initialize database
echo ""
echo "Initializing database..."
flask init-db

echo ""
echo "========================================="
echo "Setup Complete!"
echo "========================================="
echo ""
echo "Next steps:"
echo "1. Edit the .env file with your configuration"
echo "2. Create an admin user: flask create-admin"
echo "3. (Optional) Seed sample data: flask seed-data"
echo "4. Run the application: flask run"
echo ""
echo "To activate the virtual environment in the future:"
echo "  source venv/bin/activate"
echo ""
