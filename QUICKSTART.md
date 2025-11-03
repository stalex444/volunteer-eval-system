# Quick Start Guide

Get the Volunteer Evaluation System up and running in 5 minutes!

## Option 1: Automated Setup (Recommended)

```bash
# Run the setup script
./setup.sh

# Create an admin user
flask create-admin

# Start the application
flask run
```

Visit `http://localhost:5000` in your browser!

## Option 2: Manual Setup

### 1. Create Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Configure Environment
```bash
cp .env.example .env
# Edit .env with your settings (optional for local development)
```

### 4. Initialize Database
```bash
flask init-db
```

### 5. Create Admin User
```bash
flask create-admin
# Enter username, email, and password when prompted
```

### 6. (Optional) Add Sample Data
```bash
flask seed-data
```

### 7. Run the Application
```bash
flask run
```

## First Steps After Installation

### 1. Access the Public Evaluation Form
- Navigate to `http://localhost:5000`
- Click "Submit Evaluation"
- Fill out and submit a test evaluation

### 2. Access the Leadership Dashboard
- Navigate to `http://localhost:5000/login`
- Log in with your admin credentials
- Explore the dashboard features

### 3. View Volunteer Profiles
- From the dashboard, click "View All Volunteers"
- Click on any volunteer to see their detailed profile

## Common Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Run the application
flask run

# Run in debug mode
flask run --debug

# Create a new admin user
flask create-admin

# Initialize/reset database
flask init-db

# Add sample data
flask seed-data
```

## Troubleshooting

### Port Already in Use
```bash
# Run on a different port
flask run --port 5001
```

### Database Errors
```bash
# Reinitialize the database
rm -rf database/
flask init-db
```

### Module Not Found Errors
```bash
# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

## Next Steps

1. **Customize the Application**
   - Edit `config.py` for application settings
   - Modify `templates/` for UI changes
   - Update `static/css/style.css` for styling

2. **Add Real Volunteers**
   - Manually through the database
   - Import from Smartsheet (configure API credentials)
   - Use the API endpoints

3. **Deploy to Production**
   - See README.md for production deployment guidelines
   - Use a production WSGI server (Gunicorn, uWSGI)
   - Configure a reverse proxy (Nginx, Apache)
   - Use PostgreSQL instead of SQLite

## Support

For detailed documentation, see `README.md`

For issues or questions, check the troubleshooting section or contact your system administrator.
