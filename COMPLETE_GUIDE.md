# 📘 Complete Volunteer Evaluation System Guide

**Everything you need to run your volunteer evaluation system from start to finish.**

---

## 📑 Table of Contents

1. [Quick Start](#quick-start)
2. [System Overview](#system-overview)
3. [Initial Setup](#initial-setup)
4. [Daily Operations](#daily-operations)
5. [After Each Event](#after-each-event)
6. [Managing Users](#managing-users)
7. [Managing Volunteers](#managing-volunteers)
8. [Viewing & Analyzing Data](#viewing--analyzing-data)
9. [Troubleshooting](#troubleshooting)
10. [Reference](#reference)

---

## 🚀 Quick Start

### Starting the System

```bash
cd /Users/stephaniealexander/CascadeProjects/volunteer-eval-system
./venv/bin/python app_new.py
```

**Access Points:**
- **Public Evaluation Form:** http://localhost:5001/evaluate
- **Admin Dashboard:** http://localhost:5001/login
  - Username: `admin`
  - Password: `admin123`

### Stopping the System

Press `Ctrl+C` in the terminal where the server is running.

---

## 🎯 System Overview

### What This System Does

**For GLs (Group Leaders):**
- Submit evaluations for volunteers after events
- Rate volunteers on 5 categories (1-10 scale)
- Provide qualitative feedback
- Access via simple form or QR code

**For Admins:**
- View all evaluations in dashboard
- Track volunteer performance over time
- Identify top performers (≥8.0 average)
- Identify volunteers needing support (<6.0 average)
- Edit volunteer information
- Generate reports

**For Viewers (GLs with dashboard access):**
- View evaluations and statistics
- See volunteer profiles
- Cannot edit or delete data

### Key Features

✅ Beautiful Dr. Joe gradient styling
✅ 5-category rating system (Reliability, Quality, Initiative, Teamwork, Communication)
✅ Real-time overall average calculation
✅ QR code support for mobile access
✅ Automated email reminders
✅ Performance analytics
✅ Top performers & needs attention lists
✅ Individual volunteer profiles with history

---

## 🔧 Initial Setup

### First Time Only

**1. Verify Installation**

```bash
cd /Users/stephaniealexander/CascadeProjects/volunteer-eval-system
ls -la
```

You should see:
- `app_new.py`
- `models.py`
- `venv/` folder
- `volunteer_eval.db`
- `templates/` folder
- `static/` folder

**2. Check Database**

The database is already set up with:
- ✅ 9 volunteers ready to evaluate
- ✅ Admin account (admin/admin123)
- ✅ Sample evaluations

**3. Test the System**

```bash
# Start server
./venv/bin/python app_new.py

# In browser, visit:
http://localhost:5001/evaluate
http://localhost:5001/login
```

**4. Optional: Set Up Email Reminders**

See [Email Setup](#email-setup-optional) section below.

---

## 📅 Daily Operations

### Starting Your Day

**1. Start the Server**

```bash
cd /Users/stephaniealexander/CascadeProjects/volunteer-eval-system
./venv/bin/python app_new.py
```

**2. Check Dashboard**

- Go to: http://localhost:5001/login
- Login with: `admin` / `admin123`
- Review:
  - Recent evaluations
  - Top performers
  - Volunteers needing attention

**3. Monitor Submissions**

Dashboard shows:
- Total evaluations submitted
- Recent activity
- Volunteer statistics

### Ending Your Day

**1. Review Data**

- Check all evaluations were submitted
- Note any issues or patterns
- Identify follow-ups needed

**2. Stop Server (Optional)**

Press `Ctrl+C` in terminal

Or leave it running for 24/7 access

---

## 🎪 After Each Event

### ⚡ Quick Start: Send QR Code Reminder (30 Seconds)

**The fastest way to remind GLs after an event:**

**Step 1: Generate QR Code**
```bash
cd /Users/stephaniealexander/CascadeProjects/volunteer-eval-system
python generate_qr.py
```

Press Enter to use default URL. Done!

**Step 2: Open QR Code**
```bash
open qr_codes/evaluation_qr_latest.png
```

Or navigate to: `qr_codes/evaluation_qr_latest.png`

**Step 3: Copy This Message**
```
🎯 Evaluation Time!

Hey team! Please take 5 minutes to evaluate your volunteers from [EVENT NAME].

📝 Evaluation Form: http://localhost:5001/evaluate

⏰ Please complete by [DATE]

Scan the QR code with your phone camera or click the link above.

Thanks! 🙏
```

**Step 4: Post in Telegram**
1. Open your GL group chat
2. Paste the message
3. Edit [EVENT NAME] and [DATE]
4. Attach the QR code image
5. Send!

**Done!** ✅ GLs can now scan and submit evaluations.

---

### Complete Workflow (Step-by-Step)

#### **Step 1: Prepare Reminder (Choose A or B)**

**Option A: Quick Telegram Share (30 seconds)**

```bash
# Generate QR code
python generate_qr.py
```

- Press Enter to use default URL
- QR code saved to: `qr_codes/evaluation_qr_latest.png`

**Option B: Automated Email (2 minutes)**

```bash
# Send bulk emails
python send_reminders.py
```

- Enter event name: `WLR November 2025`
- Enter deadline days: `3`
- Paste GL emails/names:
  ```
  john@example.com,John Smith
  sarah@example.com,Sarah Johnson
  ```
- Press Enter twice to send

#### **Step 2: Send Reminder to GLs**

**If using Telegram:**

Post this message in your GL group:

```
🎯 Evaluation Time!

Hey team! Please take 5 minutes to evaluate your volunteers from [EVENT NAME].

📝 Evaluation Form: http://localhost:5001/evaluate

[Attach QR code image: qr_codes/evaluation_qr_latest.png]

⏰ Please complete by [DATE]

Scan the QR code with your phone camera or click the link above.

Thanks! 🙏
```

**If using Email:**

Emails are sent automatically by the script. GLs receive:
- Professional HTML email
- QR code embedded
- Clickable button
- Deadline reminder

#### **Step 3: Monitor Submissions**

**Check Dashboard Daily:**

1. Go to: http://localhost:5001/login
2. View "Recent Evaluations" table
3. Note who has submitted
4. Track completion rate

**Follow Up (Day Before Deadline):**

- Check who hasn't submitted
- Send reminder in Telegram:
  ```
  Reminder: Evaluations due tomorrow!
  Link: http://localhost:5001/evaluate
  ```

#### **Step 4: Review Results**

**After Deadline:**

1. **View All Evaluations**
   - Dashboard → Recent Evaluations
   - See all submitted forms

2. **Check Individual Volunteers**
   - Click volunteer name
   - See complete history
   - View all ratings and feedback

3. **Identify Patterns**
   - Top Performers list (≥8.0)
   - Needs Attention list (<6.0)
   - Trends over time

4. **Take Action**
   - Recognize top performers
   - Schedule check-ins for low performers
   - Plan training if needed

---

## 👥 Managing Users

### Understanding User Roles

**There are 2 types of users:**

| Role | Access Level | Can Do | Can't Do |
|------|-------------|---------|----------|
| **Admin** | Full access | View, edit, delete everything | - |
| **Viewer** | Read-only | View dashboard, profiles, evaluations | Edit or delete anything |

**Who should be what:**
- **Admins:** You, volunteer coordinators, program directors
- **Viewers:** Group Leaders (GLs) who want to see evaluations

---

### 🔐 Setting Up User Accounts

#### **Current Admin Account**

You already have one admin account:
- **Username:** `admin`
- **Password:** `admin123`

**⚠️ Important:** Change this password for security!

```bash
python change_password.py
# Select: admin
# Enter new password
```

---

#### **Add Additional Admins**

**When to do this:** When you want to give someone full access (another coordinator, director, etc.)

**How to do it:**

```bash
python add_admin.py
```

**Step-by-step:**
```
Enter username: stephanie
Enter password: SecurePass123!

✅ Admin user 'stephanie' created successfully!

Login at: http://localhost:5001/login
Username: stephanie
Password: SecurePass123!
```

**What they can do:**
- ✅ View all evaluations
- ✅ Edit volunteer information
- ✅ View all statistics
- ✅ Access all features
- ✅ Manage data

**Share credentials:** Send username/password securely via Telegram or in person

---

#### **Add GL Viewers (Read-Only Access)**

**When to do this:** When GLs want to see evaluations and stats but shouldn't edit anything

**How to do it:**

```bash
python add_viewer.py
```

**Step-by-step:**
```
Enter username (e.g., 'john_gl'): john_gl
Enter password: JohnPass123!

✅ Viewer user 'john_gl' created successfully!

This user can:
  ✓ View dashboard
  ✓ View volunteer profiles
  ✓ View all evaluations
  ✗ Cannot edit volunteers
  ✗ Cannot delete data

Login at: http://localhost:5001/login
Username: john_gl
Password: JohnPass123!
```

**What they can do:**
- ✅ Login to dashboard
- ✅ View all evaluations
- ✅ See volunteer profiles
- ✅ View statistics
- ❌ Cannot edit volunteer info
- ❌ Cannot delete evaluations
- ❌ Cannot manage users

**Share credentials:** Send to GL via Telegram

---

#### **Recommended Setup**

**For a typical program:**

1. **Create 1-2 Admin accounts:**
   ```bash
   python add_admin.py
   # Username: stephanie (you)
   
   python add_admin.py
   # Username: coordinator2 (backup admin)
   ```

2. **Create Viewer accounts for GLs who want access:**
   ```bash
   python add_viewer.py
   # Username: john_gl
   
   python add_viewer.py
   # Username: sarah_gl
   
   python add_viewer.py
   # Username: mike_gl
   ```

3. **Share credentials securely:**
   - Telegram direct message
   - In person
   - Encrypted message
   - **Never** post in public channels

---

### 📋 User Management Tasks

#### **View All Users**

```bash
python check_users.py
```

**Shows:**
```
Current Users:
1. admin (admin) - Created: 2025-11-02
2. stephanie (admin) - Created: 2025-11-02
3. john_gl (viewer) - Created: 2025-11-02
4. sarah_gl (viewer) - Created: 2025-11-02
```

#### **Change User Password**

```bash
python change_password.py
```

**Example:**
```
Select user:
1. admin
2. stephanie
3. john_gl

Enter number: 1
Enter new password: NewSecurePass123!

✅ Password updated for 'admin'
```

#### **Delete User** (if needed)

```bash
python delete_user.py
```

**Example:**
```
Select user to delete:
1. admin
2. john_gl

Enter number: 2

⚠️  Are you sure? (yes/no): yes

✅ User 'john_gl' deleted
```

---

### 🎯 Quick Setup Example

**Scenario:** You want to set up the system for your team

**Step 1: Secure the admin account**
```bash
python change_password.py
# Change 'admin' password from 'admin123' to something secure
```

**Step 2: Create your personal admin account**
```bash
python add_admin.py
# Username: stephanie
# Password: YourSecurePassword!
```

**Step 3: Create viewer accounts for 3 GLs**
```bash
python add_viewer.py
# Username: john_gl
# Password: JohnPass123!

python add_viewer.py
# Username: sarah_gl
# Password: SarahPass123!

python add_viewer.py
# Username: mike_gl
# Password: MikePass123!
```

**Step 4: Share credentials**

Send to each GL via Telegram:
```
Hi John! 👋

You now have access to the volunteer evaluation dashboard.

🔐 Login: http://localhost:5001/login
Username: john_gl
Password: JohnPass123!

You can view all evaluations and volunteer stats.
Please keep your password secure!
```

**Done!** ✅

---

### 🔒 Security Best Practices

1. **Change default password** immediately
2. **Use strong passwords** (mix of letters, numbers, symbols)
3. **Don't share admin accounts** - create separate accounts
4. **Share credentials securely** - never in public channels
5. **Review users periodically** - remove inactive accounts
6. **Different passwords** for each user
7. **Document who has access** - keep a list

---

### ❓ Common Questions

**Q: Can viewers submit evaluations?**
A: No, viewers can only view data. Anyone can submit evaluations via the public form (no login needed).

**Q: How many admin accounts should I have?**
A: 2-3 is ideal. You + backup coordinators.

**Q: Do GLs need accounts to submit evaluations?**
A: No! The evaluation form is public (no login). Accounts are only for viewing the dashboard.

**Q: Can I change someone from viewer to admin?**
A: Yes, delete their viewer account and recreate as admin.

**Q: What if someone forgets their password?**
A: Use `python change_password.py` to reset it.

**Q: Can viewers see who submitted evaluations?**
A: Yes, they can see all evaluation data including evaluator names.

**Q: Should all GLs have viewer accounts?**
A: Only if they want to see the dashboard. Most GLs just submit evaluations (no account needed).

---

## 🙋 Managing Volunteers

### View All Volunteers

**In Dashboard:**
1. Login: http://localhost:5001/login
2. Click "All Volunteers" in navigation
3. See complete list with stats

**Via Script:**
```bash
python list_volunteers.py
```

### Add New Volunteer

```bash
python add_volunteer.py
```

**Example:**
```
First Name: Maria
Last Name: Garcia
Status (active/inactive): active

✅ Volunteer 'Maria Garcia' added successfully!
```

### Edit Volunteer Information

**In Dashboard:**
1. Go to volunteer's profile
2. Click "Edit Info" button
3. Update name or status
4. Click "Save Changes"

**What you can edit:**
- First Name
- Last Name
- Status (Active/Inactive)

### View Volunteer Profile

**In Dashboard:**
1. Click volunteer name anywhere
2. See:
   - Status
   - Total evaluations
   - Performance statistics
   - Average ratings by category
   - Complete evaluation history
   - All feedback comments

---

## 📊 Viewing & Analyzing Data

### Dashboard Overview

**Summary Cards:**
- **Active Volunteers** - Currently active count
- **Total Evaluations** - All-time submissions
- **Top Performers** - Count of volunteers ≥8.0
- **Needs Attention** - Count of volunteers <6.0

**Top Performers List:**
- Shows volunteers with ≥8.0 average
- Displays average rating
- Number of evaluations
- Click name to view profile

**Needs Attention List:**
- Shows volunteers with <6.0 average
- Requires intervention/support
- Click name to view profile

**Recent Evaluations Table:**
- Date of evaluation
- Volunteer name (clickable)
- Role performed (GL, GLA, etc.)
- Event name (WLR, AFU, etc.)
- Overall score (calculated average)
- Evaluator name and role

### Volunteer Profile Page

**Access:**
- Click any volunteer name
- Or go to: All Volunteers → Click name

**What You See:**

**1. Header**
- Volunteer name
- Status badge
- "Edit Info" button

**2. Performance Statistics**
- Total evaluations
- Average overall rating
- Average by category:
  - Reliability
  - Communication
  - Teamwork
  - Initiative
  - Quality of Work
- Performance trend (improving/declining/stable)
- Recent performance (last 30 days)

**3. All Evaluations Table**
- Date
- Event
- Role
- Evaluator
- Overall score
- All 5 category ratings
- Expandable feedback:
  - 💪 Strengths
  - 📈 Areas for Improvement
  - 💬 Additional Comments

### Understanding Ratings

**Rating Scale:** 1-10
- **9-10:** Exceptional
- **8:** Very Good
- **7:** Good
- **6:** Satisfactory
- **5 or below:** Needs Improvement

**Overall Score:**
- Calculated as average of 5 categories
- Displayed with 1 decimal place
- Color-coded badges:
  - Green: ≥8.0
  - Yellow: 6.0-7.9
  - Red: <6.0

**Performance Trends:**
- **Improving:** Recent scores higher than older scores
- **Declining:** Recent scores lower than older scores
- **Stable:** Consistent performance
- Requires minimum 4 evaluations

### Exporting Data

**View Raw Data:**
```bash
python check_evaluations.py
```

Shows all evaluations in terminal.

**For Spreadsheet Analysis:**
- Data is in SQLite database: `volunteer_eval.db`
- Can export using SQLite browser
- Or create custom export script

---

## 🎓 Complete Event Workflow Example

### Scenario: WLR November 2025

**Before Event (1 day before):**
- [ ] Verify server is running
- [ ] Test evaluation form
- [ ] Ensure all volunteers in database

**During Event:**
- [ ] GLs work with volunteers
- [ ] Note who worked with whom
- [ ] Remind GLs evaluations are coming

**After Event (Same day or next day):**

**1. Generate QR Code (30 seconds)**
```bash
python generate_qr.py
# Press Enter for default URL
```

**2. Post in Telegram (1 minute)**
```
🎯 Evaluation Time!

Hey team! Please evaluate your volunteers from WLR November 2025.

📝 http://localhost:5001/evaluate

[Attach: qr_codes/evaluation_qr_latest.png]

⏰ Due: Friday, November 8

Thanks! 🙏
```

**3. Monitor Submissions (Daily)**
- Check dashboard each day
- Note completion rate
- Example: "5 of 8 GLs submitted"

**4. Send Reminder (Day before deadline)**
```
⏰ Reminder: Evaluations due tomorrow!

Please complete if you haven't already:
http://localhost:5001/evaluate

Thanks!
```

**5. Review Results (After deadline)**
- Login to dashboard
- Check Recent Evaluations
- View individual volunteer profiles
- Note patterns:
  - "Sarah received 3 evaluations, all 9+"
  - "Mike needs follow-up, scores declining"

**6. Take Action (Within 1 week)**
- Email/message top performers
- Schedule check-in with low performers
- Plan training sessions
- Update volunteer assignments

**7. Document (For records)**
- Screenshot dashboard stats
- Note key findings
- Save for quarterly review

---

## 📧 Email Setup (Optional)

### One-Time Configuration

**1. Install Dependencies**
```bash
pip install -r requirements.txt
```

**2. Create .env File**

Create file: `.env` in project root

**For Gmail:**
```bash
MAIL_SERVER=smtp.gmail.com
MAIL_PORT=587
MAIL_USE_TLS=True
MAIL_USERNAME=your-email@gmail.com
MAIL_PASSWORD=your-app-password
MAIL_DEFAULT_SENDER=your-email@gmail.com
```

**3. Get Gmail App Password**

1. Go to: https://myaccount.google.com/security
2. Enable "2-Step Verification"
3. Click "App passwords"
4. Generate new password
5. Copy 16-character password
6. Paste in `.env` file as `MAIL_PASSWORD`

**4. Test Email**
```bash
python send_reminders.py
```

Enter your own email to test:
```
Event name: Test Event
Days until deadline: 1
your-email@gmail.com,Your Name
```

Check inbox for beautiful email with QR code!

### Using Email System

**After Each Event:**
```bash
python send_reminders.py
```

**Enter Details:**
```
Event name: WLR November 2025
Days until deadline: 3

Enter GL emails and names:
john@example.com,John Smith
sarah@example.com,Sarah Johnson
mike@example.com,Mike Chen

[Press Enter twice]

✅ Sent: 3
```

**GLs Receive:**
- Professional HTML email
- QR code embedded
- Clickable button
- Deadline: November 5, 2025
- Instructions

---

## 🔧 Troubleshooting

### Server Won't Start

**Error: Port already in use**
```bash
# Find process using port 5001
lsof -i :5001

# Kill the process
kill -9 [PID]

# Restart server
./venv/bin/python app_new.py
```

**Error: Module not found**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

**Error: Database locked**
```bash
# Stop all Python processes
pkill -f app_new.py

# Restart server
./venv/bin/python app_new.py
```

### Can't Access Website

**Check server is running:**
```bash
curl http://localhost:5001/
```

If no response:
```bash
./venv/bin/python app_new.py
```

**Check correct URL:**
- ✅ http://localhost:5001/evaluate
- ❌ http://localhost:5000/evaluate (wrong port)

### Login Not Working

**Reset admin password:**
```bash
python reset_admin.py
```

**Default credentials:**
- Username: `admin`
- Password: `admin123`

### Evaluations Not Showing

**Check database:**
```bash
python check_evaluations.py
```

**Verify volunteer exists:**
```bash
python list_volunteers.py
```

**Check recent submissions:**
- Dashboard → Recent Evaluations
- Should appear immediately after submission

### Email Not Sending

**Check .env file exists:**
```bash
ls -la .env
```

**Verify credentials:**
- Gmail: Use app password, not regular password
- Check username is full email address
- Verify 2-Step Verification enabled

**Test connection:**
```bash
python test_email.py
```

### QR Code Not Working

**Regenerate QR code:**
```bash
python generate_qr.py
```

**Check URL is correct:**
- Should be: http://localhost:5001/evaluate
- Or your public URL if deployed

**Test QR code:**
- Scan with phone camera
- Should open evaluation form

---

## 📚 Reference

### File Structure

```
volunteer-eval-system/
├── app_new.py              # Main application
├── models.py               # Database models
├── volunteer_eval.db       # SQLite database
├── requirements.txt        # Python dependencies
├── .env                    # Email configuration (create this)
│
├── routes/
│   ├── auth_routes.py      # Login/logout
│   ├── dashboard_routes.py # Admin dashboard
│   └── evaluation_routes.py # Evaluation form
│
├── templates/
│   ├── base.html           # Base template
│   ├── evaluation-form.html # Public form
│   ├── dashboard.html      # Admin dashboard
│   ├── volunteer-profile.html # Individual profiles
│   ├── volunteers-list.html # All volunteers
│   └── edit-volunteer.html # Edit form
│
├── static/
│   ├── css/
│   │   └── style.css       # All styles
│   └── js/
│       ├── evaluation-form.js # Form interactions
│       └── dashboard.js    # Dashboard features
│
├── utils/
│   ├── analytics.py        # Performance calculations
│   └── notifications.py    # Email & QR codes
│
├── qr_codes/               # Generated QR codes
│   └── evaluation_qr_latest.png
│
└── Scripts/
    ├── add_admin.py        # Add admin user
    ├── add_viewer.py       # Add GL viewer
    ├── add_volunteer.py    # Add volunteer
    ├── generate_qr.py      # Generate QR code
    ├── send_reminders.py   # Send emails
    ├── check_evaluations.py # View all evaluations
    └── list_volunteers.py  # View all volunteers
```

### Important URLs

**Public Access:**
- Evaluation Form: http://localhost:5001/evaluate

**Admin Access (Login Required):**
- Login Page: http://localhost:5001/login
- Dashboard: http://localhost:5001/dashboard
- All Volunteers: http://localhost:5001/dashboard/volunteers
- Volunteer Profile: http://localhost:5001/dashboard/volunteer/[ID]
- Edit Volunteer: http://localhost:5001/dashboard/volunteer/[ID]/edit

### Database Schema

**Volunteers Table:**
- id (primary key)
- first_name
- last_name
- status (active/inactive)
- created_at

**Evaluations Table:**
- evaluation_id (primary key, auto-generated)
- volunteer_id (foreign key)
- role_performed (GL, GLA, etc.)
- event_name (WLR, AFU, etc.)
- service_month
- service_year
- evaluation_date
- reliability (1-10)
- quality_of_work (1-10)
- initiative (1-10)
- teamwork (1-10)
- communication (1-10)
- strengths (text)
- areas_for_improvement (text)
- additional_comments (text)
- evaluator_name
- evaluator_email
- evaluator_role
- submitted_at

**Users Table:**
- id (primary key)
- username
- password_hash
- role (admin/viewer)
- created_at

### Command Reference

**Server:**
```bash
# Start
./venv/bin/python app_new.py

# Stop
Ctrl+C
```

**User Management:**
```bash
python add_admin.py         # Add admin user
python add_viewer.py        # Add GL viewer
python check_users.py       # List all users
python change_password.py   # Change password
```

**Volunteer Management:**
```bash
python add_volunteer.py     # Add new volunteer
python list_volunteers.py   # List all volunteers
python check_evaluations.py # View all evaluations
```

**Reminders:**
```bash
python generate_qr.py       # Generate QR code
python send_reminders.py    # Send email reminders
```

**Database:**
```bash
python init_db.py           # Initialize database
python backup_db.py         # Backup database
```

### Event Types

- **WLR** - Weeklong Retreat
- **AFU** - Advanced Follow-Up
- **Prog** - Progressive
- **10-Day** - 10-Day Course
- **Other** - Custom event

### Roles

**Volunteer Roles:**
- GL - Group Leader
- GLA - Group Leader Assistant
- GG - Gong Girl/Guy
- Kitchen Lead
- RR Lead - Registration/Records Lead
- Medical Lead
- GC Lead - Group Coordinator Lead

**User Roles:**
- Admin - Full access
- Viewer - Read-only (for GLs)

### Rating Categories

1. **Reliability** - Shows up on time, follows through
2. **Quality of Work** - Attention to detail, thoroughness
3. **Initiative** - Takes action, proactive
4. **Teamwork** - Collaborates well, supportive
5. **Communication** - Clear, responsive, professional

### Performance Thresholds

- **Top Performer:** ≥8.0 average
- **Good Performance:** 6.0-7.9 average
- **Needs Attention:** <6.0 average

---

## 🎯 Quick Reference Cheat Sheet

### Daily Tasks

```bash
# Start server
./venv/bin/python app_new.py

# Check dashboard
# http://localhost:5001/login
```

### After Event - QR Code Reminder (FASTEST)

**30-Second Process:**

```bash
# 1. Generate QR code
python generate_qr.py

# 2. Open it
open qr_codes/evaluation_qr_latest.png

# 3. Copy this message to Telegram:
```

**Message Template:**
```
🎯 Evaluation Time!

Hey team! Please evaluate your volunteers from [EVENT NAME].

📝 http://localhost:5001/evaluate

⏰ Due: [DATE]

Scan QR code or click link. Thanks! 🙏
```

**4. Attach QR image and send!**

---

### After Event - Email Option

```bash
# Option 1: Telegram (above)
python generate_qr.py
# Share in Telegram with link

# Option 2: Email
python send_reminders.py
# Enter event details
```

### Common Tasks

```bash
# Add volunteer
python add_volunteer.py

# Add admin
python add_admin.py

# Add GL viewer
python add_viewer.py

# View all data
python check_evaluations.py
```

### Emergency

```bash
# Server crashed
pkill -f app_new.py
./venv/bin/python app_new.py

# Reset admin password
python reset_admin.py

# Backup database
cp volunteer_eval.db volunteer_eval_backup.db
```

---

## ✅ Success Checklist

### System is Working When:

- [ ] Server starts without errors
- [ ] Can access http://localhost:5001/evaluate
- [ ] Can login to dashboard
- [ ] Can submit evaluation
- [ ] Evaluation appears in dashboard
- [ ] Can view volunteer profile
- [ ] Can edit volunteer info
- [ ] QR code generates successfully
- [ ] (Optional) Emails send successfully

### You're Ready When:

- [ ] All volunteers added to database
- [ ] Admin account working
- [ ] GL viewers created (if needed)
- [ ] QR code generated
- [ ] Email configured (if using)
- [ ] Tested full workflow
- [ ] GLs know how to access form
- [ ] You know how to check dashboard

---

## 🎉 You're All Set!

This system is ready to use. Follow the workflows in this guide and you'll be efficiently managing volunteer evaluations in no time!

**Key Points to Remember:**
1. Start server before each use
2. Send reminders after each event
3. Check dashboard regularly
4. Follow up with non-responders
5. Review and act on results

**Need Help?**
- Check [Troubleshooting](#troubleshooting) section
- Review specific workflow sections
- Test with sample data first

**Good luck with your volunteer program! 🚀**
