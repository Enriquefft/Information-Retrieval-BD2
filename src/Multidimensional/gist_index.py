from psycopg2.extensions import connection, cursor

def knn_search_gist(db: connection, track_id: str, k: int = 10) -> list[tuple[str, float]]:
    db_cursor: cursor
    with db.cursor() as db_cursor:
        db_cursor.execute(
            """
            SELECT track_id
            """
        )    
    