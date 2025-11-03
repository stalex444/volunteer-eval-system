## Evaluations Table Schema Update

## Overview

The evaluations table has been completely restructured with a 1-10 rating scale, unique evaluation IDs, and relationships to roles and events.

## New Schema

### Evaluations Table

```sql
CREATE TABLE evaluations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    evaluation_id TEXT UNIQUE NOT NULL,  -- e.g., EVAL-00001
    volunteer_id INTEGER NOT NULL,
    role_id INTEGER NOT NULL,
    event_id INTEGER,
    date_of_service DATE NOT NULL,
    
    -- Performance metrics (1-10 scale)
    reliability INTEGER CHECK(reliability >= 1 AND reliability <= 10),
    quality_of_work INTEGER CHECK(quality_of_work >= 1 AND quality_of_work <= 10),
    initiative INTEGER CHECK(initiative >= 1 AND initiative <= 10),
    teamwork INTEGER CHECK(teamwork >= 1 AND teamwork <= 10),
    communication INTEGER CHECK(communication >= 1 AND communication <= 10),
    
    -- Qualitative feedback
    strengths TEXT,
    areas_for_improvement TEXT,
    additional_comments TEXT,
    
    -- Metadata
    evaluator_name TEXT,
    evaluator_email TEXT,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (volunteer_id) REFERENCES volunteers(id),
    FOREIGN KEY (role_id) REFERENCES roles(id),
    FOREIGN KEY (event_id) REFERENCES events(id)
);
```

### Events Table (New)

```sql
CREATE TABLE events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id TEXT UNIQUE NOT NULL,  -- e.g., EVENT-001
    event_name TEXT NOT NULL,
    event_date DATE NOT NULL,
    event_type TEXT,  -- Sunday Service, Special Event, Conference
    description TEXT,
    location TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Key Changes

### Rating Scale
- **Old**: 1-5 scale (5 categories + overall)
- **New**: 1-10 scale (5 categories, no separate overall)
- **Migration**: Old ratings multiplied by 2

### Rating Categories
| Old Name | New Name | Scale |
|----------|----------|-------|
| reliability_rating | reliability | 1-10 |
| communication_rating | communication | 1-10 |
| teamwork_rating | teamwork | 1-10 |
| initiative_rating | initiative | 1-10 |
| quality_rating | quality_of_work | 1-10 |
| overall_rating | *(removed)* | - |

### New Fields
- `evaluation_id` - Unique identifier (EVAL-00001, EVAL-00002, etc.)
- `role_id` - Foreign key to roles table (which role was evaluated)
- `event_id` - Foreign key to events table (which event/service)
- `date_of_service` - Date volunteer served (replaces evaluation_date)
- `submitted_at` - When evaluation was submitted (replaces created_at)

### Removed Fields
- `overall_rating` - Use `average_rating` property instead
- `evaluator_role` - Not needed
- `evaluation_date` - Renamed to `date_of_service`
- `created_at` - Renamed to `submitted_at`

## Model Updates

### New Evaluation Model

```python
class Evaluation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    evaluation_id = db.Column(db.String(20), unique=True, nullable=False)
    volunteer_id = db.Column(db.Integer, db.ForeignKey('volunteers.id'), nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    date_of_service = db.Column(db.Date, nullable=False)
    
    # Performance metrics (1-10 scale)
    reliability = db.Column(db.Integer)
    quality_of_work = db.Column(db.Integer)
    initiative = db.Column(db.Integer)
    teamwork = db.Column(db.Integer)
    communication = db.Column(db.Integer)
    
    # Qualitative feedback
    strengths = db.Column(db.Text)
    areas_for_improvement = db.Column(db.Text)
    additional_comments = db.Column(db.Text)
    
    # Metadata
    evaluator_name = db.Column(db.String(100))
    evaluator_email = db.Column(db.String(120))
    submitted_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    volunteer = relationship to Volunteer
    role = relationship to Role
    event = relationship to Event
```

### New Event Model

```python
class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.String(20), unique=True, nullable=False)
    event_name = db.Column(db.String(200), nullable=False)
    event_date = db.Column(db.Date, nullable=False)
    event_type = db.Column(db.String(50))
    description = db.Column(db.Text)
    location = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    evaluations = relationship to Evaluation
```

## New Properties

### Evaluation.average_rating
Calculates average of all 5 performance metrics (1-10 scale):

```python
evaluation.average_rating  # Returns average of all ratings
```

### Evaluation.overall_score
Converts average rating to percentage:

```python
evaluation.overall_score  # Returns percentage (0-100)
```

## Usage Examples

### Create Evaluation

```python
from models import db, Evaluation
from datetime import date

# Generate next evaluation ID
last_eval = Evaluation.query.order_by(Evaluation.id.desc()).first()
next_num = (int(last_eval.evaluation_id.split('-')[1]) + 1) if last_eval else 1
evaluation_id = f'EVAL-{next_num:05d}'

# Create evaluation
evaluation = Evaluation(
    evaluation_id=evaluation_id,
    volunteer_id=1,
    role_id=1,  # ROLE-001
    event_id=1,  # EVENT-001
    date_of_service=date(2024, 11, 2),
    reliability=8,
    quality_of_work=9,
    initiative=7,
    teamwork=10,
    communication=8,
    strengths='Excellent communication and teamwork',
    areas_for_improvement='Could take more initiative',
    evaluator_name='John Manager',
    evaluator_email='john@example.com'
)

db.session.add(evaluation)
db.session.commit()

print(f'Average Rating: {evaluation.average_rating}')  # 8.4
print(f'Overall Score: {evaluation.overall_score}%')   # 84.0%
```

### Query Evaluations

```python
# Get evaluation with relationships
evaluation = Evaluation.query.get(1)
print(f"Volunteer: {evaluation.volunteer.full_name}")
print(f"Role: {evaluation.role.role_name}")
print(f"Event: {evaluation.event.event_name}")

# Filter by volunteer
volunteer_evals = Evaluation.query.filter_by(volunteer_id=1).all()

# Filter by role
role_evals = Evaluation.query.filter_by(role_id=1).all()

# Filter by event
event_evals = Evaluation.query.filter_by(event_id=1).all()

# Filter by date range
from datetime import datetime, timedelta
start_date = datetime.utcnow() - timedelta(days=30)
recent_evals = Evaluation.query.filter(
    Evaluation.date_of_service >= start_date
).all()
```

### Work with Events

```python
from models import db, Event
from datetime import date

# Create event
event = Event(
    event_id='EVENT-008',
    event_name='Sunday Service - Week 5',
    event_date=date(2024, 2, 4),
    event_type='Sunday Service',
    description='Regular Sunday service',
    location='Main Campus'
)
db.session.add(event)
db.session.commit()

# Get event with evaluations
event = Event.query.get(1)
evaluations = event.evaluations.all()
print(f"Event: {event.event_name}")
print(f"Total evaluations: {event.evaluations.count()}")
```

## Flask CLI Commands

### List Events

```bash
flask list-events
```

Output:
```
Available Events:
----------------------------------------------------------------------------------------------------
ID           Name                           Date         Type                 Location
----------------------------------------------------------------------------------------------------
EVENT-007    Youth Event                    2024-03-02   Special Event        Youth Building
EVENT-006    Community Outreach             2024-02-17   Special Event        Community Center
EVENT-005    Special Conference             2024-02-10   Conference           Convention Center
...
----------------------------------------------------------------------------------------------------
Total: 7 events
```

### Generate Evaluation ID

```bash
flask generate-evaluation-id
```

Output:
```
Next evaluation ID: EVAL-00042
```

## Migration Process

### For New Installations

```bash
./setup.sh
flask init-db
flask run-migrations
flask seed-data
flask run
```

### For Existing Installations

**⚠️ WARNING: This will recreate the evaluations table!**

```bash
# Backup database
cp database/volunteers.db database/volunteers.db.backup

# Run migrations
flask run-migrations

# Verify
flask list-events
```

The migration will:
1. Create events table with sample data
2. Create new evaluations table
3. Convert old ratings (1-5) to new scale (1-10) by multiplying by 2
4. Generate evaluation_ids (EVAL-00001, EVAL-00002, etc.)
5. Copy all qualitative feedback
6. Preserve volunteer relationships

## API Updates

### Updated API Response

```json
{
  "id": 1,
  "evaluation_id": "EVAL-00001",
  "volunteer": {
    "id": 1,
    "full_name": "John Doe"
  },
  "role": {
    "id": 1,
    "role_name": "GL"
  },
  "event": {
    "id": 1,
    "event_name": "Sunday Service - Week 1"
  },
  "date_of_service": "2024-11-02",
  "ratings": {
    "reliability": 8,
    "quality_of_work": 9,
    "initiative": 7,
    "teamwork": 10,
    "communication": 8,
    "average": 8.4,
    "overall_score": 84.0
  },
  "feedback": {
    "strengths": "Excellent communication",
    "areas_for_improvement": "Could take more initiative",
    "additional_comments": "Great volunteer!"
  },
  "evaluator": {
    "name": "John Manager",
    "email": "john@example.com"
  },
  "submitted_at": "2024-11-02T10:30:00"
}
```

## Template Updates

### Update Evaluation Form

```html
<!-- Rating scale changed from 1-5 to 1-10 -->
<div class="rating-group">
    <label>Reliability (1-10) *</label>
    <div class="rating-scale">
        {% for i in range(1, 11) %}
        <label class="rating-option">
            <input type="radio" name="reliability" value="{{ i }}" required>
            <span>{{ i }}</span>
        </label>
        {% endfor %}
    </div>
</div>

<!-- Add role selection -->
<div class="form-group">
    <label for="role_id">Role Performed *</label>
    <select id="role_id" name="role_id" required>
        <option value="">-- Select role --</option>
        {% for role in roles %}
        <option value="{{ role.id }}">{{ role.role_name }}</option>
        {% endfor %}
    </select>
</div>

<!-- Add event selection -->
<div class="form-group">
    <label for="event_id">Event/Service</label>
    <select id="event_id" name="event_id">
        <option value="">-- Select event --</option>
        {% for event in events %}
        <option value="{{ event.id }}">{{ event.event_name }} - {{ event.event_date }}</option>
        {% endfor %}
    </select>
</div>
```

### Update Dashboard Display

```html
<!-- Display average rating instead of overall -->
<td>
    <span class="rating-badge">
        {{ "%.1f"|format(evaluation.average_rating) }}/10
    </span>
</td>

<!-- Display role and event -->
<td>{{ evaluation.role.role_name }}</td>
<td>{{ evaluation.event.event_name if evaluation.event else 'N/A' }}</td>
```

## Breaking Changes

### Code That Will Break

1. **Rating field names**:
   - `evaluation.reliability_rating` → `evaluation.reliability`
   - `evaluation.quality_rating` → `evaluation.quality_of_work`
   - `evaluation.overall_rating` → `evaluation.average_rating`

2. **Date fields**:
   - `evaluation.evaluation_date` → `evaluation.date_of_service`
   - `evaluation.created_at` → `evaluation.submitted_at`

3. **Rating scale**:
   - Old: 1-5 scale
   - New: 1-10 scale
   - Update all display logic and calculations

4. **New required fields**:
   - `evaluation_id` - Must be unique
   - `role_id` - Must reference valid role
   - Forms must collect these fields

## Testing Checklist

- [ ] Evaluations display with 1-10 scale
- [ ] Average rating calculates correctly
- [ ] Overall score shows as percentage
- [ ] Role relationship works
- [ ] Event relationship works
- [ ] Evaluation form accepts 1-10 ratings
- [ ] Evaluation ID generates uniquely
- [ ] API returns correct data structure
- [ ] Dashboard displays correctly
- [ ] Reports calculate correctly

## Sample Event Types

Pre-defined event types:
- Sunday Service
- Special Event
- Conference
- Training
- Outreach
- Youth Event
- Community Service

## Benefits

1. **More Granular Ratings**: 1-10 scale provides better differentiation
2. **Unique IDs**: Easy tracking and reference
3. **Role Context**: Know which role was being evaluated
4. **Event Context**: Track performance by specific events
5. **Better Analytics**: More data points for analysis
6. **Cleaner Data Model**: Proper relationships and constraints

## Support

For questions:
1. Review this documentation
2. Check migration files
3. Test on development environment first
4. Use `flask list-events` to verify events
5. Use `flask generate-evaluation-id` for next ID

---

**Status**: ✅ Schema updated with 1-10 scale and event tracking!
