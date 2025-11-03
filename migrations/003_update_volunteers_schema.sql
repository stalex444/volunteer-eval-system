-- Migration: Update volunteers table schema
-- Description: Restructure volunteers table to match new requirements
-- Created: 2025-11-02
-- Note: SQLite has limited ALTER TABLE support, so we need to recreate the table

-- Step 1: Create new volunteers table with updated schema
CREATE TABLE volunteers_new (
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

-- Step 2: Copy data from old table to new table
-- Splitting name into first_name and last_name
INSERT INTO volunteers_new (id, first_name, last_name, email, phone, date_first_volunteered, status, created_at)
SELECT 
    id,
    CASE 
        WHEN instr(name, ' ') > 0 THEN substr(name, 1, instr(name, ' ') - 1)
        ELSE name
    END as first_name,
    CASE 
        WHEN instr(name, ' ') > 0 THEN substr(name, instr(name, ' ') + 1)
        ELSE ''
    END as last_name,
    email,
    phone,
    start_date as date_first_volunteered,
    status,
    created_at
FROM volunteers;

-- Step 3: Drop old table
DROP TABLE volunteers;

-- Step 4: Rename new table to volunteers
ALTER TABLE volunteers_new RENAME TO volunteers;

-- Step 5: Create indexes
CREATE INDEX IF NOT EXISTS idx_volunteers_email ON volunteers(email);
CREATE INDEX IF NOT EXISTS idx_volunteers_status ON volunteers(status);
CREATE INDEX IF NOT EXISTS idx_volunteers_name ON volunteers(last_name, first_name);

-- Note: This migration will break the foreign key relationship with evaluations
-- You may need to recreate the evaluations table or handle this separately
