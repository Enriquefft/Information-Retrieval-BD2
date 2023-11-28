from psycopg2.extensions import connection, cursor

def knn_gist(db: connection, track_id: str, k: int = 10) -> list[str]:
    db_cursor: cursor
    with db.cursor() as db_cursor:
        db_cursor.execute(
            """
            SELECT features_vector
            FROM music
            WHERE track_id = %s
            """,
            (track_id,)
        )
        query_result = db_cursor.fetchone()
        if query_result is None:
            return []

        target_vector = query_result[0]

        db_cursor.execute(
            """
            SELECT track_id
            FROM music
            WHERE track_id != %s
            ORDER BY features_vector <-> %s
            LIMIT %s
            """,
            (track_id, target_vector, k)
        )
        similar_tracks = db_cursor.fetchall()

        return [track[0] for track in similar_tracks]