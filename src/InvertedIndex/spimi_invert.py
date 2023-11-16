from .preprocessor import Preprocessor
from .util import free_memory_available, sort_terms, write_block_to_disk

DEBUG = True

class ReaderRaw:
    def __init__(self, _source_filename, _positions_filename):
        self.processed_source_filename  = _source_filename
        self.positions_file             = _positions_filename
        self.preprocessor               = Preprocessor()

    def reader(self) :

        with open(self.processed_source_filename, 'r') as processed_file:
            id: int  = 1
            while True:
                # next word
                word = ""
                while (not word.endswith(" ") and not (finish := word.endswith("\n"))):
                    word += (chunk := processed_file.read(1))
                    if (chunk == ''):
                        return
                for token in self.preprocessor.preprocess_word(word):  
                    yield (token, id)
                if (finish):
                    id += 1

class SpimiInvert:
    def __init__(self, source_file: str, positions_file: str) -> None:
        self.dictionary     = dict()
        self.number_blocks  = 1
        self.source_file    = source_file
        self.reader         = ReaderRaw(self.source_file, positions_file)

    def add_to_dictionary(self, token_stream: list) -> list:
        self.dictionary[token_stream[0]] = []
        return [(token_stream[1:])]

    def get_posting_list(self, token:str) -> list:
        return self.dictionary[token]

    def add_to_posting_list(self, token:str, posting_list:list) -> None:
        posting_list.extend(self.dictionary[token])
        self.dictionary[token] = posting_list
    
    def create_blocks(self) -> tuple[int, str]:
        path: str = "blocks/"
        self.number_blocks: int = 1
        self.dictionary = dict()

        for token, doc_id in self.reader.reader():
            if not free_memory_available(self.dictionary):
                self.dictionary = sort_terms(self.dictionary)
                write_block_to_disk(self.dictionary, self.number_blocks, path)
                self.dictionary.clear()
                self.number_blocks += 1
            
            tmp = self.dictionary.get(token, {})
            count = tmp.get(doc_id, 0)
            count += 1
            tmp[doc_id] = count
            self.dictionary[token] = tmp

        self.dictionary = sort_terms(self.dictionary)
        write_block_to_disk(self.dictionary, self.number_blocks, path)
        self.dictionary.clear()
        return (self.number_blocks, "blocks/")