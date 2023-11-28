from .song_index import SongsInvertedIndex
from .api import app

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from typing import Any, cast, Optional, Final
from os import getenv
from dotenv import load_dotenv

from psycopg2 import connect
from psycopg2.extensions import connection, cursor as cursorT

from threading import Thread

from .Multidimensional.faiss_index import knn_faiss
from .Multidimensional.gist_index import knn_gist

import logging

logging.basicConfig(level=logging.INFO)
load_dotenv()

db: connection = connect(user=getenv("POSTGRES_USER") or 'postgres',
                         password=getenv("POSTGRES_PASSWORD"),
                         database=getenv("POSTGRES_DB") or 'postgres',
                         host=getenv("POSTGRES_HOST"),
                         port=getenv("POSTGRES_PORT") or 5432)

TracksInfo = list[tuple[str, float]]

from time import sleep

index_thread: Thread
index: SongsInvertedIndex

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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


@app.get("/multidimensional/faiss/knn")
async def MultidimensionalFaissKnn(track_id: str, k: int = 5):
    if index_thread.is_alive():
        raise HTTPException(status_code=500, detail="Index is not ready yet")
    else:
        return knn_faiss(track_id, k)
    
@app.get("/multidimensional/gist/knn")
async def MultidimensionalGistKnn(track_id: str, k: int = 5):
    if index_thread.is_alive():
        raise HTTPException(status_code=500, detail="Index is not ready yet")
    else:
        return knn_gist(db, track_id, k)

@app.get("/local/text")
async def LocalText(keywords: str, k: int = 10) -> TracksInfo:
    if index_thread.is_alive():
        raise HTTPException(status_code=500, detail="Index is not ready yet")
    else:
        return index.search(keywords, k)

@app.get("/postgres/text")
async def PostgresText(keywords: str, k:int = 10) -> TracksInfo:

    db_cursor: cursorT
    with db.cursor() as db_cursor:
        db_cursor.execute(
            """SELECT track_id, 0 FROM tracks WHERE to_tsvector('english', track_name || ' ' || track_artist || ' ' || lyrics) @@ to_tsquery('english', %s) LIMIT %s""",
            (keywords, k))
        results: TracksInfo = cast(TracksInfo, db_cursor.fetchall())

        return results


@app.get("/local/autocomplete")
async def LocalAutocomplete(word: str) -> list[str]:
    return [word + "a", word + "b", word + "c", word + "d", word + "e"]


@app.get("/postgres/autocomplete")
async def PostgresAutocomplete(word: str) -> list[str]:
    return [word + "a", word + "b", word + "c", word + "d", word + "e"]
