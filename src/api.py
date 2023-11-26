from .song_index import SongsInvertedIndex

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fastapi import HTTPException

from concurrent.futures import Future

from typing import Final

cors_origins: Final[list[str]] = ['*']

from enum import Enum

app: Final[FastAPI] = FastAPI()

app.add_middleware(CORSMiddleware,
                   allow_origins=cors_origins,
                   allow_methods=["*"],
                   allow_headers=["*"])


@app.get("/")
async def Health() -> bool:
    return True
