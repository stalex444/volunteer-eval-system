# Roles Feature Documentation

## Overview

The roles table has been added to track different volunteer positions with their requirements, skills, and interaction levels.

## Database Schema

### Roles Table
```sql
CREATE TABLE roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_id TEXT UNIQUE NOT NULL,        -- e.g., ROLE-001
    role_name TEXT NOT NULL,             -- GL, GLA, GG, Doors, etc.
    description TEXT,
    key_skills TEXT,
    interaction_level TEXT,              -- High, Medium, Low
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### Volunteers Table (Updated)
- Added `role_id` column as foreign key to `roles.id`
- Kept existing `role` column for backward compatibility

## Pre-defined Roles

The system comes with 13 pre-defined volunteer roles:

| Role ID   | Role Name    | Description                                    | Interaction Level |
|-----------|--------------|------------------------------------------------|-------------------|
| ROLE-001  | GL           | Greeter/Liaison - First point of contact       | High              |
| ROLE-002  | GLA          | Greeter/Liaison Assistant                      | High              |
| ROLE-003  | GG           | Greeter/Gatekeeper                             | High              |
| ROLE-004  | Doors        | Door Management                                | Medium            |
| ROLE-005  | RR           | Registration/Reception                         | High              |
| ROLE-006  | HST          | Hospitality Team                               | High              |
| ROLE-007  | HSL          | Hospitality Support/Lead                       | High              |
| ROLE-008  | FTVL         | First Time Visitor Liaison                     | High              |
| ROLE-009  | Medical      | Medical Support                                | Medium            |
| ROLE-010  | Door Lead    | Door Team Leader                               | Medium            |
| ROLE-011  | RR Lead      | Registration/Reception Lead                    | High              |
| ROLE-012  | Medical Lead | Medical Team Leader                            | Medium            |
| ROLE-013  | GC Lead      | Guest Care Lead                                | High              |

## Setup Instructions

### 1. Run Database Migrations

After setting up your environment, run the migrations to create the roles table:

```bash
# Activate virtual environment
source venv/bin/activate

# Initialize database (if not already done)
flask init-db

# Run migrations to create roles table
flask run-migrations
```

### 2. Verify Roles

List all available roles:

```bash
flask list-roles
```

Expected output:
```
Available Volunteer Roles:
--------------------------------------------------------------------------------
ID           Name                 Interaction     Description
--------------------------------------------------------------------------------
ROLE-001     GL                   High            Greeter/Liaison - First point of contact...
ROLE-002     GLA                  High            Greeter/Liaison Assistant
...
--------------------------------------------------------------------------------
Total: 13 roles
```

## Usage in Code

### Query Volunteers with Roles

```python
from models import Volunteer, Role

# Get volunteer with role information
volunteer = Volunteer.query.get(1)
if volunteer.role_info:
    print(f"Role: {volunteer.role_info.role_name}")
    print(f"Skills needed: {volunteer.role_info.key_skills}")
    print(f"Interaction level: {volunteer.role_info.interaction_level}")

# Get all volunteers for a specific role
role = Role.query.filter_by(role_name='GL').first()
volunteers = role.volunteers.all()
```

### Assign Role to Volunteer

```python
from models import db, Volunteer, Role

volunteer = Volunteer.query.get(1)
role = Role.query.filter_by(role_name='GL').first()

volunteer.role_id = role.id
db.session.commit()
```

### Create New Role

```python
from models import db, Role

new_role = Role(
    role_id='ROLE-014',
    role_name='Tech Support',
    description='Provides technical assistance',
    key_skills='Technical knowledge, Problem-solving, Patience',
    interaction_level='Medium'
)

db.session.add(new_role)
db.session.commit()
```

## API Integration

### Get Roles via API

Add to `routes/api_routes.py`:

```python
@api_bp.route('/roles', methods=['GET'])
@login_required
def get_roles():
    """Get all volunteer roles"""
    roles = Role.query.order_by(Role.role_name).all()
    
    return jsonify([{
        'id': r.id,
        'role_id': r.role_id,
        'role_name': r.role_name,
        'description': r.description,
        'key_skills': r.key_skills,
        'interaction_level': r.interaction_level,
        'volunteer_count': r.volunteers.count()
    } for r in roles])
```

## Dashboard Integration

### Display Role Information in Volunteer Profile

Update `templates/volunteer-profile.html`:

```html
{% if volunteer.role_info %}
<div class="role-info">
    <h3>Assigned Role</h3>
    <div class="role-details">
        <p><strong>Role:</strong> {{ volunteer.role_info.role_name }}</p>
        <p><strong>Description:</strong> {{ volunteer.role_info.description }}</p>
        <p><strong>Key Skills:</strong> {{ volunteer.role_info.key_skills }}</p>
        <p><strong>Interaction Level:</strong> 
            <span class="badge badge-{{ volunteer.role_info.interaction_level|lower }}">
                {{ volunteer.role_info.interaction_level }}
            </span>
        </p>
    </div>
</div>
{% endif %}
```

### Filter Volunteers by Role

Add role filter to volunteers list:

```python
@dashboard_bp.route('/volunteers')
@login_required
def volunteers_list():
    role_id = request.args.get('role_id', type=int)
    
    query = Volunteer.query
    
    if role_id:
        query = query.filter_by(role_id=role_id)
    
    volunteers = query.order_by(Volunteer.name).all()
    roles = Role.query.order_by(Role.role_name).all()
    
    return render_template(
        'volunteers-list.html',
        volunteers=volunteers,
        roles=roles,
        selected_role_id=role_id
    )
```

## Migration Notes

### Backward Compatibility

- The existing `role` text field is preserved for backward compatibility
- New implementations should use `role_id` foreign key
- Gradually migrate data from `role` to `role_id`

### Data Migration Script

To migrate existing role text data to the new roles table:

```python
@app.cli.command()
def migrate_roles():
    """Migrate existing role text data to roles table"""
    volunteers = Volunteer.query.filter(Volunteer.role.isnot(None)).all()
    
    for volunteer in volunteers:
        # Try to find matching role
        role = Role.query.filter_by(role_name=volunteer.role).first()
        
        if role:
            volunteer.role_id = role.id
            print(f"Migrated {volunteer.name} to role {role.role_name}")
        else:
            print(f"Warning: No matching role found for {volunteer.name} ({volunteer.role})")
    
    db.session.commit()
    print("Role migration complete!")
```

Run with:
```bash
flask migrate-roles
```

## Flask CLI Commands

### Available Commands

```bash
# Initialize database
flask init-db

# Run all migrations
flask run-migrations

# List all roles
flask list-roles

# Create admin user
flask create-admin

# Seed sample data
flask seed-data

# Migrate existing role data (custom command)
flask migrate-roles
```

## Troubleshooting

### Migration Fails

If migrations fail:

1. Check database permissions
2. Backup your database first
3. Run migrations one at a time manually:
   ```bash
   sqlite3 database/volunteers.db < migrations/001_create_roles_table.sql
   ```

### Role Not Found

If roles are not showing up:

1. Verify migrations ran successfully: `flask list-roles`
2. Check database: `sqlite3 database/volunteers.db "SELECT * FROM roles;"`
3. Re-run migrations if needed: `flask run-migrations`

### Foreign Key Constraint Errors

If you get foreign key errors:

1. Ensure roles table exists before adding volunteers
2. Use valid role_id values when assigning roles
3. Check that SQLite foreign key support is enabled

## Best Practices

1. **Always use role_id** for new code instead of the legacy `role` text field
2. **Validate role assignments** before saving to database
3. **Keep role definitions updated** as your organization evolves
4. **Document custom roles** if you add new ones
5. **Backup before migrations** especially in production

## Future Enhancements

Potential improvements to the roles system:

- [ ] Role-based permissions and access control
- [ ] Role requirements (certifications, training)
- [ ] Role scheduling and availability
- [ ] Role performance metrics
- [ ] Role progression paths
- [ ] Multi-role assignments per volunteer
- [ ] Role-specific evaluation criteria
- [ ] Role capacity planning

## Support

For questions or issues with the roles feature:

1. Check this documentation
2. Review migration files in `migrations/`
3. Check Flask CLI help: `flask --help`
4. Review code comments in `models.py`
