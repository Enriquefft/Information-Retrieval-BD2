import os
import re
import shutil
import unittest
from src.InvertedIndex import Index

class TestInvertIndex(unittest.TestCase):
    def setUp(self) -> None:
        self.csv_file = "./tests/data/test.csv"
        self.attr = set()


    def test_create_1_attribute_query_track_name_partial(self):
        self.attr.add("track_name")
        i = Index(self.csv_file, self.attr)
        self.assertGreater(i.n_blocks, 0)
        self.assertGreater(i.number_documents, 0)
        self.assertEqual(i.retrieval("pangarap", 1)[0][0], "0017A6SJgTbfQVU2EtsPNo")

    def test_create_2_attributes_query_partial_track_name_track_artist(self):
        self.attr.add("track_name")
        self.attr.add("track_artist")
        i = Index(self.csv_file, self.attr)
        self.assertGreater(i.n_blocks, 0)
        self.assertGreater(i.number_documents, 0)

        self.assertEqual(i.retrieval("cold outside", 1)[0][0], "00cqd6ZsSkLZqGMlQCR0Zo")
        self.assertEqual(i.retrieval("Biv", 1)[0][0], "00chLpzhgVjxs1zKC9UScL") 
    
    def test_create_3_same_attributes(self):
        self.attr.add("track_name")
        self.attr.add("lyrics")
        self.attr.add("track_artist")

        i = Index(self.csv_file, self.attr)
        self.assertGreater(i.n_blocks, 0)
        self.assertGreater(i.number_documents, 0)

        query = i.retrieval("Nang ako'y", 1)
        self.assertEqual(query[0][0], "0017A6SJgTbfQVU2EtsPNo")

        query2 = i.retrieval("spyderman and freeze full effect are singing", 3)
        self.assertEqual(query2[0][0], "00chLpzhgVjxs1zKC9UScL")
        self.assertEqual(query2[1][0], "004s3t0ONYlzxII9PLgU6z")
        self.assertEqual(query2[2][0], "00cqd6ZsSkLZqGMlQCR0Zo") 
   
    def test_create_3_different_attributes(self):
        self.attr.add("track_name")
        self.attr.add("lyrics")
        self.attr.add("track_artist")

        i = Index(self.csv_file, self.attr)
        self.assertGreater(i.n_blocks, 0)
        self.assertGreater(i.number_documents, 0)

        query = i.retrieval("sandali ang Hindi ko alam ika'y Christina Aguilera baby cold Bell Biv", 3)
        self.assertEqual(query[0][0], "0017A6SJgTbfQVU2EtsPNo")
        self.assertEqual(query[1][0], "00cqd6ZsSkLZqGMlQCR0Zo")
        self.assertEqual(query[2][0], "00chLpzhgVjxs1zKC9UScL") 
   
    def test_create_1_attribute_query_full_lyrics(self):
        self.attr.add("lyrics")

        i = Index(self.csv_file, self.attr)
        self.assertGreater(i.n_blocks, 0)
        self.assertGreater(i.number_documents, 0)

        query = i.retrieval("Minsan pa Nang ako'y napalingon Hindi ko alam Na ika'y tutugon Sa mga tanong na aking nabitawan Hindi ko alam kung ito'y totoo Pangarap ka Sa bawat sandali Langit man ang tingin ko Sayo sana'y marating Hanggang dito na lang yata Ang kaya kong gawin Mangarap na lang At bumulong sa hangin Kailan kaya Darating ulit ang isang Sandali Na ako'y lilingon muli Pangarap ka o tinig mong kay lamig Ang iyong mga ngiti na sa akin ay Nakapagbigay pansin (Ikaw ba ay isang pangarap lang) Pangarap ka o tinig mong kay lamig Ang iyong mga ngiti Na sa akin ay Nakapagbigay... Pangarap ka o tinig mong kay lamig Ang iyong mga ngiti Na sa akin ay Nakapagbigay Pangarap ka o tinig mong kay lamig Ang iyong mga ngiti Na sa akin ay Nakapagbigay pansin", 1)
        self.assertEqual(query[0][0], "0017A6SJgTbfQVU2EtsPNo")

    def test_create_2_attribute_query_full_track_artist(self):
        self.attr.add("track_artist")

        i = Index(self.csv_file, self.attr)
        self.assertGreater(i.n_blocks, 0)
        self.assertGreater(i.number_documents, 0)

        query = i.retrieval("Bell Biv DeVoe", 1)
        self.assertEqual(query[0][0], "00chLpzhgVjxs1zKC9UScL")
       
    def test_create_3_attribute_query_full_track_name(self):
        self.attr.add("track_name")

        i = Index(self.csv_file, self.attr)
        self.assertGreater(i.n_blocks, 0)
        self.assertGreater(i.number_documents, 0)

        query = i.retrieval("Baby It's Cold Outside (feat. Christina Aguilera)", 1)
        self.assertEqual(query[0][0], "00cqd6ZsSkLZqGMlQCR0Zo")
   
    def test_create_4_attribute_query_lyrics_subgenre(self):
        self.attr.add("track_name")
        self.attr.add("lyrics")
        self.attr.add("track_artist")
        self.attr.add("playlist_subgenre")

        i = Index(self.csv_file, self.attr)
        self.assertGreater(i.n_blocks, 0)
        self.assertGreater(i.number_documents, 0)

        query = i.retrieval("rock and roll dance", 1)
        self.assertEqual(query[0][0], "004s3t0ONYlzxII9PLgU6z")
   

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