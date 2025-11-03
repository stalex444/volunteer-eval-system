-- Migration: Create roles table
-- Description: Add roles table to track different volunteer positions and their requirements
-- Created: 2025-11-02

CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role_id TEXT UNIQUE NOT NULL,  -- e.g., ROLE-001
    role_name TEXT NOT NULL,  -- GL, GLA, GG, Doors, RR, HST, HSL, FTVL, Medical, Door Lead, RR Lead, Medical Lead, GC Lead
    description TEXT,
    key_skills TEXT,
    interaction_level TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create index on role_id for faster lookups
CREATE INDEX IF NOT EXISTS idx_roles_role_id ON roles(role_id);

-- Create index on role_name for filtering
CREATE INDEX IF NOT EXISTS idx_roles_role_name ON roles(role_name);

-- Insert sample roles
INSERT INTO roles (role_id, role_name, description, key_skills, interaction_level) VALUES
('ROLE-001', 'GL', 'Greeter/Liaison - First point of contact for attendees', 'Communication, Welcoming, Problem-solving', 'High'),
('ROLE-002', 'GLA', 'Greeter/Liaison Assistant', 'Communication, Support, Teamwork', 'High'),
('ROLE-003', 'GG', 'Greeter/Gatekeeper', 'Crowd management, Communication, Attention to detail', 'High'),
('ROLE-004', 'Doors', 'Door Management', 'Security awareness, Communication, Reliability', 'Medium'),
('ROLE-005', 'RR', 'Registration/Reception', 'Data entry, Communication, Organization', 'High'),
('ROLE-006', 'HST', 'Hospitality Team', 'Customer service, Multitasking, Friendliness', 'High'),
('ROLE-007', 'HSL', 'Hospitality Support/Lead', 'Leadership, Organization, Problem-solving', 'High'),
('ROLE-008', 'FTVL', 'First Time Visitor Liaison', 'Welcoming, Communication, Empathy', 'High'),
('ROLE-009', 'Medical', 'Medical Support', 'First aid, Calm under pressure, Medical knowledge', 'Medium'),
('ROLE-010', 'Door Lead', 'Door Team Leader', 'Leadership, Security, Communication', 'Medium'),
('ROLE-011', 'RR Lead', 'Registration/Reception Lead', 'Leadership, Organization, Training', 'High'),
('ROLE-012', 'Medical Lead', 'Medical Team Leader', 'Medical expertise, Leadership, Emergency response', 'Medium'),
('ROLE-013', 'GC Lead', 'Guest Care Lead', 'Leadership, Empathy, Problem-solving', 'High');
