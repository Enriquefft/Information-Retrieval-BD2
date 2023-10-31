from index import Index

attributes = set()
attributes.add("track_name")
attributes.add("track_artist")
attributes.add("lyrics")
a = Index("spotify_songs.csv", attributes)

# a.process_source_file()
# a.create_blocks()

a.n_blocks = 4
a.index_path = "./InvertedIndex/mock_blocks/"

print(a.retrieval("vaca", 3))