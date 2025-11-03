# Database Migrations

This directory contains SQL migration scripts for the volunteer evaluation system.

## Migration Files

- `001_create_roles_table.sql` - Creates the roles table with sample data
- `002_add_role_id_to_volunteers.sql` - Adds role_id foreign key to volunteers table

## Running Migrations

### Option 1: Using Flask CLI (Recommended)

```bash
# Run all migrations
flask run-migrations

# Run a specific migration
flask run-migration migrations/001_create_roles_table.sql
```

### Option 2: Manual Execution

```bash
# For SQLite
sqlite3 database/volunteers.db < migrations/001_create_roles_table.sql

# For PostgreSQL
psql -d volunteer_db -f migrations/001_create_roles_table.sql
```

## Creating New Migrations

1. Create a new SQL file with naming convention: `XXX_description.sql`
2. Include comments describing the migration
3. Use `IF NOT EXISTS` clauses where appropriate
4. Test the migration on a copy of the database first
5. Document any manual steps required

## Migration Best Practices

- Always backup the database before running migrations
- Test migrations on development/staging before production
- Include rollback instructions if possible
- Keep migrations small and focused
- Document any data transformations needed

## Rollback Instructions

### Rollback 002_add_role_id_to_volunteers.sql
```sql
-- Remove the role_id column
ALTER TABLE volunteers DROP COLUMN role_id;
DROP INDEX IF EXISTS idx_volunteers_role_id;
```

### Rollback 001_create_roles_table.sql
```sql
-- Drop the roles table
DROP TABLE IF EXISTS roles;
DROP INDEX IF EXISTS idx_roles_role_id;
DROP INDEX IF EXISTS idx_roles_role_name;
```

## Notes

- SQLite has limited ALTER TABLE support
- For complex schema changes, you may need to:
  1. Create new table with desired schema
  2. Copy data from old table
  3. Drop old table
  4. Rename new table
