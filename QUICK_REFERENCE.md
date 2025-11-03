# Quick Reference Card

## Flask CLI Commands

```bash
# Database Setup
flask init-db              # Initialize database
flask run-migrations       # Run SQL migrations

# User Management
flask create-admin         # Create admin user (quick)
flask create-user          # Create user (admin or viewer)
flask list-users           # List all users

# Data Management
flask seed-data           # Add sample volunteers
flask list-roles          # List all volunteer roles
flask list-events         # List all events
flask generate-evaluation-id  # Get next evaluation ID

# Run Application
flask run                 # Start development server
flask run --debug         # Start with debug mode
flask run --port 5001     # Run on different port
```

## Project Structure

```
volunteer-eval-system/
├── app.py                 # Main application
├── models.py              # Database models (User, Volunteer, Evaluation, Role)
├── config.py              # Configuration
├── routes/                # Route blueprints
│   ├── evaluation_routes.py
│   ├── dashboard_routes.py
│   └── api_routes.py
├── templates/             # HTML templates
├── static/                # CSS, JS, images
├── migrations/            # SQL migration files
└── utils/                 # Helper functions
```

## URLs

```
Public:
/                          # Landing page
/evaluate                  # Evaluation form
/login                     # Login page

Dashboard (Login Required):
/dashboard                 # Main dashboard
/dashboard/volunteer/<id>  # Volunteer profile
/dashboard/volunteers      # All volunteers list
/logout                    # Logout

API (Login Required):
/api/volunteers            # List volunteers
/api/volunteers/<id>       # Get volunteer details
/api/evaluations           # List evaluations
/api/stats                 # Get statistics
/api/departments           # List departments
```

## Database Models

### User
- username, email, password_hash, role (viewer/admin)

### Volunteer
- name, email, phone, department, role, role_id, status
- Relationships: evaluations, role_info

### Evaluation
- volunteer_id, evaluator info
- Ratings: reliability, communication, teamwork, initiative, quality, overall
- Feedback: strengths, areas_for_improvement, additional_comments

### Role
- role_id, role_name, description, key_skills, interaction_level
- Relationships: volunteers

## Common Python Queries

```python
from models import db, User, Volunteer, Evaluation, Role

# Get volunteer with evaluations
volunteer = Volunteer.query.get(1)
evaluations = volunteer.evaluations.all()
avg_rating = volunteer.average_rating

# Get volunteer with role
volunteer = Volunteer.query.get(1)
if volunteer.role_info:
    role_name = volunteer.role_info.role_name

# Assign role to volunteer
role = Role.query.filter_by(role_name='GL').first()
volunteer.role_id = role.id
db.session.commit()

# Get all volunteers for a role
role = Role.query.filter_by(role_name='Medical').first()
volunteers = role.volunteers.all()

# Filter volunteers
active_volunteers = Volunteer.query.filter_by(status='active').all()
dept_volunteers = Volunteer.query.filter_by(department='Operations').all()

# Get evaluations for volunteer
evaluations = Evaluation.query.filter_by(volunteer_id=1).all()

# Get recent evaluations
from datetime import datetime, timedelta
thirty_days_ago = datetime.utcnow() - timedelta(days=30)
recent = Evaluation.query.filter(Evaluation.created_at >= thirty_days_ago).all()
```

## Pre-defined Roles

| ID   | Name         | Level  | Description                    |
|------|--------------|--------|--------------------------------|
| 001  | GL           | High   | Greeter/Liaison                |
| 002  | GLA          | High   | Greeter/Liaison Assistant      |
| 003  | GG           | High   | Greeter/Gatekeeper             |
| 004  | Doors        | Medium | Door Management                |
| 005  | RR           | High   | Registration/Reception         |
| 006  | HST          | High   | Hospitality Team               |
| 007  | HSL          | High   | Hospitality Support/Lead       |
| 008  | FTVL         | High   | First Time Visitor Liaison     |
| 009  | Medical      | Medium | Medical Support                |
| 010  | Door Lead    | Medium | Door Team Leader               |
| 011  | RR Lead      | High   | Registration/Reception Lead    |
| 012  | Medical Lead | Medium | Medical Team Leader            |
| 013  | GC Lead      | High   | Guest Care Lead                |

## Rating Scale

1 = Needs Improvement
2 = Below Expectations
3 = Meets Expectations
4 = Exceeds Expectations
5 = Excellent

## Rating Categories

1. **Reliability** - Punctuality, attendance, commitment
2. **Communication** - Clarity, responsiveness, professionalism
3. **Teamwork** - Collaboration, supportiveness, adaptability
4. **Initiative** - Proactiveness, problem-solving
5. **Quality** - Attention to detail, accuracy
6. **Overall** - General impression

## Environment Variables (.env)

```bash
SECRET_KEY=your-secret-key
DATABASE_URL=sqlite:///database/volunteers.db
SMARTSHEET_API_TOKEN=your-token
SMARTSHEET_SHEET_ID=your-sheet-id
```

## Troubleshooting

### Database Issues
```bash
# Reset database
rm -rf database/
flask init-db
flask run-migrations
```

### Port Already in Use
```bash
flask run --port 5001
```

### Module Not Found
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Migrations Not Working
```bash
# Run manually
sqlite3 database/volunteers.db < migrations/001_create_roles_table.sql
```

## Documentation Files

- **README.md** - Complete documentation
- **QUICKSTART.md** - 5-minute setup
- **PROJECT_OVERVIEW.md** - Architecture
- **TESTING_GUIDE.md** - Testing procedures
- **DEPLOYMENT_CHECKLIST.md** - Production deployment
- **ROLES_FEATURE.md** - Roles system documentation
- **ROLES_UPDATE_SUMMARY.md** - Recent changes
- **QUICK_REFERENCE.md** - This file

## Quick Setup (New Installation)

```bash
# 1. Navigate to project
cd volunteer-eval-system

# 2. Run setup
./setup.sh

# 3. Activate environment
source venv/bin/activate

# 4. Initialize database
flask init-db

# 5. Run migrations
flask run-migrations

# 6. Create admin
flask create-admin

# 7. Start app
flask run

# 8. Visit http://localhost:5000
```

## Quick Setup (Existing Installation - Add Roles)

```bash
# 1. Activate environment
source venv/bin/activate

# 2. Run migrations
flask run-migrations

# 3. Verify roles
flask list-roles

# 4. Restart app
flask run
```

## Support Resources

- GitHub Issues: Report bugs
- Documentation: See docs folder
- Flask Docs: https://flask.palletsprojects.com/
- SQLAlchemy Docs: https://docs.sqlalchemy.org/

---

**Quick Tip**: Use `flask --help` to see all available commands!
