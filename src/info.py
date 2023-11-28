from psycopg2 import connect
from psycopg2.extensions import connection, cursor as cursorT

from typing import Final, Optional, cast

from os import getenv
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
from db import db

import pandas as pd

from spotipy import Spotify  # type: ignore
from spotipy.oauth2 import SpotifyClientCredentials  # type: ignore

# Set up credentials
client_id: Final[str] = '5b0ac652d91f4d2a89f62f99d568cd34'
client_secret: Final[str] = 'b450d640d4f44a13928f7725475a270b'
client_credentials_manager = SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret)
sp: Spotify = Spotify(client_credentials_manager=client_credentials_manager)

CSV_PATH: Final[Path] = Path(getenv("CSV_PATH", "data/lyrics.csv"))
TABLE_NAME: Final[str] = getenv("INFO_TABLE_NAME", "song_info")


def getLyrics(trackid: str) -> Optional[str]:
    """Get lyrics from db using trackid"""
    cursor: cursorT
    with db.cursor() as cursor:
        cursor.execute(
            f"""
        SELECT lyrics FROM {TABLE_NAME}
        WHERE trackid = %s;
        """, (trackid, ))
        response = cursor.fetchone()
        if response is None:
            raise ValueError("Trackid not found")
        return cast(str, response[0])


def create_db() -> None:
    """Create db if not exists"""
    with db.cursor() as cursor:
        cursor.execute(f"""
        CREATE TABLE IF NOT EXISTS {TABLE_NAME} (
        trackid VARCHAR(22) PRIMARY KEY,
        lyrics TEXT NOT NULL,
        uri VARCHAR(100) NOT NULL
        )""")

        db.commit()


def populate_db() -> None:
    """Populate db from csv using attribute (trackid [key]: lyrics [value], spotify_uri [value])"""
    csv = pd.read_csv(CSV_PATH,
                      index_col="track_id",
                      usecols=["track_id", "lyrics"])
    with db.cursor() as cursor:
        for trackid, lyrics in csv.iterrows():

            # Get spotify uri
            uri = sp.track(trackid)["uri"]

            cursor.execute(
                f"""
            INSERT INTO {TABLE_NAME} (trackid, lyrics, uri)
            VALUES (%s, %s, %s);
            """, (trackid, lyrics["lyrics"], uri))


create_db()
populate_db()
db.close()
