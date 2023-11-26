from Download import Downloader, DownloadMethod
from Embed import Embedder

import warnings

warnings.filterwarnings('ignore')

import tracemalloc

from typing import Final, cast

from pathlib import Path

import numpy as np

from psycopg2 import connect
from psycopg2.extensions import connection, cursor as cursorT

from dotenv import load_dotenv
from os import getenv

import logging

csv_path = getenv('CSV_PATH')
playlist_id = getenv('PLAYLIST_ID')
favourites_log_name = 'favourites'

if csv_path:
    log_name = Path(csv_path).stem
elif playlist_id:
    log_name = playlist_id
else:
    log_name = favourites_log_name

log_file = Path('logs/error') / (log_name + '.log')
logging.basicConfig(filename=log_file, filemode='w')
logging.root.setLevel(logging.WARNING)

vector_dimension: Final[int] = cast(int,
                                    getenv("VECTOR_DIMENSION")) or 16000 * 9
partition_size: Final[int] = vector_dimension // 9

load_dotenv()
db: connection = connect(user=getenv("POSTGRES_USER") or 'postgres',
                         password=getenv("POSTGRES_PASSWORD"),
                         host=getenv("POSTGRES_HOST"),
                         port=getenv("POSTGRES_PORT") or 5432)

embedder: Embedder = Embedder(
    max_duration_seconds=167.24
)  # This time often produces vectors of aproximately 16000 * 9 length

downloader = Downloader(DownloadMethod.PYTUBE,
                        csv_path=getenv('CSV_PATH'),
                        userFavourites=False,
                        playlist_id=None,
                        db=db)

TABLE_NAME = getenv('TABLE_NAME') or 'track_features'


def process_song(song_path: Path) -> None:

    track_id: str = song_path.stem

    features = embedder.get_mfcc_features_flatenized(song_path)

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
            f"""INSERT INTO {TABLE_NAME} (track_id, features1, features2, features3, features4, features5, features6, features7, features8, features9) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
            (track_id, *features_parts))
    db.commit()


def run() -> None:

    with db.cursor() as create_cursor:
        create_cursor.execute(f"""
            CREATE EXTENSION IF NOT EXISTS vector;
            CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
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
    logging.info("DB created")

    song: Path
    for song in downloader.download_songs():
        process_song(song)
    logging.info("Finished procesing")


if __name__ == "__main__":
    run()
