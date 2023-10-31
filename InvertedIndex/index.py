import csv
import pickle
from spimi_invert import SpimiInvert
from preprocessor import Preprocessor
import heapq
import math

class Index:
    UP: bool = False
    DOWN: bool = True

    def __init__(self, _source_filename: str, _index_attributes: set) -> None:
        self.number_documents: int      = 0
        self.source_filename            = _source_filename
        self.processed_source_filename  = _source_filename + ".processed"
        self.index_attributes           = _index_attributes
        self.preprocess                 = Preprocessor()
        self.index_path                 = "./blocks"
        self.n_blocks                   = 0
    
    def _read_block(self, pos: int) -> dict:
        with open(self.index_path + f"{pos}.block", "rb") as f:
            return pickle.load(f)

    def _check_block(self, term: str, pos: int, dir: bool) -> list:
        if pos < 1 or pos > self.n_blocks:
            return []
        
        block = self._read_block(pos)
        
        return block.get(term, []) + self._check_block(term, pos - 1 + 2 * dir, dir) if len(block) != 1 else []
        
                

    def _binary_search(self, term: str, l: int, u: int):
        if l > u :
            return []
        
        mid = (l + u) // 2
        block = self._read_block(mid)
        print(block)
        if term == list(block)[0] : 
            # Case 1
            return block[term] + self._check_block(term, mid - 1, self.UP)
        elif term < list(block)[0] :
            # Caso 2
            return self._binary_search(term, l, mid-1)
        elif term == list(block)[-1] :
            # Caso 3
            return block[term] + self._check_block(term, mid + 1, self.DOWN)
        elif term > list(block)[-1] :
            # Caso 4
            return self._binary_search(term, mid+1, u)
        else : 
            return block.get(term, []) + self._check_block(term, mid - 1, self.UP) + self._check_block(term, mid + 1, self.DOWN) if (len(block) == 1) else []

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
        self.n_blocks = n_blocks
        print("Merging blocks")
        self._merge(n_blocks, path)

    def _calculate_idf(self, df: int) -> float:
        if (df < 1) :
            raise Exception(f"DF {df} malo")
        return math.log10(self.number_documents / df)

    def retrieval(self, query: str, k: int) -> list:
        result = dict()

        for term, tf in self.preprocess.preprocess_text(query).items():
            # print(term)
            docs = self._binary_search(term, 1, self.n_blocks)
            if len(docs) != 0:
                idf = self._calculate_idf(len(docs))
                for doc, tf_idf in docs:
                    val         =   result.get(doc, 0)
                    val         +=  tf_idf*tf*idf
                    result[doc] =   val

        return sorted(result.items(), key=lambda t: t[1])[:k]
    
