begin transaction;

-- Inverse index
DROP INDEX IF EXISTS idx_tracks_search_gin;
CREATE INDEX idx_tracks_search_gin ON tracks USING gin(to_tsvector('english', lyrics)) WITH (fastupdate = off);

-- trigram index

-- Add extension if not already added

CREATE EXTENSION IF NOT EXISTS pg_trgm;

DROP INDEX IF EXISTS idx_tracks_search_trgm;
CREATE INDEX idx_tracks_search_trgm ON tracks USING gin(track_name gin_trgm_ops);

commit;
