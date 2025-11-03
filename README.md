# Volunteer Evaluation System

A comprehensive web application for collecting and analyzing volunteer performance evaluations.

## Features

### Public Evaluation Form
- Simple, user-friendly interface for staff to submit volunteer evaluations
- 5-point rating scale across multiple performance categories:
  - Reliability
  - Communication
  - Teamwork
  - Initiative
  - Quality of Work
  - Overall Performance
- Qualitative feedback fields for strengths, areas for improvement, and additional comments

### Leadership Dashboard
- Secure login for authorized users
- Overview statistics (total volunteers, evaluations, averages)
- Top performers identification
- Department-level performance summaries
- Recent evaluations feed
- Detailed volunteer profiles with:
  - Performance statistics
  - Trend analysis
  - Category-specific ratings
  - Complete evaluation history

### API Endpoints
- RESTful API for programmatic access to volunteer and evaluation data
- JSON responses for easy integration with other systems
- Filtering and search capabilities

### Data Import
- Smartsheet integration for importing volunteer data
- Automatic synchronization of volunteer information

## Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLite (easily upgradeable to PostgreSQL)
- **Authentication**: Flask-Login
- **Frontend**: HTML, CSS, JavaScript
- **Analytics**: NumPy, Pandas

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Setup Steps

1. **Clone or navigate to the project directory**
   ```bash
   cd volunteer-eval-system
   ```

2. **Create a virtual environment**
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env and add your configuration
   ```

5. **Initialize the database**
   ```bash
   flask init-db
   ```

6. **Create an admin user**
   ```bash
   flask create-admin
   ```

7. **(Optional) Seed sample data**
   ```bash
   flask seed-data
   ```

8. **Run the application**
   ```bash
   flask run
   ```

The application will be available at `http://localhost:5000`

## Usage

### For Staff (Submitting Evaluations)
1. Navigate to the home page
2. Click "Submit Evaluation"
3. Fill out the evaluation form
4. Submit - no login required!

### For Leadership (Viewing Dashboard)
1. Navigate to `/login`
2. Enter your credentials
3. Access the dashboard to view:
   - Overall statistics
   - Individual volunteer profiles
   - Performance trends
   - Department summaries

## Configuration

### Environment Variables

Create a `.env` file with the following variables:

```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///database/volunteers.db
SMARTSHEET_API_TOKEN=your-smartsheet-api-token
SMARTSHEET_SHEET_ID=your-sheet-id
```

### Smartsheet Integration

To enable Smartsheet integration:
1. Obtain an API token from Smartsheet
2. Get your sheet ID from the sheet URL
3. Add both to your `.env` file
4. The system will automatically sync volunteer data

## Database Schema

### Users
- Leadership users with dashboard access
- Roles: viewer, admin

### Volunteers
- Name, email, phone, department, role
- Status (active/inactive)
- Smartsheet integration ID

### Evaluations
- Linked to volunteers
- Evaluator information
- Rating categories (1-5 scale)
- Qualitative feedback
- Timestamps

### Evaluation Periods
- Define time periods for tracking
- Enable period-based reporting

## API Documentation

### Get All Volunteers
```
GET /api/volunteers
Query params: status, department
```

### Get Volunteer Details
```
GET /api/volunteers/<id>
```

### Get Evaluations
```
GET /api/evaluations
Query params: volunteer_id, limit
```

### Get Statistics
```
GET /api/stats
Query params: period (days)
```

## Development

### Project Structure
```
volunteer-eval-system/
├── app.py                      # Main Flask application
├── config.py                   # Configuration settings
├── models.py                   # Database models
├── requirements.txt            # Python dependencies
├── routes/                     # Route blueprints
│   ├── evaluation_routes.py   # Public evaluation form
│   ├── dashboard_routes.py    # Leadership dashboard
│   └── api_routes.py          # API endpoints
├── utils/                      # Utility functions
│   ├── analytics.py           # Performance calculations
│   └── data_import.py         # Smartsheet integration
├── templates/                  # HTML templates
├── static/                     # CSS, JS, images
└── database/                   # SQLite database (auto-created)
```

### Adding New Features

1. **New Routes**: Add to appropriate blueprint in `routes/`
2. **New Models**: Update `models.py` and run migrations
3. **New Analytics**: Add functions to `utils/analytics.py`
4. **New Templates**: Add to `templates/` directory

## Security Considerations

- Change the `SECRET_KEY` in production
- Use HTTPS in production
- Implement rate limiting for public forms
- Regular database backups
- Consider upgrading to PostgreSQL for production

## Future Enhancements

- [ ] Email notifications for new evaluations
- [ ] Export reports to PDF
- [ ] Advanced analytics and visualizations
- [ ] Multi-language support
- [ ] Mobile app
- [ ] Integration with more platforms (Google Sheets, Airtable)
- [ ] Automated performance reports
- [ ] Volunteer self-service portal

## License

MIT License - feel free to use and modify for your organization's needs.

## Support

For issues or questions, please contact your system administrator.
