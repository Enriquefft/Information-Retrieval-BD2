from Download import Downloader
from Embed import get_mfcc_features_flatenized, get_sample_rate

from typing import Final, cast

from pathlib import Path

import numpy as np

from psycopg2 import connect
from psycopg2.extensions import connection, cursor as cursorT

from dotenv import load_dotenv
from os import getenv

playlist_id: Final[str] = '6Nqv8Mi4xKEOXBLcIbDopO'  # Reggaeton
# playlist_id: Final[str] = '3BK3JOso50tW2O8JAlsjvn'  # BD2 Test


def run() -> None:

    load_dotenv()
    db: connection = connect(user=getenv("POSTGRES_USER") or 'postgres',
                             password=getenv("POSTGRES_PASSWORD"),
                             host=getenv("POSTGRES_HOST"),
                             port=getenv("POSTGRES_PORT") or 5432)

    downloader = Downloader(playlist_id)
    generator = downloader.download_songs()

    min_duration: float = cast(float, next(generator))
    print(f"min_duration: {min_duration}")

    vector_dimension: Final[int] = cast(
        int, getenv("VECTOR_DIMENSION")) or 16000 * 9
    print(f"vector_dimension: {vector_dimension}")

    # Create DB
    with db.cursor() as create_cursor:
        create_cursor.execute("""
            CREATE EXTENSION vector;
            CREATE TABLE song_features (
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

    for song in generator:

        song_path: Path = Path(cast(str, song))
        track_id: str = song_path.stem

        if song is not None:
            features = get_mfcc_features_flatenized(Path(cast(str, song)))

            # truncate or pad to VECTOR_DIMENSION
            if features.shape[0] > vector_dimension:
                features = features[:vector_dimension]

            if features.shape[0] < vector_dimension:
                # Repeat the last row until the dimension is the same
                features = np.pad(features,
                                  (0, vector_dimension - features.shape[0]),
                                  'edge')

            # Loop invariant xd
            if features.shape[0] != vector_dimension:
                raise ValueError(
                    f"{features.shape[0]} != vector_dimension for song {track_id}"
                )

            f1 = features[:16000]
            f2 = features[16000:32000]
            f3 = features[32000:48000]
            f4 = features[48000:64000]
            f5 = features[64000:80000]
            f6 = features[80000:96000]
            f7 = features[96000:112000]
            f8 = features[112000:128000]
            f9 = features[128000:144000]

            #INSERT INTO items (embedding) VALUES ('[1,2,3]'), ('[4,5,6]');
            # Insert the features into the database
            cursor: cursorT
            with db.cursor() as cursor:
                cursor.execute(
                    ""
                    "INSERT INTO song_features (track_id, features1, features2, features3, features4, features5, features6, features7, features8, features9) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    "", (track_id, f1.tolist(), f2.tolist(), f3.tolist(),
                         f4.tolist(), f5.tolist(), f6.tolist(), f7.tolist(),
                         f8.tolist(), f9.tolist()))
    db.commit()
    db.close()


if __name__ == "__main__":
    run()
