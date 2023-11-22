import pickle
import struct
from .spimi_invert import SpimiInvert
from .preprocessor import Preprocessor
from .util import write_block_to_disk, Merge, load_block, Block
import numpy as np
import math
from os import path

from typing import Final, TextIO, BinaryIO, cast

import logging


class Index:
    UP: Final[bool] = False
    DOWN: Final[bool] = True

    def __init__(self, _source_filename: str,
                 _index_attributes: set[str]) -> None:
        self.number_documents: int = 0
        self.source_filename = _source_filename
        self.processed_source_filename = _source_filename + ".processed"
        self.index_attributes = _index_attributes
        self.preprocess = Preprocessor()
        self.index_path = "./blocks"
        self.n_blocks = 0
        self.norms_filename = _source_filename + "_norms.dat"
        self.positions_file = _source_filename + ".position"

        if not path.exists(self.index_path):
            if self.index_attributes is None:
                raise Exception("Index attributes required")
            self.number_documents = self.preprocess.preprocess_csv(
                self.source_filename, self.processed_source_filename,
                self.positions_file, self.index_attributes)
            self.map_positions()
            self.create_blocks()

    def save(self) -> None:
        if not path.exists(self.source_filename + ".config"):
            with open(self.source_filename + ".config", "wb") as file:
                file.write(
                    struct.pack("@ii", self.number_documents, self.n_blocks))

    def load(self) -> None:
        with open(self.source_filename + ".config", "rb") as file:
            self.number_documents, self.n_blocks = struct.unpack(
                "@ii", file.read(struct.calcsize("@ii")))

    def map_positions(self) -> None:
        with open(self.source_filename,
                  "r") as source_file, open(self.positions_file,
                                            "wb") as positions:
            while source_file.readline() != "":
                physical_pos = source_file.tell()
                positions.write(struct.pack("@i", physical_pos))

    def _read_block(self, pos: int):
        with open(self.index_path + f"/{pos}.block", "rb") as f:
            return pickle.load(f)

    def _check_block(self, term: str, pos: int, dir: bool) -> list:
        if pos < 1 or pos > self.n_blocks:
            return []

        block = self._read_block(pos)

        return block.get(term, []) + self._check_block(
            term, pos - 1 + 2 * dir, dir) if len(block) != 1 else []

    def _binary_search(self, term: str, l: int, u: int):
        if l > u:
            return []

        mid = (l + u) // 2
        block = self._read_block(mid)
        if term == list(block)[0]:
            # Case 1
            return block[term] + self._check_block(term, mid - 1, self.UP)
        elif term < list(block)[0]:
            # Caso 2
            return self._binary_search(term, l, mid - 1)
        elif term == list(block)[-1]:
            # Caso 3
            return block[term] + self._check_block(term, mid + 1, self.DOWN)
        elif term > list(block)[-1]:
            # Caso 4
            return self._binary_search(term, mid + 1, u)
        else:
            return block.get(
                term, []) + (self._check_block(term, mid - 1, self.UP) +
                             self._check_block(term, mid + 1, self.DOWN) if
                             (len(block) == 1) else [])

    def _get_df(self, term: str, block_id: int) -> int:
        df = 0
        while True:
            if block_id > self.n_blocks:
                return df
            block: Block = load_block(block_id, self.index_path)
            df_block = len(block.get(term, []))
            if df_block == 0:
                return df
            df += df_block
            block_id += 1

    def _tf_idf_init(self) -> None:
        df: dict[str, int] = dict()
        for block_id in range(1, self.n_blocks + 1):
            block: Block = load_block(block_id, self.index_path)
            for term, dic in block.items():
                if term not in df:
                    df.clear()
                    df[term] = self._get_df(term, block_id)
                for doc_id, tf in dic.items():
                    idf = np.log10(self.number_documents / df[term])
                    block[term][doc_id] = tf * idf
            write_block_to_disk(block, block_id, self.index_path)

    def _calculate_idf(self, df: int) -> float:
        if (df < 1):
            raise Exception(f"DF {df} malo")
        return math.log10(self.number_documents / df)

    def _initialize_norms(self) -> None:
        file = open(f"{self.norms_filename}", "wb")

        for i in range(self.number_documents):
            norm = struct.pack('f', 0.0)
            file.write(norm)
        file.close()

    def _read_load_norm(self, file: BinaryIO, size: int) -> float:
        norm = file.read(size)
        return cast(float, struct.unpack('f', norm)[0])

    def _write_norm(self, file: BinaryIO, size: int, doc_id: int,
                    norm: float) -> None:
        norm = struct.pack('f', norm)
        file.seek((doc_id - 1) * size)
        file.write(norm)

    def _compute_norms(self) -> None:
        float_bytes_size: int = 4
        self._initialize_norms()
        file = open(f"{self.norms_filename}", "rb+")
        for block_id in range(1, self.n_blocks + 1):
            block: Block = load_block(block_id, self.index_path)
            for dic in block.values():
                for doc_id, tf_idf in dic.items():
                    file.seek((doc_id - 1) * float_bytes_size)
                    norm_doc = file.read(float_bytes_size)
                    norm_doc = struct.unpack('f', norm_doc)[0]

                    norm_doc += tf_idf**2
                    norm_doc = struct.pack('f', norm_doc)

                    file.seek((doc_id - 1) * float_bytes_size)
                    file.write(norm_doc)

        file.close()

        with open(self.norms_filename, "rb+") as file:
            for doc_id in range(1, self.number_documents + 1):
                norm_doc = self._read_load_norm(file, float_bytes_size)
                norm_doc = math.sqrt(norm_doc)
                self._write_norm(file, float_bytes_size, doc_id, norm_doc)

    def _get_norm(self, doc_id: int) -> float:
        file: BinaryIO
        with open(self.norms_filename, "rb+") as file:
            file.seek((doc_id - 1) * 4)
            norm_doc = file.read(4)
            return cast(float, struct.unpack('f', norm_doc)[0])

    def _normalize(self) -> None:
        for block_id in range(1, self.n_blocks + 1):
            block: Block = load_block(block_id, self.index_path)
            for keyword, dic in block.items():
                for doc_id, tf_idf in dic.items():
                    block[keyword][doc_id] = tf_idf / self._get_norm(doc_id)
            for k, v in block.items():
                block[k] = sorted(list(v.items()))
            write_block_to_disk(block, block_id, self.index_path)

    def _print_blocks(self) -> None:
        for block_id in range(1, self.n_blocks + 1):
            block: Block = load_block(block_id, self.index_path)
            print(f"Block {block_id}", block)

    def _print_norms(self) -> None:
        with open(self.norms_filename, "rb+") as file:
            for doc_id in range(1, self.number_documents + 1):
                norm_doc = self._read_load_norm(file, 4)
                print(f"Norm {doc_id}", norm_doc)

    def create_blocks(self) -> None:
        spimi = SpimiInvert(self.processed_source_filename,
                            self.positions_file)

        n_blocks, path = spimi.create_blocks()
        self.n_blocks = n_blocks

        self.n_blocks = Merge(n_blocks, path)

        self._tf_idf_init()

        self._compute_norms()

        self._normalize()

    def retrieve_document(self, logical_pos: int) -> None:
        """
        Return the first attribute of the corresponding row in the csv file source
        """
        with open(self.source_filename) as csv, open(self.positions_file,
                                                     "rb") as pos:
            pos.seek((logical_pos - 1) * struct.calcsize("@i"))
            physical_pos = struct.unpack("@i",
                                         pos.read(struct.calcsize("@i")))[0]
            csv.seek(physical_pos)
            line = csv.readline()
            return line.split(",")[0]

    def retrieval(self, query: str, k: int) -> list[tuple[str, float]]:
        """
        Returns at most k similar documents in descending order
        """
        result = dict()

        logging.info(f"Retrieving documents for query: {query}")

        logging.info(
            f"preprocess: {self.preprocess.preprocess_text(query).items()}")

        for term, tf in self.preprocess.preprocess_text(query).items():
            logging.info(f"n_block: {self.n_blocks}")
            docs = self._binary_search(term, 1, self.n_blocks)
            logging.info(f"docs: {docs}")
            if len(docs) != 0:
                idf = self._calculate_idf(len(docs))
                for doc, tf_idf in docs:
                    val = result.get(doc, 0)
                    val += tf_idf * tf * idf
                    result[doc] = val

        logging.info(f"Retrieved {len(result)} documents")
        logging.info(f"Retrieved {result}")

        return list(
            map(lambda x: (self.retrieve_document(x[0]), x[1]),
                sorted(result.items(), key=lambda t: t[1], reverse=True)[:k]))
