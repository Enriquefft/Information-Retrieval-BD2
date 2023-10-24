import csv
from spimi_invert import SpimiInvert
import tracemalloc
class Index:
    def __init__(self, _source_filename: str, _index_attributes: set) -> None:
        self.number_documents:int = 0
        self.source_filename = _source_filename
        self.processed_source_filename = _source_filename + ".processed"

        self.index_attributes = _index_attributes

    def process_source_file(self) -> None:
        with open(self.source_filename, newline='\n') as source_file, open(self.processed_source_filename, 'w') as processed_file:
            source_file_reader = csv.DictReader(source_file, delimiter=',')
            for row in source_file_reader:
                # Update number of documents
                self.number_documents += 1
                
                # Select attributes to be indexed
                row = {key: row[key] for key in self.index_attributes}

                # Concatenate all values in row
                concatenated_word = " ".join(row.values())

                processed_file.write(str(concatenated_word) + "\n")
    def _merge(self, number_of_blocks: int, path: str) -> None:
        ...
    def create_blocks(self) -> None:
        print("Creating blocks")
        spimi = SpimiInvert(self.processed_source_filename)
        print("Writing blocks")
        n_blocks, path = spimi.create_blocks()
        print("Merging blocks")
        self._merge(n_blocks, path)

                
attributes = set()
attributes.add("track_name")
attributes.add("track_artist")
attributes.add("lyrics")
a = Index("spotify_songs.csv", attributes)

a.process_source_file()
a.create_blocks()