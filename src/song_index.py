import sys
sys.path.append('../Information-Retrieval-BD2')

from InvertedIndex import Index

class SongsInvertedIndex():
    index:Index = None
    csv_file_path:str = "./CSV/spotify_songs.csv"

    attributes:set = set()
    attributes.add("track_name")
    attributes.add("track_artist")
    attributes.add("lyrics")

    def __init__(self) -> None:
        self.index = Index(self.csv_file_path, self.attributes)
        self.index.load()

    def search(self, keywords:str, k:int = 10):
        return self.index.retrieval(keywords, k)

