from Download import Downloader
from Embed import get_mfcc_features

from psycopg2 import connect

from typing import Final, cast

from pathlib import Path

import numpy as np

playlist_id: Final[str] = '6Nqv8Mi4xKEOXBLcIbDopO'

db = connect()


def run() -> None:
    downloader = Downloader(playlist_id)

    min_duration: float = cast(float, next(downloader.download_songs()))
    print(f"min_duration: {min_duration}")

    for song_path in downloader.download_songs():
        print(f"download_songs: {song_path}")

        if song_path is not None:
            features = get_mfcc_features(Path(cast(str, song_path)))


if __name__ == "__main__":
    run()
