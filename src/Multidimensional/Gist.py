from psycopg2.extensions import connection, cursor

def knn_search(db: connection, keywords: str, k: int = 10) -> list[tuple[str, float]]:
    db_cursor: cursor
    with db.cursor() as db_cursor:
        db_cursor.execute(
            f"SELECT id, title, artist, similarity(title, %s) AS sim FROM tracks ORDER BY sim DESC LIMIT %s",
            (keywords, k))
        return [(row[1], row[3]) for row in db_cursor.fetchall()]