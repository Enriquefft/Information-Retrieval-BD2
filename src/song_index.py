from src.InvertedIndex.index import Index

from os import getenv

from typing import Optional
from pathlib import Path

import logging


class SongsInvertedIndex():

    def __init__(self, csv_path: str) -> None:

        self.csv_path: str = csv_path

        attributes: set[str] = {"track_name", "track_artist", "lyrics"}

        logging.info(f"indexing csv file: {self.csv_path}")

        self.index: Index = Index(self.csv_path, attributes)
        self.index.save()
        self.index.load()

        logging.info("Index loaded")

    def search(self, keywords: str, k: int = 10) -> list[tuple[str, float]]:
        return self.index.retrieval(keywords, k)
