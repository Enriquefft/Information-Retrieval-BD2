"""Module for downloading a Spotify playlist using the Spotify API."""

from pytube import YouTube, Search, Stream

from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials

import numpy as np

from typing import Final, Optional, Generator

from pathlib import Path

# Set up credentials
client_id: Final[str] = '5b0ac652d91f4d2a89f62f99d568cd34'
client_secret: Final[str] = 'b450d640d4f44a13928f7725475a270b'

client_credentials_manager = SpotifyClientCredentials(
    client_id=client_id, client_secret=client_secret)
sp: Spotify = Spotify(client_credentials_manager=client_credentials_manager)

BASE_OUTPUT_PATH: Final[Path] = Path("songs/")


class Downloader():
    """Class for downloading a Spotify playlist."""

    def __init__(self, playlist_id: str):
        """Initialize a Downloader object."""
        self.playlist_id: str = playlist_id
        self.output_path: Path = BASE_OUTPUT_PATH / playlist_id

    def get_songs(
            self) -> tuple[float, Generator[tuple[str, str], None, None]]:
        """Get a list of [trackid, songname] from a Spotify playlist."""

        return min(
            (item['track']['duration_ms'])
            for item in sp.playlist(self.playlist_id)['tracks']['items']), (
                (item['track']['id'], item['track']['name'])
                for item in sp.playlist(self.playlist_id)['tracks']['items'])

    def download_songs(self) -> Generator[str | float | None, None, None]:
        """Download a song b its name."""

        min_duration, songs = self.get_songs()
        yield min_duration

        for song in songs:
            yt_result: YouTube = Search(song[1]).results[0]
            stream: Optional[Stream] = yt_result.streams.get_audio_only(
                subtype="wav") or yt_result.streams.get_audio_only()

            if stream is None:
                print(f"Could not download {song[1]}")
                yield None

            yield stream.download(output_path=self.output_path,
                                  filename=song[0])
