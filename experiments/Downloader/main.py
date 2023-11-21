import pandas as pd
from yt_dlp import YoutubeDL
import pandas as pd
from yt_dlp import YoutubeDL
df = pd.read_csv("CSV/spotify_songs.csv")

df["search"] = "ytsearch:"+df["track_name"] + " " + df["track_artist"]

import concurrent.futures

df = pd.read_csv("CSV/spotify_songs.csv")

def download_video(search_query, track_id):
    ydl_opts = {
        'outtmpl': f'mp3s/{track_id}.%(ext)s',
        'format': 'worstaudio/worst',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '64'
        }]
    }
    with YoutubeDL(ydl_opts) as ytdl:
        ytdl.download([search_query])

with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = []
    for _, row in df.iterrows():
        search_query = f'ytsearch:{row["track_name"]} {row["track_artist"]}'
        track_id = row["track_id"]
        futures.append(executor.submit(download_video, search_query, track_id))
    for future in concurrent.futures.as_completed(futures):
        try:
            future.result()
        except Exception as e:
            print(f'An error occurred: {e}')