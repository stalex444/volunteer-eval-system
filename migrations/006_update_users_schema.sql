-- Migration: Update users table schema
-- Description: Simplify users table - remove email field, set default role to admin
-- Created: 2025-11-02
-- Note: SQLite has limited ALTER TABLE support, so we need to recreate the table

-- Step 1: Create new users table with updated schema
CREATE TABLE users_new (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL,
    role TEXT DEFAULT 'admin',  -- admin, viewer
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Step 2: Copy data from old table to new table
INSERT INTO users_new (id, username, password_hash, role, created_at)
SELECT 
    id,
    username,
    password_hash,
    role,
    created_at
FROM users;

-- Step 3: Drop old table
DROP TABLE users;

-- Step 4: Rename new table to users
ALTER TABLE users_new RENAME TO users;

-- Step 5: Create indexes
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_role ON users(role);
