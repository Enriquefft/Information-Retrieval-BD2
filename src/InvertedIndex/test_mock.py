""" from index import Index

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

x = set()
x.add("track_artist")
index = Index("./../CSV/test.csv",x)
index.process_source_file()
index.create_blocks()

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
] """
import pickle
a =dict()

for i in range(1, 1000):
    a[i] = i
    print(a.__sizeof__())

print(a.__sizeof__())

data = pickle.dumps(a)

print(data.__sizeof__())

with open("test_dict", "wb") as file:
    file.write(data)


with open("test_dict", "rb") as file:
    data = file.read()
    b = pickle.loads(data)
    print(b.__sizeof__())