from dotenv import load_dotenv

from psycopg2.extensions import register_adapter, AsIs

from psycopg2 import connect
from psycopg2.extensions import connection, cursor as cursorT

import numpy as np

load_dotenv()
from os import getenv

db: connection = connect(user=getenv("POSTGRES_USER") or 'postgres',
                         password=getenv("POSTGRES_PASSWORD"),
                         database=getenv("POSTGRES_DB") or 'postgres',
                         host=getenv("POSTGRES_HOST"),
                         port=getenv("POSTGRES_PORT") or 5432)

def addapt_numpy_array(numpy_array):
    return AsIs(tuple(numpy_array))

register_adapter(np.ndarray, addapt_numpy_array)


def insert_feature(track_id: str, embedded_feature_vector: np.array) -> None:
    with db.cursor() as cursor:
        cursor.execute(
            "INSERT INTO music (track_id, features_vector) VALUES (%s, cube(%s::float[]))",
            (track_id, embedded_feature_vector.tolist()),
        )
    db.commit()

import pandas as pd
umap_df = pd.read_pickle("umap.pd")
for index, row in umap_df.iterrows():
    insert_feature(row["id"], row["data"])

print(umap_df.head())