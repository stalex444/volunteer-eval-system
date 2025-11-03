-- Migration: Create events table
-- Description: Add events table to track volunteer service events
-- Created: 2025-11-02

CREATE TABLE IF NOT EXISTS events (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    event_id TEXT UNIQUE NOT NULL,  -- e.g., EVENT-001
    event_name TEXT NOT NULL,
    event_date DATE NOT NULL,
    event_type TEXT,  -- e.g., Sunday Service, Special Event, Conference
    description TEXT,
    location TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create indexes
CREATE INDEX IF NOT EXISTS idx_events_event_id ON events(event_id);
CREATE INDEX IF NOT EXISTS idx_events_event_date ON events(event_date);
CREATE INDEX IF NOT EXISTS idx_events_event_type ON events(event_type);

-- Insert sample events
INSERT INTO events (event_id, event_name, event_date, event_type, description, location) VALUES
('EVENT-001', 'Sunday Service - Week 1', '2024-01-07', 'Sunday Service', 'Regular Sunday service', 'Main Campus'),
('EVENT-002', 'Sunday Service - Week 2', '2024-01-14', 'Sunday Service', 'Regular Sunday service', 'Main Campus'),
('EVENT-003', 'Sunday Service - Week 3', '2024-01-21', 'Sunday Service', 'Regular Sunday service', 'Main Campus'),
('EVENT-004', 'Sunday Service - Week 4', '2024-01-28', 'Sunday Service', 'Regular Sunday service', 'Main Campus'),
('EVENT-005', 'Special Conference', '2024-02-10', 'Conference', 'Annual leadership conference', 'Convention Center'),
('EVENT-006', 'Community Outreach', '2024-02-17', 'Special Event', 'Community service event', 'Community Center'),
('EVENT-007', 'Youth Event', '2024-03-02', 'Special Event', 'Youth ministry event', 'Youth Building');
