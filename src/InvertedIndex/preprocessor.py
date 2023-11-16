import os
import nltk
import csv
from collections import Counter
nltk.download('stopwords')

class Preprocessor:
    stopwords = set()

    tokenizer = nltk.tokenize.RegexpTokenizer(r'\w+')

    stemmer = nltk.stem.snowball.SnowballStemmer('english')

    def __init__(self) -> None:
        self.read_stopwords()

    def read_stopwords(self) -> None:
        if os.path.isfile('./stopwords.txt'):
            with open('stopwords.txt', 'r') as f:
                for line in f:
                    self.stopwords.add(line.strip())
        else:
            self.stopwords = set(nltk.corpus.stopwords.words('english'))

    def tokenize(self, text: str) -> list:
        return self.tokenizer.tokenize(text)
    
    def filter_stopwords(self, tokens: list) -> list:
        return [token for token in tokens if token not in self.stopwords]
    
    def stem(self, tokens: list) -> list:
        return [self.stemmer.stem(token) for token in tokens]
    
    def preprocess_text(self, text:str) -> dict:
        tokenized_list = self.tokenize(text)
        filtered_list = self.filter_stopwords(tokenized_list)
        stemmed_list = self.stem(filtered_list)
        stemmed_dict = dict(Counter(stemmed_list))
        return dict(sorted(stemmed_dict.items(), key=lambda x: x[0], reverse=False))
    
    def preprocess_word(self, word:str) -> list[str]:
        if word in self.stopwords:
            return []
        tokenized_word = self.tokenize(word)
        stemmed_word = [self.stemmer.stem(i) for i in tokenized_word]
        return stemmed_word
    
    def preprocess_csv(self, csv_filename: str, output_filename: str, positions_filename: str, attributes: set) -> int:
        import struct
        number_documents = 0
        with open(csv_filename, newline='\n') as source_file, open(output_filename, 'w') as processed_file, open(positions_filename, "wb") as positions:
            source_file_reader = csv.DictReader(source_file, delimiter=',')
            for row in source_file_reader:    
                # Update number of documents
                number_documents += 1
                
                # Select attributes to be indexed
                row = {key: row[key] for key in attributes}

                # Concatenate all values in row
                concatenated_word = " ".join(row.values())

                processed_file.write(str(concatenated_word) + "\n")

        return number_documents