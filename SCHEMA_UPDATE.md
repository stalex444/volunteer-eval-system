# Volunteers Table Schema Update

## Overview

The volunteers table has been updated to use a cleaner, more structured schema with separate first/last name fields and JSON-based preferred roles.

## Schema Changes

### Old Schema
```sql
CREATE TABLE volunteers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE,
    phone TEXT,
    department TEXT,
    role TEXT,
    role_id INTEGER,
    start_date DATE,
    status TEXT DEFAULT 'active',
    smartsheet_id TEXT UNIQUE,
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### New Schema
```sql
CREATE TABLE volunteers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    date_first_volunteered DATE,
    status TEXT DEFAULT 'Active',
    preferred_roles TEXT,  -- JSON array of role IDs
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Key Changes

1. **Name Split**: `name` → `first_name` + `last_name`
2. **Date Field**: `start_date` → `date_first_volunteered`
3. **Status Values**: `'active'/'inactive'` → `'Active'/'Inactive'` (capitalized)
4. **Removed Fields**: `department`, `role`, `role_id`, `smartsheet_id`, `updated_at`
5. **New Field**: `preferred_roles` (JSON array of role IDs)
6. **Email**: No longer unique constraint

## Model Updates

### New Volunteer Model Properties

```python
# Properties
volunteer.full_name              # Returns "First Last"
volunteer.first_name             # First name
volunteer.last_name              # Last name
volunteer.date_first_volunteered # Date first volunteered
volunteer.preferred_roles        # JSON string of role IDs

# Methods
volunteer.get_preferred_roles()  # Returns list of role IDs
volunteer.set_preferred_roles(['ROLE-001', 'ROLE-005'])  # Set roles
```

### Usage Examples

```python
from models import db, Volunteer
import json

# Create new volunteer
volunteer = Volunteer(
    first_name='Sarah',
    last_name='Williams',
    email='sarah@example.com',
    phone='555-0104',
    status='Active'
)
volunteer.set_preferred_roles(['ROLE-001', 'ROLE-006'])
db.session.add(volunteer)
db.session.commit()

# Query volunteers
volunteer = Volunteer.query.get(1)
print(volunteer.full_name)  # "Sarah Williams"
print(volunteer.get_preferred_roles())  # ['ROLE-001', 'ROLE-006']

# Update preferred roles
volunteer.set_preferred_roles(['ROLE-001', 'ROLE-005', 'ROLE-008'])
db.session.commit()

# Filter by status
active_volunteers = Volunteer.query.filter_by(status='Active').all()
```

## Migration Process

### For New Installations

Simply run the setup as normal:

```bash
./setup.sh
flask init-db
flask run-migrations
flask create-admin
flask seed-data
flask run
```

### For Existing Installations

**⚠️ WARNING: This migration will recreate the volunteers table and may lose data!**

**Backup your database first:**

```bash
# Backup database
cp database/volunteers.db database/volunteers.db.backup
```

**Option 1: Fresh Start (Recommended for Development)**

```bash
# Remove old database
rm -rf database/
flask init-db
flask run-migrations
flask create-admin
flask seed-data
```

**Option 2: Migrate Existing Data**

```bash
# Run migration 003
flask run-migrations
```

This will:
1. Create new table structure
2. Split existing names into first/last names
3. Copy data to new table
4. Drop old table

**Note**: The migration attempts to split names on the first space. Review data after migration.

## API Changes

### Updated API Responses

```json
{
  "id": 1,
  "first_name": "John",
  "last_name": "Doe",
  "full_name": "John Doe",
  "email": "john@example.com",
  "phone": "555-0101",
  "date_first_volunteered": "2024-01-15",
  "status": "Active",
  "preferred_roles": ["ROLE-001", "ROLE-005"],
  "average_rating": 4.5,
  "evaluation_count": 10
}
```

### Update API Routes

Update `routes/api_routes.py`:

```python
@api_bp.route('/volunteers', methods=['GET'])
@login_required
def get_volunteers():
    volunteers = Volunteer.query.all()
    
    return jsonify([{
        'id': v.id,
        'first_name': v.first_name,
        'last_name': v.last_name,
        'full_name': v.full_name,
        'email': v.email,
        'phone': v.phone,
        'date_first_volunteered': v.date_first_volunteered.isoformat() if v.date_first_volunteered else None,
        'status': v.status,
        'preferred_roles': v.get_preferred_roles(),
        'average_rating': v.average_rating,
        'evaluation_count': v.evaluation_count
    } for v in volunteers])
```

## Template Updates

### Update Forms

Update `templates/evaluation-form.html`:

```html
<select id="volunteer_id" name="volunteer_id" required>
    <option value="">-- Select a volunteer --</option>
    {% for volunteer in volunteers %}
    <option value="{{ volunteer.id }}">
        {{ volunteer.full_name }} - {{ volunteer.status }}
    </option>
    {% endfor %}
</select>
```

### Update Profile Display

Update `templates/volunteer-profile.html`:

```html
<div class="profile-header">
    <h1>{{ volunteer.full_name }}</h1>
    <span class="status-badge status-{{ volunteer.status|lower }}">
        {{ volunteer.status }}
    </span>
</div>

<div class="profile-info">
    <div class="info-item">
        <label>First Name:</label>
        <span>{{ volunteer.first_name }}</span>
    </div>
    <div class="info-item">
        <label>Last Name:</label>
        <span>{{ volunteer.last_name }}</span>
    </div>
    <div class="info-item">
        <label>Email:</label>
        <span>{{ volunteer.email or 'N/A' }}</span>
    </div>
    <div class="info-item">
        <label>Phone:</label>
        <span>{{ volunteer.phone or 'N/A' }}</span>
    </div>
    <div class="info-item">
        <label>First Volunteered:</label>
        <span>{{ volunteer.date_first_volunteered.strftime('%Y-%m-%d') if volunteer.date_first_volunteered else 'N/A' }}</span>
    </div>
    <div class="info-item">
        <label>Preferred Roles:</label>
        <span>
            {% set role_ids = volunteer.get_preferred_roles() %}
            {% if role_ids %}
                {{ role_ids|join(', ') }}
            {% else %}
                Not specified
            {% endif %}
        </span>
    </div>
</div>
```

## Preferred Roles Format

The `preferred_roles` field stores a JSON array of role IDs:

```json
["ROLE-001", "ROLE-005", "ROLE-008"]
```

### Working with Preferred Roles

```python
# Get roles as list
role_ids = volunteer.get_preferred_roles()
# ['ROLE-001', 'ROLE-005']

# Get full role objects
from models import Role
roles = Role.query.filter(Role.role_id.in_(role_ids)).all()
for role in roles:
    print(f"{role.role_name}: {role.description}")

# Set new preferred roles
volunteer.set_preferred_roles(['ROLE-001', 'ROLE-006', 'ROLE-008'])
db.session.commit()

# Add a role
current_roles = volunteer.get_preferred_roles()
current_roles.append('ROLE-009')
volunteer.set_preferred_roles(current_roles)
db.session.commit()

# Remove a role
current_roles = volunteer.get_preferred_roles()
current_roles.remove('ROLE-001')
volunteer.set_preferred_roles(current_roles)
db.session.commit()
```

## Breaking Changes

### Code That Will Break

1. **Direct name access**: `volunteer.name` → Use `volunteer.full_name`
2. **Department queries**: `filter_by(department='X')` → No longer available
3. **Role text field**: `volunteer.role` → Use `volunteer.get_preferred_roles()`
4. **Start date**: `volunteer.start_date` → Use `volunteer.date_first_volunteered`
5. **Status values**: `'active'` → `'Active'`, `'inactive'` → `'Inactive'`

### Update Required In

- [ ] `routes/evaluation_routes.py` - Update volunteer queries
- [ ] `routes/dashboard_routes.py` - Update volunteer display
- [ ] `routes/api_routes.py` - Update API responses
- [ ] `templates/evaluation-form.html` - Update volunteer dropdown
- [ ] `templates/dashboard.html` - Update volunteer display
- [ ] `templates/volunteer-profile.html` - Update profile display
- [ ] `templates/volunteers-list.html` - Update list display
- [ ] `utils/analytics.py` - Update analytics queries
- [ ] `utils/data_import.py` - Update Smartsheet import

## Testing Checklist

After migration:

- [ ] Volunteers display correctly in dashboard
- [ ] Full names show properly
- [ ] Evaluation form shows volunteers
- [ ] Can create new volunteers
- [ ] Can update volunteer information
- [ ] Preferred roles save and load correctly
- [ ] API endpoints return correct data
- [ ] Filtering by status works
- [ ] Search functionality works
- [ ] Reports generate correctly

## Rollback

If you need to rollback:

```bash
# Restore backup
rm database/volunteers.db
cp database/volunteers.db.backup database/volunteers.db

# Revert code changes
git checkout models.py app.py
```

## Support

For issues with migration:

1. Check migration logs
2. Verify database backup exists
3. Review `migrations/003_update_volunteers_schema.sql`
4. Test on development environment first
5. Contact system administrator if needed

## Future Enhancements

- [ ] Add middle name field
- [ ] Add preferred contact method
- [ ] Add emergency contact information
- [ ] Add volunteer skills/certifications
- [ ] Add availability schedule
- [ ] Add volunteer preferences
