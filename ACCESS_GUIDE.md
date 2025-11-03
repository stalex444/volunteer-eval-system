# 🚀 How to Access the System

## 📋 Two Different Pages

### 1. 📝 Evaluation Form (Public - No Login)
**URL:** http://localhost:5001/evaluate

**Who can access:** Anyone
**Purpose:** Submit volunteer evaluations

**What you can do:**
- Fill out evaluation forms
- Rate volunteers
- Submit feedback
- No account needed

---

### 2. 📊 Dashboard (Protected - Login Required)
**URL:** http://localhost:5001/dashboard

**Who can access:** Leadership only (with login)
**Purpose:** View all data and manage system

**What you can do:**
- View all evaluations
- See volunteer profiles
- View statistics
- Manage events
- Manage users (admin only)

---

## 🔐 First Time Setup

### Step 1: Create Your Admin Account

Run this command:
```bash
cd /Users/stephaniealexander/CascadeProjects/volunteer-eval-system
./venv/bin/python create_admin.py
```

This will create:
- **Username:** admin
- **Password:** admin123
- **Role:** admin (full access)

### Step 2: Login

1. Go to: http://localhost:5001/login
2. Enter:
   - Username: `admin`
   - Password: `admin123`
3. Click "Login"

### Step 3: Change Your Password (Recommended)

After logging in:
1. Go to "Manage Users" in the navigation
2. Click "Change Password" for the admin user
3. Set a secure password

---

## 🗺️ Navigation Map

### Public Access (No Login):
```
http://localhost:5001/evaluate
└── Evaluation Form (submit evaluations)
```

### After Login (Dashboard):
```
http://localhost:5001/dashboard
├── Dashboard (overview)
├── All Evaluations (view all submissions)
├── Manage Events (add/edit events)
├── Manage Users (admin only - add users)
└── New Evaluation (opens form in new tab)
```

---

## 👥 User Roles

### Admin
- Full access to everything
- Can manage users
- Can manage events
- Can view all evaluations

### Viewer (if you create one)
- Read-only access
- Can view dashboard
- Can view evaluations
- Cannot edit or delete

---

## 🎯 Common Workflows

### Workflow 1: Submit an Evaluation (Anyone)
1. Go to http://localhost:5001/evaluate
2. Fill out the form
3. Submit
4. Done! (No login needed)

### Workflow 2: View Evaluations (Leadership)
1. Go to http://localhost:5001/login
2. Login with credentials
3. Click "Dashboard" to see overview
4. Click "All Evaluations" to see details
5. Click volunteer names to see profiles

### Workflow 3: Add a New Event (Admin)
1. Login to dashboard
2. Click "Manage Events"
3. Fill out event form
4. Submit
5. Event now appears in evaluation form

### Workflow 4: Add a New User (Admin)
1. Login to dashboard
2. Click "Manage Users"
3. Fill out user form
4. Choose role (admin or viewer)
5. Submit
6. Give credentials to new user

---

## 🔑 Quick Reference

### URLs:
- **Evaluation Form:** http://localhost:5001/evaluate
- **Login:** http://localhost:5001/login
- **Dashboard:** http://localhost:5001/dashboard

### Default Credentials:
- **Username:** admin
- **Password:** admin123
- **⚠️ Change after first login!**

### Create Admin Command:
```bash
./venv/bin/python create_admin.py
```

---

## 🆘 Troubleshooting

### "Can't access dashboard"
- Make sure you're logged in
- Go to http://localhost:5001/login first

### "Invalid credentials"
- Run `create_admin.py` to create admin user
- Use username: `admin`, password: `admin123`

### "Page not found"
- Make sure the server is running: `./venv/bin/python app_new.py`
- Check the URL is correct

### "No volunteers in dropdown"
- You need to add volunteers to the database first
- This is a separate step (volunteer management)

---

## 📊 System Architecture

```
┌─────────────────────────────────────────┐
│         PUBLIC ACCESS                    │
│  http://localhost:5001/evaluate         │
│  (Anyone can submit evaluations)        │
└─────────────────────────────────────────┘
                    │
                    ▼
            [Evaluations saved
             to database]
                    │
                    ▼
┌─────────────────────────────────────────┐
│      PROTECTED DASHBOARD                 │
│  http://localhost:5001/dashboard        │
│  (Login required - Leadership only)     │
│                                          │
│  • View all evaluations                 │
│  • See statistics                       │
│  • Manage events                        │
│  • Manage users                         │
└─────────────────────────────────────────┘
```

---

## ✅ Next Steps

1. **Create admin user:** Run `create_admin.py`
2. **Login:** Go to http://localhost:5001/login
3. **Explore dashboard:** See all the features
4. **Add more users:** Use "Manage Users" page
5. **Test evaluation form:** Go to http://localhost:5001/evaluate

---

## 🎉 You're All Set!

The system has two parts:
- **Public evaluation form** - Anyone can use
- **Protected dashboard** - Leadership only

Both are running on the same server, just different URLs!
