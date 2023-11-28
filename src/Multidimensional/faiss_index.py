import faiss
import pandas as pd
import numpy as np

df = pd.read_pickle("df.pkl")
index = faiss.read_index("index.faiss")

# give me the feature vector in data by id

#print(df[df.id == "0017A6SJgTbfQVU2EtsPNo"].data.tolist())

def knn_faiss(id: str, k: int) -> list[str]:
    D, I = index.search(df[df.id == id].data.tolist()[0].reshape(1, -1), k)
    return list(df.iloc[I[0], :].id)

#print(knn_faiss("012mGdSYIBEmERuScm2iOl", 10))