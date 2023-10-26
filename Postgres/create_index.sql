begin transaction;

CREATE INDEX idx_tracks_search_gin ON tracks USING gin(to_tsvector('english', track_artist || ' ' || track_name || ' ' || track_album_name || ' ' || playlist_name || ' ' || playlist_genre || ' ' || lyrics)) WITH (fastupdate = off);


commit;
