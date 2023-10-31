import csv
from spimi_invert import SpimiInvert
import tracemalloc
from util import Merge

class Index:
    def __init__(self, _source_filename: str, _index_attributes: set) -> None:
        self.number_documents:int = 0
        self.source_filename = _source_filename
        self.processed_source_filename = _source_filename + "atatest.processed"

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

    def create_blocks(self) -> None:
        print("Creating blocks")
        spimi = SpimiInvert(self.processed_source_filename)
        print("Writing blocks")
        n_blocks, path = spimi.create_blocks()
        print("Merging blocks")
        Merge(n_blocks, path)


# spimi = SpimiInvert("datatest.csv")
# n, path = spimi.create_blocks()

# for i in range(1, n+1):
#     block_file = open(f"{path}/{i}.block", 'rb')

#     idx: dict[dict[int,int]] = pickle.load(block_file)

#     print(f"Block {i}", idx)
    
#     block_file.close()

# x = _merge(n, path)

x = set()
x.add("column")
index = Index("datatest.csv",x)
index.process_source_file()
index.create_blocks()

expected_result = [
    # Bloque 1
    {
    "a": {1: 1, 2: 2, 3: 1, 5: 1, 6: 1, 7: 1, 8: 1},
    "b": {3: 1, 5: 1, 7: 1},
    "c": {2: 1, 3: 1, 6: 2, 8: 1},
    "d": {1: 1},
    },
    # Bloque 2
    {
    "e": {1: 1, 8: 1},
    "i": {1: 1, 3: 1, 8: 1},
    "m": {4: 1},
    "n": {4: 1},
    },
    # Bloque 3
    {
    "o": {2: 1, 4: 1},
    "p": {5: 1, 6: 1},
    "q": {4: 1},
    "s": {5: 1, 7: 2},
    },
]