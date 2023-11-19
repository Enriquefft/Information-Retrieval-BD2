"""Module for downloading a Spotify playlist using the Spotify API."""

from pytube import YouTube, Search, Stream  # type: ignore
from pytube.exceptions import AgeRestrictedError, LiveStreamError  # type: ignore
import youtube_dl

from spotipy import Spotify  # type: ignore
from spotipy.oauth2 import SpotifyClientCredentials  # type: ignore

from concurrent.futures import ThreadPoolExecutor, as_completed

from pprint import pprint

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

from enum import Enum


class DownloadMethod(Enum):
    """Enum for the download method."""
    YOUTUBE_DL = 1
    PYTUBE = 2


class Downloader():
    """Class for downloading a Spotify playlist."""

    def __init__(self, dl_method: DownloadMethod, csv_path: Optional[Path],
                 playlist_id: Optional[str], userFavourites: bool):
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

        if dl_method == DownloadMethod.YOUTUBE_DL:
            self.download_method = self.download_song_youtube_dl
        elif dl_method == DownloadMethod.PYTUBE:
            self.download_method = self.download_song_pytube

        self.playlist_id: str | None = playlist_id
        self.userFavourites: bool = userFavourites
        self.csv_path: Optional[Path] = csv_path

        self.output_path: Path = BASE_OUTPUT_PATH / (playlist_id
                                                     or 'favourites')

    def get_songs_by_csv(self) -> Generator[tuple[str, str], None, None]:
        """Get a list of [trackid, songname] from a Spotify playlist."""

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

    def download_song_youtube_dl(self, song: tuple[str, str]) -> Path | None:
        """Download a song audio by searching its name on yt.

        @param song: A tuple of [track_id, song_name]
        @return: The path to the downloaded song
        """
        try:
            ydl_opts = {
                'default_search': 'ytsearch',
                'format': 'bestaudio/best',
                'outtmpl': f'{self.output_path}/{song[0]}.%(ext)s',
                'quiet': True,
                'no_warnings': True,
            }
            with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                info_dict = ydl.extract_info(f"ytsearch:{song[1]}",
                                             download=False)
                audio_url = info_dict['entries'][0]['webpage_url']
                pprint(info_dict['entries'])
                if audio_url is None:
                    logging.warning(
                        f"Could not find an audio URL for {song[1]}")
                    return None
                ydl.download([audio_url])
                return Path(f'{self.output_path}/{song[0]}.{info_dict["ext"]}')
        except youtube_dl.utils.DownloadError as e:
            return None

    def download_song_pytube(self, song: tuple[str, str]) -> Path | None:
        """Download a song audio by searching its name on yt.

        @param song: A tuple of [track_id, song_name]
        @return: The path to the downloaded song
        """
        try:
            yt_result: YouTube = Search(song[1]).results[0]
            stream = yt_result.streams.get_audio_only()
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
            song_path = self.download_method(song)
            if song_path is not None:
                yield song_path
