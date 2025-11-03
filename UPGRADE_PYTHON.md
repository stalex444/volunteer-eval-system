# Upgrade Python & Run the App

## Current Situation
- You have Python 3.7.4
- The app needs Python 3.9+ for latest features
- You can still run it with 3.7, but upgrading is recommended

## Option 1: Quick Upgrade (Recommended)

### Install Latest Python with Homebrew
```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.11 (latest stable)
brew install python@3.11

# Verify
python3.11 --version
```

### Set Up the App with New Python
```bash
cd /Users/stephaniealexander/CascadeProjects/volunteer-eval-system

# Remove old virtual environment
rm -rf venv

# Create new one with Python 3.11
python3.11 -m venv venv

# Activate
source venv/bin/activate

# Use latest requirements
pip install --upgrade pip
pip install -r requirements-latest.txt

# Initialize database
python app_new.py &
sleep 3
pkill -f app_new.py

# Run the app
python app_new.py
```

## Option 2: Use Automated Script

```bash
cd /Users/stephaniealexander/CascadeProjects/volunteer-eval-system

# Run the quick start script
./quick-start.sh

# Then start the app
source venv/bin/activate
python app_new.py
```

## Option 3: Stick with Python 3.7 (Works but Limited)

```bash
cd /Users/stephaniealexander/CascadeProjects/volunteer-eval-system

# The requirements.txt is already set for Python 3.7
source venv/bin/activate
pip install -r requirements.txt
python app_new.py
```

## After Running

Open your browser to:
- http://localhost:5000

Login with:
- Username: `admin`
- Password: `changeme123`

## Why Upgrade?

**Python 3.11 Benefits:**
- 10-60% faster than Python 3.7
- Better error messages
- Latest security updates
- Access to newest libraries
- Python 3.7 is end-of-life (no more updates)

## Check What You Have

```bash
# Check all Python versions
ls -la /usr/local/bin/python*

# Check Homebrew Python
brew list | grep python

# See what's available
brew search python
```

## Quick Commands After Setup

```bash
# Start app
cd /Users/stephaniealexander/CascadeProjects/volunteer-eval-system
source venv/bin/activate
python app_new.py

# Stop app
# Press Ctrl+C

# Exit virtual environment
deactivate
```
