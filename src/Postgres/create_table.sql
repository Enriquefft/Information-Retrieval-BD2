CREATE DOMAIN SPOTIFY_ID AS VARCHAR(22) 
CONSTRAINT valid_chars CHECK (VALUE ~ '^[0-9A-Za-z]{22}$');

BEGIN TRANSACTION;

DROP TABLE IF EXISTS tracks;

CREATE TABLE tracks (
    track_id SPOTIFY_ID PRIMARY KEY,
    track_name TEXT,
    track_artist TEXT,
    lyrics TEXT,
    track_popularity INT,
    track_album_id SPOTIFY_ID,
    track_album_name TEXT,
    track_album_release_date VARCHAR(20),
    playlist_name TEXT,
    playlist_id SPOTIFY_ID,
    playlist_genre TEXT,
    playlist_subgenre TEXT,
    danceability FLOAT,
    energy FLOAT,
    key INT,
    loudness FLOAT,
    mode INT,
    speechiness FLOAT,
    acousticness FLOAT,
    instrumentalness FLOAT,
    liveness FLOAT,
    valence FLOAT,
    tempo FLOAT,
    duration_ms INT,
    language VARCHAR(30)
);

COMMIT;
