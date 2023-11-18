from Download import Downloader, YOUTUBE_DL, PYTUBE
from Embed import get_mfcc_features_flatenized, get_sample_rate

from typing import Final, cast

from pathlib import Path

import numpy as np

from psycopg2 import connect
from psycopg2.extensions import connection, cursor as cursorT

from dotenv import load_dotenv
from os import getenv

import logging

# 160k * 3 floats stored in ram

playlist_id: Final[str] = '6Nqv8Mi4xKEOXBLcIbDopO'  # Reggaeton
# playlist_id: Final[str] = '3BK3JOso50tW2O8JAlsjvn'  # BD2 Test

vector_dimension: Final[int] = cast(int,
                                    getenv("VECTOR_DIMENSION")) or 16000 * 9
partition_size: Final[int] = vector_dimension // 9

load_dotenv()
db: connection = connect(user=getenv("POSTGRES_USER") or 'postgres',
                         password=getenv("POSTGRES_PASSWORD"),
                         host=getenv("POSTGRES_HOST"),
                         port=getenv("POSTGRES_PORT") or 5432)


def process_song(song: Path) -> None:

    track_id: str = song.stem

    if song is None:
        return

    features = get_mfcc_features_flatenized(song)
    logging.info(f"Processing song {track_id}")

    # truncate or pad to VECTOR_DIMENSION
    if features.shape[0] > vector_dimension:
        features = features[:vector_dimension]

    if features.shape[0] < vector_dimension:
        # Repeat the last row until the dimension is the same
        features = np.pad(features, (0, vector_dimension - features.shape[0]),
                          'edge')

    features_parts: list[list[float]] = [
        features[i:i + 16000].tolist() for i in range(0, len(features), 16000)
    ]

    #INSERT INTO items (embedding) VALUES ('[1,2,3]'), ('[4,5,6]');
    cursor: cursorT
    with db.cursor() as cursor:
        cursor.execute(
            ""
            "INSERT INTO song_features (track_id, features1, features2, features3, features4, features5, features6, features7, features8, features9) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
            "", (track_id, *features_parts))
    db.commit()


def run() -> None:

    # Create DB
    with db.cursor() as create_cursor:
        create_cursor.execute("""
            CREATE EXTENSION IF NOT EXISTS vector;
            CREATE TABLE IF NOT EXISTS song_features (
        track_id VARCHAR(22) PRIMARY KEY,
        features1 VECTOR(16000),
        features2 VECTOR(16000),
        features3 VECTOR(16000),
        features4 VECTOR(16000),
        features5 VECTOR(16000),
        features6 VECTOR(16000),
        features7 VECTOR(16000),
        features8 VECTOR(16000),
        features9 VECTOR(16000)
    );
    """)
    db.commit()

    downloader = Downloader(YOUTUBE_DL,
                            csv_path=getenv('CSV_PATH'),
                            userFavourites=False,
                            playlist_id=None)
    song: Path
    for song in downloader.download_songs():
        process_song(song)


if __name__ == "__main__":
    run()
