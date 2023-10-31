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
        pass

    def create_blocks(self) -> None:
        print("Creating blocks")
        spimi = SpimiInvert(self.processed_source_filename)
        print("Writing blocks")
        n_blocks, path = spimi.create_blocks()
        print("Merging blocks")
        self._merge(n_blocks, path)

                
# attributes = set()
# attributes.add("track_name")
# attributes.add("track_artist")
# attributes.add("lyrics")
# a = Index("spotify_songs.csv", attributes)
# a.process_source_file()
# a.create_blocks()

import pickle
import os
import typing
import heapq


Block: typing.TypeAlias = dict[str, dict[int, int]]
MAX_BLOCK_SIZE = 100 # Bytes


class MinHeap:
    def __init__(self):
        self.data = []
        self.sz = 0
    
    def push(self, key: str, value: dict[int, int], index: int) -> None:
        heapq.heappush(self.data, (key, self.sz, value, index))
        self.sz += 1
    
    def pop(self) -> tuple[str, dict[int, int], int]:
        x = heapq.heappop(self.data)
        self.sz -= 1
        return (x[0], x[2], x[3])
    
    def size(self) -> int: return self.sz

    def push_dict(self, dic: dict[int, int], index: int) -> None:
        for (key, value) in dic.items():
            heapq.heappush(self.data, (key, self.sz, value, index))
            self.sz += 1
        
# Load the block if exists
def load_block(index: int, path: str) -> Block:
    if os.path.exists(f"{path}/{index}.block"):
        with open(f"{path}/{index}.block", 'rb') as file:
            return pickle.load(file)
    else:
        return {}

def write_block_to_disk(block: Block, index: int, path: str) -> None:
        os.makedirs(path, exist_ok=True)
        with open(f"{path}/{index}.block", 'wb') as file:
            pickle.dump(block, file)

def free_memory_available(d) -> bool:
        if len(d) < 4:
            return True
        else:
            return False

def sort_terms(dictionary) -> dict[int, int]:
    return dict(sorted(dictionary.items(), key=lambda x: x[0], reverse=False))


def _merge(number_of_blocks: int, path: str) -> int:
    return MergeSortBlocks(1, number_of_blocks, path)


def MergeSortBlocks(p: int, r: int, path: str) -> int:
    """
        p: fisrt index block, 
        r: last index block,
        path: directory of blocks
        return the number of blocks that were created
    """
    if p < r:
        q: int = (p + r - 1) // 2
        MergeSortBlocks(p, q, path)
        MergeSortBlocks(q+1, r, path)
        n: int = MergeBlocks(p, q, r, path)
        # Visualización de los bloques que se han mergeado
        for i in range(n - p + 1):
            print(f"Bloque #{p + i}")
            block = load_block(p + i, path)
            print(block)
        return n - p + 1
    
    return 0


def MergeBlocks(p: int, q: int, r: int, path: str) -> int:
    print(f"Merging: {p}, {q}, {r}")
    
    i = p   # Index for the first array of blocks [p:q]
    j = q+1 # Index for the second array of blocks [q+1:r]
    k = p   # Index for the output block

    output: Block = {}
    input1: Block = load_block(i, path) # First input (blocks [p to q])
    input2: Block = load_block(j, path) # Second input (blocks [q+1 to r])

    heap = MinHeap()

    while i <= q and j <= r:
        size1: int = len(input1)
        size2: int = len(input2)

        # Push to heap
        heap.push_dict(input1, i)
        heap.push_dict(input2, j)

        count1: int = 0
        count2: int = 0

        while heap.size() > 0:
            key, value, idinput = heap.pop()
            
            if output.get(key) is None:
                output[key] = value
            else:
                output[key].update(value)

            # We must use output.__sizeof__() < FREE_MEMORY_AVAILABLE
            # but for now we will use the lenght of the block
            if not free_memory_available(output):
                write_block_to_disk(output, k, path)
                output.clear()
                k += 1

            if idinput == i:
                count1 = count1 + 1
            else:
                count2 = count2 + 1
            
            if count1 == size1:
                i = i + 1

                if i > q: break
                input1 = load_block(i, path)
                heap.push_dict(input1, i)
                count1 = 0
                size1 = len(input1)

            elif count2 == size2:
                j = j + 1

                if j > r: break
                input2 = load_block(j, path)
                heap.push_dict(input2, j)
                count2 = 0
                size2 = len(input2)

    while i <= q:
        if heap.size() == 0:
            input1 = load_block(i, path)
            heap.push_dict(input1, i)
        
        size1: int = heap.size()
        count1: int = 0

        while heap.size() > 0:
            key, value, idinput = heap.pop()
            
            if output.get(key) is None:
                output[key] = value
            else:
                output[key].update(value)

            # We must use output.__sizeof__() < FREE_MEMORY_AVAILABLE
            # but for now we will use the lenght of the block
            if not free_memory_available(output):
                write_block_to_disk(output, k, path)
                output.clear()
                k += 1

            count1 = count1 + 1
            
            if count1 == size1:
                i = i + 1

                if i > q: break
                input1 = load_block(i, path)
                heap.push_dict(input1, i)
                count1 = 0
                size1 = len(input1)


    while j <= r:
        if heap.size() == 0:
            input2 = load_block(j, path)
            heap.push_dict(input2, j)

        size2: int = heap.size()
        count2: int = 0

        while heap.size() > 0:
            key, value, idinput = heap.pop()
            
            if output.get(key) is None:
                output[key] = value
            else:
                output[key].update(value)

            # We must use output.__sizeof__() < FREE_MEMORY_AVAILABLE
            # but for now we will use the lenght of the block
            if not free_memory_available(output):
                write_block_to_disk(output, k, path)
                output.clear()
                k += 1
            
            count2 = count2 + 1

            if count2 == size2:
                j = j + 1

                if j > r: break
                input2 = load_block(j, path)
                heap.push_dict(input2, j)
                count2 = 0
                size2 = len(input2)
    
    if len(output) > 0:
        write_block_to_disk(output, k, path)
        k += 1
    
    return k - 1

    
    
spimi = SpimiInvert("datatest.csv")
n, path = spimi.create_blocks()

for i in range(1, n+1):
    block_file = open(f"{path}/{i}.block", 'rb')

    idx: dict[dict[int,int]] = pickle.load(block_file)

    print(f"Block {i}", idx)
    
    block_file.close()

x = _merge(n, path)

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