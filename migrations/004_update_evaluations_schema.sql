-- Migration: Update evaluations table schema
-- Description: Restructure evaluations table with 1-10 scale and new fields
-- Created: 2025-11-02
-- Note: SQLite has limited ALTER TABLE support, so we need to recreate the table

-- Step 1: Create new evaluations table with updated schema
CREATE TABLE evaluations_new (
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

-- Step 2: Copy and transform data from old table to new table
-- Convert 1-5 scale to 1-10 scale (multiply by 2)
INSERT INTO evaluations_new (
    id,
    evaluation_id,
    volunteer_id,
    role_id,
    event_id,
    date_of_service,
    reliability,
    quality_of_work,
    initiative,
    teamwork,
    communication,
    strengths,
    areas_for_improvement,
    additional_comments,
    evaluator_name,
    evaluator_email,
    submitted_at
)
SELECT 
    id,
    'EVAL-' || printf('%05d', id) as evaluation_id,
    volunteer_id,
    NULL as role_id,  -- Will need to be populated manually
    NULL as event_id,
    evaluation_date as date_of_service,
    reliability_rating * 2 as reliability,
    quality_rating * 2 as quality_of_work,
    initiative_rating * 2 as initiative,
    teamwork_rating * 2 as teamwork,
    communication_rating * 2 as communication,
    strengths,
    areas_for_improvement,
    additional_comments,
    evaluator_name,
    evaluator_email,
    created_at as submitted_at
FROM evaluations;

-- Step 3: Drop old table
DROP TABLE evaluations;

-- Step 4: Rename new table to evaluations
ALTER TABLE evaluations_new RENAME TO evaluations;

-- Step 5: Create indexes
CREATE INDEX IF NOT EXISTS idx_evaluations_evaluation_id ON evaluations(evaluation_id);
CREATE INDEX IF NOT EXISTS idx_evaluations_volunteer_id ON evaluations(volunteer_id);
CREATE INDEX IF NOT EXISTS idx_evaluations_role_id ON evaluations(role_id);
CREATE INDEX IF NOT EXISTS idx_evaluations_event_id ON evaluations(event_id);
CREATE INDEX IF NOT EXISTS idx_evaluations_date ON evaluations(date_of_service);
CREATE INDEX IF NOT EXISTS idx_evaluations_submitted_at ON evaluations(submitted_at);
