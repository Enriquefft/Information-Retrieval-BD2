from psycopg2 import connect
from psycopg2.extensions import connection, cursor as cursorT

from typing import Final, Optional, cast

from os import getenv
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()
from db import db

import pandas as pd

CSV_PATH: Final[Path] = Path(getenv("CSV_PATH", "data/lyrics.csv"))
TABLE_NAME: Final[str] = getenv("LYRICS_TABLE_NAME", "lyrics")


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
        lyrics TEXT NOT NULL
        )""")

        db.commit()


def populate_db() -> None:
    """Populate db from csv using attribute (trackid [key]: lyrics [value])"""
    csv = pd.read_csv(CSV_PATH,
                      index_col="track_id",
                      usecols=["track_id", "lyrics"])
    with db.cursor() as cursor:
        for trackid, lyrics in csv.iterrows():
            print(len(trackid))
            cursor.execute(
                f"""
            INSERT INTO {TABLE_NAME} (trackid, lyrics)
            VALUES (%s, %s);
            """, (trackid, lyrics["lyrics"]))
        db.commit()


create_db()
populate_db()
db.close()
