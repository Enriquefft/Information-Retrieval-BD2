import os
import re
import shutil
import unittest
from InvertedIndex import Index

class TestInvertIndex(unittest.TestCase):
    def setUp(self) -> None:
        self.csv_file = "./tests/data/test.csv"
        self.attr = set()

    def test_create_simple(self):
        self.attr.add("track_name")
        i = Index(self.csv_file, self.attr)
        self.assertGreater(i.n_blocks, 0)
        self.assertGreater(i.number_documents, 0)
        self.assertEqual(i.retrieval("pangarap", 1)[0][0], "0017A6SJgTbfQVU2EtsPNo")

    def test_create_2_attributes(self):
        # self.attr.add("track_name")
        self.attr.add("track_artist")
        i = Index(self.csv_file, self.attr)
        self.assertGreater(i.n_blocks, 0)
        self.assertGreater(i.number_documents, 0)
        self.assertEqual(i.retrieval("CeeLo Green", 1)[0][0], "00cqd6ZsSkLZqGMlQCR0Zo")

    def tearDown(self) -> None:
        self.attr.clear()
        for blocks_dir in os.listdir():
            if re.match(".*blocks", blocks_dir):
                shutil.rmtree(blocks_dir)
        
        base_name = os.path.dirname(self.csv_file)
        for meta_file in os.listdir(base_name):
            if meta_file != os.path.basename(self.csv_file):
                os.remove(base_name +"/" + meta_file)
        
if __name__ == '__main__':
    unittest.main()