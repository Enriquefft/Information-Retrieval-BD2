import faiss
import pandas as pd
import numpy as np

df = pd.read_pickle("df.pkl")
index = faiss.read_index("index.faiss")

def knn_faiss(id: str, k: int) -> list[str]:
    D, I = index.search(df[df.id == id].data.tolist()[0].reshape(1, -1), k)
    return list(df.iloc[I[0], :].id)