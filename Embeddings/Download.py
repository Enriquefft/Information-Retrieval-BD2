"""Module for downloading a Spotify playlist using the Spotify API."""

from pytube import YouTube, Search, Stream
from pytube.exceptions import AgeRestrictedError, LiveStreamError

from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

from concurrent.futures import ThreadPoolExecutor, as_completed

import numpy as np

from typing import Final, Optional, Generator

from pathlib import Path

from csv import reader

import logging

# Set up credentials
client_id: Final[str] = '5b0ac652d91f4d2a89f62f99d568cd34'
client_secret: Final[str] = 'b450d640d4f44a13928f7725475a270b'

client_credentials_manager = SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret)
sp: Spotify = Spotify(client_credentials_manager=client_credentials_manager)

BASE_OUTPUT_PATH: Final[Path] = Path("songs/")


class Downloader():
    """Class for downloading a Spotify playlist."""

    def __init__(self, csv_path: Optional[Path], playlist_id: Optional[str],
                 userFavourites: bool):
        """Initialize a Downloader object."""

        # Only one of csv_path and playlist_id should be set
        if sum([csv_path is not None, playlist_id is not None,
                userFavourites]) != 1:
            raise ValueError(
                "Only one of csv_path, playlist_id, and userFavourites should be set"
            )

        if csv_path is not None:
            self.get_method = self.get_songs_by_csv
        elif playlist_id is not None:
            self.get_method = self.get_songs_by_playlist
        elif userFavourites:
            self.get_method = self.get_songs_by_favourites

        self.playlist_id: str | None = playlist_id
        self.userFavourites: bool = userFavourites
        self.csv_path: Optional[Path] = csv_path

        self.output_path: Path = BASE_OUTPUT_PATH / (playlist_id
                                                     or 'favourites')

    def get_songs_by_csv(self) -> Generator[tuple[str, str], None, None]:

        if self.csv_path is None:
            raise ValueError("csv_path is None")

        with open(self.csv_path, 'r') as file:
            csv_reader = reader(file)
            headers = next(csv_reader)  # Skip the header row
            track_id_index = headers.index('track_id')
            track_name_index = headers.index('track_name')
            for row in csv_reader:
                yield (row[track_id_index], row[track_name_index])

    def get_songs_by_playlist(self) -> Generator[tuple[str, str], None, None]:
        """Get a list of [trackid, songname] from a Spotify playlist."""

        return ((item['track']['id'], item['track']['name'])
                for item in sp.playlist_tracks(self.playlist_id)['items'])

    def get_songs_by_favourites(
            self) -> Generator[tuple[str, str], None, None]:
        """Get a list of [trackid, songname] from a Spotify playlist."""
        return ((item['track']['id'], item['track']['name'])
                for item in sp.playlist(self.playlist_id)['tracks']['items'])

    def download_song(self, song: tuple[str, str]) -> Path | None:
        try:
            yt_result: YouTube = Search(song[1]).results[0]
            stream = yt_result.streams.get_audio_only(subtype="mp4")
            if stream is None:
                logging.warning(
                    f"Could not find an mp4 audio stream for {song[1]}")
                return None

            return Path(
                stream.download(output_path=self.output_path,
                                filename=song[0]))
        except (AgeRestrictedError, LiveStreamError) as e:
            return None

    def download_songs(self) -> Generator[Path, None, None]:
        """Download a song b its name."""

        for song in self.get_method():
            song_path = self.download_song(song)
            if song_path is not None:
                yield song_path
