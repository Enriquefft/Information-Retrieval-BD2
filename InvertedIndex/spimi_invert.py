import typing

class SpimiInvert:
    dictionary:dict = dict()

    output_file:typing.TextIO = None 
    output_file_name:str = ""

    number_blocks:int = 1

    def free_memory_available(self) -> bool:
        if (len(self.dictionary) < 3):
            return True
        else:
            return False

    def add_to_dictionary(self, token_stream: list) -> list:
        self.dictionary[token_stream[0]] = []
        return [(token_stream[1:])]

    def get_posting_list(self, token:str) -> list:
        return self.dictionary[token]

    def add_to_posting_list(self, token:str, posting_list:list) -> None:
        posting_list.extend(self.dictionary[token])
        self.dictionary[token] = posting_list

    def sort_terms(self) -> dict:
        return dict(sorted(self.dictionary.items(), key=lambda x: x[0], reverse=False))

    def write_block_to_disk(self) -> None:
        pass

    def spimi_invert(self, token_stream: list) -> None:
        if (self.output_file == None):
            self.output_file_name = f"{self.number_blocks}.block"
            self.output_file = open(self.output_file_name, 'w')

        while (self.free_memory_available()):
            token = token_stream[0]
            if (token not in self.dictionary):
                posting_list = self.add_to_dictionary(self.dictionary, token_stream)
            else:
                posting_list = self.get_posting_list(self.dictionary, token)
            
            self.add_to_posting_list(token, posting_list)

        self.dictionary = self.sort_terms(self.dictionary)

        self.write_block_to_disk()

        return self.output_file_name