#!/bin/bash

echo "🚀 Volunteer Evaluation System - Quick Start"
echo "============================================"
echo ""

# Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "📍 Current Python version: $PYTHON_VERSION"
echo ""

# Recommend upgrade if needed
MAJOR=$(echo $PYTHON_VERSION | cut -d. -f1)
MINOR=$(echo $PYTHON_VERSION | cut -d. -f2)

if [ "$MAJOR" -lt 3 ] || ([ "$MAJOR" -eq 3 ] && [ "$MINOR" -lt 9 ]); then
    echo "⚠️  Warning: Python 3.9+ recommended for best compatibility"
    echo "   Current version: Python $PYTHON_VERSION"
    echo ""
    echo "To upgrade Python:"
    echo "  brew install python@3.11"
    echo "  Then run: python3.11 -m venv venv"
    echo ""
    read -p "Continue with Python $PYTHON_VERSION? (y/n) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip -q

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Create database directory
mkdir -p database

# Check if database exists
if [ ! -f "database/volunteers.db" ]; then
    echo "🗄️  Initializing database..."
    python -c "from app_new import create_app; app = create_app()" 2>/dev/null
    echo "✅ Database created with default admin user"
    echo "   Username: admin"
    echo "   Password: changeme123"
fi

echo ""
echo "✨ Setup complete!"
echo ""
echo "To start the application:"
echo "  source venv/bin/activate"
echo "  python app_new.py"
echo ""
echo "Then visit: http://localhost:5000"
echo "Login with: admin / changeme123"
echo ""
