-- Init Database Schema Migration
-- Version: 001_initial_schema
-- Description: Creates core tables for tracks, units, drills, progress, and attempts

-- ============================================================================
-- ENUM TYPES
-- ============================================================================

CREATE TYPE drill_type AS ENUM ('quiz', 'explain', 'debug');

-- ============================================================================
-- TRACKS TABLE
-- ============================================================================
-- High-level learning paths (e.g., "systems-foundations", "devops-basics")

CREATE TABLE tracks (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    slug TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL,
    description TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    
    CONSTRAINT tracks_slug_format CHECK (slug ~ '^[a-z0-9-]+$')
);

CREATE INDEX idx_tracks_slug ON tracks(slug);

COMMENT ON TABLE tracks IS 'High-level learning paths (e.g., systems-foundations)';
COMMENT ON COLUMN tracks.slug IS 'URL-friendly unique identifier, lowercase with hyphens';

-- ============================================================================
-- UNITS TABLE
-- ============================================================================
-- Ordered sections within a track (chapters)

CREATE TABLE units (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    track_id UUID NOT NULL REFERENCES tracks(id) ON DELETE CASCADE,
    order_index INTEGER NOT NULL,
    title TEXT NOT NULL,
    summary_markdown TEXT NOT NULL DEFAULT '',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    
    CONSTRAINT units_order_positive CHECK (order_index >= 0),
    CONSTRAINT units_unique_order_per_track UNIQUE (track_id, order_index)
);

CREATE INDEX idx_units_track_id ON units(track_id);
CREATE INDEX idx_units_track_order ON units(track_id, order_index);

COMMENT ON TABLE units IS 'Ordered sections within a track';
COMMENT ON COLUMN units.order_index IS 'Zero-based ordering within the track';

-- ============================================================================
-- DRILLS TABLE
-- ============================================================================
-- Atomic learning actions (quiz, explain, debug)

CREATE TABLE drills (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    unit_id UUID NOT NULL REFERENCES units(id) ON DELETE CASCADE,
    slug TEXT NOT NULL,
    drill_type drill_type NOT NULL,
    prompt_markdown TEXT NOT NULL,
    rubric JSONB NOT NULL DEFAULT '{}',
    difficulty INTEGER NOT NULL DEFAULT 3,
    estimated_minutes INTEGER NOT NULL DEFAULT 5,
    concept_tags TEXT[] NOT NULL DEFAULT '{}',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    
    CONSTRAINT drills_difficulty_range CHECK (difficulty >= 1 AND difficulty <= 5),
    CONSTRAINT drills_estimated_minutes_positive CHECK (estimated_minutes >= 1),
    CONSTRAINT drills_slug_format CHECK (slug ~ '^[a-z0-9-]+$'),
    CONSTRAINT drills_unique_slug_per_unit UNIQUE (unit_id, slug)
);

CREATE INDEX idx_drills_unit_id ON drills(unit_id);
CREATE INDEX idx_drills_concept_tags ON drills USING GIN(concept_tags);
CREATE INDEX idx_drills_drill_type ON drills(drill_type);
CREATE INDEX idx_drills_difficulty ON drills(difficulty);

COMMENT ON TABLE drills IS 'Atomic learning actions - quiz, explain, or debug exercises';
COMMENT ON COLUMN drills.slug IS 'Unique identifier within unit for stable content syncing';
COMMENT ON COLUMN drills.rubric IS 'JSON rubric with criteria, expected_key_points, common_mistakes';
COMMENT ON COLUMN drills.concept_tags IS 'Array of concept tags for filtering and analytics';

-- ============================================================================
-- USER DRILL PROGRESS TABLE
-- ============================================================================
-- Tracks mastery and spaced repetition scheduling per user per drill

CREATE TABLE user_drill_progress (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    drill_id UUID NOT NULL REFERENCES drills(id) ON DELETE CASCADE,
    mastery_score INTEGER NOT NULL DEFAULT 0,
    attempt_count INTEGER NOT NULL DEFAULT 0,
    last_attempt_at TIMESTAMPTZ,
    next_review_due_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    
    CONSTRAINT progress_mastery_range CHECK (mastery_score >= 0 AND mastery_score <= 5),
    CONSTRAINT progress_attempt_count_positive CHECK (attempt_count >= 0),
    CONSTRAINT progress_unique_user_drill UNIQUE (user_id, drill_id)
);

CREATE INDEX idx_progress_user_id ON user_drill_progress(user_id);
CREATE INDEX idx_progress_drill_id ON user_drill_progress(drill_id);
CREATE INDEX idx_progress_user_next_review ON user_drill_progress(user_id, next_review_due_at);
CREATE INDEX idx_progress_mastery ON user_drill_progress(user_id, mastery_score);

COMMENT ON TABLE user_drill_progress IS 'Per-user progress and spaced repetition state for each drill';
COMMENT ON COLUMN user_drill_progress.mastery_score IS 'Mastery level 0-5, determines review intervals';
COMMENT ON COLUMN user_drill_progress.next_review_due_at IS 'When this drill should next appear for review';

-- ============================================================================
-- DRILL ATTEMPTS TABLE
-- ============================================================================
-- Records each attempt at a drill with AI feedback

CREATE TABLE drill_attempts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL,
    drill_id UUID NOT NULL REFERENCES drills(id) ON DELETE CASCADE,
    user_response TEXT NOT NULL,
    ai_feedback JSONB NOT NULL DEFAULT '{}',
    score INTEGER,
    max_score INTEGER,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    
    CONSTRAINT attempts_score_valid CHECK (score IS NULL OR (score >= 0 AND (max_score IS NULL OR score <= max_score)))
);

CREATE INDEX idx_attempts_user_id ON drill_attempts(user_id);
CREATE INDEX idx_attempts_drill_id ON drill_attempts(drill_id);
CREATE INDEX idx_attempts_user_drill ON drill_attempts(user_id, drill_id);
CREATE INDEX idx_attempts_user_created ON drill_attempts(user_id, created_at DESC);
CREATE INDEX idx_attempts_created ON drill_attempts(created_at DESC);

COMMENT ON TABLE drill_attempts IS 'Historical record of all drill attempts with AI grading feedback';
COMMENT ON COLUMN drill_attempts.ai_feedback IS 'Structured feedback from AI grading (scores, justification, improvement)';

-- ============================================================================
-- UPDATED_AT TRIGGER FUNCTION
-- ============================================================================

CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = now();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Apply trigger to tables with updated_at
CREATE TRIGGER tracks_updated_at
    BEFORE UPDATE ON tracks
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER units_updated_at
    BEFORE UPDATE ON units
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER drills_updated_at
    BEFORE UPDATE ON drills
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER progress_updated_at
    BEFORE UPDATE ON user_drill_progress
    FOR EACH ROW EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- ROW LEVEL SECURITY (RLS)
-- ============================================================================

-- Enable RLS on all tables
ALTER TABLE tracks ENABLE ROW LEVEL SECURITY;
ALTER TABLE units ENABLE ROW LEVEL SECURITY;
ALTER TABLE drills ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_drill_progress ENABLE ROW LEVEL SECURITY;
ALTER TABLE drill_attempts ENABLE ROW LEVEL SECURITY;

-- Tracks: readable by all authenticated users
CREATE POLICY "Tracks are viewable by authenticated users"
    ON tracks FOR SELECT
    TO authenticated
    USING (true);

-- Units: readable by all authenticated users
CREATE POLICY "Units are viewable by authenticated users"
    ON units FOR SELECT
    TO authenticated
    USING (true);

-- Drills: readable by all authenticated users
CREATE POLICY "Drills are viewable by authenticated users"
    ON drills FOR SELECT
    TO authenticated
    USING (true);

-- User Drill Progress: users can only access their own progress
CREATE POLICY "Users can view own progress"
    ON user_drill_progress FOR SELECT
    TO authenticated
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own progress"
    ON user_drill_progress FOR INSERT
    TO authenticated
    WITH CHECK (auth.uid() = user_id);

CREATE POLICY "Users can update own progress"
    ON user_drill_progress FOR UPDATE
    TO authenticated
    USING (auth.uid() = user_id)
    WITH CHECK (auth.uid() = user_id);

-- Drill Attempts: users can only access their own attempts
CREATE POLICY "Users can view own attempts"
    ON drill_attempts FOR SELECT
    TO authenticated
    USING (auth.uid() = user_id);

CREATE POLICY "Users can insert own attempts"
    ON drill_attempts FOR INSERT
    TO authenticated
    WITH CHECK (auth.uid() = user_id);

-- Note: Attempts are append-only, no update/delete policies

-- ============================================================================
-- SERVICE ROLE POLICIES (for backend seeding)
-- ============================================================================
-- The service role bypasses RLS, so no explicit policies needed for seeding.
-- These policies allow the backend to manage content.

CREATE POLICY "Service role can manage tracks"
    ON tracks FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

CREATE POLICY "Service role can manage units"
    ON units FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

CREATE POLICY "Service role can manage drills"
    ON drills FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

CREATE POLICY "Service role can manage progress"
    ON user_drill_progress FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);

CREATE POLICY "Service role can manage attempts"
    ON drill_attempts FOR ALL
    TO service_role
    USING (true)
    WITH CHECK (true);
