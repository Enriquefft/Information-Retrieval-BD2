import faiss
import pandas as pd
import numpy as np

df = pd.read_pickle("df.pkl")
index = faiss.read_index("index.faiss")


def get_knn(id: str, k: int) -> list[str]:
    D, I = index.search(df[df.id == id].data, k)
    return list(df.iloc[I[0], :].id)