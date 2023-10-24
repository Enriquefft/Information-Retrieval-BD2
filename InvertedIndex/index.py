import csv
import ast

from preprocessor import Preprocessor

class Index:
    preprocessor = Preprocessor()

    number_documents:int = 0
    #number_terms:int = 0

    # File names
    source_filename:str = ""
    processed_source_filename:str = ""
    
    # Attributes to index
    index_attributes:set = set()

    def __init__(self, _source_filename: str, _index_attributes: set) -> None:
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

                # Preprocess document  { keyword : term_frequency, ...} 
                processed_list = self.preprocessor.preprocess_text(concatenated_word)

                # Write keyword with its frequency and document id
                for keyword in processed_list:
                    term_frequency = processed_list[keyword]
                    processed_file.write(f"('{keyword}', {term_frequency}, {self.number_documents})\n")

                # processed_file.write(str(processed_list) + "\n")
                
                if (self.number_documents == 10):
                    break

    def create_blocks(self) -> None:
        # Read processed file
        with open(self.processed_source_filename, 'r') as processed_file:
            while True:
                if (processed_file.readline() == ""):
                    break

                

attributes = set()
attributes.add("track_name")

a = Index("spotify_songs.csv", attributes)

a.process_source_file()
a.create_blocks()