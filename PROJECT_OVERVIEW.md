# Volunteer Evaluation System - Project Overview

## Purpose
A web-based system for collecting, managing, and analyzing volunteer performance evaluations. Designed to streamline the feedback process and provide leadership with actionable insights.

## Key Components

### 1. Public Evaluation Form
**Purpose**: Allow staff members to submit evaluations without requiring login

**Features**:
- Clean, intuitive interface
- 5-point rating scale across 6 categories
- Qualitative feedback fields
- Volunteer selection dropdown
- Form validation

**Access**: `http://localhost:5000/evaluate`

### 2. Leadership Dashboard
**Purpose**: Provide leadership with comprehensive performance insights

**Features**:
- Overview statistics
- Top performers identification
- Department-level summaries
- Recent evaluations feed
- Trend analysis
- Detailed volunteer profiles

**Access**: `http://localhost:5000/dashboard` (requires login)

### 3. RESTful API
**Purpose**: Enable programmatic access to data

**Endpoints**:
- `/api/volunteers` - List all volunteers
- `/api/volunteers/<id>` - Get volunteer details
- `/api/evaluations` - List evaluations
- `/api/stats` - Get statistics
- `/api/departments` - List departments

**Authentication**: Required (Flask-Login)

### 4. Data Import System
**Purpose**: Sync volunteer data from Smartsheet

**Features**:
- Automatic data synchronization
- Create/update volunteers
- Preserve existing evaluations

**Configuration**: Set `SMARTSHEET_API_TOKEN` and `SMARTSHEET_SHEET_ID` in `.env`

## Technical Architecture

### Backend
- **Framework**: Flask 3.0
- **Database**: SQLAlchemy ORM with SQLite (production: PostgreSQL)
- **Authentication**: Flask-Login
- **Security**: Werkzeug password hashing

### Frontend
- **Templates**: Jinja2
- **Styling**: Custom CSS with CSS variables
- **JavaScript**: Vanilla JS (no frameworks)
- **Responsive**: Mobile-friendly design

### Database Schema

**Users Table**
- id, username, email, password_hash, role, created_at

**Volunteers Table**
- id, name, email, phone, department, role, start_date, status, smartsheet_id

**Evaluations Table**
- id, volunteer_id, evaluator info, ratings (6 categories), feedback, dates

**Evaluation Periods Table**
- id, name, start_date, end_date, is_active

## Rating Categories

1. **Reliability** - Punctuality, attendance, commitment
2. **Communication** - Clarity, responsiveness, professionalism
3. **Teamwork** - Collaboration, supportiveness, adaptability
4. **Initiative** - Proactiveness, problem-solving, self-direction
5. **Quality of Work** - Attention to detail, accuracy, thoroughness
6. **Overall Performance** - General impression

Scale: 1 (Needs Improvement) to 5 (Excellent)

## Analytics Features

### Volunteer Statistics
- Total evaluation count
- Average overall rating
- Category-specific averages
- Performance trend (improving/stable/declining)
- Recent performance (last 30 days)

### Department Analytics
- Volunteer count per department
- Average ratings by department
- Department comparisons

### Trend Analysis
- Monthly performance trends
- Historical comparisons
- Identification of patterns

### Advanced Analytics (utils/analytics.py)
- Top performers identification
- Volunteers needing attention
- Category correlation analysis
- Statistical calculations

## File Structure

```
volunteer-eval-system/
├── app.py                      # Main application & CLI commands
├── config.py                   # Configuration management
├── models.py                   # Database models
├── requirements.txt            # Python dependencies
├── .env.example                # Environment template
├── .gitignore                  # Git ignore rules
├── setup.sh                    # Automated setup script
├── README.md                   # Full documentation
├── QUICKSTART.md               # Quick start guide
├── PROJECT_OVERVIEW.md         # This file
│
├── routes/                     # Route blueprints
│   ├── __init__.py
│   ├── evaluation_routes.py   # Public form routes
│   ├── dashboard_routes.py    # Dashboard routes
│   └── api_routes.py          # API endpoints
│
├── utils/                      # Utility modules
│   ├── __init__.py
│   ├── analytics.py           # Performance calculations
│   └── data_import.py         # Smartsheet integration
│
├── templates/                  # HTML templates
│   ├── base.html              # Base template
│   ├── evaluation-form.html   # Evaluation form
│   ├── login.html             # Login page
│   ├── dashboard.html         # Main dashboard
│   ├── volunteer-profile.html # Individual profile
│   └── volunteers-list.html   # All volunteers list
│
├── static/                     # Static assets
│   ├── css/
│   │   └── style.css          # Main stylesheet
│   ├── js/
│   │   ├── evaluation-form.js # Form interactions
│   │   └── dashboard.js       # Dashboard functionality
│   └── images/                # Image assets
│
└── database/                   # SQLite database (auto-created)
    └── volunteers.db
```

## Deployment Considerations

### Development
- SQLite database
- Flask development server
- Debug mode enabled

### Production
- PostgreSQL database
- Gunicorn/uWSGI WSGI server
- Nginx reverse proxy
- HTTPS/SSL certificates
- Environment-based configuration
- Regular database backups
- Rate limiting on public endpoints
- Monitoring and logging

## Security Features

- Password hashing (Werkzeug)
- Session management (Flask-Login)
- CSRF protection (Flask-WTF recommended for production)
- SQL injection prevention (SQLAlchemy ORM)
- XSS protection (Jinja2 auto-escaping)
- Secure session cookies

## Future Enhancement Ideas

1. **Email Notifications**
   - Alert volunteers of new evaluations
   - Weekly summary reports to leadership

2. **Advanced Reporting**
   - PDF export of reports
   - Custom date range filtering
   - Comparative analysis tools

3. **Volunteer Portal**
   - Self-service access to own evaluations
   - Goal setting and tracking
   - Training recommendations

4. **Integration Expansions**
   - Google Sheets integration
   - Calendar integration for evaluation reminders
   - Slack/Teams notifications

5. **Enhanced Analytics**
   - Predictive analytics
   - Machine learning for pattern detection
   - Visualization dashboards (Chart.js, Plotly)

6. **Mobile Application**
   - Native iOS/Android apps
   - Progressive Web App (PWA)

## Customization Guide

### Changing Rating Categories
1. Edit `models.py` - Update `Evaluation` model
2. Edit `templates/evaluation-form.html` - Update form fields
3. Edit `utils/analytics.py` - Update calculations
4. Run database migration

### Adding New User Roles
1. Edit `models.py` - Update `User.role` options
2. Add role-based access control in routes
3. Update templates for role-specific features

### Modifying Styling
1. Edit `static/css/style.css`
2. Update CSS variables in `:root` for theme changes
3. Modify component styles as needed

### Adding New Pages
1. Create route in appropriate blueprint
2. Create template in `templates/`
3. Add navigation links in `base.html`

## Maintenance Tasks

### Regular
- Monitor database size
- Review and archive old evaluations
- Update volunteer statuses
- Check for security updates

### Periodic
- Database backups
- Performance optimization
- User access review
- Feature usage analysis

## Support & Documentation

- **README.md**: Complete setup and usage guide
- **QUICKSTART.md**: Fast setup instructions
- **PROJECT_OVERVIEW.md**: This architectural overview
- **Code Comments**: Inline documentation in all modules

## License
MIT License - Free to use and modify for your organization's needs.
