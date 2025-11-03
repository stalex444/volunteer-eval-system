# Quick Start - Get the App Running

## Option 1: Use Latest Python (Recommended)

### Step 1: Check your Python version
```bash
python3 --version
```

You currently have Python 3.7.4. For best compatibility, upgrade to Python 3.9+ if possible.

### Step 2: Install Python 3.9+ (if needed)

**Using Homebrew (recommended for Mac):**
```bash
# Install Homebrew if you don't have it
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python 3.11 (latest stable)
brew install python@3.11

# Verify installation
python3.11 --version
```

### Step 3: Create Virtual Environment with Latest Python
```bash
cd /Users/stephaniealexander/CascadeProjects/volunteer-eval-system

# Remove old venv if it exists
rm -rf venv

# Create new venv with Python 3.11
python3.11 -m venv venv

# Activate it
source venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### Step 4: Initialize Database
```bash
# Create database directory
mkdir -p database

# Initialize database with default admin user
python app_new.py &
sleep 2
pkill -f app_new.py
```

### Step 5: Run the App
```bash
python app_new.py
```

## Option 2: Use Your Current Python 3.7

If you can't upgrade Python right now, here's what to do:

### Step 1: Update requirements.txt for Python 3.7
The requirements.txt has been updated to work with Python 3.7.

### Step 2: Install Dependencies
```bash
cd /Users/stephaniealexander/CascadeProjects/volunteer-eval-system

# Activate virtual environment
source venv/bin/activate

# Install
pip install -r requirements.txt
```

### Step 3: Run the App
```bash
python app_new.py
```

## Access the Application

Once running, open your browser to:
- **Dashboard**: http://localhost:5000/
- **Login**: http://localhost:5000/login
  - Username: `admin`
  - Password: `changeme123`

## Troubleshooting

### Port 5000 already in use
```bash
# Run on different port
python app_new.py
# Then edit app_new.py to change port to 5001
```

### Database errors
```bash
# Reset database
rm -rf database/
mkdir database
python app_new.py
```

### Import errors
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt
```

## Quick Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Run app
python app_new.py

# Stop app
# Press Ctrl+C in terminal

# Deactivate virtual environment
deactivate
```
