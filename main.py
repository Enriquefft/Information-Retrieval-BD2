from fastapi import FastAPI

app = FastAPI()


mock_data = [
    {
        "track_id": "004s3t0ONYlzxII9PLgU6z",
        "track_name": "Canción A",
        "track_artist": "Artista A",
        "lyrics": "Letras de la canción A.",
        "track_popularity": 80,
        "track_album_id": "A1",
        "track_album_name": "Álbum A",
        "track_album_release_date": "2022-01-15",
        "playlist_name": "Playlist A",
        "playlist_id": "PA1",
        "playlist_genre": "Pop",
        "playlist_subgenre": "Indie Pop",
        "danceability": 0.75,
        "energy": 0.85,
        "key": 7,
        "loudness": -4.2,
        "mode": 1,
        "speechiness": 0.12,
        "acousticness": 0.2,
        "instrumentalness": 0.03,
        "liveness": 0.1,
        "valence": 0.88,
        "tempo": 120,
        "duration_ms": 240000,
        "language": "es"
    }
] * 100000000

@app.get("/search")
async def root(k: int = 10):
    return {"result": mock_data[:k]}

@app.get("/autocomplete")
async def root(word: str):
    return {"result": [
        word + "a", 
        word + "b", 
        word + "c", 
        word + "d", 
        word + "e"
        ]}
