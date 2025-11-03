# Quick Start Guide - Phase 1

## 🚀 Get Started in 5 Minutes

### 1. Navigate to Project
```bash
cd /Users/stephaniealexander/CascadeProjects/volunteer-eval-system
```

### 2. Set Up Virtual Environment
```bash
# Create virtual environment
python -m venv venv

# Activate it
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Initialize Database
```bash
# Run migrations to create all tables
flask run-migrations

# Or use the Phase 1 app to auto-create
python -c "from app_new import create_app; app = create_app()"
```

### 5. Start the Application
```bash
# Option 1: Run directly
python app_new.py

# Option 2: Use Flask CLI
export FLASK_APP=app_new.py
flask run
```

### 6. Access the System

**Dashboard (Login Required)**
- URL: http://localhost:5000/
- Username: `admin`
- Password: `changeme123`

**Public Evaluation Form (No Login)**
- URL: http://localhost:5000/evaluate/

## 📋 What You Can Do Now

### As Admin
1. **View Dashboard** - See statistics, top performers, recent evaluations
2. **Manage Users** - Add/delete users, change passwords
3. **Manage Events** - Add/delete events (WLR, AFU, Prog, 10-Day)
4. **View Volunteers** - See all volunteers and their profiles
5. **View Evaluations** - Browse all submitted evaluations

### As Public User
1. **Submit Evaluations** - Fill out evaluation form for any volunteer
2. **No login required** - Direct access to evaluation form

## 🔧 Useful Commands

```bash
# List all users
flask list-users

# List all roles
flask list-roles

# List all events
flask list-events

# Create a new admin user
flask create-admin

# Create a new user (admin or viewer)
flask create-user

# Add sample volunteer data
flask seed-data
```

## 📊 Sample Data

To populate with sample data:
```bash
flask seed-data
```

This creates:
- 3 sample volunteers (John Doe, Jane Smith, Bob Johnson)
- Each with preferred roles assigned

## 🔐 Change Default Password

**IMPORTANT**: Change the default admin password immediately!

1. Log in as admin
2. Go to: http://localhost:5000/dashboard/users
3. Click "Change Password" for admin user
4. Enter new password

## 🎯 Test the System

### Test Evaluation Submission
1. Go to http://localhost:5000/evaluate/
2. Fill out the form:
   - Select a volunteer
   - Select a role
   - Select an event (optional)
   - Rate on 1-10 scale
   - Add feedback
3. Submit and verify success

### Test Dashboard
1. Log in at http://localhost:5000/login
2. View dashboard statistics
3. Click on a volunteer to see their profile
4. Check recent evaluations

### Test User Management
1. Go to http://localhost:5000/dashboard/users
2. Add a new viewer user
3. Log out and log in as the viewer
4. Verify read-only access

## 🐛 Troubleshooting

### Database Not Found
```bash
# Create database directory
mkdir -p database

# Re-run initialization
python -c "from app_new import create_app; app = create_app()"
```

### Import Errors
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

### Port Already in Use
```bash
# Run on different port
flask run --port 5001
```

## 📁 Project Structure

```
volunteer-eval-system/
├── app_new.py              # Phase 1 Flask app
├── config.py               # Configuration
├── models.py               # Database models
├── requirements.txt        # Dependencies
├── routes/
│   ├── evaluation_routes_phase1.py
│   └── dashboard_routes_phase1.py
├── templates/
│   ├── login.html
│   ├── manage-users.html
│   └── ... (other templates)
├── static/
│   ├── css/style.css
│   └── js/...
└── database/
    └── volunteers.db       # SQLite database
```

## ✅ Phase 1 Checklist

- [ ] Virtual environment created
- [ ] Dependencies installed
- [ ] Database initialized
- [ ] Default admin password changed
- [ ] Test evaluation submitted
- [ ] Dashboard accessed
- [ ] New user created
- [ ] Sample data loaded

## 🎉 You're Ready!

Phase 1 is complete and running. You now have:
- ✅ Working authentication system
- ✅ Public evaluation form
- ✅ Leadership dashboard
- ✅ User management
- ✅ Event management
- ✅ Volunteer tracking

**Next**: Proceed to Phase 2 for advanced features!
