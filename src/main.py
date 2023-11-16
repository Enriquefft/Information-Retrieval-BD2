from src.song_index import SongsInvertedIndex
from fastapi import FastAPI

from pydantic import BaseModel

from psycopg2 import connect, extensions
from psycopg2.extensions import connection, cursor

from typing import Any, cast
from os import getenv
from dotenv import load_dotenv

load_dotenv()
app = FastAPI()

songs_index = SongsInvertedIndex()

db: connection = connect(host=getenv("POSTGRES_HOST"), dbname="postgres", user=getenv("POSTGRES_USER") , password=getenv("POSTGRES_PASSWORD") )

TracksInfo = list[tuple[str, float]]


@app.get("/local/text")
async def LocalText(keywords: str, k: int = 10) -> TracksInfo:
    return songs_index.search(keywords, k)


@app.get("/postgres/text")
async def PostgresText(keywords: str) -> TracksInfo:

    db_cursor: cursor
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
