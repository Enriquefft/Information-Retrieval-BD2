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
    
def remove_block(index: int, path: str) -> None:
    if os.path.exists(f"{path}/{index}.block"):
        os.remove(f"{path}/{index}.block")
    else:
        raise Exception(f"Block {path}/{index}.block does not exits")
    
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


def Merge(number_of_blocks: int, path: str) -> int:
    n = MergeSortBlocks(1, number_of_blocks, path)
    for i in range(n+1, number_of_blocks+1):
        remove_block(i, path)
        

def MergeSortBlocks(p: int, r: int, path: str) -> int:
    """
        p: fisrt index block, 
        r: last index block,
        path: directory of blocks
        return the number of blocks that were created
    """
    if p < r:
        q: int = (p + r - 1) // 2
        k1: int = MergeSortBlocks(p, q, path)
        k2: int = MergeSortBlocks(q+1, r, path)
        n: int = MergeBlocks(p, k1, q+1, k2, path)
        return n
    
    return r


def MergeBlocks(p: int, q1: int, q2: int, r: int, path: str) -> int:

    i = p   # Index for the first array of blocks [p:q]
    j = q2 # Index for the second array of blocks [q+1:r]
    k = p   # Index for the output block

    output: Block = {}
    input1: Block = load_block(i, path) # First input (blocks [p to q])
    input2: Block = load_block(j, path) # Second input (blocks [q+1 to r])

    heap = MinHeap()

    while i <= q1 and j <= r:
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

                if i > q1: break
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

    while i <= q1:
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

                if i > q1: break
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