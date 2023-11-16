from src.InvertedIndex.index import Index

from os import getenv

from typing import Optional
from pathlib import Path


class SongsInvertedIndex():

    def __init__(self, csv_path: Optional[str] = None) -> None:

        if csv_path is None:
            csv_path = getenv('CSV_PATH')
            if csv_path is None:
                raise ValueError(
                    "csv_path must be present as env or input parameter")

        attributes: set[str] = {"track_name", "track_artist", "lyrics"}

        self.index: Index = Index(csv_path, attributes)
        self.index.save()
        self.index.load()

    def search(self, keywords: str, k: int = 10) -> list[tuple[str, float]]:
        return self.index.retrieval(keywords, k)
