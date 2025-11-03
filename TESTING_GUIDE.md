# Testing Guide

## Manual Testing Checklist

### Initial Setup Testing

- [ ] Virtual environment creates successfully
- [ ] All dependencies install without errors
- [ ] Database initializes correctly
- [ ] Admin user creation works
- [ ] Sample data seeds properly
- [ ] Application starts without errors

### Public Evaluation Form Testing

#### Form Display
- [ ] Form loads at `/` and `/evaluate`
- [ ] All form fields are visible
- [ ] Volunteer dropdown populates
- [ ] Rating scales display correctly (1-5)
- [ ] All 6 rating categories present

#### Form Validation
- [ ] Required fields enforce validation
- [ ] Cannot submit without selecting volunteer
- [ ] Cannot submit without all ratings
- [ ] Email field accepts valid emails only
- [ ] Form shows error messages appropriately

#### Form Submission
- [ ] Successful submission shows success message
- [ ] Data saves to database correctly
- [ ] Form clears after submission
- [ ] Can submit multiple evaluations
- [ ] Evaluator information saves correctly

### Authentication Testing

#### Login
- [ ] Login page loads at `/login`
- [ ] Valid credentials allow login
- [ ] Invalid credentials show error
- [ ] Redirects to dashboard after login
- [ ] Session persists across page loads

#### Logout
- [ ] Logout button works
- [ ] Session clears properly
- [ ] Redirects to public page
- [ ] Cannot access dashboard after logout

#### Authorization
- [ ] Dashboard requires login
- [ ] API endpoints require authentication
- [ ] Unauthenticated users redirect to login
- [ ] Public form accessible without login

### Dashboard Testing

#### Overview Page
- [ ] Statistics display correctly
- [ ] Total volunteers count accurate
- [ ] Total evaluations count accurate
- [ ] Top performers list shows correctly
- [ ] Department summary displays
- [ ] Recent evaluations feed works

#### Volunteer List
- [ ] All volunteers display
- [ ] Department filter works
- [ ] Status filter works
- [ ] Sorting functionality works
- [ ] Links to profiles work

#### Volunteer Profile
- [ ] Profile loads with correct data
- [ ] Contact information displays
- [ ] Statistics calculate correctly
- [ ] Average ratings show properly
- [ ] Evaluation history displays
- [ ] Trend indicator shows (if applicable)
- [ ] Qualitative feedback displays

### API Testing

Test with curl or Postman (requires authentication):

#### Get All Volunteers
```bash
curl -X GET http://localhost:5000/api/volunteers \
  -H "Cookie: session=YOUR_SESSION_COOKIE"
```
- [ ] Returns JSON array
- [ ] Includes all volunteer data
- [ ] Filters work (status, department)

#### Get Volunteer Details
```bash
curl -X GET http://localhost:5000/api/volunteers/1 \
  -H "Cookie: session=YOUR_SESSION_COOKIE"
```
- [ ] Returns single volunteer
- [ ] Includes evaluations
- [ ] Shows statistics

#### Get Evaluations
```bash
curl -X GET http://localhost:5000/api/evaluations \
  -H "Cookie: session=YOUR_SESSION_COOKIE"
```
- [ ] Returns evaluation list
- [ ] Filtering by volunteer_id works
- [ ] Limit parameter works

#### Get Statistics
```bash
curl -X GET http://localhost:5000/api/stats?period=30 \
  -H "Cookie: session=YOUR_SESSION_COOKIE"
```
- [ ] Returns statistics
- [ ] Period parameter works
- [ ] Calculations are accurate

### Analytics Testing

#### Volunteer Statistics
- [ ] Average ratings calculate correctly
- [ ] Trend detection works (improving/declining/stable)
- [ ] Recent performance calculates properly
- [ ] Category averages are accurate

#### Department Analytics
- [ ] Department summaries accurate
- [ ] Volunteer counts correct
- [ ] Average ratings per department correct

#### Performance Identification
- [ ] Top performers identified correctly
- [ ] Minimum evaluation threshold enforced
- [ ] Sorting by rating works

### UI/UX Testing

#### Responsive Design
- [ ] Desktop view (1920x1080)
- [ ] Laptop view (1366x768)
- [ ] Tablet view (768x1024)
- [ ] Mobile view (375x667)
- [ ] Navigation adapts to screen size

#### Visual Elements
- [ ] Rating badges color-coded correctly
- [ ] Status badges display properly
- [ ] Tables are readable
- [ ] Forms are well-spaced
- [ ] Buttons have hover states
- [ ] Flash messages display and dismiss

#### Accessibility
- [ ] Form labels associated with inputs
- [ ] Keyboard navigation works
- [ ] Tab order is logical
- [ ] Color contrast is sufficient
- [ ] Error messages are clear

### Data Integrity Testing

#### Database Operations
- [ ] Volunteers create correctly
- [ ] Evaluations link to volunteers
- [ ] Cascade deletes work (if volunteer deleted)
- [ ] Timestamps save correctly
- [ ] Updates modify records properly

#### Data Validation
- [ ] Rating values constrained to 1-5
- [ ] Email format validated
- [ ] Required fields enforced
- [ ] Date fields handle correctly
- [ ] Status values constrained

### Edge Cases Testing

#### Empty States
- [ ] Dashboard with no data
- [ ] Volunteer with no evaluations
- [ ] Department with no volunteers
- [ ] No recent evaluations

#### Boundary Values
- [ ] Rating of 1 (minimum)
- [ ] Rating of 5 (maximum)
- [ ] Very long text in feedback fields
- [ ] Special characters in names
- [ ] Empty optional fields

#### Error Handling
- [ ] Invalid volunteer ID
- [ ] Non-existent routes (404)
- [ ] Database connection errors
- [ ] Invalid form data
- [ ] Duplicate submissions

### Performance Testing

#### Load Testing
- [ ] Multiple simultaneous form submissions
- [ ] Dashboard with 100+ volunteers
- [ ] Profile with 50+ evaluations
- [ ] API requests under load

#### Response Times
- [ ] Form submission < 1 second
- [ ] Dashboard load < 2 seconds
- [ ] Profile load < 2 seconds
- [ ] API responses < 500ms

### Security Testing

#### Authentication
- [ ] Passwords are hashed
- [ ] Sessions expire appropriately
- [ ] Cannot access dashboard without login
- [ ] SQL injection attempts fail
- [ ] XSS attempts are escaped

#### Data Protection
- [ ] Sensitive data not in URLs
- [ ] Session cookies are secure
- [ ] CSRF protection (if implemented)
- [ ] No sensitive data in error messages

## Automated Testing Setup

### Unit Tests (Future Implementation)

Create `tests/test_models.py`:
```python
import unittest
from models import Volunteer, Evaluation, User

class TestModels(unittest.TestCase):
    def test_volunteer_creation(self):
        # Test volunteer model
        pass
    
    def test_evaluation_calculations(self):
        # Test rating calculations
        pass
```

### Integration Tests (Future Implementation)

Create `tests/test_routes.py`:
```python
import unittest
from app import app

class TestRoutes(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
    
    def test_evaluation_form_loads(self):
        response = self.app.get('/evaluate')
        self.assertEqual(response.status_code, 200)
```

## Test Data

### Sample Volunteers
```python
volunteers = [
    {
        'name': 'John Doe',
        'email': 'john@example.com',
        'department': 'Operations',
        'role': 'Event Coordinator'
    },
    {
        'name': 'Jane Smith',
        'email': 'jane@example.com',
        'department': 'Marketing',
        'role': 'Social Media'
    }
]
```

### Sample Evaluations
```python
evaluation = {
    'evaluator_name': 'Test Manager',
    'evaluator_email': 'manager@example.com',
    'reliability_rating': 5,
    'communication_rating': 4,
    'teamwork_rating': 5,
    'initiative_rating': 4,
    'quality_rating': 5,
    'overall_rating': 5,
    'strengths': 'Excellent communication and teamwork',
    'areas_for_improvement': 'Could take more initiative'
}
```

## Bug Reporting Template

When you find a bug, document it:

```
**Bug Title**: Brief description

**Steps to Reproduce**:
1. Step one
2. Step two
3. Step three

**Expected Behavior**: What should happen

**Actual Behavior**: What actually happens

**Environment**:
- OS: macOS/Windows/Linux
- Python Version: 3.x
- Browser: Chrome/Firefox/Safari

**Screenshots**: If applicable

**Additional Context**: Any other relevant information
```

## Testing Checklist Summary

### Pre-Deployment
- [ ] All manual tests pass
- [ ] No console errors
- [ ] All links work
- [ ] Forms validate properly
- [ ] Authentication works
- [ ] Data persists correctly
- [ ] API endpoints functional
- [ ] Responsive design verified

### Post-Deployment
- [ ] Production database initialized
- [ ] Admin users created
- [ ] SSL/HTTPS working
- [ ] Environment variables set
- [ ] Backups configured
- [ ] Monitoring active
- [ ] Error logging working

## Continuous Testing

### Daily
- Submit test evaluation
- Check dashboard loads
- Verify recent data displays

### Weekly
- Review error logs
- Check database size
- Test all user roles
- Verify integrations (Smartsheet)

### Monthly
- Full regression testing
- Performance benchmarking
- Security audit
- Backup restoration test

## Tools & Resources

- **Browser DevTools**: Inspect elements, check console
- **Postman**: API testing
- **DB Browser for SQLite**: Database inspection
- **Python debugger**: `import pdb; pdb.set_trace()`
- **Flask Debug Toolbar**: Development debugging

## Getting Help

If tests fail:
1. Check error logs
2. Review console output
3. Verify configuration
4. Check database state
5. Consult documentation
6. Search for similar issues
