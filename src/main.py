# from .song_index import SongsInvertedIndex
from .api import app

from .db import db

from .info import getLyrics, getUri

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

TracksInfo = list[tuple[str, float]]

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
async def PostgresText(keywords: str, k: int = 10) -> TracksInfo:

    db_cursor: cursorT
    with db.cursor() as db_cursor:
        db_cursor.execute(
            """SELECT track_id, 0 FROM tracks WHERE to_tsvector('english', track_name || ' ' || track_artist || ' ' || lyrics) @@ to_tsquery('english', %s) LIMIT %s""",
            (keywords, k))
        results: TracksInfo = cast(TracksInfo, db_cursor.fetchall())

        return results


@app.get("/faiss/audio")
async def FaissAudio(trackid: str) -> TracksInfo:
    return []


@app.get("/rtree/audio")
async def RTreeAudio(trackid: str) -> TracksInfo:
    return []


@app.get("/knn/audio")
async def KnnAudio(trackid: str) -> TracksInfo:
    return []


@app.get("/shazam/audio")
async def ShazamAudio(trackid: str) -> TracksInfo:
    return []


@app.get("/shazam/lyrics")
async def ShazamLyrics(trackid: str) -> TracksInfo:
    return []


@app.get("/lyrics")
async def QueryLyrics(track_id: str) -> str:
    response = getLyrics(track_id)
    if response is None:
        raise HTTPException(status_code=404, detail="Lyrics not found")
    return response


@app.get("/local/autocomplete")
async def LocalAutocomplete(word: str) -> list[str]:
    return [word + "a", word + "b", word + "c", word + "d", word + "e"]


@app.get("/postgres/autocomplete")
async def PostgresAutocomplete(word: str) -> list[str]:
    with db.cursor() as db_cursor:
        db_cursor.execute(
            """SELECT track_name, track_name <-> %s as dist FROM tracks ORDER BY dist LIMIT 3""",
            (word, ))
        results: list[tuple[str, float]] = cast(list[tuple[str, float]],
                                                db_cursor.fetchall())
        return [result[0] for result in results]
