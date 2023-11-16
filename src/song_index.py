from src.InvertedIndex.index import Index
from config import CSV_PATH


class SongsInvertedIndex():

    attributes: set[str] = set()
    attributes.add("track_name")
    attributes.add("track_artist")
    attributes.add("lyrics")

    def __init__(self) -> None:

        attributes: set[str] = {"track_name", "track_artist", "lyrics"}

        self.index: Index = Index(str(CSV_PATH), attributes)
        self.index.save()
        self.index.load()

    def search(self, keywords: str, k: int = 10) -> list[tuple[str, float]]:
        return self.index.retrieval(keywords, k)
