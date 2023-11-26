begin transaction;

DROP INDEX IF EXISTS idx_tracks_search_gin;
CREATE INDEX idx_tracks_search_gin ON tracks USING gin(to_tsvector('english', lyrics)) WITH (fastupdate = off);


commit;
