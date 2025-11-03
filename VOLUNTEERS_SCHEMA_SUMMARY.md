# Volunteers Table Schema Update - Summary

## What Changed

The volunteers table has been restructured to match your new requirements.

## New Schema

```sql
CREATE TABLE volunteers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT,
    phone TEXT,
    date_first_volunteered DATE,
    status TEXT DEFAULT 'Active',  -- Active, Inactive
    preferred_roles TEXT,  -- JSON array of role IDs
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Key Features

### 1. Separate Name Fields
- `first_name` and `last_name` instead of single `name` field
- New `full_name` property: `volunteer.full_name` returns "First Last"

### 2. Preferred Roles (JSON Array)
- Store multiple role preferences per volunteer
- Format: `["ROLE-001", "ROLE-005", "ROLE-008"]`
- Helper methods:
  - `volunteer.get_preferred_roles()` - Returns list
  - `volunteer.set_preferred_roles(['ROLE-001'])` - Sets roles

### 3. Cleaner Date Field
- `date_first_volunteered` instead of `start_date`
- More descriptive and accurate

### 4. Simplified Status
- Values: `'Active'` or `'Inactive'` (capitalized)
- Default: `'Active'`

## Files Created/Modified

### New Files (2)
1. **`migrations/003_update_volunteers_schema.sql`**
   - Recreates volunteers table with new schema
   - Migrates existing data (splits names)
   - Creates indexes

2. **`SCHEMA_UPDATE.md`**
   - Complete migration guide
   - Code examples
   - Breaking changes documentation

### Modified Files (2)
1. **`models.py`**
   - Updated `Volunteer` model
   - Added `full_name` property
   - Added `get_preferred_roles()` and `set_preferred_roles()` methods

2. **`app.py`**
   - Updated `seed_data()` command with new schema

## Quick Start

### For New Installations
```bash
./setup.sh
flask init-db
flask run-migrations
flask seed-data
flask run
```

### For Existing Installations
```bash
# BACKUP FIRST!
cp database/volunteers.db database/volunteers.db.backup

# Run migration
flask run-migrations

# Verify
flask list-roles
```

## Usage Examples

### Create Volunteer
```python
from models import db, Volunteer
import json

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
```

### Query Volunteers
```python
# Get volunteer
volunteer = Volunteer.query.get(1)
print(volunteer.full_name)  # "Sarah Williams"
print(volunteer.get_preferred_roles())  # ['ROLE-001', 'ROLE-006']

# Filter by status
active = Volunteer.query.filter_by(status='Active').all()
```

### Update Preferred Roles
```python
# Set new roles
volunteer.set_preferred_roles(['ROLE-001', 'ROLE-005', 'ROLE-008'])

# Add a role
roles = volunteer.get_preferred_roles()
roles.append('ROLE-009')
volunteer.set_preferred_roles(roles)

# Remove a role
roles = volunteer.get_preferred_roles()
roles.remove('ROLE-001')
volunteer.set_preferred_roles(roles)

db.session.commit()
```

## Sample Data

The seed command now creates volunteers with the new schema:

```python
Volunteer(
    first_name='John',
    last_name='Doe',
    email='john@example.com',
    phone='555-0101',
    date_first_volunteered=date(2024, 1, 15),
    status='Active',
    preferred_roles='["ROLE-001", "ROLE-005"]'  # GL, RR
)
```

## API Response Format

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

## Breaking Changes

### What No Longer Works

❌ `volunteer.name` → ✅ Use `volunteer.full_name`
❌ `volunteer.start_date` → ✅ Use `volunteer.date_first_volunteered`
❌ `volunteer.role` → ✅ Use `volunteer.get_preferred_roles()`
❌ `volunteer.department` → ✅ Removed (not in new schema)
❌ `status='active'` → ✅ Use `status='Active'` (capitalized)

## Migration Notes

### Data Transformation

The migration automatically:
- Splits `name` into `first_name` and `last_name` (on first space)
- Renames `start_date` to `date_first_volunteered`
- Converts status values to capitalized format
- Preserves all evaluations (foreign key maintained)

### What's Removed

These fields are no longer in the schema:
- `department` - Removed
- `role` (text field) - Replaced with `preferred_roles` (JSON)
- `role_id` - Replaced with `preferred_roles` array
- `smartsheet_id` - Removed
- `updated_at` - Removed

## Next Steps

### Required Updates

To fully integrate the new schema, update:

1. **Templates** - Use `volunteer.full_name` instead of `volunteer.name`
2. **API Routes** - Return new field names
3. **Forms** - Update volunteer creation/edit forms
4. **Analytics** - Update queries to use new field names
5. **Reports** - Update report generation

### Recommended Enhancements

- Add volunteer creation form with first/last name fields
- Add role selection UI for preferred roles
- Display preferred roles in volunteer profiles
- Filter volunteers by preferred roles
- Add role assignment workflow

## Testing

After migration, verify:

- ✅ Volunteers display with full names
- ✅ Preferred roles save and load correctly
- ✅ Evaluations still link to volunteers
- ✅ Status filtering works
- ✅ API returns correct data
- ✅ Forms work with new fields

## Documentation

Complete documentation available:
- **`SCHEMA_UPDATE.md`** - Detailed migration guide
- **`models.py`** - Model code with comments
- **`migrations/003_update_volunteers_schema.sql`** - SQL migration

## Support

For questions:
1. Review `SCHEMA_UPDATE.md` for details
2. Check migration SQL file
3. Test on development environment first
4. Backup before migrating production

---

**Status**: ✅ Schema updated and ready to use!

**Next**: Run `flask run-migrations` to apply changes
