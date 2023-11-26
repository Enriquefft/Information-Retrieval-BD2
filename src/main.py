from .song_index import SongsInvertedIndex
from .api import app

from fastapi import FastAPI, HTTPException

from typing import Any, cast, Optional, Final
from os import getenv
from dotenv import load_dotenv

from psycopg2 import connect
from psycopg2.extensions import connection, cursor as cursorT

from threading import Thread

import logging

logging.basicConfig(level=logging.INFO)
load_dotenv()

db: connection = connect(user=getenv("POSTGRES_USER") or 'postgres',
                         password=getenv("POSTGRES_PASSWORD"),
                         host=getenv("POSTGRES_HOST"),
                         port=getenv("POSTGRES_PORT") or 5432)

TracksInfo = list[tuple[str, float]]

from time import sleep

index_thread: Thread
index: SongsInvertedIndex


@app.on_event("startup")
async def startup_event() -> None:
    global index_thread, index

    def get_idx() -> None:
        global index
        ENV_CSV: Optional[str] = getenv("CSV_PATH")
        if ENV_CSV is None:
            raise HTTPException(
                status_code=500,
                detail="CSV_PATH environment variable is required")
        index = SongsInvertedIndex(ENV_CSV)
        logging.info("Textual inverted index is ready to use")

    logging.info("Api is ready to be used")

    index_thread = Thread(target=get_idx)
    index_thread.start()


@app.get("/local/text")
async def LocalText(keywords: str, k: int = 10) -> TracksInfo:
    if index_thread.is_alive():
        raise HTTPException(status_code=500, detail="Index is not ready yet")
    else:
        return index.search(keywords, k)


@app.get("/postgres/text")
async def PostgresText(keywords: str) -> TracksInfo:

    db_cursor: cursorT
    with db.cursor() as db_cursor:
        db_cursor.execute(
            """SELECT track_id FROM tracks WHERE to_tsvector('english', lyrics) @@ to_tsquery('english', %s);""",
            (keywords, ))
        results: TracksInfo = cast(TracksInfo, db_cursor.fetchall())

        return results


@app.get("/local/autocomplete")
async def LocalAutocomplete(word: str) -> list[str]:
    return [word + "a", word + "b", word + "c", word + "d", word + "e"]


@app.get("/postgres/autocomplete")
async def PostgresAutocomplete(word: str) -> list[str]:
    return [word + "a", word + "b", word + "c", word + "d", word + "e"]
