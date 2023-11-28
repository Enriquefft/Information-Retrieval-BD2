from dotenv import load_dotenv

from psycopg2.extensions import register_adapter, AsIs

from psycopg2 import connect
from psycopg2.extensions import connection, cursor as cursorT

from Embeddings.UmapEmbedding import load_umap_dataset

import numpy as np

load_dotenv()
from os import getenv

db: connection = connect(user=getenv("POSTGRES_USER") or 'postgres',
                         password=getenv("POSTGRES_PASSWORD"),
                         host=getenv("POSTGRES_HOST"),
                         port=getenv("POSTGRES_PORT") or 5432)


def addapt_numpy_array(numpy_array):
    return AsIs(tuple(numpy_array))

register_adapter(np.ndarray, addapt_numpy_array)

def insert_feature(track_id: str, embedded_feature_vector: np.array) -> None:

    db_cursor: cursorT
    with db.cursor() as db_cursor:
        db_cursor.execute(
            "INSERT INTO music (track_id, features_vector) VALUES (%s, cube(%s::float[]))",
            (track_id, embedded_feature_vector.tolist()),
        )
    connection.commit()