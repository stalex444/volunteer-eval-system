-- Migration: Add role_id to volunteers table
-- Description: Add foreign key relationship between volunteers and roles
-- Created: 2025-11-02

-- Add role_id column to volunteers table
ALTER TABLE volunteers ADD COLUMN role_id INTEGER REFERENCES roles(id);

-- Create index on role_id for faster lookups
CREATE INDEX IF NOT EXISTS idx_volunteers_role_id ON volunteers(role_id);

-- Optional: Migrate existing role text data to new roles table
-- This is a manual step that should be done carefully based on your data
-- Example:
-- UPDATE volunteers SET role_id = (SELECT id FROM roles WHERE role_name = volunteers.role) WHERE role IS NOT NULL;
